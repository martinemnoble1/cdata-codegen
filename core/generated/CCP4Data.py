"""Auto-generated from CCP4i2 metadata. DO NOT EDIT.

To extend these classes, create subclasses in core/extensions/
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

# Metadata system
from core.base_object.class_metadata import cdata_class, attribute, AttributeType

# Base classes
from core.base_object.base_classes import CData

# Fundamental types
from core.base_object.fundamental_types import CFloat, CInt, CList, CString


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
        "charWidth": 10,
    },
    qualifiers_order=['charWidth'],
    qualifiers_definition={
        "charWidth": {'type': 'int'},
    },
)
class CBaseData(CData):
    """Base class for simple classes"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CBaseData.

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
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0,
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
class COneWord(CString):
    """A single word string - no white space"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize COneWord.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


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
class CCollection(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CCollection.

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
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0,
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
class CUUID(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CUUID.

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
        "listMaxLength": 250,
    },
    qualifiers_order=[
        'listMinLength',
        'listMaxLength',
        'listCompare',
        'nameRoot'],
    qualifiers_definition={
        "default": {'type': 'list'},
        "listMaxLength": {'type': 'int', 'description': 'Inclusive maximum length of list'},
        "listMinLength": {'type': 'int', 'description': 'Inclusive minimum length of list'},
        "listCompare": {'type': 'int', 'description': 'If has value 1/-1 consecutive items in list must be greater/less than preceeding item. The list item class must have a __cmp__() method.'},
        "nameRoot": {'type': 'str', 'description': 'Name hint for the base name of output files'},
    },
)
class COutputFileList(CList):
    """A list with all items of one CData sub-class"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize COutputFileList.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    error_codes={
        "101": {
            "description": "End of range less than start"
        },
        "102": {
            "description": "End of range greater than start"
        }
    },
    qualifiers_order=['compare'],
    qualifiers_definition={
        "compare": {'type': 'int', 'description': 'If value is  1/-1 the end value must be greater/less than start.'},
    },
    contents_order=['start', 'end'],
)
class CRange(CData):
    """Base class for CIntRange and CFloatRange"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRange.

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
        "enumerators": ['CPdbDataFile', 'CSeqDataFile', 'CObsDataFile', 'CPhsDataFile', 'CMapCoeffsDataFile', 'CFreeRDataFile', 'CMtzDataFile', 'CDictDataFile', 'CDataFile', 'CInt', 'CFloat', 'CString', 'CRefmacKeywordFile'],
        "menuText": [],
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
class CI2DataType(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CI2DataType.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "taskName": attribute(AttributeType.STRING),
        "patch": attribute(AttributeType.STRING),
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
    contents_order=['taskName', 'patch'],
)
class CPatchSelection(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    taskName: Optional[CString] = None
    patch: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPatchSelection.

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
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0,
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
class CJobTitle(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CJobTitle.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    error_codes={
        "201": {
            "description": "Range selection contains invalid character"
        },
        "202": {
            "description": "Range selection contains bad syntax"
        }
    },
    qualifiers={
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0,
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
class CRangeSelection(CString):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRangeSelection.

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
        "max": None,
        "min": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'],
    qualifiers_definition={
        "default": {'type': 'int'},
        "max": {'type': 'int', 'description': 'The inclusive minimum allowed value'},
        "min": {'type': 'int', 'description': 'The inclusive maximum allowed value'},
        "enumerators": {'type': 'list', 'listItemType': "<class 'int'>", 'description': 'A Python list of allowed or recommended values - see onlyEnumerators'},
        "menuText": {'type': 'list', 'listItemType': "<class 'str'>", 'description': 'A Python list of strings, matching items in enumerators list, to appear on GUI menu'},
        "onlyEnumerators": {'type': 'bool', 'description': 'If this is true then the enumerators are obligatory - otherwise they are treated as recommended values'},
    },
)
class CJobStatus(CInt):
    """An integer"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CJobStatus.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    error_codes={
        "101": {
            "description": "Attempting to access unknown item"
        },
        "102": {
            "description": "Unknown error trying to create new item"
        },
        "103": {
            "description": "Attempting to add item which is not appropriate class"
        }
    },
    qualifiers={
        "default": {},
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
class CDict(CCollection):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDict.

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
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0,
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
class CFollowFromJob(CUUID):
    """A string"""

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFollowFromJob.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "start": attribute(AttributeType.FLOAT),
        "end": attribute(AttributeType.FLOAT),
    },
    error_codes={
        "101": {
            "description": "End of range less than start"
        },
        "102": {
            "description": "End of range greater than start"
        }
    },
    qualifiers_order=['compare'],
    qualifiers_definition={
        "compare": {'type': 'int', 'description': 'If value is  1/-1 the end value must be greater/less than start.'},
    },
    contents_order=['start', 'end'],
)
class CFloatRange(CRange):
    """Two floats defining start and end of range"""

    start: Optional[CFloat] = None
    end: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CFloatRange.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "start": attribute(AttributeType.INT),
        "end": attribute(AttributeType.INT),
    },
    error_codes={
        "101": {
            "description": "End of range less than start"
        },
        "102": {
            "description": "End of range greater than start"
        }
    },
    qualifiers_order=['compare'],
    qualifiers_definition={
        "compare": {'type': 'int', 'description': 'If value is  1/-1 the end value must be greater/less than start.'},
    },
    contents_order=['start', 'end'],
)
class CIntRange(CRange):
    """Two integers defining start and end of range"""

    start: Optional[CInt] = None
    end: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CIntRange.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)
