import logging
import pathlib
import json
import gemmi
import re
from core.base_object.cdata_file import CDataFile
from core.CCP4XtalData import CMtzDataFile
from django.utils.text import slugify
from django.http import HttpRequest
from core import CCP4File
from core import CCP4XtalData
from core.CCP4XtalData import CMtzDataFile

# Use core method for find_by_path - no import needed
from .available_name import available_file_name_based_on
from ..plugins.plugin_context import get_plugin_with_context
from ..formats.gemmi_split_mtz import gemmi_split_mtz
from ..parameters.save_params import save_params_for_job
from ..containers.json_encoder import CCP4i2JsonEncoder
from ..parameters.value_dict import value_dict_for_object
from .detect_type import detect_file_type
from ..parameters.set_parameter import set_parameter, set_parameter_container
from ccp4x.db import models

logger = logging.getLogger(f"ccp4x:{__name__}")


def normalize_object_path(object_path: str) -> str:
    """
    Normalize object paths from frontend to match backend container structure.

    The frontend JSON encoder includes the full hierarchy path which includes
    `.container.` (e.g., `prosmart_refmac.container.inputData.XYZIN`), but the
    backend container structure doesn't have that extra level.

    This function strips the `.container.` segment if present after the task name.

    Args:
        object_path: Path like "prosmart_refmac.container.inputData.XYZIN"

    Returns:
        Normalized path like "prosmart_refmac.inputData.XYZIN"
    """
    # Split into parts
    parts = object_path.split('.')

    # If second element is 'container', remove it
    # e.g., ['prosmart_refmac', 'container', 'inputData', 'XYZIN']
    #    -> ['prosmart_refmac', 'inputData', 'XYZIN']
    if len(parts) >= 2 and parts[1] == 'container':
        parts = [parts[0]] + parts[2:]

    return '.'.join(parts)


def extract_from_first_bracketed(path: str) -> str:
    parts = path.split(".")
    for i, part in enumerate(parts):
        if re.search(r"\[.*\]", part):
            return ".".join(parts[i:])
    return parts[-1]  # fallback to the last part if no bracketed part found


