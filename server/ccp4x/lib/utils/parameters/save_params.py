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

    pass  # DEBUG: print(f"[DEBUG save_params_for_job] mode={mode}, fileName={fileName}, relocated_file_path={relocated_file_path}")

    if relocated_file_path.exists():
        CCP4Utils.backupFile(str(relocated_file_path), delete=False)

    # IMPORTANT: Convert pathlib.Path to absolute string path
    # Otherwise CI2XmlDataFile.getFullPath() returns just the filename
    f = CCP4File.CI2XmlDataFile(fullPath=str(relocated_file_path.absolute()))

    # Debug: check what setFullPath did
    pass  # DEBUG: print(f"[DEBUG save_params_for_job] After init: baseName.value={f.baseName.value}, relPath.value={getattr(f.relPath, 'value', 'N/A')}")
    pass  # DEBUG: print(f"[DEBUG save_params_for_job] After init: getFullPath()={f.getFullPath()}")

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

    # DEBUG: Check container structure before saving
    print(f"\n[DEBUG save_params] === Container structure for job {the_job.number} ===")
    print(f"[DEBUG save_params] exclude_unset parameter: {exclude_unset}")
    print(f"[DEBUG save_params] Container type: {type(old_job_container).__name__}")

    try:
        # Show all top-level attributes
        for attr_name in ['inputData', 'outputData', 'controlParameters']:
            if hasattr(old_job_container, attr_name):
                section = getattr(old_job_container, attr_name)
                print(f"[DEBUG save_params]   {attr_name}: type={type(section).__name__}")

                # Check specific file attributes
                if attr_name == 'inputData':
                    for attr in ['HKLIN', 'XYZIN', 'UNMERGEDFILES']:
                        if hasattr(section, attr):
                            attr_obj = getattr(section, attr)
                            print(f"[DEBUG save_params]     {attr}: type={type(attr_obj).__name__}, isSet={attr_obj.isSet() if hasattr(attr_obj, 'isSet') else 'N/A'}")
                            if hasattr(attr_obj, '__len__'):
                                print(f"[DEBUG save_params]       length: {len(attr_obj)}")
    except Exception as e:
        print(f"[DEBUG save_params] Error checking container structure: {e}")

    # Use the exclude_unset parameter passed to this function
    print(f"[DEBUG save_params] Calling getEtree with excludeUnset={exclude_unset}")
    body_etree = old_job_container.getEtree(excludeUnset=exclude_unset)

    # DEBUG: Check what's in body_etree
    import xml.etree.ElementTree as ET
    body_xml = ET.tostring(body_etree, encoding='unicode')
    print(f"[DEBUG save_params] Body etree length: {len(body_xml)}")
    if 'UNMERGEDFILES' in body_xml:
        print(f"[DEBUG save_params] ✓ UNMERGEDFILES found in body etree")
        # Find and print the UNMERGEDFILES section
        start_idx = body_xml.index('<UNMERGEDFILES>')
        end_idx = body_xml.index('</UNMERGEDFILES>') + len('</UNMERGEDFILES>')
        print(f"[DEBUG save_params] UNMERGEDFILES section:")
        print(body_xml[start_idx:end_idx])
    else:
        print(f"[DEBUG save_params] ✗ UNMERGEDFILES NOT found in body etree!")
        print(f"[DEBUG save_params] Body etree (first 1000 chars): {body_xml[:1000]}")

    f.saveFile(bodyEtree=body_etree)
    logger.info(f"[DEBUG save_params] Saved params to {relocated_file_path}")

    # Verify file was actually written
    import os
    if os.path.exists(relocated_file_path):
        pass  # DEBUG: print(f"[DEBUG save_params] ✓ Verified file exists: {relocated_file_path}")
    else:
        pass  # DEBUG: print(f"[DEBUG save_params] ✗ WARNING: File does NOT exist after saveFile(): {relocated_file_path}")
