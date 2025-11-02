import logging
import pathlib
import getpass

from core import CCP4File
from core import CCP4Utils
from core import CCP4PluginScript
from core import CCP4Container
from ccp4x.db import models

logger = logging.getLogger(f"ccp4x:{__name__}")


def save_params_for_job(
    the_job_plugin: CCP4PluginScript.CPluginScript,
    the_job: models.Job,
    mode="JOB_INPUT",
    exclude_unset=False,
):
    """
    Save parameters for a given job to an XML file.

    This function generates a file name based on the job plugin and mode,
    relocates the file path to the job's directory, and saves the job's
    parameters in XML format. If a file with the same name already exists,
    it creates a backup before saving the new file.

    Args:
        the_job_plugin (CCP4PluginScript.CPluginScript): The job plugin script instance.
        the_job (models.Job): The job instance containing job details.
        mode (str, optional): The mode for generating the file name. Defaults to "JOB_INPUT".
        exclude_unset (bool, optional): Flag to exclude unset parameters. Defaults to False.

    Returns:
        None
    """
    fileName = the_job_plugin.makeFileName(mode)
    # Rework to the directory of "the_job"
    relocated_file_path = the_job.directory / pathlib.Path(fileName).name

    if relocated_file_path.exists():
        CCP4Utils.backupFile(str(relocated_file_path), delete=False)

    f = CCP4File.CI2XmlDataFile(fullPath=(relocated_file_path))

    # CI2XmlDataFile already has a header instance created during __init__
    # Just populate it with job information
    f.header.function.set("PARAMS")
    f.header.projectName.set(the_job.project.name)
    f.header.projectId.set(str(the_job.project.uuid))
    f.header.jobNumber.set(the_job.number)
    f.header.jobId.set(str(the_job.uuid))
    f.header.setCurrent()
    f.header.pluginName.set(the_job.task_name)
    f.header.userId.set(getpass.getuser())
    old_job_container: CCP4Container.CContainer = the_job_plugin.container

    # DEBUG: Check if file attributes are set before saving
    logger.info(f"[DEBUG save_params] Checking file attributes before save...")
    try:
        if hasattr(old_job_container, 'inputData'):
            input_data = old_job_container.inputData
            for attr_name in ['HKLIN', 'XYZIN']:
                if hasattr(input_data, attr_name):
                    file_obj = getattr(input_data, attr_name)
                    if hasattr(file_obj, 'baseName') and hasattr(file_obj.baseName, 'value'):
                        logger.info(f"[DEBUG save_params]   {attr_name}.baseName = '{file_obj.baseName.value}'")
                    if hasattr(file_obj, 'project') and hasattr(file_obj.project, 'value'):
                        logger.info(f"[DEBUG save_params]   {attr_name}.project = '{file_obj.project.value}'")
    except Exception as e:
        logger.warning(f"[DEBUG save_params] Error checking file attributes: {e}")

    body_etree = old_job_container.getEtree(excludeUnset=exclude_unset)
    f.saveFile(bodyEtree=body_etree)
    logger.info(f"[DEBUG save_params] Saved params for job {the_job.number}")
