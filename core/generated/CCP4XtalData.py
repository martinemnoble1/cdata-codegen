"""Auto-generated from CCP4i2 metadata. DO NOT EDIT.

To extend these classes, create subclasses in core/extensions/
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

# Metadata system
from core.base_object.class_metadata import cdata_class, attribute, AttributeType

# Base classes
from core.base_object.base_classes import CData, CDataFile, CDataFileContent

# Fundamental types
from core.base_object.fundamental_types import CBoolean, CFloat, CInt, CList, COneWord, CProjectId, CString, CUUID

# Cross-file class references
from core.generated.CCP4Data import CRangeSelection
from core.generated.CCP4File import CFilePath, CMmcifData, CMmcifDataFile
from core.generated.CCP4ModelData import CElement, CSeqDataFile


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
        "default": 'SAD',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CExperimentalDataType(CString):
    """Experimental data type e.g. native or peak"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CExperimentalDataType.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "toolTip": 'json data files',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CDialsJsonFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDialsJsonFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "toolTip": 'Phaser rfile solutions for rotation search',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CPhaserRFileDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPhaserRFileDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "default": [],
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CProgramColumnGroup(CData):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CProgramColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTip": 'Unique identifier for dataset (one word)',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CDatasetName(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDatasetName.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "h": attribute(AttributeType.STRING, tooltip="h attribute"),
        "k": attribute(AttributeType.STRING, tooltip="k attribute"),
        "l": attribute(AttributeType.STRING, tooltip="l attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['h', 'k', 'l'],
)
class CReindexOperator(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    h: Optional[CString] = None
    k: Optional[CString] = None
    l: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CReindexOperator.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#shelxfa',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CShelxFADataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CShelxFADataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "helpFile": 'crystal_data#space_group',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CSpaceGroup(CString):
    """A string holding the space group"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CSpaceGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "moleculeType": attribute(AttributeType.STRING, tooltip="moleculeType attribute"),
        "seqFile": attribute(AttributeType.CUSTOM, custom_class="CSeqDataFile", tooltip="seqFile attribute"),
        "numberOfCopies": attribute(AttributeType.INT, tooltip="numberOfCopies attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CAsuComponent(CData):
    """A component of the asymmetric unit. This is for use in MR, defining
what we are searching for. """

    moleculeType: Optional[CString] = None
    seqFile: Optional[CSeqDataFile] = None
    numberOfCopies: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAsuComponent.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#mmCIF',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CMmcifReflDataFile(CMmcifDataFile):
    """A reflection file in mmCIF format"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMmcifReflDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTip": 'Cell length in A',
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'],
    qualifiers_definition={
        "default": {'type': 'float'},
        "max": {'description': 'The inclusive maximum value'},
        "min": {'description': 'The inclusive minimum value'},
        "enumerators": {'type': 'list', 'description': 'A Python list of allowed or recommended values - see onlyEnumerators'},
        "menuText": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A Python list of strings, matching items in enumerators list, to appear on GUI menu'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
    },
)
class CCellLength(CFloat):
    """A cell length"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CCellLength.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "columnGroupType": attribute(AttributeType.CUSTOM, custom_class="COneWord", tooltip="columnGroupType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
        "dataset": attribute(AttributeType.STRING, tooltip="dataset attribute"),
        "columnList": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="columnList attribute"),
        "selected": attribute(AttributeType.BOOLEAN, tooltip="selected attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CColumnGroup(CData):
    """Groups of columns in MTZ - probably from analysis by hklfile"""

    columnGroupType: Optional[COneWord] = None
    contentFlag: Optional[CInt] = None
    dataset: Optional[CString] = None
    columnList: Optional[CList] = None
    selected: Optional[CBoolean] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "saveToDb": True,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CMergeMiniMtzList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMergeMiniMtzList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTip": 'Data collection wavelength in Angstrom',
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'],
    qualifiers_definition={
        "default": {'type': 'float'},
        "max": {'description': 'The inclusive maximum value'},
        "min": {'description': 'The inclusive minimum value'},
        "enumerators": {'type': 'list', 'description': 'A Python list of allowed or recommended values - see onlyEnumerators'},
        "menuText": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A Python list of strings, matching items in enumerators list, to appear on GUI menu'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
    },
)
class CWavelength(CFloat):
    """Wavelength in Angstrom"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CWavelength.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CRunBatchRangeList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRunBatchRangeList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CImageFileList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CImageFileList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CAltSpaceGroupList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAltSpaceGroupList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTip": 'Unique identifier for crystal (one word)',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CCrystalName(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CCrystalName.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "Fp": attribute(AttributeType.FLOAT, tooltip="Fp attribute"),
        "Fpp": attribute(AttributeType.FLOAT, tooltip="Fpp attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['Fp', 'Fpp'],
)
class CFormFactor(CData):
    """The for factor (Fp and Fpp) for a giving element and wavelength"""

    Fp: Optional[CFloat] = None
    Fpp: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFormFactor.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "name": attribute(AttributeType.STRING, tooltip="name attribute"),
        "columnGroups": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="columnGroups attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CMtzDataset(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    name: Optional[CString] = None
    columnGroups: Optional[CList] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMtzDataset.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "runNumber": attribute(AttributeType.INT, tooltip="runNumber attribute"),
        "batchRange0": attribute(AttributeType.INT, tooltip="batchRange0 attribute"),
        "batchRange1": attribute(AttributeType.INT, tooltip="batchRange1 attribute"),
        "resolution": attribute(AttributeType.FLOAT, tooltip="resolution attribute"),
        "fileNumber": attribute(AttributeType.INT, tooltip="fileNumber attribute"),
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
        "toolTip": 'Specify range of reflections to treat as one run',
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CRunBatchRange(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    runNumber: Optional[CInt] = None
    batchRange0: Optional[CInt] = None
    batchRange1: Optional[CInt] = None
    resolution: Optional[CFloat] = None
    fileNumber: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRunBatchRange.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CMiniMtzDataFileList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMiniMtzDataFileList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTip": 'Cell angle in degrees',
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'],
    qualifiers_definition={
        "default": {'type': 'float'},
        "max": {'description': 'The inclusive maximum value'},
        "min": {'description': 'The inclusive minimum value'},
        "enumerators": {'type': 'list', 'description': 'A Python list of allowed or recommended values - see onlyEnumerators'},
        "menuText": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A Python list of strings, matching items in enumerators list, to appear on GUI menu'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
    },
)
class CCellAngle(CFloat):
    """A cell angle"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CCellAngle.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "default": 'Se',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CAnomalousScatteringElement(CElement):
    """Definition of a anomalous scattering element"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAnomalousScatteringElement.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#MTZ',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "sameCrystalAs": {'type': 'str', 'description': 'Name of CMtzDataFile object that crystal parameters should match - probably the observed data'},
        "sameCrystalLevel": {'type': 'int', 'description': 'Rigour of same crystal test'},
    },
)
class CMtzDataFile(CDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMtzDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CColumnTypeList(CList):
    """A list of acceptable MTZ column types"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CColumnTypeList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#phasersol',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CPhaserSolDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPhaserSolDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CColumnGroupList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CColumnGroupList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "toolTip": 'Xia2/Dials pickle data files',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CDialsPickleFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDialsPickleFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "toolTip": 'A file containing keywords as they are meant to be read by refmac5',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CRefmacKeywordFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRefmacKeywordFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "low": attribute(AttributeType.FLOAT, tooltip="low attribute"),
        "high": attribute(AttributeType.FLOAT, tooltip="high attribute"),
    },
    error_codes={
        "201": {
            "description": "High/low resolution wrong way round?"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CResolutionRange(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    low: Optional[CFloat] = None
    high: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CResolutionRange.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Contents of asymmetric unit',
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CAsuComponentList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAsuComponentList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "default": 'F',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CColumnType(CString):
    """A list of recognised MTZ column types"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CColumnType.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTip": 'Hint to Shelx for the use of the dataset',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CShelxLabel(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CShelxLabel.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CXia2ImageSelectionList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CXia2ImageSelectionList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "fileContentClassName": None,
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CImosflmXmlDataFile(CDataFile):
    """An iMosflm data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CImosflmXmlDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CUnmergedDataFileList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CUnmergedDataFileList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#unmerged_data',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CUnmergedDataFile(CDataFile):
    """Handle MTZ, XDS and scalepack files. Allow wildcard filename"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CUnmergedDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#map_files',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CMapDataFile(CDataFile):
    """A CCP4 Map file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMapDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'import_merged#file_formats',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CGenericReflDataFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CGenericReflDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "toolTip": 'First image file in a directory',
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
        'requiredContentFlag'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool', 'description': 'Flag if data file can be undefined at run time'},
        "mustExist": {'type': 'bool', 'description': 'Flag if data file must exist at run time'},
        "fromPreviousJob": {'type': 'bool', 'description': 'Flag if input data file can be inferred from preceeding jobs'},
        "jobCombo": {'type': 'bool', 'description': 'Flag if data widget should be a combo box '},
        "mimeTypeName": {'type': 'str', 'description': ''},
        "mimeTypeDescription": {'type': 'str', 'description': ''},
        "fileLabel": {'type': 'str', 'description': 'Label for file'},
        "fileExtensions": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of strings containing allowed file extensions (no dot)'},
        "fileContentClassName": {'type': 'str', 'editable': False, 'description': 'A string containing the name of a class which will hold the file contents'},
        "isDirectory": {'type': 'bool', 'description': 'Flag if the data is a directory'},
        "ifInfo": {'type': 'bool', 'description': 'Flag if gui widget should have info icon'},
        "saveToDb": {'type': 'bool', 'description': 'Save the name of this file in the database'},
        "requiredSubType": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed sub types'},
        "requiredContentFlag": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A list of allowed content flags'},
    },
)
class CImageFile(CDataFile):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CImageFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "listMinLength": 0,
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CDatasetList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDatasetList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
    },
    qualifiers_order=['listMinLength', 'listMaxLength', 'listCompare'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
    },
)
class CImportUnmergedList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CImportUnmergedList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Hendrickson-Lattmann coefficients',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CHLColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CHLColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Anomalous structure factors and sigma',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CFPairColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFPairColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Structure factor and sigma',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CFSigFColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFSigFColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Intensity and sigma',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CISigIColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CISigIColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Structure factor and phase to define a map',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CMapColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMapColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Phase and figure of merit',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CPhiFomColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPhiFomColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Anomalous intensities and sigma',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CIPairColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CIPairColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Intensity and anomalous intensity',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CAnomalousIntensityColumnGroup(CProgramColumnGroup):
    """Selection of I and AnomI columns from MTZ.
Expected to be part of ab initio phasing dataset ( CDataset)"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAnomalousIntensityColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "toolTipList": ['The real part of the experimental structure factors', 'The anomalous part of the experimental structure factors'],
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CAnomalousColumnGroup(CProgramColumnGroup):
    """Selection of F/I and AnomF/I columns from MTZ.
Expected to be part of ab initio phasing dataset ( CDataset)"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAnomalousColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "guiLabel": 'Set of FreeR flags',
    },
    qualifiers_order=['mtzFileKey', 'mustExist', 'toolTipList', 'default'],
    qualifiers_definition={
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
        "toolTipList": {'type': 'list', 'description': 'Tooltips for columns in group'},
        "default": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'Preferred values for column names'},
    },
)
class CFreeRColumnGroup(CProgramColumnGroup):
    """A group of MTZ columns required for program input"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFreeRColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "helpFile": 'crystal_data#space_group',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CAltSpaceGroup(CSpaceGroup):
    """A string holding the space group"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAltSpaceGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "a": attribute(AttributeType.CUSTOM, custom_class="CCellLength", tooltip="a attribute"),
        "b": attribute(AttributeType.CUSTOM, custom_class="CCellLength", tooltip="b attribute"),
        "c": attribute(AttributeType.CUSTOM, custom_class="CCellLength", tooltip="c attribute"),
        "alpha": attribute(AttributeType.CUSTOM, custom_class="CCellAngle", tooltip="alpha attribute"),
        "beta": attribute(AttributeType.CUSTOM, custom_class="CCellAngle", tooltip="beta attribute"),
        "gamma": attribute(AttributeType.CUSTOM, custom_class="CCellAngle", tooltip="gamma attribute"),
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
        "helpFile": 'crystal_data#cell',
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['a', 'b', 'c', 'alpha', 'beta', 'gamma'],
)
class CCell(CData):
    """A unit cell"""

    a: Optional[CCellLength] = None
    b: Optional[CCellLength] = None
    c: Optional[CCellLength] = None
    alpha: Optional[CCellAngle] = None
    beta: Optional[CCellAngle] = None
    gamma: Optional[CCellAngle] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CCell.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "toolTip": "Unmerged experimental data in CCP4's MTZ format",
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
        'requiredContentFlag'],
    qualifiers_definition={
        "sameCrystalAs": {'type': 'str', 'description': 'Name of CMtzDataFile object that crystal parameters should match - probably the observed data'},
        "sameCrystalLevel": {'type': 'int', 'description': 'Rigour of same crystal test'},
    },
)
class CUnmergedMtzDataFile(CMtzDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CUnmergedMtzDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#MTZ',
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
        'sameCrystalAs'],
    qualifiers_definition={
        "correctColumns": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of coloumn data types expected in the file'},
    },
)
class CMiniMtzDataFile(CMtzDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMiniMtzDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "columnName": attribute(AttributeType.CUSTOM, custom_class="COneWord", tooltip="columnName attribute"),
        "defaultList": attribute(AttributeType.STRING, tooltip="defaultList attribute"),
        "columnType": attribute(AttributeType.CUSTOM, custom_class="CColumnTypeList", tooltip="columnType attribute"),
        "partnerTo": attribute(AttributeType.CUSTOM, custom_class="COneWord", tooltip="partnerTo attribute"),
        "partnerOffset": attribute(AttributeType.INT, tooltip="partnerOffset attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CColumnGroupItem(CData):
    """Definition of set of columns that form a 'group'"""

    columnName: Optional[COneWord] = None
    defaultList: Optional[CString] = None
    columnType: Optional[CColumnTypeList] = None
    partnerTo: Optional[COneWord] = None
    partnerOffset: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CColumnGroupItem.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
        "default": 'F',
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'],
    qualifiers_definition={
        "default": {'type': 'str'},
        "maxLength": {'type': 'int', 'description': 'Maximum length of string'},
        "minLength": {'type': 'int', 'description': 'Minimum length of string'},
        "enumerators": {'type': 'list', 'description': 'A list of allowed or recommended values for string'},
        "menuText": {'type': 'list', 'description': 'A list of strings equivalent to the enumerators that will appear in the GUI'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
        "allowedCharsCode": {'type': 'int', 'description': 'Flag if the text is limited to set of allowed characters'},
    },
)
class CMtzColumnGroupType(CColumnType):
    """A list of recognised MTZ column types"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMtzColumnGroupType.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "columnLabel": attribute(AttributeType.CUSTOM, custom_class="COneWord", tooltip="columnLabel attribute"),
        "columnType": attribute(AttributeType.CUSTOM, custom_class="CColumnType", tooltip="columnType attribute"),
        "dataset": attribute(AttributeType.CUSTOM, custom_class="COneWord", tooltip="dataset attribute"),
        "groupIndex": attribute(AttributeType.INT, tooltip="groupIndex attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CMtzColumn(CData):
    """An MTZ column with column label and column type"""

    columnLabel: Optional[COneWord] = None
    columnType: Optional[CColumnType] = None
    dataset: Optional[COneWord] = None
    groupIndex: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMtzColumn.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "imageFile": attribute(AttributeType.CUSTOM, custom_class="CImageFile", tooltip="imageFile attribute"),
        "imageStart": attribute(AttributeType.INT, tooltip="imageStart attribute"),
        "imageEnd": attribute(AttributeType.INT, tooltip="imageEnd attribute"),
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
        "toolTip": 'select an image file and an optional range of files to define a dataset',
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['imageFile', 'imageStart', 'imageEnd'],
)
class CXia2ImageSelection(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    imageFile: Optional[CImageFile] = None
    imageStart: Optional[CInt] = None
    imageEnd: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CXia2ImageSelection.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "file": attribute(AttributeType.CUSTOM, custom_class="CUnmergedDataFile", tooltip="file attribute"),
        "cell": attribute(AttributeType.CUSTOM, custom_class="CCell", tooltip="cell attribute"),
        "wavelength": attribute(AttributeType.CUSTOM, custom_class="CWavelength", tooltip="wavelength attribute"),
        "crystalName": attribute(AttributeType.STRING, tooltip="crystalName attribute"),
        "dataset": attribute(AttributeType.STRING, tooltip="dataset attribute"),
        "excludeSelection": attribute(AttributeType.CUSTOM, custom_class="CRangeSelection", tooltip="excludeSelection attribute"),
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
        "helpFile": 'import_merged#file_formats',
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['file', 'crystalName', 'dataset', 'excludeSelection'],
)
class CImportUnmerged(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    file: Optional[CUnmergedDataFile] = None
    cell: Optional[CCell] = None
    wavelength: Optional[CWavelength] = None
    crystalName: Optional[CString] = None
    dataset: Optional[CString] = None
    excludeSelection: Optional[CRangeSelection] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CImportUnmerged.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "cell": attribute(AttributeType.CUSTOM, custom_class="CCell", tooltip="cell attribute"),
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroup", tooltip="spaceGroup attribute"),
        "resolutionRange": attribute(AttributeType.CUSTOM, custom_class="CResolutionRange", tooltip="resolutionRange attribute"),
        "listOfColumns": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="listOfColumns attribute"),
        "datasets": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="datasets attribute"),
        "crystalNames": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="crystalNames attribute"),
        "wavelengths": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="wavelengths attribute"),
        "datasetCells": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="datasetCells attribute"),
        "merged": attribute(AttributeType.BOOLEAN, tooltip="merged attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CMtzData(CDataFileContent):
    """Base class for classes holding file contents"""

    cell: Optional[CCell] = None
    spaceGroup: Optional[CSpaceGroup] = None
    resolutionRange: Optional[CResolutionRange] = None
    listOfColumns: Optional[CList] = None
    datasets: Optional[CList] = None
    crystalNames: Optional[CList] = None
    wavelengths: Optional[CList] = None
    datasetCells: Optional[CList] = None
    merged: Optional[CBoolean] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMtzData.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "cell": attribute(AttributeType.CUSTOM, custom_class="CCell", tooltip="cell attribute"),
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroup", tooltip="spaceGroup attribute"),
        "wavelength": attribute(AttributeType.CUSTOM, custom_class="CWavelength", tooltip="wavelength attribute"),
        "haveFreeRColumn": attribute(AttributeType.BOOLEAN, tooltip="haveFreeRColumn attribute"),
        "haveFobsColumn": attribute(AttributeType.BOOLEAN, tooltip="haveFobsColumn attribute"),
        "haveFpmObsColumn": attribute(AttributeType.BOOLEAN, tooltip="haveFpmObsColumn attribute"),
        "haveIobsColumn": attribute(AttributeType.BOOLEAN, tooltip="haveIobsColumn attribute"),
        "haveIpmObsColumn": attribute(AttributeType.BOOLEAN, tooltip="haveIpmObsColumn attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CMmcifReflData(CMmcifData):
    """Generic mmCIF data.
This is intended to be a base class for other classes
specific to coordinates, reflections or geometry data."""

    cell: Optional[CCell] = None
    spaceGroup: Optional[CSpaceGroup] = None
    wavelength: Optional[CWavelength] = None
    haveFreeRColumn: Optional[CBoolean] = None
    haveFobsColumn: Optional[CBoolean] = None
    haveFpmObsColumn: Optional[CBoolean] = None
    haveIobsColumn: Optional[CBoolean] = None
    haveIpmObsColumn: Optional[CBoolean] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMmcifReflData.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroup", tooltip="spaceGroup attribute"),
        "cell": attribute(AttributeType.CUSTOM, custom_class="CCell", tooltip="cell attribute"),
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
        "helpFile": 'crystal_data#cell_space_group',
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['spaceGroup', 'cell'],
)
class CSpaceGroupCell(CData):
    """Cell space group and parameters"""

    spaceGroup: Optional[CSpaceGroup] = None
    cell: Optional[CCell] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CSpaceGroupCell.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "format": attribute(AttributeType.STRING, tooltip="format attribute"),
        "merged": attribute(AttributeType.STRING, tooltip="merged attribute"),
        "crystalName": attribute(AttributeType.CUSTOM, custom_class="CCrystalName", tooltip="crystalName attribute"),
        "datasetName": attribute(AttributeType.CUSTOM, custom_class="CDatasetName", tooltip="datasetName attribute"),
        "cell": attribute(AttributeType.CUSTOM, custom_class="CCell", tooltip="cell attribute"),
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroup", tooltip="spaceGroup attribute"),
        "batchs": attribute(AttributeType.STRING, tooltip="batchs attribute"),
        "lowRes": attribute(AttributeType.FLOAT, tooltip="lowRes attribute"),
        "highRes": attribute(AttributeType.FLOAT, tooltip="highRes attribute"),
        "knowncell": attribute(AttributeType.BOOLEAN, tooltip="knowncell attribute"),
        "knownwavelength": attribute(AttributeType.BOOLEAN, tooltip="knownwavelength attribute"),
        "numberLattices": attribute(AttributeType.INT, tooltip="numberLattices attribute"),
        "wavelength": attribute(AttributeType.CUSTOM, custom_class="CWavelength", tooltip="wavelength attribute"),
        "numberofdatasets": attribute(AttributeType.INT, tooltip="numberofdatasets attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CUnmergedDataContent(CDataFileContent):
    """Base class for classes holding file contents"""

    format: Optional[CString] = None
    merged: Optional[CString] = None
    crystalName: Optional[CCrystalName] = None
    datasetName: Optional[CDatasetName] = None
    cell: Optional[CCell] = None
    spaceGroup: Optional[CSpaceGroup] = None
    batchs: Optional[CString] = None
    lowRes: Optional[CFloat] = None
    highRes: Optional[CFloat] = None
    knowncell: Optional[CBoolean] = None
    knownwavelength: Optional[CBoolean] = None
    numberLattices: Optional[CInt] = None
    wavelength: Optional[CWavelength] = None
    numberofdatasets: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CUnmergedDataContent.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#Phs',
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
        'sameCrystalAs'],
    qualifiers_definition={
        "correctColumns": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of coloumn data types expected in the file'},
    },
)
class CPhsDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPhsDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#Obs',
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
        'sameCrystalAs'],
    qualifiers_definition={
        "correctColumns": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of coloumn data types expected in the file'},
    },
)
class CObsDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CObsDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#MapCoeffs',
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
        'sameCrystalAs'],
    qualifiers_definition={
        "correctColumns": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of coloumn data types expected in the file'},
    },
)
class CMapCoeffsDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMapCoeffsDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "project": attribute(AttributeType.PROJECT_ID, tooltip="project attribute"),
        "baseName": attribute(AttributeType.FILEPATH, tooltip="baseName attribute"),
        "relPath": attribute(AttributeType.FILEPATH, tooltip="relPath attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
        "dbFileId": attribute(AttributeType.UUID, tooltip="dbFileId attribute"),
        "subType": attribute(AttributeType.INT, tooltip="subType attribute"),
        "contentFlag": attribute(AttributeType.INT, tooltip="contentFlag attribute"),
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
        "helpFile": 'data_files#FreeR',
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
        'sameCrystalAs'],
    qualifiers_definition={
        "correctColumns": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A list of coloumn data types expected in the file'},
    },
)
class CFreeRDataFile(CMiniMtzDataFile):
    """An MTZ experimental data file"""

    project: Optional[CProjectId] = None
    baseName: Optional[CFilePath] = None
    relPath: Optional[CFilePath] = None
    annotation: Optional[CString] = None
    dbFileId: Optional[CUUID] = None
    subType: Optional[CInt] = None
    contentFlag: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFreeRDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "fileName": attribute(AttributeType.CUSTOM, custom_class="CMiniMtzDataFile", tooltip="fileName attribute"),
        "columnTag": attribute(AttributeType.STRING, tooltip="columnTag attribute"),
        "columnNames": attribute(AttributeType.STRING, tooltip="columnNames attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['fileName', 'columnTag', 'columnNames'],
)
class CMergeMiniMtz(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    fileName: Optional[CMiniMtzDataFile] = None
    columnTag: Optional[CString] = None
    columnNames: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMergeMiniMtz.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "groupType": attribute(AttributeType.CUSTOM, custom_class="CMtzColumnGroupType", tooltip="groupType attribute"),
        "columns": attribute(AttributeType.CUSTOM, custom_class="CList", tooltip="columns attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CMtzColumnGroup(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    groupType: Optional[CMtzColumnGroupType] = None
    columns: Optional[CList] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CMtzColumnGroup.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "selected": attribute(AttributeType.BOOLEAN, tooltip="selected attribute"),
        "obsDataFile": attribute(AttributeType.CUSTOM, custom_class="CObsDataFile", tooltip="obsDataFile attribute"),
        "crystalName": attribute(AttributeType.CUSTOM, custom_class="CCrystalName", tooltip="crystalName attribute"),
        "datasetName": attribute(AttributeType.CUSTOM, custom_class="CDatasetName", tooltip="datasetName attribute"),
        "formFactors": attribute(AttributeType.CUSTOM, custom_class="CFormFactor", tooltip="formFactors attribute"),
        "formFactorSource": attribute(AttributeType.STRING, tooltip="formFactorSource attribute"),
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
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
)
class CDataset(CData):
    """The experimental data model for ab initio phasing"""

    selected: Optional[CBoolean] = None
    obsDataFile: Optional[CObsDataFile] = None
    crystalName: Optional[CCrystalName] = None
    datasetName: Optional[CDatasetName] = None
    formFactors: Optional[CFormFactor] = None
    formFactorSource: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDataset.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "columnGroup": attribute(AttributeType.CUSTOM, custom_class="CMtzColumnGroup", tooltip="columnGroup attribute"),
        "datasetName": attribute(AttributeType.STRING, tooltip="datasetName attribute"),
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
        "groupTypes": [],
    },
    qualifiers_order=['groupTypes', 'mtzFileKey', 'mustExist'],
    qualifiers_definition={
        "groupTypes": {'type': 'list', 'description': 'Type of columnGroup required by program'},
        "mtzFileKey": {'type': 'str', 'description': 'The key for a CMtxDataFile in the same CContainer'},
        "mustExist": {'type': 'bool', 'description': 'Flag if the parameter must be set at run time'},
    },
)
class CProgramColumnGroup0(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    columnGroup: Optional[CMtzColumnGroup] = None
    datasetName: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CProgramColumnGroup0.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)
