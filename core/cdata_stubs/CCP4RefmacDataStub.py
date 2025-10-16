"""Generated classes from CCP4RefmacData.py"""

from ..base_object.base_classes import CData, CContainer
from ..CCP4FundamentalTypes import CInt, CList, CBoolean, CFloat, CString, COneWord
from ..base_object.class_metadata import cdata_class, attribute, AttributeType

from .CCP4BaseFile-stub import CDataFileContent, CDataFile, CXmlDataFile, CI2XmlDataFile


@cdata_class(
    attributes={
        "chain_id": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="chain_id attribute"),
        "residue_1": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="residue_1 attribute"),
        "residue_2": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="residue_2 attribute")
    },
    error_codes={
        "101": {
            "description": "No sequence identity or structure RMS to target set"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['chain_id', 'residue_1', 'residue_2'],
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
    gui_label="CRefmacRigidGroupSegment",
)
class CRefmacRigidGroupSegment(CData):
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
    gui_label="CRefmacRigidGroupList",
)
class CRefmacRigidGroupList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "rigid_group_id": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="rigid_group_id attribute"),
        "segmentList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="segmentList attribute")
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
    gui_label="CRefmacRigidGroupItem",
)
class CRefmacRigidGroupItem(CData):
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
        "fileLabel": 'restraints',
        "mimeTypeName": 'application/refmac-external-restraints',
        "mimeTypeDescription": 'Refmac external restraints',
        "guiLabel": 'Additional restraints',
        "fileExtensions": ['txt']
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
    gui_label="CRefmacRestraintsDataFile",
)
class CRefmacRestraintsDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass


@cdata_class(
    attributes={
        "atomType": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="atomType attribute"),
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
    gui_label="CRefmacAnomalousAtom",
)
class CRefmacAnomalousAtom(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""
    pass
