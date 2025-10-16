"""Generated classes from CCP4Annotation.py"""

from ..base_object.base_classes import CData, CContainer
from ..CCP4FundamentalTypes import CInt, CList, CBoolean, CFloat, CString, COneWord
from ..base_object.class_metadata import cdata_class, attribute, AttributeType

from .CCP4BaseFile-stub import CDataFileContent, CDataFile, CXmlDataFile, CI2XmlDataFile


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
        "label": 'User id',
        "toolTip": 'User id as me@myplace.ac.uk'
    },
    qualifiers_order=[
        'minLength',
        'maxLength',
        'onlyEnumerators',
        'enumerators',
        'menuText',
        'allowedCharsCode'
    ],
    gui_label="CUserId",
)
class CUserId(CString):
    """A user ID"""
    pass


@cdata_class(
    attributes={
        "platformNode": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="platformNode attribute"),
        "userId": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4Annotation.CUserId", tooltip="userId attribute")
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
        "label": 'User id and current machine',
        "toolTip": 'User id as me@myplace.ac.uk and machine name'
    },
    contents_order=['platformNode', 'userId'],
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
    gui_label="CUserAddress",
)
class CUserAddress(CData):
    """User id and platform node"""
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
        "min": 0,
        "label": 'Time',
        "toolTip": 'Time and date as hh:mm dd/mm/yyyy',
        "format": '%H:%M %d/%b/%y'
    },
    qualifiers_order=[
        'format'
    ],
    qualifiers_definition={
        "format": {"type": str, "description": "Argument to Python time.strftime to display time in human readable format"}
    },
    gui_label="CTime",
)
class CTime(CInt):
    """The time. Uses Python time module"""
    pass


@cdata_class(
    attributes={
        "name": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="name attribute"),
        "mechanism": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="mechanism attribute"),
        "serverList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="serverList attribute"),
        "userExtensible": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="userExtensible attribute"),
        "customCodeFile": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CDataFile", tooltip="customCodeFile attribute"),
        "queueOptionsFile": attribute(AttributeType.CUSTOM, custom_class="core.CCP4File.CDataFile", tooltip="queueOptionsFile attribute"),
        "ccp4Dir": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="ccp4Dir attribute"),
        "tempDir": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="tempDir attribute"),
        "sge_root": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="sge_root attribute"),
        "keyFilename": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="keyFilename attribute"),
        "validate": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="validate attribute"),
        "timeout": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CFloat", tooltip="timeout attribute"),
        "maxTries": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="maxTries attribute")
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
    contents_order=['name', 'mechanism', 'serverList', 'userExtensible', 'ccp4Dir',
                    'tempDir', 'sge_root', 'keyFilename', 'validate', 'customCodeFile', 'queueOptionsFile'],
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
    gui_label="CServerGroup",
)
class CServerGroup(CData):
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
    gui_label="CMetaDataTagList",
)
class CMetaDataTagList(CList):
    """A list with all items of one CData sub-class"""
    pass


@cdata_class(
    attributes={
        "tag": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="tag attribute")
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
        "enumeratorsFunction": None,
        "addEnumeratorFunction": None
    },
    contents_order=['tag'],
    qualifiers_order=[
        'enumeratorsFunction',
        'addEnumeratorFunction'
    ],
    qualifiers_definition={
        "enumeratorsFunction": {"type": "method", "definition": "Function returning list of enumerators"},
        "addEnumeratorFunction": {"type": "method", "definition": "Function to add to list of enumerators"}
    },
    gui_label="CMetaDataTag",
)
class CMetaDataTag(CData):
    """This class will extend list of enumerators if new value for string is entered"""
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
        "label": 'Machine name',
        "toolTip": 'Hostname as mycomputer.myplace.ac.uk'
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
    gui_label="CHostName",
)
class CHostName(CString):
    """Computer name"""
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
        "label": 'Machine name',
        "toolTip": 'Hostname as mycomputer.myplace.ac.uk'
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
    gui_label="CHostname",
)
class CHostname(CHostName):
    """Computer name"""
    pass


@cdata_class(
    attributes={
        "family": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="family attribute"),
        "style": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="style attribute"),
        "pointSize": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="pointSize attribute"),
        "weight": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="weight attribute")
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
    gui_label="CFont",
)
class CFont(CData):
    """Simplified Qt font options"""
    pass


@cdata_class(
    attributes={
        "year": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="year attribute"),
        "month": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="month attribute"),
        "day": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="day attribute"),
        "yearRange": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="yearRange attribute"),
        "monthRange": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="monthRange attribute"),
        "dayRange": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="dayRange attribute")
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
    contents_order=['year', 'month', 'day',
                    'yearRange', 'monthRange', 'dayRange'],
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
    gui_label="CDateRange",
)
class CDateRange(CData):
    """A date range - may be on a scale of years,months or days"""
    pass


@cdata_class(
    attributes={
        "taskName": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="taskName attribute"),
        "version": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="version attribute"),
        "title": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="title attribute"),
        "references": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="references attribute")
    },
    error_codes={
        "100": {
            "description": "Failed attempting to load MedLine file - file not found"
        },
        "101": {
            "description": "Failed attempting to find references file"
        },
        "102": {
            "description": "Error copying file"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['taskName', 'version', 'title', 'references'],
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
    gui_label="CBibReferenceGroup",
)
class CBibReferenceGroup(CData):
    """Set of bibliographic references for a task"""
    pass


@cdata_class(
    attributes={
        "pmid": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CInt", tooltip="pmid attribute"),
        "title": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="title attribute"),
        "authorList": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CList", tooltip="authorList attribute"),
        "source": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="source attribute"),
        "url": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="url attribute"),
        "selected": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CBoolean", tooltip="selected attribute")
    },
    error_codes={
        "101": {
            "description": "Failed to load Medline data"
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False
    },
    contents_order=['pmid', 'title', 'authorList',
                    'source', 'url', 'selected'],
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
    gui_label="CBibReference",
)
class CBibReference(CData):
    """Bibliographic reference"""
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
        "minLength": None,
        "maxLength": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False,
        "charWidth": -1,
        "allowedCharsCode": 0
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
    gui_label="CAuthor",
)
class CAuthor(CString):
    """Placeholder for bibliographic author"""
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
    gui_label="CAnnotationList",
)
class CAnnotationList(CList):
    """A list of annotation"""
    pass


@cdata_class(
    attributes={
        "text": attribute(AttributeType.CUSTOM, custom_class="core.CCP4Data.CString", tooltip="text attribute"),
        "time": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4Annotation.CTime", tooltip="time attribute"),
        "author": attribute(AttributeType.CUSTOM, custom_class="ccp4x.data_scan.CCP4Annotation.CUserId", tooltip="author attribute")
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
        "label": 'Annotation',
        "toolTip": 'Enter your comments'
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
    gui_label="CAnnotation",
)
class CAnnotation(CData):
    """Annotation text with user id and time"""
    pass
