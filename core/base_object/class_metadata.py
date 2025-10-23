"""Decorator-based metadata system for CData classes.

This module provides decorators and utilities to embed metadata directly
in class definitions, making the system more maintainable than external JSON files.
"""

from typing import Dict, Any, Optional, Type, List
from dataclasses import dataclass, field
from enum import Enum


class AttributeType(Enum):
    """Types of attributes that can be created.

    Only fundamental types (CInt, CFloat, CBoolean, CString) have their own enum values.
    All other types (CFilePath, CUUID, CList, etc.) should use CUSTOM with custom_class parameter.
    """

    INT = "CInt"
    FLOAT = "CFloat"
    BOOLEAN = "CBoolean"
    STRING = "CString"
    CUSTOM = "Custom"


@dataclass
class AttributeDefinition:
    """Definition of a class attribute.

    All attribute constraints (min/max/default/enumerators/etc.) should be
    defined in the class-level qualifiers, not here. This class only defines
    what TYPE of attribute to create.
    """

    attr_type: AttributeType
    custom_class: Optional[str] = None  # For AttributeType.CUSTOM types


@dataclass
class ClassMetadata:
    """Complete metadata for a CData class."""

    attributes: Dict[str, AttributeDefinition] = field(default_factory=dict)
    qualifiers: Dict[str, Any] = field(default_factory=dict)
    error_codes: Dict[int, str] = field(default_factory=dict)
    docstring: Optional[str] = None
    file_extensions: Optional[List[str]] = None
    mime_type: Optional[str] = None
    gui_label: Optional[str] = None
    contents_order: Optional[List[str]] = None
    qualifiers_order: Optional[List[str]] = None
    qualifiers_definition: Optional[Dict[str, Any]] = None


# Global registry of class metadata
_CLASS_METADATA_REGISTRY: Dict[str, ClassMetadata] = {}


def attribute(attr_type: AttributeType, custom_class: Optional[str] = None) -> AttributeDefinition:
    """Helper function to create attribute definitions.

    All attribute constraints (min/max/default/enumerators/etc.) should be
    defined in class-level qualifiers, not here.

    Args:
        attr_type: The type of attribute (INT, FLOAT, STRING, CUSTOM, etc.)
        custom_class: For AttributeType.CUSTOM, the class name to instantiate

    Returns:
        AttributeDefinition instance

    Example:
        project = attribute(AttributeType.CUSTOM, custom_class="CProjectId")
        label = attribute(AttributeType.CUSTOM, custom_class="COneWord")
        items = attribute(AttributeType.CUSTOM, custom_class="CList")
    """
    return AttributeDefinition(attr_type=attr_type, custom_class=custom_class)


def cdata_class(
    attributes: Optional[Dict[str, AttributeDefinition]] = None,
    qualifiers: Optional[Dict[str, Any]] = None,
    error_codes: Optional[Dict[int, str]] = None,
    file_extensions: Optional[List[str]] = None,
    mime_type: Optional[str] = None,
    gui_label: Optional[str] = None,
    contents_order: Optional[List[str]] = None,
    qualifiers_order: Optional[List[str]] = None,
    qualifiers_definition: Optional[Dict[str, Any]] = None,
):
    """Class decorator to add metadata to CData classes.

    Args:
        attributes: Dictionary of attribute name -> AttributeDefinition
        qualifiers: Dictionary of class qualifiers
        error_codes: Dictionary of error code -> message
        file_extensions: List of supported file extensions
        mime_type: MIME type for file classes
        gui_label: Label for GUI display
        contents_order: List specifying display order of attributes in UI
        qualifiers_order: List specifying display order of qualifiers
        qualifiers_definition: Dictionary of qualifier type definitions

    Example:
        @cdata_class(
            attributes={
                'project': attribute(AttributeType.CUSTOM, custom_class="CProjectId"),
                'baseName': attribute(AttributeType.CUSTOM, custom_class="CFilePath"),
                'size': attribute(AttributeType.INT, default=0, min_value=0)
            },
            file_extensions=['dat', 'txt'],
            mime_type='text/plain'
        )
        class CDataFile(CData):
            '''A data file with embedded metadata.'''
            pass
    """

    def decorator(cls: Type) -> Type:
        # Create metadata object
        metadata = ClassMetadata(
            attributes=attributes or {},
            qualifiers=qualifiers or {},
            error_codes=error_codes or {},
            docstring=cls.__doc__,
            file_extensions=file_extensions,
            mime_type=mime_type,
            gui_label=gui_label,
            contents_order=contents_order,
            qualifiers_order=qualifiers_order,
            qualifiers_definition=qualifiers_definition,
        )

        # Store in global registry
        _CLASS_METADATA_REGISTRY[cls.__name__] = metadata

        # Store as class attribute for easy access
        cls._metadata = metadata

        return cls

    return decorator


def get_class_metadata(class_name: str) -> Optional[ClassMetadata]:
    """Get metadata for a class by name.

    Args:
        class_name: Name of the class

    Returns:
        ClassMetadata instance or None if not found
    """
    return _CLASS_METADATA_REGISTRY.get(class_name)


