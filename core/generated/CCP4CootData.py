"""Auto-generated from CCP4i2 metadata. DO NOT EDIT.

To extend these classes, create subclasses in core/extensions/
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

# Metadata system
from core.base_object.class_metadata import cdata_class, attribute, AttributeType

# Base classes
from core.base_object.base_classes import CDataFile

# Fundamental types
from core.base_object.fundamental_types import CInt, CProjectId, CString, CUUID

# Cross-file class references
from core.generated.CCP4File import CFilePath


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
        "mimeTypeName": 'application/coot-script',
        "mimeTypeDescription": 'Coot history/script file',
        "fileExtensions": ['scm', 'py'],
        "fileContentClassName": None,
        "guiLabel": 'Coot history',
        "fileLabel": 'coot_history',
        "toolTip": 'history.scm or 0-state.scm file from Coot',
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
class CCootHistoryDataFile(CDataFile):
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
        Initialize CCootHistoryDataFile.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)
