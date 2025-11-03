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

    # DEBUG: Check container structure before saving
    logger.info(f"[DEBUG save_params] === Container structure for job {the_job.number} ===")
    logger.info(f"[DEBUG save_params] exclude_unset parameter: {exclude_unset}")
    logger.info(f"[DEBUG save_params] Container type: {type(old_job_container).__name__}")

    try:
        # Show all top-level attributes
        for attr_name in ['inputData', 'outputData', 'controlParameters']:
            if hasattr(old_job_container, attr_name):
                section = getattr(old_job_container, attr_name)
                logger.info(f"[DEBUG save_params]   {attr_name}: type={type(section).__name__}")

                # Show all attributes in this section
                if hasattr(section, '__dict__'):
                    section_attrs = [a for a in dir(section) if not a.startswith('_') and not callable(getattr(section, a, None))]
                    logger.info(f"[DEBUG save_params]     attributes: {section_attrs}")

                    # Check specific file attributes
                    for attr in ['HKLIN', 'XYZIN']:
                        if hasattr(section, attr):
                            file_obj = getattr(section, attr)
                            logger.info(f"[DEBUG save_params]     {attr}: {file_obj}")
                            if hasattr(file_obj, 'baseName'):
                                logger.info(f"[DEBUG save_params]       baseName: {file_obj.baseName}")
                            if hasattr(file_obj, 'fullPath'):
                                logger.info(f"[DEBUG save_params]       fullPath: {file_obj.fullPath}")
    except Exception as e:
        logger.warning(f"[DEBUG save_params] Error checking container structure: {e}")

    # DEBUG: Log container and XYZIN object IDs with timestamp
    import sys
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(f"DEBUG save_params [{timestamp}]: === SAVE STARTING ===", file=sys.stderr)
    print(f"DEBUG save_params [{timestamp}]: target file = {relocated_file_path.absolute()}", file=sys.stderr)
    print(f"DEBUG save_params [{timestamp}]: container id={id(old_job_container)}", file=sys.stderr)
    if hasattr(old_job_container, 'inputData') and hasattr(old_job_container.inputData, 'XYZIN'):
        xyzin_obj = old_job_container.inputData.XYZIN
        print(f"DEBUG save_params [{timestamp}]: XYZIN id={id(xyzin_obj)}", file=sys.stderr)
        if hasattr(xyzin_obj, 'selection') and hasattr(xyzin_obj.selection, 'text'):
            print(f"DEBUG save_params [{timestamp}]: selection.text id={id(xyzin_obj.selection.text)}, value='{xyzin_obj.selection.text.value}'", file=sys.stderr)

    # FORCE exclude_unset to False for debugging
    logger.info(f"[DEBUG save_params] Calling getEtree with excludeUnset=False (FORCED)")
    body_etree = old_job_container.getEtree(excludeUnset=False)

    # Log the XML structure
    import xml.etree.ElementTree as ET
    xml_str = ET.tostring(body_etree, encoding='unicode')
    logger.info(f"[DEBUG save_params] Generated XML length: {len(xml_str)} chars")
    logger.info(f"[DEBUG save_params] XML preview (first 500 chars):\n{xml_str[:500]}")

    # Check specifically for selection element
    import sys
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    if '<selection>' in xml_str:
        print(f"DEBUG save_params [{timestamp}]: ✓ <selection> element IS in generated XML", file=sys.stderr)
        # Find and print the selection part
        sel_start = xml_str.find('<selection>')
        sel_end = xml_str.find('</selection>') + len('</selection>')
        print(f"DEBUG save_params [{timestamp}]: selection XML: {xml_str[sel_start:sel_end]}", file=sys.stderr)
    else:
        print(f"DEBUG save_params [{timestamp}]: ✗ <selection> element NOT in generated XML", file=sys.stderr)

    f.saveFile(bodyEtree=body_etree)
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    logger.info(f"[DEBUG save_params] Saved params to {relocated_file_path}")
    print(f"DEBUG save_params [{timestamp}]: saveFile() completed", file=sys.stderr)

    # Verify what was actually written to disk
    if relocated_file_path.exists():
        with open(relocated_file_path, 'r') as check_file:
            saved_xml = check_file.read()
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            if '<selection>' in saved_xml:
                print(f"DEBUG save_params [{timestamp}]: ✓ <selection> IS in saved file {relocated_file_path.absolute()}", file=sys.stderr)
            else:
                print(f"DEBUG save_params [{timestamp}]: ✗ <selection> NOT in saved file {relocated_file_path.absolute()}", file=sys.stderr)
    print(f"DEBUG save_params [{timestamp}]: === SAVE COMPLETE ===", file=sys.stderr)
