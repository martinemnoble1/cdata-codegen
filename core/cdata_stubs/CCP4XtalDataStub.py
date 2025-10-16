"""Generated classes from CCP4XtalData.py"""

from ..base_object.base_classes import CData, CContainer
from ..CCP4FundamentalTypes import CInt, CList, CBoolean, CFloat, CString, COneWord
from ..base_object.class_metadata import cdata_class, attribute, AttributeType

from .CCP4BaseFile-stub import CDataFileContent, CDataFile, CXmlDataFile, CI2XmlDataFile


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CXia2ImageSelectionList",
)
class CXia2ImageSelectionList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "imageFile": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CImageFile", tooltip="imageFile attribute"),
        "imageStart": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="imageStart attribute"),
        "imageEnd": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="imageEnd attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "toolTip": 'select an image file and an optional range of files to define a dataset'
    },
    contents_order=['imageFile', 'imageStart', 'imageEnd'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CXia2ImageSelection",
)
class CXia2ImageSelection(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "below minimum"
        },
        "102": {
            "description": "above maximum"
        },
        "103": {
            "description": "not one of limited allowed values"
        }
    },
    qualifiers={
        "min": 0.0,
        "toolTip": 'Data collection wavelength in Angstrom'
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'
    ],
    qualifiers_definition={
        "default": {"type": float},
        "max": {"description": "The inclusive maximum value"},
        "min": {"description": "The inclusive minimum value"},
        "enumerators": {"type": list, "description": "A Python list of allowed or recommended values - see onlyEnumerators"},
        "menuText": {"type": list, "listItemType": "<class 'str'>", "description": "A Python list of strings, matching items in enumerators list, to appear on GUI menu"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"}
    },
    gui_label="CWavelength",
)
class CWavelength(CFloat):
    """Wavelength in Angstrom"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CUnmergedDataFileList",
)
class CUnmergedDataFileList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-unmerged-experimental',
        "mimeTypeDescription": 'Unmerged experimental data',
        "fileExtensions": ['mtz', 'hkl', 'HKL', 'sca', 'SCA', 'ent', 'cif'],
        "fileContentClassName": 'CUnmergedDataContent',
        "guiLabel": 'Unmerged reflections',
        "toolTip": 'Unmerged experimental data in any format',
        "helpFile": 'data_files#unmerged_data'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CUnmergedDataFile",
)
class CUnmergedDataFile(CDataFile):
    """Handle MTZ, XDS and scalepack files. Allow wildcard filename"""
    pass


@cdata_class(
    attributes={
        "format": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="format attribute"),
        "merged": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="merged attribute"),
        "crystalName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCrystalName", tooltip="crystalName attribute"),
        "datasetName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CDatasetName", tooltip="datasetName attribute"),
        "cell": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCell", tooltip="cell attribute"),
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CSpaceGroup", tooltip="spaceGroup attribute"),
        "batchs": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="batchs attribute"),
        "lowRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="lowRes attribute"),
        "highRes": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="highRes attribute"),
        "knowncell": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="knowncell attribute"),
        "knownwavelength": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="knownwavelength attribute"),
        "numberLattices": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="numberLattices attribute"),
        "wavelength": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CWavelength", tooltip="wavelength attribute"),
        "numberofdatasets": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="numberofdatasets attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CUnmergedDataContent",
)
class CUnmergedDataContent(CDataFileContent):
    """Base class for classes holding file contents"""
    pass


@cdata_class(
    attributes={
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CSpaceGroup", tooltip="spaceGroup attribute"),
        "cell": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCell", tooltip="cell attribute")
    },
    error_codes={
        "101": {
            "description": "Cell lengths should NOT be identical"
        },
        "102": {
            "description": "Cell angles should NOT be identical"
        },
        "103": {
            "description": "Cell angle should be 90"
        },
        "104": {
            "description": "Cell angle should NOT be 90"
        },
        "105": {
            "description": "Cell lengths should be identical"
        },
        "106": {
            "description": "Cell angle should be 120"
        },
        "107": {
            "description": "Cell angle should be identical"
        }
    },
    qualifiers={
        "toolTip": 'Space group and cell length and angles',
        "helpFile": 'crystal_data#cell_space_group'
    },
    contents_order=['spaceGroup', 'cell'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CSpaceGroupCell",
)
class CSpaceGroupCell(CData):
    """Cell space group and parameters"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Invalid space group"
        },
        "102": {
            "description": "Space group is not chiral",
            "severity": 2
        },
        "103": {
            "description": "Space group is not Hermann-Mauguin standard"
        },
        "104": {
            "description": "Space group is not a chiral Hermann-Mauguin standard. Full syminfo.lib information not loaded."
        },
        "105": {
            "description": "Space group is not Hermann-Mauguin standard - has wrong number of spaces?"
        },
        "106": {
            "description": "Space group is undefined",
            "severity": 1
        },
        "107": {
            "description": "Space group is undefined"
        },
        "108": {
            "description": "Space group is incomplete",
            "severity": 2
        }
    },
    qualifiers={
        "allowUndefined": True,
        "toolTip": 'Hermann-Mauguin space group name',
        "helpFile": 'crystal_data#space_group'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CSpaceGroup",
)
class CSpaceGroup(CString):
    """A string holding the space group"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "String too short"
        },
        "102": {
            "description": "String too long"
        },
        "103": {
            "description": "not one of limited allowed values"
        },
        "104": {
            "description": "Contains disallowed characters"
        }
    },
    qualifiers={
        "onlyEnumerators": True,
        "default": 'UNDEFINED',
        "enumerators": ['UNDEFINED', 'HREM', 'LREM', 'PEAK', 'INFL', 'NAT', 'DERI'],
        "menuText": ['undefined', 'high remote', 'low remote', 'peak', 'inflection', 'native', 'derivative'],
        "toolTip": 'Hint to Shelx for the use of the dataset'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CShelxLabel",
)
class CShelxLabel(CString):
    """A string"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-shelx-FA',
        "mimeTypeDescription": 'Shelx FA',
        "fileExtensions": ['hkl'],
        "fileContentClassName": None,
        "fileLabel": 'shelx_FA',
        "guiLabel": 'Shelx FA',
        "toolTip": 'Data used by Shelx programs',
        "helpFile": 'data_files#shelxfa'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CShelxFADataFile",
)
class CShelxFADataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 1
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CRunBatchRangeList",
)
class CRunBatchRangeList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "runNumber": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="runNumber attribute"),
        "batchRange0": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="batchRange0 attribute"),
        "batchRange1": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="batchRange1 attribute"),
        "resolution": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="resolution attribute"),
        "fileNumber": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="fileNumber attribute")
    },
    error_codes={
        "101": {
            "description": "End of batch range less than start"
        },
        "102": {
            "description": "All items must be set"
        }
    },
    qualifiers={
        "toolTip": 'Specify range of reflections to treat as one run'
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CRunBatchRange",
)
class CRunBatchRange(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "low": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="low attribute"),
        "high": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="high attribute")
    },
    error_codes={
        "201": {
            "description": "High/low resolution wrong way round?"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CResolutionRange",
)
class CResolutionRange(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "h": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="h attribute"),
        "k": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="k attribute"),
        "l": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="l attribute")
    },
    error_codes={
        "201": {
            "description": "Operator has bad syntax (needs three comma-separated fields)"
        },
        "202": {
            "description": "Operator contains invalid characters"
        },
        "203": {
            "description": "Operator is not set"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['h', 'k', 'l'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CReindexOperator",
)
class CReindexOperator(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/refmac-keywords',
        "mimeTypeDescription": 'Refmac keyword file',
        "fileExtensions": ['txt'],
        "fileContentClassName": None,
        "fileLabel": 'refmac_keywords',
        "guiLabel": 'Refmac keyword file',
        "toolTip": 'A file containing keywords as they are meant to be read by refmac5'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CRefmacKeywordFile",
)
class CRefmacKeywordFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "columnGroup": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CMtzColumnGroup", tooltip="columnGroup attribute"),
        "datasetName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="datasetName attribute")
    },
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "MTZ file is not defined",
            "severity": 2
        },
        "104": {
            "description": "No column group selected"
        },
        "105": {
            "description": "No column group selected",
            "severity": 2
        }
    },
    qualifiers={
        "mustExist": False,
        "mtzFileKey": '',
        "groupTypes": []
    },
    qualifiers_order=[
        'groupTypes',
        'mtzFileKey',
        'mustExist'
    ],
    qualifiers_definition={
        "groupTypes": {"type": list, "description": "Type of columnGroup required by program"},
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"}
    },
    gui_label="CProgramColumnGroup0",
)
class CProgramColumnGroup0(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "mustExist": False,
        "mtzFileKey": '',
        "toolTipList": [],
        "default": []
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CProgramColumnGroup",
)
class CProgramColumnGroup(CData):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Phase and figure of merit'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CPhiFomColumnGroup",
)
class CPhiFomColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/phaser-sol',
        "mimeTypeDescription": 'Phaser solution file',
        "fileExtensions": ['phaser_sol.pkl'],
        "fileContentClassName": None,
        "fileLabel": 'phaser_sol',
        "guiLabel": 'Phaser solutions',
        "toolTip": 'Possible solutions passed between runs of the Phaser program',
        "helpFile": 'data_files#phasersol'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CPhaserSolDataFile",
)
class CPhaserSolDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/phaser-rfile',
        "mimeTypeDescription": 'Phaser rotation solution file',
        "fileExtensions": ['phaser_rlist.pkl'],
        "fileContentClassName": None,
        "fileLabel": 'phaser_rfile',
        "guiLabel": 'Phaser rotation solution',
        "toolTip": 'Phaser rfile solutions for rotation search'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CPhaserRFileDataFile",
)
class CPhaserRFileDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "name": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="name attribute"),
        "columnGroups": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="columnGroups attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMtzDataset",
)
class CMtzDataset(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "151": {
            "description": "Failed converting MTZ file to alternative format"
        },
        "152": {
            "description": "Failed merging MTZ file - invalid input"
        },
        "153": {
            "description": "Failed merging MTZ files - error running cmtzjoin - see log"
        },
        "154": {
            "description": "Failed merging MTZ files - error running cad - see log"
        },
        "401": {
            "description": "MTZ file header data differs"
        },
        "402": {
            "description": "MTZ file columns differ"
        },
        "403": {
            "description": "Error trying to access number of reflections",
            "severity": 2
        },
        "404": {
            "description": "MTZ files have different number of reflections"
        },
        "405": {
            "description": "MTZ column mean value differs"
        },
        "406": {
            "description": "MTZ file header data differs - may be autogenerated names",
            "severity": 2
        },
        "407": {
            "description": "Error splitting MTZ file - failed creating input command to cmtzsplit"
        },
        "408": {
            "description": "Error splitting MTZ file - output file missing"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz',
        "mimeTypeDescription": 'MTZ experimental data',
        "fileExtensions": ['mtz'],
        "fileContentClassName": 'CMtzData',
        "guiLabel": 'Experimental data',
        "toolTip": "Experimental data in CCP4's MTZ format",
        "helpFile": 'data_files#MTZ'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "sameCrystalAs": {"type": str, "description": "Name of CMtzDataFile object that crystal parameters should match - probably the observed data"},
        "sameCrystalLevel": {"type": int, "description": "Rigour of same crystal test"}
    },
    gui_label="CMtzDataFile",
)
class CMtzDataFile(CDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "151": {
            "description": "Failed converting MTZ file to alternative format"
        },
        "152": {
            "description": "Failed merging MTZ file - invalid input"
        },
        "153": {
            "description": "Failed merging MTZ files - error running cmtzjoin - see log"
        },
        "154": {
            "description": "Failed merging MTZ files - error running cad - see log"
        },
        "401": {
            "description": "MTZ file header data differs"
        },
        "402": {
            "description": "MTZ file columns differ"
        },
        "403": {
            "description": "Error trying to access number of reflections",
            "severity": 2
        },
        "404": {
            "description": "MTZ files have different number of reflections"
        },
        "405": {
            "description": "MTZ column mean value differs"
        },
        "406": {
            "description": "MTZ file header data differs - may be autogenerated names",
            "severity": 2
        },
        "407": {
            "description": "Error splitting MTZ file - failed creating input command to cmtzsplit"
        },
        "408": {
            "description": "Error splitting MTZ file - output file missing"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz-unmerged',
        "mimeTypeDescription": 'MTZ unmerged experimental data',
        "fileExtensions": ['mtz'],
        "fileContentClassName": None,
        "guiLabel": 'Unmerged MTZ reflections',
        "toolTip": "Unmerged experimental data in CCP4's MTZ format"
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "sameCrystalAs": {"type": str, "description": "Name of CMtzDataFile object that crystal parameters should match - probably the observed data"},
        "sameCrystalLevel": {"type": int, "description": "Rigour of same crystal test"}
    },
    gui_label="CUnmergedMtzDataFile",
)
class CUnmergedMtzDataFile(CMtzDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    attributes={
        "cell": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCell", tooltip="cell attribute"),
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CSpaceGroup", tooltip="spaceGroup attribute"),
        "resolutionRange": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CResolutionRange", tooltip="resolutionRange attribute"),
        "listOfColumns": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="listOfColumns attribute"),
        "datasets": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="datasets attribute"),
        "crystalNames": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="crystalNames attribute"),
        "wavelengths": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="wavelengths attribute"),
        "datasetCells": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="datasetCells attribute"),
        "merged": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="merged attribute")
    },
    error_codes={
        "101": {
            "description": "Attempting to load MTZ data from non-existant/broken file"
        },
        "102": {
            "description": "Error creating command file for mtzdump"
        },
        "103": {
            "description": "No log file found from mtzdump"
        },
        "104": {
            "description": "Error reading log file from mtzdump"
        },
        "105": {
            "severity": 2,
            "description": "Different spacegroup"
        },
        "106": {
            "severity": 2,
            "description": "Different cell parameter"
        },
        "107": {
            "severity": 2,
            "description": "Different cell parameters"
        },
        "108": {
            "severity": 4,
            "description": "Different Laue group"
        },
        "109": {
            "severity": 4,
            "description": "Different point group"
        },
        "410": {
            "description": "Invalid CSeqDataFile passed to matthewCoeff"
        },
        "411": {
            "description": "Failed to run matthewCoeff"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMtzData",
)
class CMtzData(CDataFileContent):
    """Base class for classes holding file contents"""
    pass


@cdata_class(
    attributes={
        "groupType": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CMtzColumnGroupType", tooltip="groupType attribute"),
        "columns": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="columns attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMtzColumnGroup",
)
class CMtzColumnGroup(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "columnLabel": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="columnLabel attribute"),
        "columnType": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CColumnType", tooltip="columnType attribute"),
        "dataset": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="dataset attribute"),
        "groupIndex": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="groupIndex attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMtzColumn",
)
class CMtzColumn(CData):
    """An MTZ column with column label and column type"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "guiLabel": 'mmCIF reflection data',
        "mimeTypeName": 'chemical/x-cif',
        "toolTip": 'A reflection file in mmCIF format',
        "fileContentClassName": 'CMmcifReflData',
        "helpFile": 'data_files#mmCIF'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CMmcifReflDataFile",
)
class CMmcifReflDataFile(CMmcifDataFile):
    """A reflection file in mmCIF format"""
    pass


@cdata_class(
    attributes={
        "cell": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCell", tooltip="cell attribute"),
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CSpaceGroup", tooltip="spaceGroup attribute"),
        "wavelength": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CWavelength", tooltip="wavelength attribute"),
        "haveFreeRColumn": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="haveFreeRColumn attribute"),
        "haveFobsColumn": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="haveFobsColumn attribute"),
        "haveFpmObsColumn": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="haveFpmObsColumn attribute"),
        "haveIobsColumn": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="haveIobsColumn attribute"),
        "haveIpmObsColumn": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="haveIpmObsColumn attribute")
    },
    error_codes={
        "101": {
            "description": "Attempting to load mmCIF data from non-existant/broken file"
        },
        "102": {
            "description": "Error reading interpreting line in cif file"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMmcifReflData",
)
class CMmcifReflData(CMmcifData):
    """Generic mmCIF data.
