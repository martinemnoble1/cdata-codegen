import json
import logging
import gemmi
from core import CCP4File
from core import CCP4XtalData
from core import CCP4ModelData
from core.CCP4Container import CContainer
from core.CCP4XtalData import CGenericReflDataFile
from core.CCP4XtalData import CMapDataFile
from core.CCP4ModelData import CPdbDataFile, CDictDataFile
from core import CCP4DataManager
from core.CCP4File import CDataFile
from core.CCP4File import CDataFile
from ccp4i2.pipelines.import_merged.script import mmcifutils
from .find_objects import find_objects, find_object_by_path
from .get_job_container import get_job_container
from .json_encoder import CCP4i2JsonEncoder
from .parse_cif_ligand_summary import parse_cif_ligand_summary
from .value_dict_for_object import value_dict_for_object
from ...db import models
from ..parse import identify_data_type

logger = logging.getLogger(f"ccp4x:{__name__}")

FILETYPES_TEXT = [
    "Unknown",
    "application/CCP4-seq",
    "chemical/x-pdb",
    "MultiPDB",
    "application/CCP4-mtz",
    "application/CCP4-unmerged-mtz",
    "application/CCP4-unmerged-experimental",
    "application/CCP4-map",
    "application/refmac-dictionary",
    "application/refmac-TLS",
    "application/CCP4-mtz-freerflag",
    "application/CCP4-mtz-observed",
    "application/CCP4-mtz-phases",
    "application/CCP4-mtz-map",
    "Dummy",
    "application/CCP4-seqalign",
    "application/CCP4-mtz-mini",
    "application/coot-script",
    "application/refmac-external-restraints",
    "application/CCP4-scene",
    "application/CCP4-shelx-FA",
    "application/phaser-sol",
    "chemical/x-mdl-molfile",
    "application/iMosflm-xml",
    "application/CCP4-image",
    "application/CCP4-generic-reflections",
    "application/HHPred-alignments",
    "application/Blast-alignments",
    "chemical/x-pdb-ensemble",
    "application/CCP4-asu-content",
    "application/dials-jfile",
    "application/dials-pfile",
    "application/phaser-rfile",
    "application/refmac-keywords",
    "application/x-pdf",
    "application/postscript",
    "application/EBI-validation-xml",
    "chemical/x-cif",
]
FILETYPES_CLASS = [
    "DataFile",
    "SeqDataFile",
    "PdbDataFile",
    "",
    "MtzDataFile",
    "MtzDataFile",
    "UnmergedDataFile",
    "MapDataFile",
    "DictDataFile",
    "TLSDataFile",
    "FreeRDataFile",
    "ObsDataFile",
    "PhsDataFile",
    "MapCoeffsDataFile",
    "",
    "SeqAlignDataFile",
    "MiniMtzDataFile",
    "CootHistoryDataFile",
    "RefmacRestraintsDataFile",
    "SceneDataFile",
    "ShelxFADataFile",
    "PhaserSolDataFile",
    "MDLMolDataFile",
    "ImosflmXmlDataFile",
    "ImageFile",
    "GenericReflDataFile",
    "HhpredDataFile",
    "BlastDataFile",
    "EnsemblePdbDataFile",
    "AsuDataFile",
    "DialsJsonFile",
    "DialsPickleFile",
    "PhaserRFileDataFile",
    "RefmacKeywordFile",
    "PDFDataFile",
    "PostscriptDataFile",
    "EBIValidationXMLDataFile",
    "MmcifReflDataFile",
]


def is_basic_type(obj):
    return isinstance(obj, (str, int, float, bool, type(None)))


def is_custom_class_instance(obj):
    return not is_basic_type(obj) and not isinstance(obj, (list, dict, tuple))


