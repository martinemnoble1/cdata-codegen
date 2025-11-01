import logging
import contextlib
import asyncio
from xml.etree import ElementTree as ET

from core.CCP4TaskManager import TASKMANAGER
from core import CCP4PluginScript, CCP4Modules
from PySide2 import QtCore

from ...db import models
from ...db.ccp4i2_django_db_handler import CCP4i2DjangoDbHandler
from ...db.async_db_handler import AsyncDatabaseHandler
from ..async_import_files import import_input_files_async
from .get_job_plugin import get_job_plugin
from .save_params_for_job import save_params_for_job
from .set_output_file_names import set_output_file_names
from asgiref.sync import async_to_sync

logger = logging.getLogger(f"ccp4x:{__name__}")
logger.setLevel(logging.DEBUG)


def run_job(jobId: str):
    """
    Executes a job based on the provided job ID.

    This function retrieves the job from the database using the job ID, sets up the necessary
    environment, and executes the job while redirecting stdout and stderr to respective files
    in the job's directory.

    Args:
        jobId (str): The unique identifier of the job to be executed.

    Raises:
        models.Job.DoesNotExist: If no job with the given jobId is found in the database.
        Exception: If any error occurs during the execution of the job.

    Side Effects:
        - Creates or overwrites "stdout.txt" and "stderr.txt" in the job's directory.
        - Executes the job's plugin and handles database interactions.

    """
    new_job = models.Job.objects.get(uuid=jobId)
    logger.info(f"Running job in {new_job.directory}")

    # Remove any existing params.xml to ensure we start fresh from input_params.xml
    # params.xml will be regenerated during the run at appropriate lifecycle stages:
    # - After checkInputData() - with validated inputs
    # - After checkOutputData() - with computed output paths
    # - After processOutputFiles() - with actual outputs
    params_file = new_job.directory / "params.xml"
    if params_file.exists():
        logger.info(f"Removing old params.xml to start fresh from input_params.xml")
        params_file.unlink()

    with open(new_job.directory / "stdout.txt", "w", encoding="utf-8") as stdout_file:
        with contextlib.redirect_stdout(stdout_file):
            with open(
                new_job.directory / "stderr.txt", "w", encoding="utf-8"
            ) as stderr_file:
                with contextlib.redirect_stderr(stderr_file):
                    db_handler = setup_db_handler(new_job)
                    application_inst = setup_application_instance(new_job)
                    the_plugin = retrieve_plugin(new_job, application_inst, db_handler)
                    new_job.status = models.Job.Status.RUNNING
                    new_job.save()
                    logger.info("Status running set")
                    logger.info(f"About to call set_output_file_names for job {new_job.number}")
                    logger.info(f"  projectId={new_job.project.uuid}, jobNumber={new_job.number}")
                    set_output_file_names(
                        the_plugin.container,
                        projectId=str(new_job.project.uuid),
                        jobNumber=new_job.number,
                        force=True,
                    )
                    logger.info(f"Finished set_output_file_names")
                    _import_files(new_job, the_plugin)
                    # Save params.xml AFTER importing files so file attributes are populated
                    save_params_for_job(the_plugin, new_job, mode="PARAMS")
                    logger.info(f"Saved params.xml with imported file attributes")
                    try:
                        executePlugin(the_plugin, new_job)
                    except Exception as err:
                        logger.exception("Failed to execute plugin", exc_info=err)
                    finally:
                        maybe_updated_job = models.Job.objects.get(id=new_job.id)
                        if maybe_updated_job.status not in [
                            models.Job.Status.FINISHED,
                            models.Job.Status.FAILED,
                            models.Job.Status.UNSATISFACTORY,
                        ]:
                            maybe_updated_job.status = models.Job.Status.FAILED
                            maybe_updated_job.save()
                        maybe_updated_job.process_id = None
                        maybe_updated_job.save()
                        logger.info("Job finished")


def setup_db_handler(new_job: models.Job):
    db_handler = CCP4i2DjangoDbHandler()
    db_handler.projectName = new_job.project.name
    db_handler.projectId = str(new_job.project.uuid)
    return db_handler


def setup_application_instance(the_job: models.Job):
    application_inst = QtCore.QEventLoop(parent=CCP4Modules.QTAPPLICATION())
    application_inst.pluginName = the_job.task_name
    application_inst.comFilePath = str(the_job.directory)
    logger.info(
        "Application_inst is %s with parent %s",
        str(application_inst),
        str(application_inst.parent()),
    )
    return application_inst


def retrieve_plugin(
    new_job: models.Job,
    application_inst: QtCore.QEventLoop,
    dbHandler: CCP4i2DjangoDbHandler,
):
    try:
        the_plugin = get_job_plugin(
            new_job, parent=application_inst, dbHandler=dbHandler
        )
        the_plugin.setDbData(
            handler=dbHandler,
            projectName=new_job.project.name,
            projectId=str(new_job.project.uuid).replace("-", ""),
            jobNumber=new_job.number,
            jobId=str(new_job.uuid).replace("-", ""),
        )
        logger.info(f"Retrieved plugin {new_job.task_name}")
    except Exception as err:
        logger.exception(f"Err getting job {str(err)}", exc_info=err)
        new_job.status = models.Job.Status.FAILED
        new_job.save()
        raise err
    return install_closeApp_handler(the_plugin, new_job, application_inst)