This is intended to be a base class for other classes
specific to coordinates, reflections or geometry data."""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CMiniMtzDataFileList",
)
class CMiniMtzDataFileList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "201": {
            "description": "Wrong number of columns"
        },
        "202": {
            "description": "Wrong column types"
        },
        "203": {
            "description": "No correct column types found in file"
        },
        "204": {
            "description": "Duplicate or additional column types found in file"
        },
        "205": {
            "description": "Columns in file have non-standard labels"
        },
        "206": {
            "description": "File contains unmerged data"
        },
        "210": {
            "description": "Failed creating mini-MTZ"
        },
        "211": {
            "description": "Insufficient columns selected from imported MTZ"
        },
        "212": {
            "description": "Data already imported as",
            "severity": 2
        },
        "220": {
            "description": "Can not convert file content, file does not exist"
        },
        "221": {
            "description": "Can not convert file content, existing content insufficiently rich"
        },
        "222": {
            "description": "Can not convert file content, bad input for target content"
        },
        "223": {
            "description": "Can not recognise file content"
        },
        "224": {
            "description": "Not possible to convert to required content - no mechanism implemented"
        },
        "225": {
            "description": "Failed importing from an mmcif file - failed running cif2mtz"
        },
        "226": {
            "description": "Failed importing from an mmcif file - no output from cif2mtz"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz-mini',
        "fileExtensions": ['mtz', 'cif', 'ent'],
        "fileContentClassName": 'CMtzData',
        "saveToDb": True,
        "correctColumns": ['FQ', 'JQ', 'GLGL', 'KMKM', 'AAAA', 'PW', 'FP', 'I'],
        "toolTip": 'Mini-MTZ file containing reflection,phases,FreeR set or map coefficients',
        "helpFile": 'data_files#MTZ'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag',
        'correctColumns',
        'columnGroupClassList',
        'sameCrystalAs'
    ],
    qualifiers_definition={
        "correctColumns": {"type": list, "listItemType": "<class 'str'>", "description": "A list of coloumn data types expected in the file"}
    },
    gui_label="CMiniMtzDataFile",
)
class CMiniMtzDataFile(CMtzDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "201": {
            "description": "Wrong number of columns"
        },
        "202": {
            "description": "Wrong column types"
        },
        "203": {
            "description": "No correct column types found in file"
        },
        "204": {
            "description": "Duplicate or additional column types found in file"
        },
        "205": {
            "description": "Columns in file have non-standard labels"
        },
        "206": {
            "description": "File contains unmerged data"
        },
        "210": {
            "description": "Failed creating mini-MTZ"
        },
        "211": {
            "description": "Insufficient columns selected from imported MTZ"
        },
        "212": {
            "description": "Data already imported as",
            "severity": 2
        },
        "220": {
            "description": "Can not convert file content, file does not exist"
        },
        "221": {
            "description": "Can not convert file content, existing content insufficiently rich"
        },
        "222": {
            "description": "Can not convert file content, bad input for target content"
        },
        "223": {
            "description": "Can not recognise file content"
        },
        "224": {
            "description": "Not possible to convert to required content - no mechanism implemented"
        },
        "225": {
            "description": "Failed importing from an mmcif file - failed running cif2mtz"
        },
        "226": {
            "description": "Failed importing from an mmcif file - no output from cif2mtz"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz-phases',
        "mimeTypeDescription": 'MTZ phases',
        "fileExtensions": ['mtz', 'cif', 'ent'],
        "fileContentClassName": 'CMtzData',
        "guiLabel": 'Phases',
        "fileLabel": 'phases',
        "toolTip": 'Phases in Hendrickson-Lattmann or Phi/FOM form',
        "correctColumns": ['AAAA', 'PW'],
        "columnGroupClassList": ["<class 'ccp4x.data_scan.CCP4XtalData.CHLColumnGroup'>", "<class 'ccp4x.data_scan.CCP4XtalData.CPhiFomColumnGroup'>"],
        "helpFile": 'data_files#Phs'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag',
        'correctColumns',
        'columnGroupClassList',
        'sameCrystalAs'
    ],
    qualifiers_definition={
        "correctColumns": {"type": list, "listItemType": "<class 'str'>", "description": "A list of coloumn data types expected in the file"}
    },
    gui_label="CPhsDataFile",
)
class CPhsDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "301": {
            "description": "Running ctruncate failed"
        },
        "302": {
            "description": "Running cmtzsplit to convert observed data type failed"
        },
        "303": {
            "description": "Running sftools failed"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz-observed',
        "mimeTypeDescription": 'MTZ observed',
        "fileExtensions": ['mtz', 'cif', 'ent'],
        "fileContentClassName": 'CMtzData',
        "fileLabel": 'observed_data',
        "guiLabel": 'Reflections',
        "toolTip": 'Observed structure factors or intensities',
        "correctColumns": ['KMKM', 'GLGL', 'JQ', 'FQ'],
        "columnGroupClassList": ["<class 'ccp4x.data_scan.CCP4XtalData.CIPairColumnGroup'>", "<class 'ccp4x.data_scan.CCP4XtalData.CFPairColumnGroup'>", "<class 'ccp4x.data_scan.CCP4XtalData.CISigIColumnGroup'>", "<class 'ccp4x.data_scan.CCP4XtalData.CFSigFColumnGroup'>"],
        "downloadModes": ['ebiSFs'],
        "helpFile": 'data_files#Obs'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag',
        'correctColumns',
        'columnGroupClassList',
        'sameCrystalAs'
    ],
    qualifiers_definition={
        "correctColumns": {"type": list, "listItemType": "<class 'str'>", "description": "A list of coloumn data types expected in the file"}
    },
    gui_label="CObsDataFile",
)
class CObsDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 2,
        "saveToDb": True
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CMergeMiniMtzList",
)
class CMergeMiniMtzList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "fileName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CMiniMtzDataFile", tooltip="fileName attribute"),
        "columnTag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="columnTag attribute"),
        "columnNames": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="columnNames attribute")
    },
    error_codes={
        "201": {
            "description": "Selected file is not a suitable 'mini' MTZ containing experimental data object"
        },
        "202": {
            "description": "Output column name list does not have correct number of names"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['fileName', 'columnTag', 'columnNames'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CMergeMiniMtz",
)
class CMergeMiniMtz(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-map',
        "mimeTypeDescription": 'Map',
        "fileExtensions": ['map', 'mrc'],
        "fileContentClassName": None,
        "guiLabel": 'Map',
        "toolTip": 'A map in CCP4/MRC format',
        "helpFile": 'data_files#map_files'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CMapDataFile",
)
class CMapDataFile(CDataFile):
    """A CCP4 Map file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Structure factor and phase to define a map'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CMapColumnGroup",
)
class CMapColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "201": {
            "description": "Wrong number of columns"
        },
        "202": {
            "description": "Wrong column types"
        },
        "203": {
            "description": "No correct column types found in file"
        },
        "204": {
            "description": "Duplicate or additional column types found in file"
        },
        "205": {
            "description": "Columns in file have non-standard labels"
        },
        "206": {
            "description": "File contains unmerged data"
        },
        "210": {
            "description": "Failed creating mini-MTZ"
        },
        "211": {
            "description": "Insufficient columns selected from imported MTZ"
        },
        "212": {
            "description": "Data already imported as",
            "severity": 2
        },
        "220": {
            "description": "Can not convert file content, file does not exist"
        },
        "221": {
            "description": "Can not convert file content, existing content insufficiently rich"
        },
        "222": {
            "description": "Can not convert file content, bad input for target content"
        },
        "223": {
            "description": "Can not recognise file content"
        },
        "224": {
            "description": "Not possible to convert to required content - no mechanism implemented"
        },
        "225": {
            "description": "Failed importing from an mmcif file - failed running cif2mtz"
        },
        "226": {
            "description": "Failed importing from an mmcif file - no output from cif2mtz"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz-map',
        "mimeTypeDescription": 'MTZ F-phi',
        "fileExtensions": ['mtz', 'cif', 'ent'],
        "fileContentClassName": 'CMtzData',
        "fileLabel": 'map_coefficients',
        "guiLabel": 'Map coefficients',
        "toolTip": 'Electron density map coefficients: F,Phi',
        "correctColumns": ['FP', 'FQP'],
        "columnGroupClassList": ["<class 'ccp4x.data_scan.CCP4XtalData.CMapColumnGroup'>"],
        "downloadModes": ['Uppsala-EDS'],
        "helpFile": 'data_files#MapCoeffs'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag',
        'correctColumns',
        'columnGroupClassList',
        'sameCrystalAs'
    ],
    qualifiers_definition={
        "correctColumns": {"type": list, "listItemType": "<class 'str'>", "description": "A list of coloumn data types expected in the file"}
    },
    gui_label="CMapCoeffsDataFile",
)
class CMapCoeffsDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 1
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CImportUnmergedList",
)
class CImportUnmergedList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "file": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CUnmergedDataFile", tooltip="file attribute"),
        "cell": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCell", tooltip="cell attribute"),
        "wavelength": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CWavelength", tooltip="wavelength attribute"),
        "crystalName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="crystalName attribute"),
        "dataset": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="dataset attribute"),
        "excludeSelection": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CRangeSelection", tooltip="excludeSelection attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "toolTip": 'Imported data file, cell parameters and crystal/dataset identifiers',
        "helpFile": 'import_merged#file_formats'
    },
    contents_order=['file', 'crystalName', 'dataset', 'excludeSelection'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CImportUnmerged",
)
class CImportUnmerged(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "fileLabel": 'imosflm',
        "mimeTypeName": 'application/iMosflm-xml',
        "mimeTypeDescription": 'iMosflm data',
        "guiLabel": 'iMosflm data',
        "fileExtensions": ['imosflm.xml'],
        "fileContentClassName": None
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CImosflmXmlDataFile",
)
class CImosflmXmlDataFile(CDataFile):
    """An iMosflm data file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CImageFileList",
)
class CImageFileList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-image',
        "mimeTypeDescription": 'Image file',
        "fileExtensions": ['img', 'cbf', 'mccd', 'mar1600', 'h5', 'nxs'],
        "fileContentClassName": None,
        "guiLabel": 'Image file',
        "toolTip": 'First image file in a directory'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CImageFile",
)
class CImageFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Intensity and sigma'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CISigIColumnGroup",
)
class CISigIColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Anomalous intensities and sigma'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CIPairColumnGroup",
)
class CIPairColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Hendrickson-Lattmann coefficients'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CHLColumnGroup",
)
class CHLColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "guiLabel": 'Reflection data',
        "mimeTypeName": 'application/CCP4-generic-reflections',
        "toolTip": 'A reflection data file in MTZ or a non-CCP4 format',
        "fileContentClassName": 'CUnmergedDataContent',
        "fileExtensions": ['mtz', 'hkl', 'HKL', 'sca', 'SCA', 'mmcif', 'cif', 'ent'],
        "downloadModes": ['ebiSFs'],
        "helpFile": 'import_merged#file_formats'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CGenericReflDataFile",
)
class CGenericReflDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "201": {
            "description": "Wrong number of columns"
        },
        "202": {
            "description": "Wrong column types"
        },
        "203": {
            "description": "No correct column types found in file"
        },
        "204": {
            "description": "Duplicate or additional column types found in file"
        },
        "205": {
            "description": "Columns in file have non-standard labels"
        },
        "206": {
            "description": "File contains unmerged data"
        },
        "210": {
            "description": "Failed creating mini-MTZ"
        },
        "211": {
            "description": "Insufficient columns selected from imported MTZ"
        },
        "212": {
            "description": "Data already imported as",
            "severity": 2
        },
        "220": {
            "description": "Can not convert file content, file does not exist"
        },
        "221": {
            "description": "Can not convert file content, existing content insufficiently rich"
        },
        "222": {
            "description": "Can not convert file content, bad input for target content"
        },
        "223": {
            "description": "Can not recognise file content"
        },
        "224": {
            "description": "Not possible to convert to required content - no mechanism implemented"
        },
        "225": {
            "description": "Failed importing from an mmcif file - failed running cif2mtz"
        },
        "226": {
            "description": "Failed importing from an mmcif file - no output from cif2mtz"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/CCP4-mtz-freerflag',
        "mimeTypeDescription": 'FreeR flag',
        "fileExtensions": ['mtz', 'cif', 'ent'],
        "fileContentClassName": 'CMtzData',
        "fileLabel": 'freeRflag',
        "guiLabel": 'Free R set',
        "toolTip": 'Set of reflections used for FreeR calculation',
        "correctColumns": ['I'],
        "columnGroupClassList": ["<class 'ccp4x.data_scan.CCP4XtalData.CFreeRColumnGroup'>"],
        "helpFile": 'data_files#FreeR'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag',
        'correctColumns',
        'columnGroupClassList',
        'sameCrystalAs'
    ],
    qualifiers_definition={
        "correctColumns": {"type": list, "listItemType": "<class 'str'>", "description": "A list of coloumn data types expected in the file"}
    },
    gui_label="CFreeRDataFile",
)
class CFreeRDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Set of FreeR flags'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CFreeRColumnGroup",
)
class CFreeRColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    attributes={
        "Fp": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="Fp attribute"),
        "Fpp": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="Fpp attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['Fp', 'Fpp'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CFormFactor",
)
class CFormFactor(CData):
    """The for factor (Fp and Fpp) for a giving element and wavelength"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Structure factor and sigma'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CFSigFColumnGroup",
)
class CFSigFColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "guiLabel": 'Anomalous structure factors and sigma'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CFPairColumnGroup",
)
class CFPairColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "String too short"
        },
        "102": {
            "description": "String too long"
        },
        "103": {
            "description": "not one of limited allowed values"
        },
        "104": {
            "description": "Contains disallowed characters"
        }
    },
    qualifiers={
        "onlyEnumerators": True,
        "enumerators": ['native', 'derivative', 'SAD', 'peak', 'inflection', 'high_remote', 'low_remote', ''],
        "default": 'SAD'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CExperimentalDataType",
)
class CExperimentalDataType(CString):
    """Experimental data type e.g. native or peak"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/dials-pfile',
        "mimeTypeDescription": 'Dials pickle data file',
        "fileExtensions": ['pickle', 'refl'],
        "fileContentClassName": None,
        "fileLabel": 'dials_pdata',
        "guiLabel": 'Xia2/Dials pickle data',
        "toolTip": 'Xia2/Dials pickle data files'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CDialsPickleFile",
)
class CDialsPickleFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "101": {
            "description": "File does not exist"
        },
        "102": {
            "description": "No mime type for data file"
        },
        "103": {
            "description": "Attempting to set file content with inappropriate data"
        },
        "104": {
            "description": "There is no file content class specified for this type of file"
        },
        "105": {
            "description": "The file content class specified for this type of file can not be found"
        },
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "305": {
            "description": "Neither original nor test file exists",
            "severity": 0
        },
        "306": {
            "description": "Original file does not exists"
        },
        "307": {
            "description": "Test file does not exist "
        },
        "308": {
            "description": "Files failed checksum comparison"
        },
        "309": {
            "description": "Files failed size comparison"
        },
        "310": {
            "description": "No comparison testing implemented for this file type",
            "severity": 2
        },
        "311": {
            "description": "Failed loading original file for comparison"
        },
        "312": {
            "description": "Failed loading test file for comparison"
        },
        "313": {
            "description": "Files failed simple text diff comparison"
        },
        "320": {
            "description": "Unrecognised error attempting to load file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/dials-jfile',
        "mimeTypeDescription": 'Dials json data file',
        "fileExtensions": ['json', 'expt', 'jsn'],
        "fileContentClassName": None,
        "fileLabel": 'dials_jdata',
        "guiLabel": 'json data',
        "toolTip": 'json data files'
    },
    qualifiers_order=[
        'fileExtensions',
        'mimeTypeName',
        'mimeTypeDescription',
        'fileLabel',
        'allowUndefined',
        'mustExist',
        'fromPreviousJob',
        'jobCombo',
        'fileContentClassName',
        'isDirectory',
        'saveToDb',
        'requiredSubType',
        'requiredContentFlag'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if data file can be undefined at run time"},
        "mustExist": {"type": bool, "description": "Flag if data file must exist at run time"},
        "fromPreviousJob": {"type": bool, "description": "Flag if input data file can be inferred from preceeding jobs"},
        "jobCombo": {"type": bool, "description": "Flag if data widget should be a combo box "},
        "mimeTypeName": {"type": str, "description": ""},
        "mimeTypeDescription": {"type": str, "description": ""},
        "fileLabel": {"type": str, "description": "Label for file"},
        "fileExtensions": {"type": list, "listItemType": "<class 'str'>", "description": "A list of strings containing allowed file extensions (no dot)"},
        "fileContentClassName": {"type": str, "editable": "False", "description": "A string containing the name of a class which will hold the file contents"},
        "isDirectory": {"type": bool, "description": "Flag if the data is a directory"},
        "ifInfo": {"type": bool, "description": "Flag if gui widget should have info icon"},
        "saveToDb": {"type": bool, "description": "Save the name of this file in the database"},
        "requiredSubType": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed sub types"},
        "requiredContentFlag": {"type": list, "listItemType": "<class 'int'>", "description": "A list of allowed content flags"}
    },
    gui_label="CDialsJsonFile",
)
class CDialsJsonFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "String too short"
        },
        "102": {
            "description": "String too long"
        },
        "103": {
            "description": "not one of limited allowed values"
        },
        "104": {
            "description": "Contains disallowed characters"
        }
    },
    qualifiers={
        "allowUndefined": False,
        "allowedChars": 1,
        "minLength": 1,
        "toolTip": 'Unique identifier for dataset (one word)'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CDatasetName",
)
class CDatasetName(CString):
    """A string"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CDatasetList",
)
class CDatasetList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "selected": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="selected attribute"),
        "obsDataFile": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CObsDataFile", tooltip="obsDataFile attribute"),
        "crystalName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCrystalName", tooltip="crystalName attribute"),
        "datasetName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CDatasetName", tooltip="datasetName attribute"),
        "formFactors": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CFormFactor", tooltip="formFactors attribute"),
        "formFactorSource": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="formFactorSource attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CDataset",
)
class CDataset(CData):
    """The experimental data model for ab initio phasing"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "String too short"
        },
        "102": {
            "description": "String too long"
        },
        "103": {
            "description": "not one of limited allowed values"
        },
        "104": {
            "description": "Contains disallowed characters"
        }
    },
    qualifiers={
        "allowUndefined": False,
        "minLength": 1,
        "allowedChars": 1,
        "toolTip": 'Unique identifier for crystal (one word)'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CCrystalName",
)
class CCrystalName(CString):
    """A string"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CColumnTypeList",
)
class CColumnTypeList(CList):
    """A list of acceptable MTZ column types"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "String too short"
        },
        "102": {
            "description": "String too long"
        },
        "103": {
            "description": "not one of limited allowed values"
        },
        "104": {
            "description": "Contains disallowed characters"
        }
    },
    qualifiers={
        "enumerators": ['H', 'J', 'F', 'D', 'Q', 'G', 'L', 'K', 'M', 'E', 'P', 'W', 'A', 'B', 'Y', 'I', 'R'],
        "onlyEnumerators": True,
        "default": 'F'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CColumnType",
)
class CColumnType(CString):
    """A list of recognised MTZ column types"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "String too short"
        },
        "102": {
            "description": "String too long"
        },
        "103": {
            "description": "not one of limited allowed values"
        },
        "104": {
            "description": "Contains disallowed characters"
        }
    },
    qualifiers={
        "enumerators": ['H', 'J', 'F', 'D', 'Q', 'G', 'L', 'K', 'M', 'E', 'P', 'W', 'A', 'B', 'Y', 'I', 'R'],
        "onlyEnumerators": True,
        "default": 'F'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CMtzColumnGroupType",
)
class CMtzColumnGroupType(CColumnType):
    """A list of recognised MTZ column types"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CColumnGroupList",
)
class CColumnGroupList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "columnName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="columnName attribute"),
        "defaultList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="defaultList attribute"),
        "columnType": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CColumnTypeList", tooltip="columnType attribute"),
        "partnerTo": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="partnerTo attribute"),
        "partnerOffset": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="partnerOffset attribute")
    },
    error_codes={
        "1": {
            "description": "Attempting to change immutable object"
        },
        "2": {
            "description": "Attempting to access unknown attribute"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CColumnGroupItem",
)
class CColumnGroupItem(CData):
    """Definition of set of columns that form a 'group'"""
    pass


@cdata_class(
    attributes={
        "columnGroupType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.COneWord", tooltip="columnGroupType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute"),
        "dataset": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="dataset attribute"),
        "columnList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="columnList attribute"),
        "selected": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="selected attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CColumnGroup",
)
class CColumnGroup(CData):
    """Groups of columns in MTZ - probably from analysis by hklfile"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "below minimum"
        },
        "102": {
            "description": "above maximum"
        },
        "103": {
            "description": "not one of limited allowed values"
        }
    },
    qualifiers={
        "min": 0.0,
        "default": None,
        "allowUndefined": False,
        "toolTip": 'Cell length in A'
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'
    ],
    qualifiers_definition={
        "default": {"type": float},
        "max": {"description": "The inclusive maximum value"},
        "min": {"description": "The inclusive minimum value"},
        "enumerators": {"type": list, "description": "A Python list of allowed or recommended values - see onlyEnumerators"},
        "menuText": {"type": list, "listItemType": "<class 'str'>", "description": "A Python list of strings, matching items in enumerators list, to appear on GUI menu"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"}
    },
    gui_label="CCellLength",
)
class CCellLength(CFloat):
    """A cell length"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "below minimum"
        },
        "102": {
            "description": "above maximum"
        },
        "103": {
            "description": "not one of limited allowed values"
        }
    },
    qualifiers={
        "min": 0.0,
        "max": 180.0,
        "default": None,
        "allowUndefined": True,
        "toolTip": 'Cell angle in degrees'
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'
    ],
    qualifiers_definition={
        "default": {"type": float},
        "max": {"description": "The inclusive maximum value"},
        "min": {"description": "The inclusive minimum value"},
        "enumerators": {"type": list, "description": "A Python list of allowed or recommended values - see onlyEnumerators"},
        "menuText": {"type": list, "listItemType": "<class 'str'>", "description": "A Python list of strings, matching items in enumerators list, to appear on GUI menu"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"}
    },
    gui_label="CCellAngle",
)
class CCellAngle(CFloat):
    """A cell angle"""
    pass


@cdata_class(
    attributes={
        "a": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCellLength", tooltip="a attribute"),
        "b": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCellLength", tooltip="b attribute"),
        "c": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCellLength", tooltip="c attribute"),
        "alpha": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCellAngle", tooltip="alpha attribute"),
        "beta": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCellAngle", tooltip="beta attribute"),
        "gamma": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4XtalData.CCellAngle", tooltip="gamma attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "toolTip": 'Cell lengths and angles',
        "helpFile": 'crystal_data#cell'
    },
    contents_order=['a', 'b', 'c', 'alpha', 'beta', 'gamma'],
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CCell",
)
class CCell(CData):
    """A unit cell"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 1,
        "guiLabel": 'Contents of asymmetric unit'
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CAsuComponentList",
)
class CAsuComponentList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "moleculeType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="moleculeType attribute"),
        "seqFile": attribute(AttributeType.CUSTOM, custom_class="core.CCP4ModelData.CSeqDataFile", tooltip="seqFile attribute"),
        "numberOfCopies": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="numberOfCopies attribute")
    },
    error_codes={
        "0": {
            "severity": 0,
            "description": "OK"
        },
        "1": {
            "severity": 1,
            "description": "Data has undefined value"
        },
        "2": {
            "severity": 3,
            "description": "Data has undefined value"
        },
        "3": {
            "severity": 2,
            "description": "Missing data"
        },
        "4": {
            "description": "Missing data"
        },
        "5": {
            "description": "Attempting to set data of wrong type"
        },
        "6": {
            "description": "Default value does not satisfy validity check"
        },
        "7": {
            "severity": 2,
            "description": "Unrecognised qualifier in data input"
        },
        "8": {
            "severity": 2,
            "description": "Attempting to get inaccessible attribute:"
        },
        "9": {
            "description": "Failed to get property"
        },
        "10": {
            "severity": 2,
            "description": "Attempting to set inaccessible attribute:"
        },
        "11": {
            "description": "Failed to set property:"
        },
        "12": {
            "description": "Undetermined error setting value from XML"
        },
        "13": {
            "description": "Unrecognised class name in qualifier"
        },
        "14": {
            "severity": 2,
            "description": "No object name when saving qualifiers to XML"
        },
        "15": {
            "description": "Error saving qualifier to XML"
        },
        "16": {
            "severity": 2,
            "description": "Unrecognised item in XML data file"
        },
        "17": {
            "description": "Attempting to set unrecognised qualifier"
        },
        "18": {
            "description": "Attempting to set qualifier with wrong type"
        },
        "19": {
            "description": "Attempting to set qualifier with wrong list item type"
        },
        "20": {
            "description": "Error creating a list/dict item object"
        },
        "21": {
            "description": "Unknown error setting qualifiers from Xml file"
        },
        "22": {
            "description": "Unknown error testing validity"
        },
        "23": {
            "description": "Error saving data object to XML"
        },
        "24": {
            "description": "Unable to test validity of default",
            "severity": 2
        },
        "300": {
            "description": "Compared objects are the same",
            "severity": 0
        },
        "315": {
            "description": "Both compared objects are null",
            "severity": 0
        },
        "301": {
            "description": "Unable to compare this class of data",
            "severity": 2
        },
        "302": {
            "description": "Other data has null value"
        },
        "303": {
            "description": "My data has null value"
        },
        "304": {
            "description": "Data has different values"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool},
        "default": {"type": dict},
        "toolTip": {"type": str},
        "guiLabel": {"type": str},
        "guiDefinition": {"type": dict},
        "helpFile": {"type": str},
        "saveToDb": {"type": bool, "description": "Save this data in the database"}
    },
    gui_label="CAsuComponent",
)
class CAsuComponent(CData):
    """A component of the asymmetric unit. This is for use in MR, defining
what we are searching for. """
    pass


