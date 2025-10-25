

# --- CDataFileContent migrated from CCP4File.py ---


import sys
import os
from typing import Any, Dict
from enum import Enum, auto
from .metadata_system import MetadataRegistry
from .class_metadata import cdata_class, attribute, AttributeType

# --- CDataFileContent migrated from CCP4File.py ---


# (Place this after the CData class definition)

"""Base classes for the new CData hierarchy."""

import sys
import os
from typing import Any, Dict
from enum import Enum, auto
from .metadata_system import MetadataRegistry
from .class_metadata import cdata_class, attribute, AttributeType

# Import HierarchicalObject from the core system
#sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from .hierarchy_system import HierarchicalObject


class ValueState(Enum):
    """States that a value can be in."""

    NOT_SET = auto()  # Value has never been explicitly set
    DEFAULT = auto()  # Value is using a default from qualifiers
    EXPLICITLY_SET = auto()  # Value has been explicitly assigned


@cdata_class(gui_label="CData")
class CData(HierarchicalObject):
    """Base class for all CCP4i2 data objects with hierarchical relationships."""

    def __init__(self, parent=None, name=None, **kwargs):
        # Initialize hierarchical object first (it only takes parent and name)
        super().__init__(parent=parent, name=name)
        print(f"[DEBUG] Initializing CData instance of type {self.__class__.__name__} with name '{name}'")
        # Initialize set state tracking
        self._value_states: Dict[str, ValueState] = {}
        self._default_values: Dict[str, Any] = {}

        # Mark that hierarchy is initialized - now we can use custom setattr
        self._hierarchy_initialized = True

        # Load default values from qualifiers if available
        self._load_default_values()

        # NEW: Apply metadata-driven attribute creation
        self._apply_metadata_attributes()

        # --- Per-instance metadata copying and override ---
        # Copy class-level metadata to instance for override flexibility
        cls = self.__class__
        # Qualifiers
        if hasattr(cls, 'qualifiers'):
            class_qualifiers = getattr(cls, 'qualifiers')
            print(f"[DEBUG] {cls.__name__}.qualifiers type: {type(class_qualifiers)}, value: {class_qualifiers}")
            if not isinstance(class_qualifiers, dict):
                print(f"[WARNING] Class-level qualifiers for {cls.__name__} is not a dict: {type(class_qualifiers)}")
            if isinstance(class_qualifiers, dict):
                self.qualifiers = dict(class_qualifiers)
            elif hasattr(class_qualifiers, 'items'):
                self.qualifiers = dict(class_qualifiers.items())
            else:
                self.qualifiers = {}
        # Qualifiers order
        if hasattr(cls, 'qualifiers_order'):
            self.qualifiers_order = list(getattr(cls, 'qualifiers_order'))
        # Qualifiers definition
        if hasattr(cls, 'qualifiers_definition'):
            self.qualifiers_definition = dict(getattr(cls, 'qualifiers_definition'))
        # CONTENT_ORDER
        if hasattr(cls, 'CONTENT_ORDER'):
            self.CONTENT_ORDER = list(getattr(cls, 'CONTENT_ORDER'))
        # For CList: subitem
        if hasattr(cls, 'subItem'):
            self.subItem = getattr(cls, 'subItem')

        # Allow overrides via kwargs
        for meta_key in ['qualifiers', 'qualifiers_order', 'qualifiers_definition', 'CONTENT_ORDER', 'subitem']:
            if meta_key in kwargs:
                # Set qualifiers directly as a dict to avoid wrapping as CData
                if meta_key == 'qualifiers' and isinstance(kwargs[meta_key], dict):
                    self.qualifiers = kwargs.pop(meta_key)
                else:
                    setattr(self, meta_key, kwargs.pop(meta_key))

        # Apply provided attributes with hierarchy handling
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _load_default_values(self):
        """Load default values from qualifiers metadata."""
        # Try to get default values from metadata system
        try:
            from .metadata_system import MetadataRegistry
            metadata = MetadataRegistry.get_class_metadata(self.__class__.__name__)
            if metadata:
                for field_name, field_meta in metadata.fields.items():
                    if field_meta.default_value is not None:
                        self._default_values[field_name] = field_meta.default_value
                        self._value_states[field_name] = ValueState.NOT_SET
        except Exception:
            # If metadata not available, that's okay
            pass

    def _apply_metadata_attributes(self):
        """Apply metadata-driven attribute creation if metadata is available."""
        try:
            from .class_metadata import apply_metadata_to_instance

            apply_metadata_to_instance(self)
        except ImportError:
            # Metadata system not available, skip
            pass
        except Exception:
            # Any other error, skip silently to avoid breaking existing code
            pass

    def get_qualifier(self, key, default=None):
        """Get a qualifier value for this instance."""
        if hasattr(self, 'qualifiers') and self.qualifiers is not None:
            return self.qualifiers.get(key, default)
        return default

    def set_qualifier(self, key, value):
        """Set or override a qualifier value for this instance."""
        if not hasattr(self, 'qualifiers') or self.qualifiers is None:
            self.qualifiers = {}
        self.qualifiers[key] = value

    def set(self, values: dict):
        """Set attributes from dict, unsetting others."""
        for key in list(self.__dict__.keys()):
            if not key.startswith('_') and key not in values:
                if hasattr(self, key):
                    delattr(self, key)
        for key, value in values.items():
            setattr(self, key, value)

    def update(self, values: dict):
        """Update attributes from dict without unsetting others."""
        for key, value in values.items():
            setattr(self, key, value)

    def objectPath(self) -> str:
        """Return the full hierarchical path to this object.

        Returns:
            String path like "project.inputData.XYZIN" for hierarchical objects
        """
        path_parts = []
        current = self

        # Walk up the hierarchy collecting names
        while current is not None:
            if hasattr(current, 'name') and current.name:
                path_parts.insert(0, current.name)
            current = getattr(current, 'parent', None)

        return ".".join(path_parts) if path_parts else ""

    def objectName(self) -> str:
        """Return the name of this object.

        Returns:
            The object's name attribute or empty string
        """
        return getattr(self, 'name', '')

    def isSet(self, field_name: str = None) -> bool:
        """Check if a field has been explicitly set.

        Args:
            field_name: Name of the field to check. If None, checks the 'value' attribute.

        Returns:
            True if field has been explicitly set, False otherwise
        """
        if field_name is None:
            field_name = "value"
        return (
            self._value_states.get(field_name, ValueState.NOT_SET)
            == ValueState.EXPLICITLY_SET
        )

    def unSet(self, field_name: str):
        """Return a field to its not-set state.

        Args:
            field_name: Name of the field to unset
        """
        # Special case for 'value' property in fundamental types
        if field_name == 'value' and hasattr(self, '_value'):
            # Reset the internal _value to None
            self._value = None
        elif hasattr(self, field_name):
            attr = getattr(self, field_name)
            # If the attribute is a CData (or HierarchicalObject), call destroy before deleting
            if isinstance(attr, HierarchicalObject):
                try:
                    attr.destroy()
                except Exception:
                    pass
            try:
                delattr(self, field_name)
            except AttributeError:
                # Can't delete properties without deleters - that's OK
                pass

        # Mark as not set
        self._value_states[field_name] = ValueState.NOT_SET

    def getValueState(self, field_name: str) -> ValueState:
        """Get the current state of a field.

        Args:
            field_name: Name of the field

        Returns:
            ValueState indicating current state
        """
        return self._value_states.get(field_name, ValueState.NOT_SET)

    def setToDefault(self, field_name: str):
        """Set a field to its default value.

        Args:
            field_name: Name of the field to set to default
        """
        if field_name in self._default_values:
            # Set without triggering "explicitly set" state
            self._value_states[field_name] = ValueState.DEFAULT
            super().__setattr__(field_name, self._default_values[field_name])
        else:
            # No default available, unset it
            self.unSet(field_name)

    def setDefault(self, value: Any):
        """Set the default value for this object (old API compatibility).

        Args:
            value: The default value to set
        """
        # For simple value types, set the value and mark as DEFAULT
        if hasattr(self, 'value'):
            super().__setattr__('_value', value)
            self._value_states['value'] = ValueState.DEFAULT
            self._default_values['value'] = value
        else:
            # For complex types, store in default values
            self._default_values['default'] = value

    def getDefaultValue(self, field_name: str) -> Any:
        """Get the default value for a field.

        Args:
            field_name: Name of the field

        Returns:
            Default value or None if no default exists
        """
        return self._default_values.get(field_name)

    def validity(self):
        """Validate this object and return an error report.

        This method checks the object's state and validates it against
        qualifiers (min, max, enumerators, etc.). Subclasses should
        override this to add custom validation logic.

        Returns:
            CErrorReport containing any validation errors/warnings
        """
        from .error_reporting import CErrorReport, SEVERITY_ERROR

        report = CErrorReport()

        # Base CData validation - can be extended by subclasses
        # Check if object has required qualifiers
        if hasattr(self, 'qualifiers') and self.qualifiers:
            # Basic validation is done here
            # Subclasses will add their own validation
            pass

        return report

    def getEtree(self, name: str = None):
        """Serialize this object to an XML ElementTree element.

        Args:
            name: Optional name for the XML element (uses self.name if not provided)

        Returns:
            xml.etree.ElementTree.Element representing this object
        """
        import xml.etree.ElementTree as ET

        element_name = name if name is not None else getattr(self, 'name', 'data')
        elem = ET.Element(element_name)

        # For simple value types, store the value as text
        if hasattr(self, 'value'):
            value = getattr(self, 'value')
            if value is not None:
                elem.text = str(value)

        # For containers and complex types, serialize children
        for attr_name, attr_value in self.__dict__.items():
            if attr_name.startswith('_') or attr_name in ['parent', 'name', 'children', 'signals']:
                continue
            if isinstance(attr_value, CData):
                child_elem = attr_value.getEtree(attr_name)
                elem.append(child_elem)

        return elem

    def setEtree(self, element, ignore_missing: bool = False):
        """Deserialize from an XML ElementTree element.

        Args:
            element: xml.etree.ElementTree.Element to deserialize from
            ignore_missing: If True, ignore attributes in XML that don't exist on this object
        """
        # For simple value types, read from text
        if hasattr(self, 'value') and element.text:
            # Determine the type and convert
            if hasattr(self, '__class__'):
                class_name = self.__class__.__name__
                if class_name == 'CInt':
                    self.value = int(element.text)
                elif class_name == 'CFloat':
                    self.value = float(element.text)
                elif class_name == 'CBoolean':
                    self.value = element.text.lower() in ('true', '1', 'yes')
                elif class_name == 'CString':
                    self.value = element.text
                else:
                    self.value = element.text

        # For containers, deserialize children
        for child in element:
            child_name = child.tag
            if hasattr(self, child_name):
                child_obj = getattr(self, child_name)
                if isinstance(child_obj, CData):
                    child_obj.setEtree(child, ignore_missing=ignore_missing)
            elif not ignore_missing:
                raise AttributeError(f"Object has no attribute '{child_name}'")

    def getQualifiersEtree(self):
        """Serialize qualifiers to an XML ElementTree element.

        Returns:
            xml.etree.ElementTree.Element containing qualifiers
        """
        import xml.etree.ElementTree as ET

        qualifiers_elem = ET.Element('qualifiers')

        if hasattr(self, 'qualifiers') and self.qualifiers:
            for key, value in self.qualifiers.items():
                qual_elem = ET.Element(key)
                if value is not None:
                    if isinstance(value, bool):
                        qual_elem.text = 'true' if value else 'false'
                    elif isinstance(value, list):
                        qual_elem.text = ','.join(str(v) for v in value)
                    else:
                        qual_elem.text = str(value)
                qualifiers_elem.append(qual_elem)

        return qualifiers_elem

    def setQualifiersEtree(self, qualifiers_element):
        """Deserialize qualifiers from an XML ElementTree element.

        Args:
            qualifiers_element: xml.etree.ElementTree.Element containing qualifiers
        """
        if qualifiers_element is None:
            return

        for child in qualifiers_element:
            key = child.tag
            text = child.text

            # Parse the value based on content
            if text is None:
                value = None
            elif text.lower() in ('true', 'false'):
                value = text.lower() == 'true'
            elif ',' in text:
                # List of values
                value = [item.strip() for item in text.split(',')]
            else:
                # Try to parse as number, otherwise keep as string
                try:
                    if '.' in text:
                        value = float(text)
                    else:
                        value = int(text)
                except (ValueError, AttributeError):
                    value = text

            self.set_qualifier(key, value)

