import datetime
import logging
import os
import pathlib
import shutil
import uuid
import re
import hashlib

from core import CCP4Container
from core.base_object.cdata_file import CDataFile
from core import CCP4File
from core import CCP4PluginScript
from core.base_object.fundamental_types import CList
from core.CCP4File import CI2XmlDataFile as CI2XmlDataFile

from ...db import models
from .save_params_for_job import save_params_for_job
# Legacy import removed - using modern hierarchy traversal instead
# from .find_objects import find_objects


logger = logging.getLogger(f"ccp4x:{__name__}")

# Map CDataFile class names to MIME types (from ccp4i2_static_data.py)
# This is more reliable than using qualifiers["mimeTypeName"]
FILE_CLASS_TO_MIMETYPE = {
    'CPdbDataFile': 'chemical/x-pdb',
    'CMtzDataFile': 'application/CCP4-mtz',
    'CMapDataFile': 'application/CCP4-map',
    'CSeqDataFile': 'application/CCP4-seq',
    'CDictDataFile': 'application/refmac-dictionary',
    'CUnmergedDataFile': 'application/CCP4-unmerged-experimental',
    'CObsDataFile': 'application/CCP4-mtz-observed',
    'CFreeRDataFile': 'application/CCP4-mtz-freerflag',
    'CMiniMtzDataFile': 'application/CCP4-mtz-mini',
    'CI2XmlDataFile': 'application/xml',
    'CPhsDataFile': 'application/CCP4-mtz-phases',
    'CSceneDataFile': 'application/CCP4-scene',
    'CPDFDataFile': 'application/x-pdf',
    'CPostscriptDataFile': 'application/postscript',
    'CEBIValidationXMLDataFile': 'application/EBI-validation-xml',
    'CMmcifDataFile': 'chemical/x-cif',
}


def extract_from_first_bracketed(path: str) -> str:
    parts = path.split(".")
    for i, part in enumerate(parts):
        if re.search(r"\[.*\]", part):
            return ".".join(parts[i:])
    return parts[-1]  # fallback to the last part if no bracketed part found


