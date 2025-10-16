"""Generated classes from CCP4File.py"""

from ..base_object.base_classes import CData, CContainer
from ..CCP4FundamentalTypes import CInt, CList, CBoolean, CFloat, CString, COneWord
from ..base_object.class_metadata import cdata_class, attribute, AttributeType

from .CCP4BaseFile-stub import CDataFileContent, CDataFile, CXmlDataFile, CI2XmlDataFile


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "mimeTypeName": '"text/plain"',
        "mimeTypeDescription": 'Standard plain text',
        "guiLabel": 'yml file',
        "fileExtensions": ['yml']
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
    gui_label="CYmlFile",
)
class CYmlFile(CDataFile):
    """A yml data file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "mimeTypeName": 'application/grace',
        "fileExtensions": ['xmgr']
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
    gui_label="CXmgrDataFile",
)
class CXmgrDataFile(CDataFile):
    """An xmgr format file. This is the input format for xmgrace, as output by scala or aimless"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Version is not of form n.m or n.m.i"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "default": None,
        "charWidth": 10
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'charWidth'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if allow an unset value at run time"},
        "default": {"description": "A default value"},
        "charWidth": {"type": int, "description": "Number of characters allowed for widget in GUI"}
    },
    gui_label="CVersion",
)
class CVersion(CString):
    """A (string) version number of the form n.m.i"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "mimeTypeName": '"text/plain"',
        "mimeTypeDescription": 'Standard plain text',
        "fileLabel": None,
        "fileExtensions": ['txt', 'log']
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
    gui_label="CTextDataFile",
)
class CTextDataFile(CDataFile):
    """A text data file"""
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
    gui_label="CSearchPathList",
)
class CSearchPathList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "name": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="name attribute"),
        "path": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CDataFile", tooltip="path attribute")
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
    gui_label="CSearchPath",
)
class CSearchPath(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "fileLabel": 'scene',
        "mimeTypeName": 'application/CCP4-scene',
        "mimeTypeDescription": 'CCP4mg scene file',
        "guiLabel": 'CCP4mg scene',
        "fileExtensions": ['scene.xml']
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
    gui_label="CSceneDataFile",
)
class CSceneDataFile(CDataFile):
    """An xml format file for defining scene in CCP4mg."""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Invalid project name"
        },
        "102": {
            "description": "Project does not have directory set"
        },
        "103": {
            "description": "Project directory does not exist"
        },
        "104": {
            "severity": 2,
            "description": "Warning - Project name is a directory alias"
        },
        "105": {
            "severity": 2,
            "description": "Warning - Project does not have directory set"
        },
        "106": {
            "severity": 2,
            "description": "Warning - Project directory does not exist"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "allowAlias": True,
        "allowUnfound": True,
        "default": None
    },
    qualifiers_order=[
        'allowUndefined',
        'allowAlias',
        'allowUnfound',
        'default'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if allow undefined value at run time"},
        "allowAlias": {"type": bool, "description": "Flag if allow project to be directory alias at run time"},
        "allowUnfound": {"type": bool, "description": "Flag if allow unfound project at run time"},
        "default": {"type": str}
    },
    gui_label="CProjectName",
)
class CProjectName(CString):
    """The name of a CCP4i project or directory alias"""
    pass


@cdata_class(
    error_codes={
        "201": {
            "description": "Unrecognised projectId"
        },
        "202": {
            "description": "Project does not have directory set"
        },
        "203": {
            "description": "Project directory does not exist"
        },
        "205": {
            "severity": 2,
            "description": "Warning - Project does not have directory set"
        },
        "206": {
            "severity": 2,
            "description": "Warning - Project directory does not exist"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "allowUnfound": True,
        "default": None
    },
    qualifiers_order=[
        'allowUndefined',
        'allowUnfound',
        'default'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if allow undefined value at run time"},
        "allowUnfound": {"type": bool, "description": "Flag if allow unfound project at run time"},
        "default": {"type": str}
    },
    gui_label="CProjectId",
)
class CProjectId(CUUID):
    """The CCP4i2 database project id - a global unique id"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "mimeTypeName": 'application/postscript',
        "fileExtensions": ['ps'],
        "guiLabel": 'Postscript file'
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
    gui_label="CPostscriptDataFile",
)
class CPostscriptDataFile(CDataFile):
    """A postscript format file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "mimeTypeName": 'application/x-pdf',
        "fileExtensions": ['pdf'],
        "guiLabel": 'PDF file'
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
    gui_label="CPDFDataFile",
)
class CPDFDataFile(CDataFile):
    """An PDF format file"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "fileExtensions": ['cif', 'ent']
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
    gui_label="CMmcifDataFile",
)
class CMmcifDataFile(CDataFile):
    """A generic mmCIF format file.
This is intended to be a base class for other classes
specific to coordinates, reflections or geometry data."""
    pass


@cdata_class(
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
    gui_label="CMmcifData",
)
class CMmcifData(CDataFileContent):
    """Generic mmCIF data.
This is intended to be a base class for other classes
specific to coordinates, reflections or geometry data."""
    pass