def get_class_metadata_by_type(cls: Type) -> Optional[ClassMetadata]:
    """Get metadata for a class by type.

    Args:
        cls: The class type

    Returns:
        ClassMetadata instance or None if not found
    """
    return getattr(cls, "_metadata", None)


class MetadataAttributeFactory:
    """Factory for creating attribute objects from metadata definitions."""

    @classmethod
    def create_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj
    ) -> Any:
        """Create an attribute object from definition, sourcing qualifiers from class-level metadata."""
        from .base_classes import ValueState

        # Get class-level qualifiers from parent_obj's class metadata
        qualifiers = {}
        meta = getattr(parent_obj.__class__, '_metadata', None)
        if meta and hasattr(meta, 'qualifiers') and meta.qualifiers:
            qualifiers = meta.qualifiers

        # Helper to get qualifier value, fallback to attribute definition
        def q(key, default=None):
            return qualifiers.get(key, getattr(attr_def, key, default))

        # Patch: pass qualifiers to attribute creation
        if attr_def.attr_type == AttributeType.INT:
            return cls._create_int_attribute(name, attr_def, parent_obj, qualifiers)
        elif attr_def.attr_type == AttributeType.FLOAT:
            return cls._create_float_attribute(name, attr_def, parent_obj, qualifiers)
        elif attr_def.attr_type == AttributeType.BOOLEAN:
            return cls._create_boolean_attribute(name, attr_def, parent_obj, qualifiers)
        elif attr_def.attr_type == AttributeType.STRING:
            return cls._create_string_attribute(name, attr_def, parent_obj, qualifiers)
        elif attr_def.attr_type == AttributeType.CUSTOM:
            return cls._create_custom_attribute(name, attr_def, parent_obj, qualifiers)
        else:
            raise ValueError(f"Unknown attribute type: {attr_def.attr_type}")

    @classmethod
    def _create_int_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj, qualifiers
    ):
        """Create an integer attribute, sourcing min/max/default from qualifiers."""
        from .base_classes import CData, ValueState

        attr = CData(parent=parent_obj, name=name)

        # Set default value from qualifiers
        default_value = qualifiers.get('default', 0)
        attr.__dict__["value"] = default_value

        # Create methods
        def set_value(val):
            min_value = qualifiers.get('min')
            max_value = qualifiers.get('max')
            if min_value is not None and val < min_value:
                raise ValueError(
                    f"{name} value {val} is below minimum {min_value}"
                )
            if max_value is not None and val > max_value:
                raise ValueError(
                    f"{name} value {val} is above maximum {max_value}"
                )

            attr.__dict__["value"] = int(val)
            if hasattr(parent_obj, "_value_states"):
                parent_obj._value_states[name] = ValueState.EXPLICITLY_SET

        def is_set(field_name: str = None) -> bool:
            if field_name is None:
                field_name = name
            return (
                parent_obj._value_states.get(field_name, ValueState.NOT_SET)
                == ValueState.EXPLICITLY_SET
            )

        attr.set = set_value
        attr.isSet = is_set
        attr.__str__ = lambda: str(attr.value)
        attr.__int__ = lambda: int(attr.value)

        return attr

    @classmethod
    def _create_float_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj, qualifiers
    ):
        """Create a float attribute, sourcing min/max/default from qualifiers."""
        from .base_classes import CData, ValueState

        attr = CData(parent=parent_obj, name=name)

        # Set default value from qualifiers
        default_value = qualifiers.get('default', 0.0)
        attr.__dict__["value"] = default_value

        def set_value(val):
            min_value = qualifiers.get('min')
            max_value = qualifiers.get('max')
            if min_value is not None and val < min_value:
                raise ValueError(
                    f"{name} value {val} is below minimum {min_value}"
                )
            if max_value is not None and val > max_value:
                raise ValueError(
                    f"{name} value {val} is above maximum {max_value}"
                )

            attr.__dict__["value"] = float(val)
            if hasattr(parent_obj, "_value_states"):
                parent_obj._value_states[name] = ValueState.EXPLICITLY_SET

        def is_set(field_name: str = None) -> bool:
            if field_name is None:
                field_name = name
            return (
                parent_obj._value_states.get(field_name, ValueState.NOT_SET)
                == ValueState.EXPLICITLY_SET
            )

        attr.set = set_value
        attr.isSet = is_set
        attr.__str__ = lambda: str(attr.value)
        attr.__float__ = lambda: float(attr.value)

        return attr

    @classmethod
    def _create_boolean_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj, qualifiers
    ):
        """Create a boolean attribute, sourcing default from qualifiers."""
        from .base_classes import CData, ValueState

        attr = CData(parent=parent_obj, name=name)

        # Set default value from qualifiers
        default_value = qualifiers.get('default', False)
        attr.__dict__["value"] = default_value

        def set_value(val):
            attr.__dict__["value"] = bool(val)
            if hasattr(parent_obj, "_value_states"):
                parent_obj._value_states[name] = ValueState.EXPLICITLY_SET

        def is_set(field_name: str = None) -> bool:
            if field_name is None:
                field_name = name
            return (
                parent_obj._value_states.get(field_name, ValueState.NOT_SET)
                == ValueState.EXPLICITLY_SET
            )

        attr.set = set_value
        attr.isSet = is_set
        attr.__str__ = lambda: str(attr.value)
        attr.__bool__ = lambda: bool(attr.value)

        return attr

    @classmethod
    def _create_string_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj, qualifiers
    ):
        """Create a string-type attribute, sourcing default from qualifiers."""
        from .fundamental_types import CString

        attr = CString(parent=parent_obj, name=name)

        # Set default value from qualifiers if provided
        default_value = qualifiers.get('default')
        if default_value is not None:
            attr.value = str(default_value)

        return attr

    @classmethod
    def _create_custom_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj, qualifiers
    ):
        """Create a custom attribute type using the custom_class specification."""
        from .base_classes import CData, ValueState

        # Get the custom class name
        custom_class_name = attr_def.custom_class
        if not custom_class_name:
            # Fallback to CString if no custom class specified
            return cls._create_string_attribute(name, attr_def, parent_obj, qualifiers)

        # Build a class registry (similar to DEF XML parser)
        custom_class = cls._get_class_from_registry(custom_class_name)

        if custom_class is None:
            # Class not found, fallback to CString
            print(f"Warning: Custom class '{custom_class_name}' not found for attribute '{name}', using CString")
            return cls._create_string_attribute(name, attr_def, parent_obj, qualifiers)

        # Create instance of the custom class
        try:
            obj = custom_class(parent=parent_obj, name=name)

            # Apply qualifiers
            if qualifiers:
                # Ensure qualifiers attribute exists
                if not hasattr(obj, 'qualifiers') or obj.qualifiers is None:
                    obj.qualifiers = {}
                # Update qualifiers
                if isinstance(obj.qualifiers, dict):
                    obj.qualifiers.update(qualifiers)
                else:
                    obj.qualifiers = qualifiers

            # Set default value from qualifiers if provided
            default_value = qualifiers.get('default')
            if default_value is not None and hasattr(obj, 'value'):
                obj.value = default_value
                if hasattr(parent_obj, "_value_states"):
                    parent_obj._value_states[name] = ValueState.DEFAULT

            return obj
        except Exception as e:
            print(f"Warning: Failed to create custom class '{custom_class_name}': {e}")
            return cls._create_string_attribute(name, attr_def, parent_obj, qualifiers)

    @classmethod
    def _get_class_from_registry(cls, class_name: str):
        """Get a class from the registry, building it if needed."""
        # Import here to avoid circular dependencies
        from .fundamental_types import CInt, CFloat, CBoolean, CString, CList
        from .base_classes import CContainer

        # Build a simple registry - only fundamental types and container
        # Other classes are imported dynamically below
        registry = {
            "CInt": CInt,
            "CFloat": CFloat,
            "CBoolean": CBoolean,
            "CString": CString,
            "CContainer": CContainer,
            "CList": CList,
        }

        # Try to get from basic registry first
        if class_name in registry:
            return registry[class_name]

        # Try to import from core.generated modules
        try:
            import importlib
            # Try importing from various possible locations
            # Order matters - try most specific first
            possible_modules = [
                'core.generated.CCP4Data',      # COneWord, CDict, etc.
                'core.generated.CCP4ModelData', # CEnsemble, CPdbDataFile, etc.
                'core.generated.CCP4File',      # CFilePath, CI2XmlDataFile, etc.
                f'core.generated.{class_name}', # Direct module match
                f'core.{class_name}',           # Core module match
            ]

            for module_path in possible_modules:
                try:
                    module = importlib.import_module(module_path)
                    if hasattr(module, class_name):
                        return getattr(module, class_name)
                except (ImportError, AttributeError):
                    continue
        except Exception:
            pass

        return None


def apply_metadata_to_instance(instance):
    """Apply metadata-defined attributes to a class instance.

    Args:
        instance: The instance to apply metadata to
    """
    # Collect attributes from all ancestor classes with metadata
    # Walk MRO in REVERSE order so that child classes override parent classes
    merged_attributes = {}
    for cls in reversed(instance.__class__.__mro__):
        if cls is object:
            continue
        metadata = getattr(cls, "_metadata", None)
        if metadata:
            # Parent attributes are added first (because we're in reverse),
            # then child overrides them
            merged_attributes.update(metadata.attributes)

    # Create attributes from merged metadata
    for attr_name, attr_def in merged_attributes.items():
        # Check if attribute exists in instance __dict__ (not class attributes)
        # This is important because generated classes have type annotations like
        # `label: Optional[COneWord] = None` which creates a class attribute,
        # but we want to replace it with an actual COneWord instance
        if attr_name not in instance.__dict__:
            attr_obj = MetadataAttributeFactory.create_attribute(
                attr_name, attr_def, instance
            )
            instance.__dict__[attr_name] = attr_obj

            if hasattr(instance, "_value_states"):
                from .base_classes import ValueState

                instance._value_states[attr_name] = ValueState.NOT_SET