def upload_file_param(job: models.Job, request: HttpRequest) -> dict:

    logger.info("=== upload_file_param START ===")
    logger.info("job: %s (task: %s)", job.uuid, job.task_name)

    # Use plugin context for consistent container access (same as set_param/get_param/digest)
    plugin_result = get_plugin_with_context(job)
    if not plugin_result.success:
        raise ValueError(f"Failed to load plugin: {plugin_result.error}")

    plugin = plugin_result.data
    container = plugin.container
    object_path = request.POST.get("objectPath")
    files = request.FILES.getlist("file")

    logger.info("object_path from request: %s", object_path)
    logger.info("files: %s", [f.name for f in files])

    # Normalize path to strip .container. segment if present from frontend
    normalized_path = normalize_object_path(object_path)
    logger.info("normalized_path: %s", normalized_path)

    param_object = container.find_by_path(normalized_path, skip_first=True)
    logger.info("param_object: %s (type: %s)", param_object, type(param_object).__name__)
    # Look for existing file import for this job/job_param_name and delete
    # the associated file if exists

    job_param_name = extract_from_first_bracketed(object_path)

    # Look to see if file import(s) already exist(s) for this param in the current job
    try:
        previous_files = models.File.objects.filter(
            job=job, job_param_name=job_param_name
        )
        for previous_file in previous_files:
            logger.warning(
                "Upload will replace existing imported file [%s]", previous_file
            )
            try:
                file_import = models.FileImport.objects.get(file=previous_file)
                file_import.delete()
            except models.FileImport.DoesNotExist:
                logger.warning(
                    "No file import for job %s job_param_name %s",
                    job.uuid,
                    job_param_name,
                )
            try:
                previous_file.path.unlink()
                previous_file.delete()
            except Exception as err:
                logger.exception(
                    "Error deleting file import %s for job %s job_param_name %s",
                    previous_file,
                    job.uuid,
                    job_param_name,
                    exc_info=err,
                )
                continue

    except models.File.DoesNotExist:
        logger.warning(
            "No previous file import for job %s job_param_name %s",
            job.uuid,
            job_param_name,
        )

    assert isinstance(
        param_object,
        (
            CCP4File.CDataFile,
            CDataFile,
            CCP4XtalData.CMtzDataFile,
            CMtzDataFile,
        ),
    ), f"param_object must be CDataFile, got {type(param_object)}"
    assert len(files) == 1, f"Expected 1 file, got {len(files)}"

    # Check MRO for debugging
    logger.info("param_object MRO: %s", [c.__name__ for c in type(param_object).__mro__])
    logger.info("isinstance CMtzDataFile check: %s", isinstance(param_object, (CCP4XtalData.CMtzDataFile, CMtzDataFile)))

    # Reached here and confirmed that the param to which we are associatnig the file is
    # based on CDataFile
    initial_download_project_folder = (
        "CCP4_DOWNLOADED_FILES"
        if isinstance(
            param_object,
            (
                CCP4XtalData.CMtzDataFile,
                CMtzDataFile,
            ),
        )
        else "CCP4_IMPORTED_FILES"
    )
    logger.info("initial_download_project_folder: %s", initial_download_project_folder)

    downloaded_file_path = download_file(job, files[0], initial_download_project_folder)
    assert downloaded_file_path.exists(), f"Downloaded file not found: {downloaded_file_path}"
    file_type = detect_file_type(downloaded_file_path)

    logger.info(
        "param_object: %s, class: %s, file_type: %s",
        param_object,
        param_object.__class__.__name__,
        file_type,
    )

    if isinstance(
        param_object,
        (
            CCP4XtalData.CMtzDataFile,
            CMtzDataFile,
        ),
    ):
        column_selector = request.POST.get("column_selector", None)
        logger.info("MTZ path - column_selector: %s", column_selector)
        imported_file_path = handle_reflections(
            job, param_object, files[0].name, column_selector, downloaded_file_path
        )
        logger.info("handle_reflections returned: %s", imported_file_path)
    else:
        logger.info("Non-MTZ path - using downloaded file directly")
        imported_file_path = downloaded_file_path

    logger.error(
        "Final imported file destination is %s %s",
        imported_file_path,
        imported_file_path.name,
    )

    logger.info("Setting full path on param_object: %s", imported_file_path)
    param_object.setFullPath(str(imported_file_path))
    logger.info("Loading file...")
    param_object.loadFile()
    # Modern CDataFile.setContentFlag() auto-detects content, no reset parameter needed
    logger.info("Setting content flag...")
    param_object.setContentFlag()

    # Note deliberate explicit for != None instead of is not None
    try:
        subType = int(param_object.subType)
    except Exception:
        subType = 1
    try:
        contentFlag = int(param_object.contentFlag)
    except Exception:
        contentFlag = 0

    logger.info("subType: %s, contentFlag: %s", subType, contentFlag)

    try:
        # Use modern CData API: get_qualifier() instead of QUALIFIERS dict
        mime_type_name = param_object.get_qualifier("mimeTypeName")
        type = models.FileType.objects.get(name=mime_type_name)
        logger.info("FileType from mimeTypeName '%s': %s", mime_type_name, type)
    except models.FileType.DoesNotExist:
        type = models.FileType.objects.get(name="Unknown")
        logger.info("FileType not found, using Unknown")

    # Okay, so here is a thing. I do not think that the apropriate value for "job_param_name" is param_object.object_name()
    # Consider the "source" file in a CAsuContentSeq object. The object name is "source" but the relevant parameter name is
    # ASU_CONTENT[i].source , where i is the number of the asu content in the CAsuContentSeqLIst list. This is gernally true for items that
    # are children of lists (Don't even get me started on CEnsembles, where files are children of a list of lists)
    # So, we need to get the parameter name from the object path. I propose to look at the objects "path" and adopt the
    # value from just before the first array-indirection brackets.  hence coot_rebuild.outputData.XYZOUT[0] becomes
    # job_param_name XYZOUT[0]. This is a bit of a hack, but it works.

    new_file = models.File(
        job=job,
        name=str(imported_file_path.name),
        directory=models.File.Directory.IMPORT_DIR,
        type=type,
        annotation=f"Imported from {files[0].name}",
        job_param_name=job_param_name,
        sub_type=subType,
        content=contentFlag,
    )
    new_file.save()

    new_file_import = models.FileImport(
        file=new_file, name=files[0].name, checksum=param_object.checksum()
    )
    new_file_import.save()
    # Note: calling set_parameter here would invalidate "param_object" (since it takes job argument and constructs a new container),
    # replacing it with updated
    updated_object_dict = {
        "project": str(job.project.uuid).replace("-", ""),
        "baseName": new_file.name,
        "relPath": pathlib.Path(imported_file_path)
        .relative_to(job.project.directory)
        .parent,
        "annotation": new_file.annotation,
        "dbFileId": str(new_file.uuid).replace("-", ""),
        "subType": new_file.sub_type,
        "contentFlag": new_file.content,
    }
    logger.info("Calling set_parameter_container with path: %s", normalized_path)
    logger.info("updated_object_dict: %s", updated_object_dict)
    updated_object = set_parameter_container(
        container,
        normalized_path,
        updated_object_dict,
    )
    logger.info("set_parameter_container returned: %s", updated_object)
    save_params_for_job(the_job_plugin=plugin, the_job=job)

    result = json.loads(json.dumps(updated_object, cls=CCP4i2JsonEncoder))
    logger.info("=== upload_file_param END - returning: %s ===", result)
    return result