def flatten_instance(obj):
    if is_basic_type(obj):
        return obj
    elif isinstance(obj, list):
        return [flatten_instance(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(flatten_instance(item) for item in obj)
    elif isinstance(obj, dict):
        return {key: flatten_instance(value) for key, value in obj.items()}
    elif hasattr(obj, "__dict__"):
        return {
            key: flatten_instance(value)
            for key, value in vars(obj).items()
            if not callable(value) and not key.startswith("_")
        }
    elif hasattr(obj, "__slots__"):
        return {
            slot: flatten_instance(getattr(obj, slot))
            for slot in obj.__slots__
            if hasattr(obj, slot)
        }
    else:
        # fallback: use repr to avoid exceptions
        return repr(obj)


def digest_file(the_file: models.File):
    mimetype = the_file.type.pk
    if mimetype not in FILETYPES_TEXT:
        return {"status": "Failed", "reason": "File type not supported for digest"}

    mimetype_index = FILETYPES_TEXT.index(mimetype)
    logger.debug("mimetype_index %s", mimetype_index)
    if mimetype_index >= len(FILETYPES_CLASS):
        return {"status": "Failed", "reason": "File type not supported for digest"}
    class_name = FILETYPES_CLASS[mimetype_index]
    logger.debug("class_name %s", class_name)
    data_manager: CCP4DataManager.CDataManager = CCP4DataManager.CDataManager()
    the_class = data_manager.getClass(f"C{class_name}")
    if the_class is None:
        return {"status": "Failed", "reason": "File type not supported for digest"}
    logger.debug("the_class %s", the_class)
    try:
        file_object = the_class()
        file_object.setFullPath(str(the_file.path))
    except Exception as err:
        logger.exception("Error creating file object %s", the_file, exc_info=err)
        return {"status": "Failed", "reason": str(err), "digest": {}}
    return digest_file_object(file_object)


def digest_param_file(the_job, object_path):
    the_container: CContainer = get_job_container(the_job)
    try:
        file_object: CDataFile = find_object_by_path(the_container, object_path)
        return digest_file_object(file_object)
    except IndexError as err:
        logger.exception("Error finding object with path %s", object_path, exc_info=err)
        return {"status": "Failed", "reason": str(err), "digest": {}}
    except Exception as err:
        logger.exception("Other exception %s", object_path, exc_info=err)
        return {"status": "Failed", "reason": str(err), "digest": {}}


def digest_file_object(file_object: CDataFile):
    if not isinstance(file_object, CCP4File.CDataFile):
        return {"status": "Failed", "reason": "Not a valid file object", "digest": {}}
    if not file_object.isSet():
        return {"status": "Failed", "reason": "File object is not set", "digest": {}}
    print("oops")
    if isinstance(file_object, CCP4ModelData.CPdbDataFile):
        return digest_cpdbdata_file_object(file_object)
    if isinstance(file_object, CCP4XtalData.CGenericReflDataFile):
        return digest_cgenericrefldatafile_file_object(file_object)
    if isinstance(file_object, CCP4ModelData.CSeqDataFile):
        return digest_cseqdata_file_object(file_object)
    if isinstance(file_object, (CCP4ModelData.CDictDataFile, CDictDataFile)):
        return digest_cdictdata_file_object(file_object)
    if type(file_object) is CCP4File.CDataFile:
        return digest_cdatafile_file_object(file_object)
    return digest_other_file_object(file_object)


def digest_other_file_object(file_object: CDataFile):
    try:
        file_object.loadFile()
        file_object.setContentFlag(reset=True)
        contents = file_object.getFileContent()
        content_dict = value_dict_for_object(contents)
        return content_dict
    except Exception as err:
        logger.exception("Error digesting file %s", file_object, exc_info=err)
        return {
            "status": "Failed",
            "reason": f"Failed digesting CDataFile {err}",
            "digest": {},
        }


def digest_cpdbdata_file_object(file_object: CPdbDataFile):
    content_dict = {}
    if not isinstance(file_object, CCP4ModelData.CPdbDataFile):
        return {"status": "Failed", "reason": "Not a CPdbDataFile object", "digest": {}}
    if not file_object.isSet():
        return {"status": "Failed", "reason": "File object is not set", "digest": {}}
    try:
        file_object.loadFile()
        file_object.setContentFlag(reset=True)
        contents = file_object.getFileContent()
        contents.loadFile(file_object.fullPath)
        contents.loadSequences(contents.molHnd)
        content_dict = {
            "sequences": contents.sequences,
            "composition": {
                key: getattr(contents.composition, key)
                for key in [
                    "chains",
                    "peptides",
                    "nucleics",
                    "solventChains",
                    "monomers",
                    "nresSolvent",
                    "moleculeType",
                    "containsHydrogen",
                ]
            },
        }
        return content_dict
    except Exception as err:
        logger.exception("Error digesting file %s", file_object, exc_info=err)
        return {
            "status": "Failed",
            "reason": f"Failed digesting CPdbDataFile {err}",
            "digest": {},
        }


def digest_cseqdata_file_object(file_object: CPdbDataFile):
    content_dict = {}
    if not isinstance(file_object, CCP4ModelData.CSeqDataFile):
        return {"status": "Failed", "reason": "Not a CSeqDataFile object", "digest": {}}
    if not file_object.isSet():
        return {"status": "Failed", "reason": "File object is not set", "digest": {}}
    try:
        file_object.loadFile()
        file_object.setContentFlag(reset=True)
        contents = file_object.getFileContent()
        content_dict = value_dict_for_object(contents)
        return content_dict
    except Exception as err:
        logger.exception("Error digesting file %s", file_object, exc_info=err)
        return {
            "status": "Failed",
            "reason": f"Failed digesting CSeqDataFile {err}",
            "digest": {},
        }


def digest_cdictdata_file_object(file_object: CPdbDataFile):
    if not isinstance(file_object, (CCP4ModelData.CDictDataFile, CDictDataFile)):
        return {
            "status": "Failed",
            "reason": "Not a CDictDataFile object",
            "digest": {},
        }
    content_dict = parse_cif_ligand_summary(file_object.fullPath.__str__())
    return content_dict


def digest_cgenericrefldatafile_file_object(file_object: CGenericReflDataFile):
    content_dict = {}
    if not isinstance(file_object, CCP4XtalData.CGenericReflDataFile):
        return {
            "status": "Failed",
            "reason": "Not a CGenericReflDataFile object",
            "digest": {},
        }
    if not file_object.isSet():
        return {"status": "Failed", "reason": "File object is not set", "digest": {}}
    try:
        file_object.loadFile()
        file_object.setContentFlag(reset=True)
        contents = file_object.getFileContent()
        content_dict = value_dict_for_object(contents)
        content_dict["format"] = file_object.getFormat()
        content_dict["merged"] = file_object.getMerged()
        if file_object.getFormat() == "mmcif":
            mmcif = gemmi.cif.read_file(file_object.fullPath.__str__())
            rblocks = gemmi.as_refln_blocks(mmcif)
            rblock_infos = []
            for rb in rblocks:
                blkinfo = mmcifutils.CifBlockInfo(rb)
                rblock_infos.append(flatten_instance(blkinfo))
            content_dict["rblock_infos"] = rblock_infos
        return content_dict
    except Exception as err:
        logger.exception("Error digesting file %s", file_object, exc_info=err)
        return {
            "status": "Failed",
            "reason": f"Failed digesting CGenericReflDataFile {err}",
            "digest": {},
        }


def digest_cdatafile_file_object(file_object: CDataFile):
    if not isinstance(file_object, CCP4File.CDataFile):
        return {"status": "Failed", "reason": "Not a CDataFile object", "digest": {}}
    if not file_object.isSet():
        return {"status": "Failed", "reason": "File object is not set", "digest": {}}
    try:
        result = identify_data_type(str(file_object.fullPath))
        if result["data_type_name"] in ["mtz", "sfcif"]:
            specific_object = CCP4XtalData.CGenericReflDataFile()
            specific_object.setFullPath(str(file_object.fullPath))
            return digest_cgenericrefldatafile_file_object(specific_object)
        elif result["data_type_name"] == "model":
            specific_object = CCP4ModelData.CPdbDataFile()
            specific_object.setFullPath(str(file_object.fullPath))
            return digest_cpdbdata_file_object(specific_object)
        elif result["data_type_name"] == "map":
            specific_object = CCP4XtalData.CMapDataFile()
            specific_object.setFullPath(str(file_object.fullPath))
            return digest_other_file_object(specific_object)
        elif result["data_type_name"] == "sequence":
            specific_object = CCP4ModelData.CSeqDataFile()
            specific_object.setFullPath(str(file_object.fullPath))
            return digest_cseqdata_file_object(specific_object)
        return digest_other_file_object(file_object)

    except Exception as err:
        logger.exception("Error digesting file %s", file_object, exc_info=err)
        return {
            "status": "Failed",
            "reason": f"Failed digesting CDataFile {err}",
            "digest": {},
        }
