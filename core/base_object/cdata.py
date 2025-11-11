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
import logging

from .hierarchy_system import HierarchicalObject

# Configure logger
logger = logging.getLogger(__name__)


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
        logger.debug("Initializing CData instance of type %s with name '%s'", self.__class__.__name__, name)
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
        # Qualifiers - store in _qualifiers (private) to leave qualifiers() method free for legacy API
        if hasattr(cls, '_class_qualifiers'):
            class_qualifiers = getattr(cls, '_class_qualifiers')
            logger.debug("%s._class_qualifiers type: %s, value: %s", cls.__name__, type(class_qualifiers), class_qualifiers)

            # Handle case where qualifiers is a dict-like object
            if isinstance(class_qualifiers, dict):
                self._qualifiers = dict(class_qualifiers)
            elif hasattr(class_qualifiers, 'items') and callable(getattr(class_qualifiers, 'items', None)):
                try:
                    self._qualifiers = dict(class_qualifiers.items())
                except (AttributeError, TypeError) as e:
                    logger.error("Error calling .items() on _class_qualifiers for %s: %s (type: %s)", cls.__name__, e, type(class_qualifiers))
                    self._qualifiers = {}
            else:
                # Not a dict and doesn't have .items() - set to empty dict
                logger.warning("Class-level _class_qualifiers for %s is not dict-like: %s, setting to empty dict", cls.__name__, type(class_qualifiers))
                self._qualifiers = {}
        else:
            self._qualifiers = {}
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
                    self._qualifiers = kwargs.pop(meta_key)
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
        if hasattr(self, '_qualifiers') and self._qualifiers is not None:
            return self._qualifiers.get(key, default)
        return default

    def set_qualifier(self, key, value):
        """Set or override a qualifier value for this instance."""
        if not hasattr(self, '_qualifiers') or self._qualifiers is None:
            self._qualifiers = {}
        self._qualifiers[key] = value

    def qualifiers(self, key=None, default=None):
        """
        Legacy compatibility method for getting qualifiers.

        Provided for backward compatibility with legacy ccp4i2 plugin code
        that calls qualifiers('key') instead of get_qualifier('key').

        Args:
            key: Optional qualifier key to get. If None, returns all qualifiers dict.
            default: Default value if key not found

        Returns:
            If key is provided, returns the qualifier value (or default).
            If key is None, returns the _qualifiers dict.

        Example:
            # Legacy code pattern:
            label = obj.qualifiers('guiLabel')

            # All qualifiers:
            all_quals = obj.qualifiers()
        """
        if key is None:
            # Return all qualifiers
            return getattr(self, '_qualifiers', {})
        else:
            # Return specific qualifier
            return self.get_qualifier(key, default)

    def setQualifier(self, key, value):
        """
        Legacy compatibility alias for set_qualifier().

        Provided for backward compatibility with legacy ccp4i2 plugin code.
        New code should use set_qualifier() instead.
        """
        return self.set_qualifier(key, value)

    def setQualifiers(self, qualifiers_dict):
        """
        Set multiple qualifiers from a dictionary.

        Provided for backward compatibility with legacy ccp4i2 plugin code
        that calls setQualifiers() with a dictionary of qualifier key-value pairs.

        Args:
            qualifiers_dict: Dictionary of qualifier key-value pairs to set

        Example:
            obj.setQualifiers({'listMinLength': 0, 'listMaxLength': 10})
        """
        if not isinstance(qualifiers_dict, dict):
            raise TypeError(f"setQualifiers() expects a dict, got {type(qualifiers_dict).__name__}")

        for key, value in qualifiers_dict.items():
            self.set_qualifier(key, value)

    def set(self, values):
        """
        Set attributes from dict or CData object, unset others.
        Uses smart assignment to avoid overwriting CData objects.

        Args:
            values: Either a dict of attributes, or another CData object to copy from
        """
        # If values is a CData object, extract its attributes as a dict
        if isinstance(values, CData):
            source_obj = values  # Keep reference to original CData object
            if hasattr(values, 'get') and callable(values.get):
                values_dict = values.get()
                # Filter to only include fields that are explicitly set in the source object
                # This prevents validation errors when copying unset fields with constraints
                values = {}
                for k, v in values_dict.items():
                    source_field = getattr(source_obj, k, None)
                    # Only include if the field is set in the source
                    if hasattr(source_field, 'isSet') and callable(source_field.isSet):
                        if source_field.isSet():
                            values[k] = v
                    else:
                        # For non-CData fields, include them
                        values[k] = v
            else:
                # Fallback: create dict from CData attributes
                values = {
                    k: getattr(values, k)
                    for k in dir(values)
                    if not k.startswith('_') and not callable(getattr(values, k))
                    and k not in ['parent', 'name', 'children', 'signals']
                }

        # Ensure values is a dict at this point
        if not isinstance(values, dict):
            raise TypeError(f"set() expects dict or CData, got {type(values).__name__}")

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
                # For CContainer types, DON'T unset fields that aren't in the source
                # This allows merging data from a source that has fewer fields
                # (e.g., phaser_pipeline.inputData → phaser_MR_AUTO.inputData)
                # For non-container types, unset fields not in values (original behavior)
                from .ccontainer import CContainer
                if not isinstance(self, CContainer):
                    if hasattr(self, k):
                        self.unSet(k)

        # Mark the object itself as set when values are provided
        # This is important for legacy code that checks `object.isSet()`
        if values and hasattr(self, '_value_states'):
            self._value_states['value'] = ValueState.EXPLICITLY_SET

    def get(self, child_name=None):
        """Get child by name or all attributes as dict. Compatible with old CCP4i2 API.

        If child_name is provided, returns the child object with that name.
        Otherwise, returns a dict of all CData attributes and their values.

        Args:
            child_name: Optional name of child to retrieve

        Returns:
            If child_name provided: The child object with that name
            If child_name is None: Dict of attribute names to values
        """
        # Legacy API: get(childName) retrieves child by name
        if child_name is not None:
            return getattr(self, child_name, None)

        # Modern API: get() returns dict representation
        result = {}

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
                and k not in ['parent', 'name', 'children', 'signals', 'content']
            ]

        for field_name in all_fields:
            if not hasattr(self, field_name):
                continue

            value = getattr(self, field_name)

            # Handle CData objects recursively
            if isinstance(value, CData):
                # If it has a value attribute, use that
                if hasattr(value, 'value'):
                    result[field_name] = value.value
                else:
                    # Otherwise recurse
                    result[field_name] = value.get()
            else:
                result[field_name] = value

        return result

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
            if hasattr(current, 'objectName') and current.objectName():
                path_parts.insert(0, current.objectName())
            # parent is now a method, not a property - must call it
            current = current.parent() if hasattr(current, 'parent') and callable(current.parent) else None

        return ".".join(path_parts) if path_parts else ""

    def objectName(self) -> str:
        """Return the name of this object from the HierarchicalObject hierarchy.

        This returns the hierarchical object name (stored in _name), NOT any
        CData 'name' attribute that may be stored in __dict__['name'].

        Returns:
            The hierarchical object's name or empty string
        """
        # Access _name directly to avoid collision with CData 'name' attributes
        return getattr(self, '_name', '')

    @property
    def CONTENTS(self):
        """
        Get list of child CData objects or attributes.

        For CContainer: Returns list of child CData objects (children)
        For other CData types: Returns list of attribute names that are CData objects

        This provides a unified interface for navigating the CData hierarchy,
        similar to legacy CCP4i2's CONTENTS pattern.

        Returns:
            List of CData objects (for CContainer) or list of attribute names (for other CData)
        """
        # Import CContainer here to avoid circular imports
        from .ccontainer import CContainer

        # For CContainer, return actual children objects
        if isinstance(self, CContainer):
            return list(self.get_children())

        # For other CData types, return list of CData attribute names
        cdata_attributes = []

        # Try metadata-aware approach first
        try:
            from .metadata_system import MetadataRegistry
            metadata = MetadataRegistry.get_class_metadata(self.__class__.__name__)
            if metadata:
                for field_name, field_meta in metadata.fields.items():
                    if hasattr(self, field_name):
                        value = getattr(self, field_name)
                        if isinstance(value, CData):
                            cdata_attributes.append(field_name)
                return cdata_attributes
        except Exception:
            pass

        # Fallback: inspect actual attributes
        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue
            if attr_name in ['parent', 'name', 'children', 'signals', 'content', 'CONTENTS']:
                continue
            try:
                value = getattr(self, attr_name)
                if isinstance(value, CData):
                    cdata_attributes.append(attr_name)
            except Exception:
                continue

        return cdata_attributes

    def isSet(self, field_name: str = None, allowUndefined: bool = False,
              allowDefault: bool = False, allSet: bool = True) -> bool:
        """Check if a field has been explicitly set.

        Args:
            field_name: Name of the field to check. If None, checks the 'value' attribute.
            allowUndefined: If True, allow None/undefined values to be considered "set"
                          if the qualifier 'allowUndefined' is True
            allowDefault: If False, consider values that equal the default as "not set"
            allSet: For container types - if True, all children must be set;
                   if False, at least one child must be set

        Returns:
            True if field has been set according to the criteria, False otherwise
        """
        if field_name is None:
            # For container objects without a 'value' attribute, check if ANY child is set
            if not hasattr(self, 'value'):
                # Check if any child attribute is set
                for attr_name, state in self._value_states.items():
                    if state == ValueState.EXPLICITLY_SET:
                        return True
                    if state == ValueState.DEFAULT and allowDefault:
                        return True

                # Also check CData children recursively (e.g., CList, nested CContainer)
                # This handles cases like container.UNMERGEDFILES.append(item)
                # where UNMERGEDFILES itself is set but not explicitly assigned
                for attr_name in dir(self):
                    if attr_name.startswith('_'):
                        continue
                    try:
                        attr = getattr(self, attr_name)
                        if isinstance(attr, CData) and hasattr(attr, 'isSet'):
                            if attr.isSet(field_name=None, allowUndefined=allowUndefined,
                                        allowDefault=allowDefault, allSet=allSet):
                                return True
                    except Exception:
                        continue

                return False
            field_name = "value"

        # If the attribute exists and is a CData object, delegate to it
        # This includes CDataFile objects which have special isSet() logic that checks baseName
        if hasattr(self, field_name):
            attr = getattr(self, field_name, None)
            if isinstance(attr, CData) and hasattr(attr, 'isSet'):
                # Delegate to the child object to check if it's set
                return attr.isSet(field_name=None, allowUndefined=allowUndefined,
                                allowDefault=allowDefault, allSet=allSet)

        # Check basic set state from parent's tracking
        state = self._value_states.get(field_name, ValueState.NOT_SET)

        # If checking for explicit set only
        if state == ValueState.NOT_SET:
            # Special handling for allowUndefined
            if allowUndefined and self.get_qualifier('allowUndefined', False):
                return True
            return False

        # If state is DEFAULT, check if we allow defaults
        if state == ValueState.DEFAULT:
            if not allowDefault:
                return False

        # Check the actual value
        if hasattr(self, field_name):
            value = getattr(self, field_name, None)

            # Handle None values
            if value is None or value is NotImplemented:
                if not allowUndefined or not self.get_qualifier('allowUndefined', False):
                    return False
                return True

            # Check if value equals default (if allowDefault is False)
            if not allowDefault:
                default = self.get_qualifier('default')
                if default is not None and value == default:
                    return False

        return True

    def unSet(self, field_name: str = 'value'):
        """Return a field to its not-set state.

        Args:
            field_name: Name of the field to unset (defaults to 'value' for fundamental types)
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

    def isDefault(self, field_name: str = 'value') -> bool:
        """Check if a field is at its default value.

        Args:
            field_name: Name of the field to check (default: 'value')

        Returns:
            True if the field is at its default value, False otherwise
        """
        return self.getValueState(field_name) == ValueState.DEFAULT

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
        if hasattr(self, '_qualifiers') and self._qualifiers:
            # Basic validation is done here
            # Subclasses will add their own validation
            pass

        return report

    def dataOrder(self) -> list:
        """Return the order of child data items.

        This method provides compatibility with the legacy CCP4i2 API where
        dataOrder() was expected to exist on all CData objects.

        For fundamental types (CInt, CFloat, CString, CBoolean), this returns
        an empty list since they have no child data items.

        Container types (CContainer, CList) override this method to return
        their child item names or indices.

        Returns:
            Empty list for base CData and fundamental types
        """
        return []

    def getEtree(self, name: str = None, excludeUnset: bool = False):
        """Serialize this object to an XML ElementTree element.

        Args:
            name: Optional name for the XML element (uses self.name if not provided)
            excludeUnset: If True, only serialize fields that have been explicitly set

        Returns:
            xml.etree.ElementTree.Element representing this object
        """
        import xml.etree.ElementTree as ET

        # Use objectName() to get hierarchical object name, not CData 'name' attribute
        element_name = name if name is not None else (self.objectName() if hasattr(self, 'objectName') else 'data')
        elem = ET.Element(element_name)

        # For simple value types, store the value as text
        if hasattr(self, 'value'):
            value = getattr(self, 'value')

            if value is not None:
                # Check if we should exclude this based on set state
                if excludeUnset and hasattr(self, 'isSet'):
                    # Use allowDefault=False to exclude default values
                    if not self.isSet('value', allowDefault=False):
                        return elem  # Return empty element for unset values
                elem.text = str(value)

        # For containers and complex types, serialize children
        from core.base_object.signal_system import Signal
        for attr_name, attr_value in self.__dict__.items():
            if attr_name.startswith('_') or attr_name in ['parent', 'children', 'signals']:
                continue
            # Skip Signal objects (child_added, child_removed, etc.)
            if isinstance(attr_value, Signal):
                continue
            # No special handling needed for 'name' anymore - HierarchicalObject uses '_name' internally
            # ONLY serialize CData objects - plain Python values should not be serialized unless wrapped
            if isinstance(attr_value, CData):
                # Check if child should be excluded
                if excludeUnset and hasattr(attr_value, 'isSet'):
                    # For CData objects, check if they have any set values
                    if not attr_value.isSet(allowDefault=False):
                        continue  # Skip unset children

                child_elem = attr_value.getEtree(attr_name, excludeUnset=excludeUnset)

                # Only append if the child element has content
                if excludeUnset:
                    # Check if element has text or children
                    if child_elem.text or len(child_elem) > 0:
                        elem.append(child_elem)
                else:
                    elem.append(child_elem)

        # Special handling for CContainer - also serialize _container_items
        if hasattr(self, '_container_items'):
            for item in self._container_items:
                if isinstance(item, CData):
                    # Check if item should be excluded
                    if excludeUnset and hasattr(item, 'isSet'):
                        if not item.isSet(allowDefault=False):
                            continue  # Skip unset items

                    # Use class name as the tag for list items (e.g., "CAsuContentSeq")
                    item_name = item.__class__.__name__
                    child_elem = item.getEtree(item_name, excludeUnset=excludeUnset)
                    # Only append if the child element has content
                    if excludeUnset:
                        if child_elem.text or len(child_elem) > 0:
                            elem.append(child_elem)
                    else:
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
            # Temporarily disable validation during deserialization
            # This prevents validation errors when loading values from XML that may
            # not meet current min/max constraints but were valid when saved
            old_skip_validation = getattr(self, '_skip_validation', False)
            self._skip_validation = True
            try:
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
            finally:
                # Restore previous validation state
                self._skip_validation = old_skip_validation

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

        if hasattr(self, '_qualifiers') and self._qualifiers:
            for key, value in self._qualifiers.items():
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
        """Handle smart assignment from another CData object.

        For containers, this merges children from source into self.
        For value types, this copies the value.
        """
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
            # Complex type assignment (like containers and lists)
            # For CList types, copy items from source to self
            from .fundamental_types import CList
            if isinstance(self, CList) and isinstance(source, CList):
                # Clear existing items
                self.clear()
                # Copy items from source to self
                for item in source:
                    self.append(item)
                return

            # For containers, merge attributes from source instead of replacing
            from .ccontainer import CContainer
            if isinstance(self, CContainer) and isinstance(source, CContainer):
                # Container merging: iterate over source's public attributes (those added via setattr)
                # These may not be in children() yet if they're being parsed
                for key in dir(source):
                    if not key.startswith("_") and key[0].isupper():  # Skip private and methods
                        try:
                            child = getattr(source, key)
                            # Only copy CData objects (skip methods)
                            if isinstance(child, CData):
                                # Check if we already have an attribute with this name
                                if hasattr(self, key):
                                    # Attribute already exists - recursively merge if both are containers
                                    existing_child = getattr(self, key)
                                    if isinstance(existing_child, CContainer) and isinstance(child, CContainer):
                                        existing_child._smart_assign_from_cdata(child)
                                    else:
                                        # Not containers - replace with new one
                                        setattr(self, key, child)
                                else:
                                    # New attribute - add it
                                    # Need to reparent the child from source to self
                                    child.set_parent(self)
                                    setattr(self, key, child)
                        except:
                            # Skip attributes that can't be accessed
                            pass
            else:
                # Non-container complex type: copy all attributes
                for key, value in source.__dict__.items():
                    # Note: 'name' is NOT in this filter list - it's a regular CData attribute that should be copied
                    # HierarchicalObject's hierarchical name is stored separately in '_name'
                    if not key.startswith("_") and key not in [
                        "parent",
                        "children",
                        "signals",
                    ]:
                        setattr(self, key, value)

    def _setup_hierarchy_for_value(self, key: str, value: Any):
        """Set up hierarchical relationships for attribute values.

        Only sets parent if not already set, respecting explicit parent assignments.
        Only sets name if not already set.
        """
        if isinstance(value, CData):
            # Only set parent if not already set (respect explicit parent assignment)
            if value.parent() is None:
                value.set_parent(self)
            # Only set hierarchical name if not already set
            if not value._name:
                value._name = key
        elif isinstance(value, list):
            # Handle list of CData objects
            for i, item in enumerate(value):
                if isinstance(item, CData):
                    # Only set parent if not already set
                    if item.parent() is None:
                        item.set_parent(self)
                    if not item._name:
                        item._name = f"{key}[{i}]"

    def __setattr__(self, name: str, value: Any):
        """Override setattr to handle smart assignment and hierarchical relationships."""

        # Allow setting internal attributes normally during initialization
        # Note: 'name' is NOT in this list - it's a regular CData attribute that uses smart assignment
        # HierarchicalObject's hierarchical name is stored separately in '_name'
        if (
            name.startswith("_")
            or name in ["parent", "children", "signals"]
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
        # Since HierarchicalObject uses _name (not name), there's no collision with CData 'name' attributes
        existing_attr = getattr(self, name, None)

        # DEBUG: Print all contentFlag assignments
        if name == 'contentFlag':
            import traceback
            logger.debug(
                "[SETATTR] %s.%s = %s (type: %s)\n  existing: %s (type: %s)\n  Stack: %s",
                self.__class__.__name__, name, value, type(value).__name__,
                existing_attr, type(existing_attr).__name__,
                ''.join(traceback.format_stack()[-4:-1])
            )

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
            # Only perform assignment if the source value is actually set
            # This prevents copying unset/default values which would mark them as explicitly set
            if hasattr(value, 'isSet') and not value.isSet():
                # Source value is not set - skip the assignment
                # This prevents legacy code like: obj.FRAC = source.FREER_FRACTION
                # from marking FRAC as set when FREER_FRACTION is just a default
                return

            if name in ['contentFlag', 'subType']:  # DEBUG
                logger.debug("Branch: CData to CData for %s", name)  # DEBUG
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
                logger.debug("Branch: Value type smart assign for %s", name)  # DEBUG
            # Primitive value assignment to existing CData value type
            # e.g., ctrl.NCYCLES = 25 where ctrl.NCYCLES is a CInt
            if isinstance(value, (int, float, str, bool)):
                # Check type compatibility and perform conversions if needed
                type_compatible = False
                converted_value = value
                if hasattr(existing_attr, "value"):
                    # Import types locally to avoid circular import
                    from .fundamental_types import CInt, CFloat, CBoolean
                    try:
                        from .fundamental_types import CString
                    except ImportError:
                        CString = None

                    # Handle CInt: accept int or string convertible to int
                    if isinstance(existing_attr, CInt):
                        if isinstance(value, int):
                            type_compatible = True
                        elif isinstance(value, str):
                            # Legacy code often uses str(int_value) - convert back
                            try:
                                converted_value = int(value)
                                type_compatible = True
                            except (ValueError, TypeError):
                                pass

                    # Handle CFloat: accept float, int, or string convertible to float
                    elif isinstance(existing_attr, CFloat):
                        if isinstance(value, (int, float)):
                            type_compatible = True
                        elif isinstance(value, str):
                            try:
                                converted_value = float(value)
                                type_compatible = True
                            except (ValueError, TypeError):
                                pass

                    # Handle CBoolean: accept bool or string convertible to bool
                    elif isinstance(existing_attr, CBoolean):
                        if isinstance(value, bool):
                            type_compatible = True
                        elif isinstance(value, str):
                            # Handle common boolean string representations
                            if value.lower() in ('true', 'yes', '1'):
                                converted_value = True
                                type_compatible = True
                            elif value.lower() in ('false', 'no', '0'):
                                converted_value = False
                                type_compatible = True

                    # Handle CString: always accept strings
                    elif CString is not None and isinstance(existing_attr, CString) and isinstance(value, str):
                        type_compatible = True

                if type_compatible:
                    # Update the value attribute of the existing CData object
                    if name in ['contentFlag', 'subType']:  # DEBUG
                        logger.debug("[SMART ASSIGN] Updating %s.value = %s, keeping %s", name, converted_value, type(existing_attr).__name__)  # DEBUG
                    existing_attr.value = converted_value
                    # Mark as explicitly set (no longer needed with delegation, but keeping for non-CData attributes)
                    if hasattr(self, "_value_states"):
                        self._value_states[name] = ValueState.EXPLICITLY_SET
                    return  # Don't replace the object, just update its value

        # For new attributes or non-smart assignment, handle hierarchy and set normally
        self._setup_hierarchy_for_value(name, value)
        super().__setattr__(name, value)
        # Track that this value has been explicitly set (unless it's internal)
        # IMPORTANT: Don't mark 'value' attribute here for types with @property setters
        # (CInt, CFloat, CBoolean) because those setters handle state tracking themselves.
        # This prevents parameters without defaults from being incorrectly marked as EXPLICITLY_SET
        # during .def.xml loading and container merging operations.
        # However, DO track for CString which doesn't use a @property setter.
        from .fundamental_types import CInt, CFloat, CBoolean
        has_value_property = isinstance(self, (CInt, CFloat, CBoolean))
        skip_value_tracking = (name == "value" and has_value_property)

        # Exclusion list for value state tracking
        # Note: 'name' is NOT excluded - HierarchicalObject uses _name, so no collision
        exclusion_list = ["parent", "children", "signals"]

        # DEBUG: Track name assignments
        if name == "name":
            print(f"[SETATTR DEBUG] Setting {name} on {self.__class__.__name__}")
            print(f"[SETATTR DEBUG]   has _value_states: {hasattr(self, '_value_states')}")
            print(f"[SETATTR DEBUG]   skip_value_tracking: {skip_value_tracking}")
            print(f"[SETATTR DEBUG]   name in exclusion_list: {name in exclusion_list}")

        if (hasattr(self, "_value_states") and not name.startswith("_")
            and name not in exclusion_list
            and not skip_value_tracking):
            self._value_states[name] = ValueState.EXPLICITLY_SET
            if name == "name":
                print(f"[SETATTR DEBUG]   MARKED AS EXPLICITLY_SET!")

    def __getattr__(self, name: str):
        """Auto-create metadata-defined attributes when accessed.

        This is called when normal attribute lookup fails. If the attribute
        is defined in metadata but hasn't been instantiated yet, create it.
        """
        # Avoid infinite recursion - only process if object is fully initialized
        if name.startswith("_") or not hasattr(self, "_hierarchy_initialized"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Check if this attribute is defined in metadata
        metadata = getattr(self.__class__, "_metadata", None)
        if metadata and name in metadata.attributes:
            # Auto-create the attribute from metadata
            from .class_metadata import MetadataAttributeFactory
            attr_def = metadata.attributes[name]
            attr_obj = MetadataAttributeFactory.create_attribute(name, attr_def, self)

            # Store it in __dict__ so subsequent access finds it directly
            self.__dict__[name] = attr_obj

            # Mark as NOT_SET initially (will be marked EXPLICITLY_SET when assigned)
            if hasattr(self, "_value_states"):
                self._value_states[name] = ValueState.NOT_SET

            return attr_obj

        # Not a metadata attribute - raise AttributeError
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