@cdata_class(
    attributes={
        "function": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFileFunction", tooltip="function attribute"),
        "userId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Annotation.CUserId", tooltip="userId attribute"),
        "hostName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Annotation.CHostName", tooltip="hostName attribute"),
        "creationTime": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Annotation.CTime", tooltip="creationTime attribute"),
        "ccp4iVersion": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CVersion", tooltip="ccp4iVersion attribute"),
        "pluginName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="pluginName attribute"),
        "pluginVersion": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CVersion", tooltip="pluginVersion attribute"),
        "pluginTitle": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="pluginTitle attribute"),
        "projectName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectName", tooltip="projectName attribute"),
        "projectId": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="projectId attribute"),
        "jobId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="jobId attribute"),
        "jobNumber": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="jobNumber attribute"),
        "comment": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="comment attribute"),
        "OS": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="OS attribute")
    },
    error_codes={
        "101": {
            "description": "Attempting to read header from non-existant Xml file"
        },
        "102": {
            "description": "Error loading file to read header"
        },
        "103": {
            "description": "Error finding <ccp4i2_header> in file"
        },
        "104": {
            "description": "Error interpreting header from file"
        },
        "105": {
            "description": "File does not have <ccp4i2> root node"
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
    gui_label="CI2XmlHeader",
)
class CI2XmlHeader(CData):
    """Container for header info from XML file"""
    pass


@cdata_class(
    error_codes={
        "101": {
            "description": "Invalid characters in file name"
        },
        "102": {
            "severity": 2,
            "description": "Invalid characters in file name"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "allowedCharacters": '',
        "allowedCharactersMode": 1,
        "default": None
    },
    qualifiers_order=[
        'allowUndefined',
        'allowedCharacters',
        'allowedCharactersMode',
        'default'
    ],
    qualifiers_definition={
        "allowUndefined": {"type": bool, "description": "Flag if allow undefined value at run time"},
        "allowedCharacters": {"type": str, "description": "Set of characters allowed in file name"},
        "allowedCharactersMode": {"type": int, "description": "Handling of violation of allowed characters"},
        "default": {"type": str, "description": "Default file path"}
    },
    gui_label="CFilePath",
)
class CFilePath(CString):
    """A file path"""
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
        "enumerators": ['DEF', 'PARAMS', 'LOG', 'PROJECTDIRECTORIES', 'COM', 'REFMAC', 'OUTPUT', 'STATUS', 'PROJECTDATABASE', 'MGSCENE', 'JOBSERVERSTATUS', 'WORKFLOW', 'COMFILEPATCH', 'CUSTOMTASK', 'IMPORTEDJOB', 'I1SUPPLEMENT', 'ASUCONTENT', 'UNKNOWN'],
        "onlyEnumerators": True
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
        "enumerators": {"type": list},
        "onlyEnumerators": {"type": bool, "editable": "False"}
    },
    gui_label="CFileFunction",
)
class CFileFunction(CString):
    """List of recognised XML file functions"""
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
    gui_label="CExportedFileList",
)
class CExportedFileList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "exportId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="exportId attribute")
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
    gui_label="CExportedFile",
)
class CExportedFile(CData):
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
    gui_label="CExePathList",
)
class CExePathList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "exeName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="exeName attribute"),
        "exePath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CDataFile", tooltip="exePath attribute")
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
    contents_order=['exeName', 'exePath'],
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
    gui_label="CExePath",
)
class CExePath(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CUUID", tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="contentFlag attribute")
    },
    error_codes={
        "1001": {
            "description": "Unknown error reading XML file"
        },
        "1002": {
            "description": "Error trying to find root node in XML"
        },
        "1006": {
            "description": "Attempting to save XML file with incorrect body"
        },
        "1007": {
            "description": "Error creating XML text"
        },
        "1008": {
            "description": "Error saving XML text to file"
        },
        "1009": {
            "description": "Error reading XML file"
        },
        "1010": {
            "description": "XML file does not exist"
        },
        "1011": {
            "description": "No file name given for making I2XMlDataFile"
        },
        "1012": {
            "description": "Error creating I2XMlDataFile object"
        },
        "1013": {
            "description": "Error creating I2XMlDataFile file"
        }
    },
    qualifiers={
        "mimeTypeName": 'application/EBI-validation-xml',
        "fileExtensions": ['xml'],
        "guiLabel": 'EBI Validation XML'
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
    gui_label="CEBIValidationXMLDataFile",
)
class CEBIValidationXMLDataFile(CXmlDataFile):
    """An XLM file returned from the EBI validation server """
    pass


@cdata_class(
    attributes={
        "project": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CProjectId", tooltip="project attribute"),
        "baseName": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4File.CFilePath", tooltip="relPath attribute"),
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
        "guiLabel": 'Reflections from DIALS',
        "fileExtensions": ['refl']
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
    gui_label="CDataReflFile",
)
class CDataReflFile(CDataFile):
    """Reflection file from DIALS"""
    pass
