"""
CData - Base class for all CCP4i2 data objects.

This is the fundamental base class that provides:
- Hierarchical object relationships
- Value state tracking (NOT_SET, DEFAULT, EXPLICITLY_SET)
- Smart assignment (preserves CData objects, updates .value for value types)
- Metadata integration
- Qualifier system
"""

import sys
import os
from typing import Any, Dict
from enum import Enum, auto

from .hierarchy_system import HierarchicalObject


class ValueState(Enum):
    """States that a value can be in."""
    NOT_SET = auto()  # Value has never been explicitly set
    DEFAULT = auto()  # Value is using a default from qualifiers
    EXPLICITLY_SET = auto()  # Value has been explicitly assigned


# Import decorator after ValueState definition
from .class_metadata import cdata_class


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
        # Flag to skip validation (used during .def.xml parsing)
        self._skip_validation: bool = False

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
        """Set attributes from dict, unset others. Uses smart assignment to avoid overwriting CData objects."""
        # Get all fields (metadata-aware)
        metadata = None
        try:
            from .metadata_system import MetadataRegistry
            metadata = MetadataRegistry.get_class_metadata(self.__class__.__name__)
        except Exception:
            pass

        if metadata:
            all_fields = list(metadata.fields.keys())
        else:
            all_fields = [
                k for k in self.__dict__
                if not k.startswith('_')
                and k not in ['parent', 'name', 'children', 'signals']
            ]

        # Smart assignment for fields
        for k in all_fields:
            if k in values:
                current = getattr(self, k, None)
                new_value = values[k]
                # Smart assignment: if current is a CData value type, update its value
                if hasattr(current, 'value') and not isinstance(new_value, type(current)):
                    current.value = new_value
                else:
                    setattr(self, k, new_value)
                self._value_states[k] = ValueState.EXPLICITLY_SET
            else:
                # Unset fields not in values
                if hasattr(self, k):
                    self.unSet(k)

        # Mark the object itself as set when values are provided
        # This is important for legacy code that checks `object.isSet()`
        if values and hasattr(self, '_value_states'):
            self._value_states['value'] = ValueState.EXPLICITLY_SET

    def update(self, values: dict):
        """Update only provided attributes. Uses smart assignment to avoid overwriting CData objects."""
        for k, v in values.items():
            current = getattr(self, k, None)
            # Smart assignment: if current is a CData value type, update its value
            if hasattr(current, 'value') and not isinstance(v, type(current)):
                current.value = v
            else:
                setattr(self, k, v)

            # Mark as explicitly set
            if hasattr(self, '_value_states'):
                self._value_states[k] = ValueState.EXPLICITLY_SET

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

    def _setup_hierarchy_for_value(self, key: str, value: Any):
        """Set up hierarchical relationships for attribute values.

        Only sets parent if not already set, respecting explicit parent assignments.
        Only sets name if not already set.
        """
        if isinstance(value, CData):
            # Only set parent if not already set (respect explicit parent assignment)
            if value.parent is None:
                value.set_parent(self)
            # Only set name if not already set
            if not value.name:
                value.name = key
        elif isinstance(value, list):
            # Handle list of CData objects
            for i, item in enumerate(value):
                if isinstance(item, CData):
                    # Only set parent if not already set
                    if item.parent is None:
                        item.set_parent(self)
                    if not item.name:
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

        # DEBUG: Print all contentFlag assignments
        if name == 'contentFlag':
            import traceback
            print(f"\n[SETATTR] {self.__class__.__name__}.{name} = {value} (type: {type(value).__name__})")
            print(f"  existing: {existing_attr} (type: {type(existing_attr).__name__})")
            print(f"  Stack:")
            for line in traceback.format_stack()[-4:-1]:
                print(f"    {line.strip()}")
            print()

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
            if name in ['contentFlag', 'subType']:  # DEBUG
                print(f"[DEBUG] Branch: CData to CData for {name}")  # DEBUG
            existing_attr._smart_assign_from_cdata(value)
            # Mark as explicitly set since we're assigning a new value
            if hasattr(self, "_value_states"):
                self._value_states[name] = ValueState.EXPLICITLY_SET
            return  # Don't replace the object, just update it

        elif (
            hasattr(existing_attr, 'setFullPath')
            and callable(getattr(existing_attr, 'setFullPath'))
            and isinstance(value, str)
        ):
            # Special case: Assigning a string path to an existing CDataFile
            # e.g., task.container.inputData.HKLIN = "/path/to/file.mtz"
            # Use duck typing to avoid circular import
            existing_attr.setFullPath(value)
            # Mark as explicitly set
            if hasattr(self, "_value_states"):
                self._value_states[name] = ValueState.EXPLICITLY_SET
            return  # Don't replace the object, just update its path

        elif (
            existing_attr is not None and isinstance(existing_attr, CData)
            and existing_attr._is_value_type()
        ):
            if name in ['contentFlag', 'subType']:  # DEBUG
                print(f"[DEBUG] Branch: Value type smart assign for {name}")  # DEBUG
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
                    if name in ['contentFlag', 'subType']:  # DEBUG
                        print(f"[SMART ASSIGN] Updating {name}.value = {value}, keeping {type(existing_attr).__name__}")  # DEBUG
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

