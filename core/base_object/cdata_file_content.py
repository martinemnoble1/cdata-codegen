"""
CDataFileContent - Base class for file content data objects.

This class extends CData with validation in set_qualifier() to prevent common errors.
Most functionality is inherited from CData or provided by the @cdata_class decorator.

The @cdata_class decorator adds:
- Error codes for file content operations
- Default qualifiers (allowUndefined, saveToDb, etc.)
- Metadata methods (validate, get_metadata, get_field_info) automatically
"""

from .cdata import CData
from .class_metadata import cdata_class


@cdata_class(
    error_codes={
        '0': {'severity': 0, 'description': 'OK'},
        '1': {'severity': 1, 'description': 'Data has undefined value'},
        '2': {'severity': 3, 'description': 'Data has undefined value'},
        '3': {'severity': 2, 'description': 'Missing data'},
        '4': {'description': 'Missing data'},
        '5': {'description': 'Attempting to set data of wrong type'},
        '6': {'description': 'Default value does not satisfy validity check'},
        '7': {'severity': 2, 'description': 'Unrecognised qualifier in data input'},
        '8': {'severity': 2, 'description': 'Attempting to get inaccessible attribute:'},
        '9': {'description': 'Failed to get property'},
        '10': {'severity': 2, 'description': 'Attempting to set inaccessible attribute:'},
        '11': {'description': 'Failed to set property:'},
        '12': {'description': 'Undetermined error setting value from XML'},
        '13': {'description': 'Unrecognised class name in qualifier'},
        '14': {'severity': 2, 'description': 'No object name when saving qualifiers to XML'},
        '15': {'description': 'Error saving qualifier to XML'},
        '16': {'severity': 2, 'description': 'Unrecognised item in XML data file'},
        '17': {'description': 'Attempting to set unrecognised qualifier'},
        '18': {'description': 'Attempting to set qualifier with wrong type'},
        '19': {'description': 'Attempting to set qualifier with wrong list item type'},
        '20': {'description': 'Error creating a list/dict item object'},
        '21': {'description': 'Unknown error setting qualifiers from Xml file'},
        '22': {'description': 'Unknown error testing validity'},
        '23': {'description': 'Error saving data object to XML'},
        '24': {'description': 'Unable to test validity of default', 'severity': 2},
        '300': {'description': 'Compared objects are the same', 'severity': 0},
        '315': {'description': 'Both compared objects are null', 'severity': 0},
        '301': {'description': 'Unable to compare this class of data', 'severity': 2},
        '302': {'description': 'Other data has null value'},
        '303': {'description': 'My data has null value'},
        '304': {'description': 'Data has different values'}
    },
    qualifiers={
        'allowUndefined': True,
        'default': 'NotImplemented',
        'toolTip': 'NotImplemented',
        'guiLabel': 'NotImplemented',
        'guiDefinition': {},
        'helpFile': 'NotImplemented',
        'saveToDb': False
    },
    qualifiers_order=['allowUndefined', 'default', 'toolTip', 'guiLabel', 'guiDefinition', 'helpFile', 'saveToDb'],
    qualifiers_definition={
        'allowUndefined': {'type': "<class 'bool'>"},
        'default': {'type': "<class 'dict'>"},
        'toolTip': {'type': "<class 'str'>"},
        'guiLabel': {'type': "<class 'str'>"},
        'guiDefinition': {'type': "<class 'dict'>"},
        'helpFile': {'type': "<class 'str'>"},
        'saveToDb': {'type': "<class 'bool'>", 'description': 'Save this data in the database'}
    },
    gui_label='CDataFileContent'
)
class CDataFileContent(CData):
    """
    Base class for file content data objects.

    This class adds validation to set_qualifier() to prevent common errors.
    All other functionality is inherited from CData or provided by the @cdata_class decorator.
    """

    def set_qualifier(self, key, value):
        """Set or override a qualifier value. Adds validation to prevent CData objects as values."""
        # Validation: prevent accidental primitive overwrites
        if not isinstance(self, CData):
            raise TypeError(
                f"set_qualifier called on non-CData object of type {type(self)}. "
                "This usually means you overwrote your CData instance with a primitive value."
            )

        # Validation: prevent CData objects as qualifier values
        if isinstance(value, CData):
            raise TypeError("Qualifier values must not be CData objects.")

        # Call parent implementation
        super().set_qualifier(key, value)