# --- CDataFileContent migrated from CCP4File.py ---
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
    """Base class for file content data objects."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def get_qualifier(self, key, default=None):
        """Get a qualifier value for this instance."""
        if hasattr(self, 'qualifiers') and self.qualifiers is not None:
            return self.qualifiers.get(key, default)
        return default

    def set_qualifier(self, key, value):
        """Set or override a qualifier value for this instance. Prevent CData objects as values."""
        if not isinstance(self, CData):
            raise TypeError(f"set_qualifier called on non-CData object of type {type(self)}. "
                            "This usually means you overwrote your CData instance with a primitive value.")
        if not hasattr(self, 'qualifiers') or self.qualifiers is None or not isinstance(self.qualifiers, dict):
            if hasattr(self, 'qualifiers'):
                print(f"[WARNING] self.qualifiers is not a dict in set_qualifier: type={type(self.qualifiers)}, value={self.qualifiers}")
            else:
                print(f"[WARNING] self.qualifiers attribute is missing in set_qualifier for {type(self)}")
            self.qualifiers = {}
        # Prevent storing CData objects as qualifier values
        if isinstance(value, CData):
            raise TypeError("Qualifier values must not be CData objects.")
        self.qualifiers[key] = value

    def _setup_hierarchy_for_value(self, key: str, value: Any):
        """Set up hierarchical relationships for attribute values."""
        if isinstance(value, CData):
            # Set this object as parent and the attribute name as the child's name
            value.set_parent(self)
            value.name = key
        elif isinstance(value, list):
            # Handle list of CData objects
            for i, item in enumerate(value):
                if isinstance(item, CData):
                    item.set_parent(self)
                    item.name = f"{key}[{i}]"

    def _is_value_type(self) -> bool:
        """Check if this is a simple value type (like CString, CInt, etc.)."""
        # Simple heuristic: if class has only basic Python types as attributes
        # and no complex CData children, it's likely a value type
        value_type_patterns = ["String", "Int", "Float", "Bool", "OneWord"]
        return any(
            pattern in self.__class__.__name__ for pattern in value_type_patterns
        )

    def _smart_assign_from_dict(self, source_dict: dict):
        """Assign values from dictionary to object attributes."""
        for key, value in source_dict.items():
            setattr(self, key, value)

    def _smart_assign_from_cdata(self, source: "CData"):
        """Handle smart assignment from another CData object."""
        if self._is_value_type() and source._is_value_type():
            # Value assignment: copy the underlying value
            # For simple types, copy their primary value attribute
            primary_attrs = ["value", "text", "string", "content"]
            for attr in primary_attrs:
                if hasattr(source, attr):
                    setattr(self, attr, getattr(source, attr))
                    return

            # If no primary attribute found, copy all non-internal attributes
            for key, value in source.__dict__.items():
                if not key.startswith("_") and key not in [
                    "parent",
                    "name",
                    "children",
                    "signals",
                ]:
                    setattr(self, key, value)
        else:
            # Reference assignment for complex types
            # This would typically involve replacing this object with the source
            # For now, copy all attributes
            for key, value in source.__dict__.items():
                if not key.startswith("_") and key not in [
                    "parent",
                    "name",
                    "children",
                    "signals",
                ]:
                    setattr(self, key, value)

    def _load_default_values(self):
        """Load default values from qualifiers metadata."""
        # Try to get default values from metadata system
        try:
            metadata = MetadataRegistry.get_class_metadata(self.__class__.__name__)
            if metadata:
                for field_name, field_meta in metadata.fields.items():
                    if field_meta.default_value is not None:
                        self._default_values[field_name] = field_meta.default_value
                        self._value_states[field_name] = ValueState.NOT_SET
        except Exception:
            # If metadata not available, that's okay
            pass

    def objectPath(self) -> str:
        """Return the full hierarchical path to this object.

        Returns:
            String path like "project.inputData.XYZIN" for hierarchical objects
        """
        path_parts = []
        current = self

        # Walk up the hierarchy collecting names
        while current is not None:
            if hasattr(current, 'name') and current.name:
                path_parts.insert(0, current.name)
            current = getattr(current, 'parent', None)

        return ".".join(path_parts) if path_parts else ""

    def objectName(self) -> str:
        """Return the name of this object.

        Returns:
            The object's name attribute or empty string
        """
        return getattr(self, 'name', '')

    def isSet(self, field_name: str = None) -> bool:
        """Check if a field has been explicitly set.

        Args:
            field_name: Name of the field to check. If None, checks the 'value' attribute.

        Returns:
            True if field has been explicitly set, False otherwise
        """
        if field_name is None:
            field_name = "value"
        return (
            self._value_states.get(field_name, ValueState.NOT_SET)
            == ValueState.EXPLICITLY_SET
        )

    def unSet(self, field_name: str):
        """Return a field to its not-set state.

        Args:
            field_name: Name of the field to unset
        """
        # Special case for 'value' property in fundamental types
        if field_name == 'value' and hasattr(self, '_value'):
            # Reset the internal _value to None
            self._value = None
        elif hasattr(self, field_name):
            attr = getattr(self, field_name)
            # If the attribute is a CData (or HierarchicalObject), call destroy before deleting
            if isinstance(attr, HierarchicalObject):
                try:
                    attr.destroy()
                except Exception:
                    pass
            try:
                delattr(self, field_name)
            except AttributeError:
                # Can't delete properties without deleters - that's OK
                pass

        # Mark as not set
        self._value_states[field_name] = ValueState.NOT_SET

    def getValueState(self, field_name: str) -> ValueState:
        """Get the current state of a field.

        Args:
            field_name: Name of the field

        Returns:
            ValueState indicating current state
        """
        return self._value_states.get(field_name, ValueState.NOT_SET)

    def setToDefault(self, field_name: str):
        """Set a field to its default value.

        Args:
            field_name: Name of the field to set to default
        """
        if field_name in self._default_values:
            # Set without triggering "explicitly set" state
            self._value_states[field_name] = ValueState.DEFAULT
            super().__setattr__(field_name, self._default_values[field_name])
        else:
            # No default available, unset it
            self.unSet(field_name)

    def setDefault(self, value: Any):
        """Set the default value for this object (old API compatibility).

        Args:
            value: The default value to set
        """
        # For simple value types, set the value and mark as DEFAULT
        if hasattr(self, 'value'):
            super().__setattr__('_value', value)
            self._value_states['value'] = ValueState.DEFAULT
            self._default_values['value'] = value
        else:
            # For complex types, store in default values
            self._default_values['default'] = value

    def getDefaultValue(self, field_name: str) -> Any:
        """Get the default value for a field.

        Args:
            field_name: Name of the field

        Returns:
            Default value or None if no default exists
        """
        return self._default_values.get(field_name)

    def __setattr__(self, name: str, value: Any):
        """Override setattr to handle smart assignment and hierarchical relationships."""

        # Allow setting internal attributes normally during initialization
        if (
            name.startswith("_")
            or name in ["parent", "name", "children", "signals"]
            or not hasattr(self, "_hierarchy_initialized")
        ):
            super().__setattr__(name, value)
            return

        # Special handling for metadata attributes: assign directly if dict or list
        if name in ["qualifiers", "qualifiers_order", "qualifiers_definition", "CONTENT_ORDER", "subitem"]:
            if isinstance(value, (dict, list)):
                object.__setattr__(self, name, value)
                return

        # Handle smart assignment patterns
        existing_attr = getattr(self, name, None)

        if isinstance(value, dict):
            # Dictionary assignment: update object attributes from dictionary
            if existing_attr is None:
                # Create new CData object and populate from dict
                new_obj = CData(name=name)
                new_obj._smart_assign_from_dict(value)
                self._setup_hierarchy_for_value(name, new_obj)
                super().__setattr__(name, new_obj)
                return
            elif isinstance(existing_attr, CData):
                # Update existing CData object from dictionary
                existing_attr._smart_assign_from_dict(value)
                # Mark as explicitly set since we're assigning new values
                if hasattr(self, "_value_states"):
                    self._value_states[name] = ValueState.EXPLICITLY_SET
                return  # Don't replace the object, just update it

        elif isinstance(value, CData) and isinstance(existing_attr, CData):
            # CData to CData assignment: use smart assignment logic
            existing_attr._smart_assign_from_cdata(value)
            # Mark as explicitly set since we're assigning a new value
            if hasattr(self, "_value_states"):
                self._value_states[name] = ValueState.EXPLICITLY_SET
            return  # Don't replace the object, just update it

        elif (
            existing_attr is not None and isinstance(existing_attr, CData)
            and existing_attr._is_value_type()
        ):
            # Primitive value assignment to existing CData value type
            # e.g., ctrl.NCYCLES = 25 where ctrl.NCYCLES is a CInt
            if isinstance(value, (int, float, str, bool)):
                # Check type compatibility
                type_compatible = False
                if hasattr(existing_attr, "value"):
                    # Import types locally to avoid circular import
                    from .fundamental_types import CInt, CFloat, CBoolean
                    try:
                        from .fundamental_types import CString
                    except ImportError:
                        CString = None
                    if isinstance(existing_attr, CInt) and isinstance(value, int):
                        type_compatible = True
                    elif isinstance(existing_attr, CFloat) and isinstance(value, (int, float)):
                        type_compatible = True
                    elif isinstance(existing_attr, CBoolean) and isinstance(value, bool):
                        type_compatible = True
                    elif CString is not None and isinstance(existing_attr, CString) and isinstance(value, str):
                        type_compatible = True
                if type_compatible:
                    # Update the value attribute of the existing CData object
                    existing_attr.value = value
                    # Mark as explicitly set
                    if hasattr(self, "_value_states"):
                        self._value_states[name] = ValueState.EXPLICITLY_SET
                    return  # Don't replace the object, just update its value

        # For new attributes or non-smart assignment, handle hierarchy and set normally
        self._setup_hierarchy_for_value(name, value)
        super().__setattr__(name, value)
        # Track that this value has been explicitly set (unless it's internal)
        if (hasattr(self, "_value_states") and not name.startswith("_")
            and name not in ["parent", "name", "children", "signals"]):
            self._value_states[name] = ValueState.EXPLICITLY_SET

    def __str__(self):
        attrs = []
        for k, v in self.__dict__.items():
            if not k.startswith("_") and k not in [
                "parent",
                "name",
                "children",
                "signals",
            ]:
                attrs.append(f"{k}={v}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __repr__(self):
        return self.__str__()


    def set(self, values: dict):
        """Set attributes from dict, unset others. Avoid overwriting CData-derived attributes with primitives."""
        metadata = None
        try:
            metadata = MetadataRegistry.get_class_metadata(self.__class__.__name__)
        except Exception:
            pass
        if metadata:
            all_fields = list(metadata.fields.keys())
        else:
            all_fields = [k for k in self.__dict__ if not k.startswith('_')
                         and k not in ['parent', 'name', 'children', 'signals']]
        for k in all_fields:
            if k in values:
                current = getattr(self, k, None)
                new_value = values[k]
                # If current is CData-derived and new_value is primitive, update .value
                if hasattr(current, 'value') and not isinstance(new_value, type(current)):
                    current.value = new_value
                else:
                    setattr(self, k, new_value)
                self._value_states[k] = ValueState.EXPLICITLY_SET
            else:
                self.unSet(k)


    def update(self, values: dict):
        """Update only provided attributes from dict. Avoid overwriting CData-derived attributes with primitives."""
        for k, v in values.items():
            current = getattr(self, k, None)
            if hasattr(current, 'value') and not isinstance(v, type(current)):
                current.value = v
            else:
                setattr(self, k, v)
            self._value_states[k] = ValueState.EXPLICITLY_SET

    def get_metadata(self):
        """Get metadata for this class."""
        return MetadataRegistry.get_by_class(self.__class__)

    def validate(self):
        """Validate this instance using its metadata."""
        metadata = self.get_metadata()
        if metadata:
            return metadata.validate_instance(self)
        return []

    def get_field_info(self, field_name: str):
        """Get metadata for a specific field."""
        metadata = self.get_metadata()
        if metadata:
            return metadata.get_field_metadata(field_name)
        return None

    def get_field_tooltip(self, field_name: str):
        """Get tooltip for a field."""
        field_info = self.get_field_info(field_name)
        return field_info.tooltip if field_info else None

    def get_field_enumerators(self, field_name: str):
        """Get valid enumerators for a field."""
        field_info = self.get_field_info(field_name)
        return field_info.enumerators if field_info else None

    @classmethod
    def get_error_message(cls, error_code: int):
        """Get error message for an error code."""
        from .metadata_system import get_error_message

        return get_error_message(error_code)

    def get_merged_metadata(self, key: str) -> dict:
        """
        Dynamically merge metadata (e.g., qualifiers, qualifiers_definition, etc.) from all ancestors.
        Child class values override parent values.
        Usage: self.get_merged_metadata('qualifiers')
        """
        merged = {}
        for cls in self.__class__.__mro__:
            if hasattr(cls, key):
                parent_meta = getattr(cls, key)
                if isinstance(parent_meta, dict):
                    merged.update(parent_meta)
        # Instance-level overrides
        if hasattr(self, key):
            instance_meta = getattr(self, key)
            if isinstance(instance_meta, dict):
                merged.update(instance_meta)
        return merged

    def get_merged_order(self, key: str) -> list:
        """
        Dynamically merge order lists (e.g., contents_order, qualifiers_order) from all ancestors.
        Child class values extend parent values, with duplicates removed (child order wins).
        Usage: self.get_merged_order('contents_order')
        """
        seen = set()
        merged = []
        for cls in reversed(self.__class__.__mro__):
            if hasattr(cls, key):
                parent_order = getattr(cls, key)
                if isinstance(parent_order, list):
                    for item in parent_order:
                        if item not in seen:
                            merged.append(item)
                            seen.add(item)
        # Instance-level overrides
        if hasattr(self, key):
            instance_order = getattr(self, key)
            if isinstance(instance_order, list):
                for item in instance_order:
                    if item not in seen:
                        merged.append(item)
                        seen.add(item)
        return merged


@cdata_class(
    attributes={
        "project": attribute(AttributeType.STRING),
        "baseName": attribute(AttributeType.STRING),
        "relPath": attribute(AttributeType.STRING),
        "annotation": attribute(AttributeType.STRING),
        "dbFileId": attribute(AttributeType.STRING),
        "subType": attribute(AttributeType.INT),
        "contentFlag": attribute(AttributeType.INT),
    },
    qualifiers={
        "allowUndefined": True,
        "mustExist": False,
        "fromPreviousJob": False,
        "jobCombo": True,
        "mimeTypeName": "",
        "mimeTypeDescription": "",
        "fileLabel": None,
        "fileExtensions": [],
        "fileContentClassName": None,
        "isDirectory": False,
        "saveToDb": True,
        "requiredSubType": None,
        "requiredContentFlag": None,
    },
    gui_label="CDataFile",
    qualifiers_order=[
        "fileExtensions",
        "mimeTypeName",
        "mimeTypeDescription",
        "fileLabel",
        "allowUndefined",
        "mustExist",
        "fromPreviousJob",
        "jobCombo",
        "fileContentClassName",
        "isDirectory",
        "saveToDb",
        "requiredSubType",
        "requiredContentFlag",
    ],
    qualifiers_definition={
        "allowUndefined": {
            "type": "bool",
            "description": "Flag if data file can be undefined at run time",
        },
        "mustExist": {
            "type": "bool",
            "description": "Flag if data file must exist at run time",
        },
        "fromPreviousJob": {
            "type": "bool",
            "description": "Flag if input data file can be inferred from preceeding jobs",
        },
        "jobCombo": {
            "type": "bool",
            "description": "Flag if data widget should be a combo box ",
        },
        "mimeTypeName": {"type": "str", "description": ""},
        "mimeTypeDescription": {"type": "str", "description": ""},
        "fileLabel": {"type": "str", "description": "Label for file"},
        "fileExtensions": {
            "type": "list",
            "listItemType": "str",
            "description": "A list of strings containing allowed file extensions (no dot)",
        },
        "fileContentClassName": {
            "type": "str",
            "editable": False,
            "description": "A string containing the name of a class which will hold the file contents",
        },
        "isDirectory": {
            "type": "bool",
            "description": "Flag if the data is a directory",
        },
        "ifInfo": {
            "type": "bool",
            "description": "Flag if gui widget should have info icon",
        },
        "saveToDb": {
            "type": "bool",
            "description": "Save the name of this file in the database",
        },
        "requiredSubType": {
            "type": "list",
            "listItemType": "int",
            "description": "A list of allowed sub types",
        },
        "requiredContentFlag": {
            "type": "list",
            "listItemType": "int",
            "description": "A list of allowed content flags",
        },
    },
)
class CDataFile(CData):
    """Base class for file-related CData classes.

    Attributes are automatically created from embedded metadata:
    - project: CProjectId - Project identifier
    - baseName: CFilePath - Base filename
    - relPath: CFilePath - Relative path to file
    - annotation: CString - File annotation
    - dbFileId: CUUID - Database file identifier
    - subType: CInt - File subtype (optional)
    - contentFlag: CInt - Content flag (min=0, optional)
    """

    def __init__(self, file_path: str = None, parent=None, name=None, **kwargs):
        # Pass per-instance metadata overrides to base
        super().__init__(parent=parent, name=name, **kwargs)

        # Legacy compatibility
        self.file_path = file_path

    def load_from_file(self, file_path: str):
        """Load data from file."""
        self.file_path = file_path
        # TODO: Implement file loading logic

    def save_to_file(self, file_path: str = None):
        """Save data to file."""
        path = file_path or self.file_path
        if not path:
            raise ValueError("No file path specified")
        # TODO: Implement file saving logic


@cdata_class(
    error_codes={
        "101": {
            "description": "Error parsing XML"
        },
        "102": {
            "description": "Missing information"
        },
        "103": {
            "description": "Unknown data class"
        },
        "104": {
            "description": "Error creating data object"
        },
        "105": {
            "description": "Error setting data object qualifiers"
        },
        "106": {
            "description": "Error loading container definition"
        },
        "107": {
            "description": "XML file does not have correct function defined in the header"
        },
        "108": {
            "description": "XML undefined error interpreting sub-container"
        },
        "109": {
            "description": "Error attempting to access unknown attribute",
            "severity": 2
        },
        "110": {
            "description": "Error creating sub-container"
        },
        "111": {
            "description": "XML file does not have expected pluginName defined in the header"
        },
        "113": {
            "description": "Attempting to add object that is not a CData"
        },
        "114": {
            "description": "Attempting to add object without valid name"
        },
        "115": {
            "description": "Attempting to add object with name that is already in container"
        },
        "116": {
            "description": "Error while attempting to add object"
        },
        "117": {
            "description": "Attempting to delete object with unrecognised name"
        },
        "118": {
            "description": "Error while attempting to delete object"
        },
        "119": {
            "description": "Error while attempting to set this container as object parent"
        },
        "120": {
            "description": "Attempting to add object of unrecognised class to container contents"
        },
        "121": {
            "description": "Error while attempting to add to container contents"
        },
        "122": {
            "description": "Error while attempting to make object from new content in container"
        },
        "123": {
            "description": "Unknown error while reading container header"
        },
        "124": {
            "description": "Definition of sub-content for data of class that does not require sub-content"
        },
        "125": {
            "description": "Unknown error while reading container content"
        },
        "126": {
            "description": "No id for sub-container in XML file"
        },
        "127": {
            "description": "Attempting to load container data from file that does not exist"
        },
        "128": {
            "description": "Unknown error creating XML for sub-container"
        },
        "129": {
            "description": "Error retieving data object for XML"
        },
        "130": {
            "description": "Error saving data object to XML"
        },
        "131": {
            "description": "Unknown error writing container contents to XML file"
        },
        "132": {
            "description": "Error changing object name - no name given"
        },
        "133": {
            "description": "Error changing object name - object with new name already exists"
        },
        "134": {
            "description": "Error changing object name - no object with old name"
        },
        "135": {
            "description": "Unknown error changing object name"
        },
        "136": {
            "description": "Error inserting object in container data order"
        },
        "137": {
            "description": "Unknown error restoring data from database"
        },
        "138": {
            "description": "Attempting to copy from otherContainer which is not a CContainer"
        },
        "139": {
            "severity": 2,
            "description": "Attempting to copy data which is not in this container"
        },
        "140": {
            "severity": 2,
            "description": "Attempting to copy data which is not in the other container"
        },
        "141": {
            "severity": 2,
            "description": "Unknown error copying data"
        },
        "142": {
            "description": "Unrecognised class name in file"
        },
        "143": {
            "description": "Item in file does not have an id"
        },
        "144": {
            "description": "Item id in file is not unique"
        },
        "145": {
            "description": "Failed setting command line argument"
        },
        "146": {
            "description": "Insufficient arguments at end of command line"
        },
        "147": {
            "description": "Error handling XmlDataFile for file element in def xml"
        },
        "148": {
            "description": "XmlDataFile for file element in def xml: file not found"
        },
        "149": {
            "description": "XmlDataFile for file element in def xml: can not read xml"
        },
        "150": {
            "description": "loadDataFromXml could not find plugin def file"
        },
        "160": {
            "description": "Error in adding guiAdmin to CContainer"
        },
        "161": {
            "description": "Error adding object to guiAdmin"
        },
        "162": {
            "description": "Error adding guiAdmin to CContainer"
        },
        "310": {
            "description": "Different number of file objects to compare"
        },
        "311": {
            "description": "Different number of XData objects to compare"
        },
        "312": {
            "description": "Different number of key-value pairs to compare"
        },
        "313": {
            "description": "Different values of key-value pair"
        },
        "314": {
            "description": "Error running comparison of object"
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
)
class CContainer(CData):
    """Base class for container CData classes."""

    def __init__(self, items=None, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)
        self._container_items = []
        self._data_order = []  # Track order of content items for dataOrder()
        if items is not None:
            for item in items:
                self.add_item(item)

    def add_item(self, item):
        """Add an item to the container."""
        if isinstance(item, CData):
            item.set_parent(self)
        self._container_items.append(item)

    def get_items(self):
        """Get all container items."""
        return self._container_items[:]

    def addContent(self, content_class, name: str, **kwargs):
        """Add a new content item to the container (old API compatibility).

        Args:
            content_class: The class type to instantiate
            name: Name for the new content item
            **kwargs: Additional arguments to pass to the constructor

        Returns:
            The newly created content object
        """
        # Create instance of the content class WITHOUT parent (to avoid setattr issues)
        if isinstance(content_class, type):
            new_obj = content_class(name=name, **kwargs)
        else:
            # If it's a string, try to resolve it
            from .fundamental_types import CInt, CFloat, CBoolean, CString, CList
            class_map = {
                'CInt': CInt,
                'CFloat': CFloat,
                'CBoolean': CBoolean,
                'CString': CString,
                'CList': CList,
                'CContainer': CContainer,
            }
            cls = class_map.get(content_class)
            if cls is None:
                raise ValueError(f"Unknown content class: {content_class}")
            new_obj = cls(name=name, **kwargs)

        # Add to container
        setattr(self, name, new_obj)

        # Explicitly set parent relationship (in case setattr doesn't handle it)
        if hasattr(new_obj, 'set_parent'):
            new_obj.set_parent(self)

        self._data_order.append(name)
        return new_obj

    def addObject(self, obj: CData, name: str = None):
        """Add an existing object to the container (old API compatibility).

        Args:
            obj: The CData object to add
            name: Optional name for the object (uses obj.name if not provided)

        Returns:
            The added object
        """
        if not isinstance(obj, CData):
            raise TypeError("Object must be a CData instance")

        obj_name = name if name is not None else getattr(obj, 'name', None)
        if not obj_name:
            raise ValueError("Object must have a name")

        # Set parent relationship
        obj.set_parent(self)
        obj.name = obj_name

        # Add to container
        setattr(self, obj_name, obj)
        if obj_name not in self._data_order:
            self._data_order.append(obj_name)

        return obj

    def deleteObject(self, name: str):
        """Delete an object from the container (old API compatibility).

        Args:
            name: Name of the object to delete
        """
        if not hasattr(self, name):
            raise AttributeError(f"Container has no object named '{name}'")

        obj = getattr(self, name)

        # Cleanup hierarchy if it's a CData object
        if isinstance(obj, HierarchicalObject):
            try:
                obj.destroy()
            except Exception:
                pass

        # Remove from container
        delattr(self, name)

        # Remove from data order
        if name in self._data_order:
            self._data_order.remove(name)

    def dataOrder(self) -> list:
        """Return the order of data items in this container (old API compatibility).

        Returns:
            List of names in the order they were added
        """
        # First check if there's a CONTENT_ORDER defined
        if hasattr(self, 'CONTENT_ORDER') and self.CONTENT_ORDER:
            return list(self.CONTENT_ORDER)

        # Otherwise return the dynamic order
        return list(self._data_order)

    def clear(self):
        """Remove all content items from the container (old API compatibility)."""
        # Get list of all content items
        items_to_remove = list(self._data_order)

        # Delete each one
        for name in items_to_remove:
            try:
                self.deleteObject(name)
            except Exception:
                pass

        # Clear the order list
        self._data_order.clear()

    def loadContentsFromXml(self, xml_file: str):
        """Load container contents from an XML file (old API compatibility).

        Args:
            xml_file: Path to the XML file to load
        """
        import xml.etree.ElementTree as ET
        from pathlib import Path

        xml_path = Path(xml_file)
        if not xml_path.exists():
            raise FileNotFoundError(f"XML file not found: {xml_file}")

        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Use setEtree to deserialize
        self.setEtree(root, ignore_missing=True)

    def saveContentsToXml(self, xml_file: str):
        """Save container contents to an XML file (old API compatibility).

        Args:
            xml_file: Path to the XML file to save
        """
        import xml.etree.ElementTree as ET
        from pathlib import Path

        # Get the XML element tree
        root = self.getEtree()

        # Create the tree and write to file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")  # Pretty print with 2-space indentation
        tree.write(xml_file, encoding='utf-8', xml_declaration=True)

    def loadDataFromXml(self, xml_file: str):
        """Alias for loadContentsFromXml (old API compatibility)."""
        self.loadContentsFromXml(xml_file)

    def saveDataToXml(self, xml_file: str):
        """Alias for saveContentsToXml (old API compatibility)."""
        self.saveContentsToXml(xml_file)

    # Priority 3: DEF and PARAMS file-specific methods
    def loadDefFile(self, filename: str):
        """Load container structure from a .def.xml file (old API compatibility).

        DEF files define the structure and qualifiers of a container,
        but not the actual data values.

        Args:
            filename: Path to the .def.xml file
        """
        # For now, use loadContentsFromXml
        # In future, this could use the DEF XML parser specifically
        self.loadContentsFromXml(filename)

    def saveDefFile(self, filename: str):
        """Save container structure to a .def.xml file (old API compatibility).

        DEF files define the structure and qualifiers of a container,
        but not the actual data values.

        Args:
            filename: Path to the .def.xml file
        """
        # Save structure with qualifiers but without data values
        self.saveContentsToXml(filename)

    def loadParamsFile(self, filename: str):
        """Load container data values from a .params.xml file (old API compatibility).

        PARAMS files contain the actual data values for a container
        whose structure is already defined.

        Args:
            filename: Path to the .params.xml file
        """
        # Load data values into existing structure
        self.loadDataFromXml(filename)

    def saveParamsFile(self, filename: str):
        """Save container data values to a .params.xml file (old API compatibility).

        PARAMS files contain the actual data values for a container.

        Args:
            filename: Path to the .params.xml file
        """
        # Save only data values, not structure
        self.saveDataToXml(filename)

    def __len__(self):
        """Return number of items in container."""
        return len(self._container_items)

    def __getitem__(self, index):
        """Get item by index."""
        return self._container_items[index]

    def __getattr__(self, name: str):
        """Allow attribute-style access to children by name.

        This enables accessing child objects like container.inputData
        instead of having to search through children manually.

        Args:
            name: Name of the child to access

        Returns:
            The child object with matching name

        Raises:
            AttributeError: If no child with that name exists
        """
        # Avoid infinite recursion for internal attributes
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Check children from HierarchicalObject hierarchy
        # Use object.__getattribute__ to avoid recursion
        try:
            # Get the 'children' method from HierarchicalObject
            children_method = object.__getattribute__(self, 'children')
            children_list = children_method()  # Call the method
            for child in children_list:
                # Skip destroyed children
                if hasattr(child, 'state'):
                    from .hierarchy_system import ObjectState
                    if child.state == ObjectState.DESTROYED:
                        continue
                # Check if name matches
                if hasattr(child, 'name') and child.name == name:
                    return child
        except (AttributeError, TypeError):
            pass

        # Also check _container_items (in case items were added via add_item)
        try:
            container_items = object.__getattribute__(self, '_container_items')
            for item in container_items:
                if hasattr(item, 'name') and item.name == name:
                    return item
        except (AttributeError, TypeError):
            pass

        # Not found - raise AttributeError
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