def download_file(job: models.Job, the_file, initial_download_project_folder: str):
    logger.debug("the_file is %s", the_file.name)
    file_stem = pathlib.Path(the_file.name).stem
    file_suffix = pathlib.Path(the_file.name).suffix
    destination_dir = (
        pathlib.Path(job.project.directory) / initial_download_project_folder
    )
    if not destination_dir.is_dir():
        destination_dir.mkdir()
    dest = (destination_dir / slugify(file_stem)).with_suffix(file_suffix)
    dest = available_file_name_based_on(dest)

    assert dest.is_relative_to(destination_dir)

    logger.debug("Settled on destination path %s", dest)
    with open(dest, "wb") as uploadFile:
        CHUNK = 1024 * 1024
        while True:
            chunk = the_file.read(CHUNK)
            if not chunk:
                break
            uploadFile.write(chunk)
        uploadFile.close()
    logger.debug("Upload complete")
    return dest


def handle_reflections(
    job: models.Job,
    param_object: CMtzDataFile,
    file_name: str,
    column_selector: str,
    downloaded_file_path: pathlib.Path,
):
    logger.error(
        "Dealing with a reflection object %s %s",
        isinstance(param_object, (CMtzDataFile,)),
        isinstance(param_object, (CCP4XtalData.CMtzDataFile,)),
    )
    try:
        _ = gemmi.read_mtz_file(str(downloaded_file_path))
    except RuntimeError as err:
        logger.exception(
            "Error reading MTZ file %s", downloaded_file_path, exc_info=err
        )
        downloaded_file_path, default_column_selector = gemmi_convert_to_mtz(
            param_object, downloaded_file_path
        )
        if column_selector is None:
            column_selector = default_column_selector

    dest = (
        pathlib.Path(job.project.directory)
        / "CCP4_IMPORTED_FILES"
        / slugify(pathlib.Path(file_name).stem)
    ).with_suffix(pathlib.Path(downloaded_file_path).suffix)
    logger.error("Preferred imported file destination is %s", dest)
    imported_file_path = gemmi_split_mtz(downloaded_file_path, column_selector, dest)
    return imported_file_path


def gemmi_convert_to_mtz(dobj: CMtzDataFile, downloaded_file_path: pathlib.Path):
    document = gemmi.cif.read_file(str(downloaded_file_path))
    # But what if there are multiple blocks?
    block = gemmi.as_refln_blocks(document)[0]
    converter = gemmi.CifToMtz()
    returned_mtz = converter.convert_block_to_mtz(block)
    # print(returned_mtz.column_labels())
    dest = downloaded_file_path.with_suffix(".mtz")
    deduped_dest = available_file_name_based_on(dest)
    returned_mtz.write_to_file(str(deduped_dest))
    # print("dest", deduped_dest)
    analysis = find_column_selections(dobj, deduped_dest)
    # print(analysis)
    # FOr now assume that there is at least one matching column group and take the first
    selected_columns = analysis["options"][0]["columnPath"]
    print("selected_columns", selected_columns)
    return deduped_dest, selected_columns


def find_column_selections(data_object: CMtzDataFile, deduped_dest: pathlib.Path):
    data_object.setFullPath(str(deduped_dest))
    data_object.loadFile()
    # Data object suitable columns depend on the contents of the file...
    contents = data_object.getFileContent()
    # ...
    column_groups = contents.getColumnGroups()
    groups_dict = value_dict_for_object(column_groups)

    possibilities = []
    if isinstance(data_object, CCP4XtalData.CObsDataFile):
        possibilities = [
            column_group
            for column_group in groups_dict
            if column_group["columnGroupType"] == "Obs"
        ]
    elif isinstance(data_object, CCP4XtalData.CFreeRDataFile):
        possibilities = [
            column_group
            for column_group in groups_dict
            if column_group["columnGroupType"] == "FreeR"
        ]
    elif isinstance(data_object, CCP4XtalData.CPhsDataFile):
        possibilities = [
            column_group
            for column_group in groups_dict
            if column_group["columnGroupType"] == "Phs"
        ]
    elif isinstance(data_object, CCP4XtalData.CMapCoeffsDataFile):
        possibilities = handle_map_coeffs(groups_dict)

    if len(possibilities) == 0:
        return {"options": [], "originalName": deduped_dest.name}

    possibilities = sorted(possibilities, key=lambda example: -example["contentFlag"])
    for possibility in possibilities:
        possibility_column_path = "/*/{}/[{}]".format(
            possibility["dataset"],
            ",".join([column["columnLabel"] for column in possibility["columnList"]]),
        )
        possibility["columnPath"] = possibility_column_path
    # print("possibilities", possibilities)
    return {"options": possibilities, "originalName": deduped_dest.name}


def handle_map_coeffs(groups_dict: dict):
    fs = {}
    phis = {}
    for group in groups_dict:
        for column in group["columnList"]:
            if column["columnType"] == "F":
                fs[group["dataset"]] = column
            elif column["columnType"] == "P":
                phis[group["dataset"]] = column
    possibilities = []

    for key, f_column in fs.items():
        if key in phis:
            f_column["groupIndex"] = len(possibilities) + 1
            phis[key]["groupIndex"] = len(possibilities) + 1
            possibility = {
                "columnGroupType": "MapCoeffs",
                "contentFlag": 1,
                "dataset": key,
                "columnList": [f_column, phis[key]],
            }
            possibilities.append(possibility)

    return possibilities
