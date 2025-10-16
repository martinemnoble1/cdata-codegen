"""Decorator-based metadata system for CData classes.

This module provides decorators and utilities to embed metadata directly
in class definitions, making the system more maintainable than external JSON files.
"""

from typing import Dict, Any, Optional, Type, List
from dataclasses import dataclass, field
from enum import Enum


class AttributeType(Enum):
    """Types of attributes that can be created."""

    INT = "CInt"
    FLOAT = "CFloat"
    BOOLEAN = "CBoolean"
    STRING = "CString"
    FILEPATH = "CFilePath"
    PROJECT_ID = "CProjectId"
    UUID = "CUUID"
    JOB_TITLE = "CJobTitle"
    CUSTOM = "Custom"


@dataclass
class AttributeDefinition:
    """Definition of a class attribute."""

    attr_type: AttributeType
    default: Any = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    enumerators: Optional[List[str]] = None
    tooltip: Optional[str] = None
    must_exist: bool = False
    allow_undefined: bool = True
    file_extensions: Optional[List[str]] = None
    custom_class: Optional[str] = None  # For custom types

    def __post_init__(self):
        """Validate attribute definition."""
        if self.attr_type == AttributeType.CUSTOM and not self.custom_class:
            raise ValueError(
                "Custom attribute type requires custom_class to be specified"
            )


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


def attribute(attr_type: AttributeType, **kwargs) -> AttributeDefinition:
    """Helper function to create attribute definitions.

    Args:
        attr_type: The type of attribute
        **kwargs: Additional attribute properties

    Returns:
        AttributeDefinition instance

    Example:
        project = attribute(AttributeType.PROJECT_ID)
        size = attribute(AttributeType.INT, default=0, min_value=0)
        file_path = attribute(AttributeType.FILEPATH, file_extensions=['txt', 'log'])
    """
    return AttributeDefinition(attr_type=attr_type, **kwargs)


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
                'project': attribute(AttributeType.PROJECT_ID),
                'baseName': attribute(AttributeType.FILEPATH),
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
        """Create an attribute object from definition.

        Args:
            name: Name of the attribute
            attr_def: Attribute definition
            parent_obj: Parent object to attach attribute to

        Returns:
            Created attribute object
        """
        from .base_classes import ValueState

        if attr_def.attr_type == AttributeType.INT:
            return cls._create_int_attribute(name, attr_def, parent_obj)
        elif attr_def.attr_type == AttributeType.FLOAT:
            return cls._create_float_attribute(name, attr_def, parent_obj)
        elif attr_def.attr_type == AttributeType.BOOLEAN:
            return cls._create_boolean_attribute(name, attr_def, parent_obj)
        elif attr_def.attr_type in [
            AttributeType.STRING,
            AttributeType.FILEPATH,
            AttributeType.PROJECT_ID,
            AttributeType.UUID,
            AttributeType.JOB_TITLE,
        ]:
            return cls._create_string_attribute(name, attr_def, parent_obj)
        elif attr_def.attr_type == AttributeType.CUSTOM:
            return cls._create_custom_attribute(name, attr_def, parent_obj)
        else:
            raise ValueError(f"Unknown attribute type: {attr_def.attr_type}")

    @classmethod
    def _create_int_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj
    ):
        """Create an integer attribute."""
        from .base_classes import CData, ValueState

        attr = CData(parent=parent_obj, name=name)

        # Set default value
        default_value = attr_def.default if attr_def.default is not None else 0
        attr.__dict__["value"] = default_value

        # Create methods
        def set_value(val):
            # Validate range if specified
            if attr_def.min_value is not None and val < attr_def.min_value:
                raise ValueError(
                    f"{name} value {val} is below minimum {attr_def.min_value}"
                )
            if attr_def.max_value is not None and val > attr_def.max_value:
                raise ValueError(
                    f"{name} value {val} is above maximum {attr_def.max_value}"
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
        cls, name: str, attr_def: AttributeDefinition, parent_obj
    ):
        """Create a float attribute."""
        from .base_classes import CData, ValueState

        attr = CData(parent=parent_obj, name=name)

        # Set default value
        default_value = attr_def.default if attr_def.default is not None else 0.0
        attr.__dict__["value"] = default_value

        # Create methods
        def set_value(val):
            # Validate range if specified
            if attr_def.min_value is not None and val < attr_def.min_value:
                raise ValueError(
                    f"{name} value {val} is below minimum {attr_def.min_value}"
                )
            if attr_def.max_value is not None and val > attr_def.max_value:
                raise ValueError(
                    f"{name} value {val} is above maximum {attr_def.max_value}"
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
        cls, name: str, attr_def: AttributeDefinition, parent_obj
    ):
        """Create a boolean attribute."""
        from .base_classes import CData, ValueState

        attr = CData(parent=parent_obj, name=name)

        # Set default value
        default_value = attr_def.default if attr_def.default is not None else False
        attr.__dict__["value"] = default_value

        # Create methods
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
        cls, name: str, attr_def: AttributeDefinition, parent_obj
    ):
        """Create a string-type attribute."""
        from .base_classes import CString

        # Use the actual CString class for consistency
        attr = CString(parent=parent_obj, name=name)

        # Set default value if specified
        if attr_def.default is not None:
            attr.value = str(attr_def.default)

        return attr

    @classmethod
    def _create_custom_attribute(
        cls, name: str, attr_def: AttributeDefinition, parent_obj
    ):
        """Create a custom attribute type."""
        # This would handle custom CData subclasses
        # For now, default to CString
        return cls._create_string_attribute(name, attr_def, parent_obj)


def apply_metadata_to_instance(instance):
    """Apply metadata-defined attributes to a class instance.

    Args:
        instance: The instance to apply metadata to
    """
    # Collect attributes from all ancestor classes with metadata
    merged_attributes = {}
    for cls in instance.__class__.__mro__:
        if cls is object:
            continue
        metadata = getattr(cls, "_metadata", None)
        if metadata:
            # Parent attributes are added first, child overrides
            merged_attributes.update(metadata.attributes)

    # Create attributes from merged metadata
    for attr_name, attr_def in merged_attributes.items():
        if not hasattr(instance, attr_name):
            attr_obj = MetadataAttributeFactory.create_attribute(
                attr_name, attr_def, instance
            )
            instance.__dict__[attr_name] = attr_obj

            if hasattr(instance, "_value_states"):
                from .base_classes import ValueState

                instance._value_states[attr_name] = ValueState.NOT_SET