@cdata_class(
    error_codes={
        "201": {
            "description": "Word contains white space item"
        }
    },
    qualifiers={
        "onlyEnumerators": False,
        "enumerators": ['Br', 'Fe', 'Pt', 'Se'],
        "charWidth": 4,
        "default": 'Se'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CAnomalousScatteringElement",
)
class CAnomalousScatteringElement(CElement):
    """Definition of a anomalous scattering element"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "toolTipList": ['The real part of the experimental intensity', 'The anomalous part of the experimental intensity'],
        "guiLabel": 'Intensity and anomalous intensity'
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CAnomalousIntensityColumnGroup",
)
class CAnomalousIntensityColumnGroup(CProgramColumnGroup):
    """Selection of I and AnomI columns from MTZ.
Expected to be part of ab initio phasing dataset ( CDataset)"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Column not in MTZ file"
        },
        "102": {
            "description": "Column wrong type"
        },
        "103": {
            "description": "Error setting columnGroup qualifier"
        },
        "104": {
            "description": "Missing column selection"
        },
        "105": {
            "description": "Specified column not found in MTZ file"
        },
        "106": {
            "description": "Specified column has wrong type in MTZ file"
        },
        "107": {
            "description": "Error reading columnGroup qualifier from XML file"
        },
        "108": {
            "description": "No columnGroup qualifier"
        }
    },
    qualifiers={
        "toolTipList": ['The real part of the experimental structure factors', 'The anomalous part of the experimental structure factors']
    },
    qualifiers_order=[
        'mtzFileKey',
        'mustExist',
        'toolTipList',
        'default'
    ],
    qualifiers_definition={
        "mtzFileKey": {"type": str, "description": "The key for a CMtxDataFile in the same CContainer"},
        "mustExist": {"type": bool, "description": "Flag if the parameter must be set at run time"},
        "toolTipList": {"type": list, "description": "Tooltips for columns in group"},
        "default": {"type": list, "listItemType": "<class 'str'>", "description": "Preferred values for column names"}
    },
    gui_label="CAnomalousColumnGroup",
)
class CAnomalousColumnGroup(CProgramColumnGroup):
    """Selection of F/I and AnomF/I columns from MTZ.
Expected to be part of ab initio phasing dataset ( CDataset)"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "List shorter than required minimum length"
        },
        "102": {
            "description": "List longer than required maximum length"
        },
        "103": {
            "description": "Consecutive values in list fail comparison test"
        },
        "104": {
            "description": "Attempting to add object of wrong type"
        },
        "105": {
            "description": "Attempting to add object of correct type but wrong qualifiers"
        },
        "106": {
            "description": "Attempting to add data which does not satisfy the qualifiers for a list item"
        },
        "107": {
            "description": "Deleting item will reduce list below minimum length"
        },
        "108": {
            "description": "Adding item will extend list beyond maximum length"
        },
        "109": {
            "description": "Invalid item class"
        },
        "110": {
            "description": "etree (XML) list item of wrong type"
        },
        "112": {
            "description": "No list item object set for list"
        }
    },
    qualifiers={
        "listMinLength": 0
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare'
    ],
    qualifiers_definition={
        "default": {"type": list},
        "listMaxLength": {"type": int, "description": "Inclusive maximum length of list"},
        "listMinLength": {"type": int, "description": "Inclusive minimum length of list"},
        "listCompare": {"type": int, "description": "If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method."}
    },
    gui_label="CAltSpaceGroupList",
)
class CAltSpaceGroupList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Invalid space group"
        },
        "102": {
            "description": "Space group is not chiral",
            "severity": 2
        },
        "103": {
            "description": "Space group is not Hermann-Mauguin standard"
        },
        "104": {
            "description": "Space group is not a chiral Hermann-Mauguin standard. Full syminfo.lib information not loaded."
        },
        "105": {
            "description": "Space group is not Hermann-Mauguin standard - has wrong number of spaces?"
        },
        "106": {
            "description": "Space group is undefined",
            "severity": 1
        },
        "107": {
            "description": "Space group is undefined"
        },
        "108": {
            "description": "Space group is incomplete",
            "severity": 2
        }
    },
    qualifiers={
        "allowUndefined": True,
        "toolTip": 'Hermann-Mauguin space group name',
        "helpFile": 'crystal_data#space_group'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    qualifiers_definition={
        "default": {"type": str},
        "maxLength": {"type": int, "description": "Maximum length of string"},
        "minLength": {"type": int, "description": "Minimum length of string"},
        "enumerators": {"type": list, "description": "A list of allowed or recommended values for string"},
        "menuText": {"type": list, "description": "A list of strings equivalent to the enumerators that will appear in the GUI"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CAltSpaceGroup",
)
class CAltSpaceGroup(CSpaceGroup):
    """A string holding the space group"""
    pass