def install_closeApp_handler(
    the_plugin: CCP4PluginScript.CPluginScript,
    new_job: models.Job,
    application_inst: QtCore.QEventLoop,
):
    try:

        @QtCore.Slot(dict)
        def closeApp(completionStatus):
            try:
                logger.info("Received closeApp - %s", completionStatus)
                logger.info(
                    f"Compare {completionStatus['jobId']} with {str(new_job.uuid)}"
                )
                with open(
                    new_job.directory / "diagnostic.xml",
                    "wb",
                ) as diagnosticXML:
                    error_report = the_plugin.errorReport.getEtree()
                    ET.indent(error_report, space="\t", level=0)
                    diagnosticXML.write(ET.tostring(error_report, encoding="utf-8"))
            except Exception as err:
                logger.exception("Exception in writing diagnostics", exc_info=err)

            QtCore.QTimer.singleShot(0, application_inst.quit)
            logger.info("Set singleshot quit timer")

        the_plugin.finished.connect(closeApp)
        return the_plugin
    except Exception as err:
        logger.exception(f"Err making or connecting closeApp {str(err)}", exc_info=err)
        new_job.status = models.Job.Status.FAILED
        new_job.save()
        raise err


def _import_files(new_job: models.Job, the_plugin: CCP4PluginScript.CPluginScript):
    try:
        # Use modern async import_files with AsyncDatabaseHandler
        async_db_handler = AsyncDatabaseHandler(project_uuid=new_job.project.uuid)

        # Call async function from sync context
        files_imported = async_to_sync(import_input_files_async)(
            new_job, the_plugin, async_db_handler
        )
        logger.info(f"Imported {files_imported} files using async import system")
    except Exception as err:
        logger.exception("Failed importing files", exc_info=err)
        new_job.status = models.Job.Status.FAILED
        new_job.save()
        raise err
    logger.info("Files imported")


def _glean_files(new_job: models.Job, the_plugin: CCP4PluginScript.CPluginScript):
    """Glean output files, input file uses, and KPIs after job execution.

    This function:
    1. Discovers all output files that were created
    2. Creates File and FileUse records in the database
    3. Updates CDataFile objects with dbFileId
    4. Saves params.xml with complete file metadata

    Args:
        new_job: Django Job model instance
        the_plugin: CPluginScript instance
    """
    try:
        from ..async_glean_files import glean_all_async, save_params_after_gleaning

        # Use modern async glean_files with AsyncDatabaseHandler
        async_db_handler = AsyncDatabaseHandler(project_uuid=new_job.project.uuid)

        # Call async function from sync context
        glean_results = async_to_sync(glean_all_async)(
            new_job, the_plugin.container, async_db_handler,
            glean_outputs=True,
            glean_inputs=True,
            glean_kpis=True
        )

        logger.info(
            f"Gleaning complete: {glean_results['output_files']} output files, "
            f"{glean_results['input_uses']} input uses, {glean_results['kpis']} KPIs"
        )

        # Save params.xml with updated dbFileIds and KPIs
        async_to_sync(save_params_after_gleaning)(the_plugin, new_job)
        logger.info("Saved params.xml after gleaning with dbFileIds")

    except Exception as err:
        logger.exception("Failed gleaning files", exc_info=err)
        # Don't fail the job on gleaning errors - just log them
        logger.warning(f"Gleaning failed but job will be marked as complete: {err}")

    logger.info("File gleaning complete")


def executePlugin(
    the_plugin: CCP4PluginScript.CPluginScript,
    new_job: models.Job,
):
    # Get the parent - handle both method and attribute access
    # (plugins use HierarchicalObject.parent() method, but may also expose .parent attribute)
    if callable(getattr(the_plugin, 'parent', None)):
        application_inst: QtCore.QEventLoop = the_plugin.parent()
    else:
        # parent is an attribute, not a method (or get_parent exists)
        application_inst: QtCore.QEventLoop = getattr(the_plugin, 'parent', None) or the_plugin.get_parent()
    logger.info("Using application_inst %s", application_inst)
    try:
        rv = the_plugin.process()
    except Exception as err:
        logger.exception(f"Failed to execute plugin {new_job.task_name}", exc_info=err)
        new_job.status = models.Job.Status.FAILED
        new_job.save()
        raise err
    logger.info(f"Result from the_plugin.process is {str(rv)}")

    try:
        result = application_inst.exec_()
        logger.info(f"Returned from exec_ with result {result}")

        # Glean output files after execution completes
        _glean_files(new_job, the_plugin)

        return result
    except Exception as err:
        logger.exception(f"Failed to execute plugin {new_job.task_name}", exc_info=err)
        new_job.status = models.Job.Status.FAILED
        new_job.save()
        # backupProjectDb(new_job.projectid)
        raise err