def compute_file_checksum(file_path: pathlib.Path) -> str:
    """Compute MD5 checksum of a file."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def _process_input(
    theJob: models.Job,
    plugin: CCP4PluginScript.CPluginScript,
    input: CCP4File.CDataFile,
):
    theFile = None
    if input.dbFileId is not None and len(str(input.dbFileId)) != 0:
        theFile = models.File.objects.get(uuid=uuid.UUID(str(input.dbFileId)))
    else:
        if input.baseName is not None and len(str(input.baseName).strip()) != 0:
            sourceFilePath = pathlib.Path(str(input.relPath)) / str(input.baseName)
            if not sourceFilePath.exists():
                sourceFilePath = (
                    pathlib.Path(theJob.project.directory)
                    / str(input.relPath)
                    / str(input.baseName)
                )
            # Load file
            input.loadFile()
            input.setContentFlag()
            destFilePath = (
                pathlib.Path(theJob.project.directory)
                / "CCP4_IMPORTED_FILES"
                / sourceFilePath.name
            )
            while destFilePath.exists():
                fileRoot, fileExt = os.path.splitext(destFilePath.name)
                destFilePath = destFilePath.parent / "{}_1{}".format(fileRoot, fileExt)
            logger.debug("src %s, UniqueDestFilePath %s", sourceFilePath, destFilePath)
            shutil.copyfile(sourceFilePath, destFilePath)
            # Now have to change the plugin to reflect the new location

            try:
                # Determine MIME type from class name (more reliable than qualifiers)
                class_name = type(input).__name__
                file_mime_type = FILE_CLASS_TO_MIMETYPE.get(class_name)

                if not file_mime_type:
                    # Fallback: try qualifier
                    file_mime_type = input.get_qualifier("mimeTypeName")

                if not file_mime_type:
                    logger.warning(
                        "Class %s (%s) does not have a known MIME type mapping",
                        str(input.objectName()),
                        class_name
                    )
                    # Last resort: guess from class name
                    if 'xml' in class_name.lower():
                        file_mime_type = "application/xml"
                    else:
                        # Skip files we can't identify
                        logger.error("Cannot determine MIME type for %s, skipping", input.objectName())
                        return None
                file_type_object = models.FileType.objects.get(name=file_mime_type)

                # print('What I know about import is', str(valueDictForObject(input)))
                if (
                    not hasattr(input, "annotation")
                    or input.annotation is None
                    or len(str(input.annotation).strip()) == 0
                ):
                    annotation = f"Imported from file {sourceFilePath.name}"
                else:
                    annotation = str(input.annotation)
                job_param_name = extract_from_first_bracketed(input.objectPath())
                createDict = {
                    "name": str(destFilePath.name),
                    "annotation": annotation,
                    "type": file_type_object,
                    "job": theJob,
                    "job_param_name": job_param_name,
                    "directory": 2,
                }
                # print(createDict)
                theFile = models.File(**createDict)
                theFile.save()

                input.dbFileId.set(theFile.uuid)
                input.project.set(str(theJob.project.uuid))
                input.relPath.set("CCP4_IMPORTED_FILES")
                input.baseName.set(destFilePath.name)
                input.loadFile()
                input.setContentFlag()

                # Compute checksum of the destination file
                file_checksum = compute_file_checksum(destFilePath)

                createDict = {
                    "file": theFile,
                    "name": str(sourceFilePath),
                    "time": datetime.datetime.now(),
                    "last_modified": datetime.datetime.now(),
                    "checksum": file_checksum,
                }
                # print(createDict)
                newImportfile = models.FileImport(**createDict)
                newImportfile.save()
                # for key in createDict:
                #    setattr(newImportfile, key, createDict[key])
                #    newImportfile.save()
            except ValueError as err:
                theFile = None
                logger.error(
                    f"Encountered issue - {err} importing file {input.baseName}"
                )

    if theFile is not None:
        theRole = models.FileUse.Role.IN
        job_param_name = extract_from_first_bracketed(input.objectPath())
        createDict = {
            "file": theFile,
            "job": theJob,
            "role": theRole,
            "job_param_name": job_param_name,
        }
        already_exists = models.FileUse.objects.filter(**createDict).exists()
        if not already_exists:
            fileUse = models.FileUse(**createDict)
            fileUse.save()
        else:
            logger.warning(
                "FileUse already exists for file %s job %s role %s job_param_name %s",
                theFile,
                theJob,
                theRole,
                job_param_name,
            )


def import_files(theJob, plugin):
    """
    Import input files for a job using modern CPluginScript hierarchy.

    Uses the modern hierarchy system's find_all() method instead of legacy find_objects.
    This searches the inputData container for all CDataFile instances.
    """
    # Use modern hierarchy traversal to find all CDataFile objects
    inputs = []

    if hasattr(plugin.container, 'inputData'):
        input_data = plugin.container.inputData

        # Walk through the hierarchy to find all CDataFile instances
        # Use the modern find_all approach with type checking
        def is_file_object(obj):
            return isinstance(obj, (CDataFile, CCP4File.CDataFile))

        # Traverse children recursively
        def collect_files(container, results):
            """Recursively collect file objects from container hierarchy."""
            if hasattr(container, 'children'):
                for child in container.children():
                    if is_file_object(child):
                        results.append(child)
                    # Recurse into child containers
                    if hasattr(child, 'children'):
                        collect_files(child, results)

        collect_files(input_data, inputs)

    logger.debug("In import_files found %s input files", len(inputs))

    for the_input in inputs:
        _process_input(theJob, plugin, the_input)

    # Save parameters after import
    save_params_for_job(plugin, theJob, mode="JOB_INPUT")

    return plugin
