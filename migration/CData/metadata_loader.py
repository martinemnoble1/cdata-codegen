"""
Metadata loader for CData classes.

This module loads metadata from the JSON file and automatically creates
attributes for CData classes based on their CONTENTS specification.
"""

import json
import os
from typing import Dict, Any, Optional
from .base_classes import ValueState


class MetadataLoader:
    """Loads and applies metadata from the enhanced JSON file."""

    _metadata_cache: Optional[Dict[str, Any]] = None
    _json_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data_manager",
        "migrating_from_old_ccp4i2",
        "cdata_lookup_enhanced_full.json",
    )

    @classmethod
    def load_metadata(cls) -> Dict[str, Any]:
        """Load metadata from JSON file (cached)."""
        if cls._metadata_cache is None:
            try:
                with open(cls._json_path, "r") as f:
                    data = json.load(f)
                    cls._metadata_cache = data.get("classes", {})
            except FileNotFoundError:
                print(f"Warning: Metadata file not found at {cls._json_path}")
                cls._metadata_cache = {}
            except Exception as e:
                print(f"Warning: Error loading metadata: {e}")
                cls._metadata_cache = {}

        return cls._metadata_cache

    @classmethod
    def get_class_metadata(cls, class_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific class."""
        metadata = cls.load_metadata()
        return metadata.get(class_name)

    @classmethod
    def get_class_contents(cls, class_name: str) -> Optional[Dict[str, Any]]:
        """Get CONTENTS section for a specific class."""
        class_meta = cls.get_class_metadata(class_name)
        if class_meta:
            return class_meta.get("CONTENTS", {})
        return None

    @classmethod
    def create_attribute_from_metadata(
        cls, parent_obj, attr_name: str, attr_def: Dict[str, Any]
    ):
        """Create an attribute on parent_obj based on metadata definition.

        Args:
            parent_obj: The parent CData object
            attr_name: Name of the attribute to create
            attr_def: Attribute definition from metadata (contains 'class' and optionally 'qualifiers')

        Returns:
            The created attribute object
        """
        attr_class_name = attr_def.get("class", "CCP4Data.CString")
        qualifiers = attr_def.get("qualifiers", {})

        # Map class names to actual implementations
        attr_obj = cls._create_attribute_object(
            attr_class_name, attr_name, parent_obj, qualifiers
        )

        # Set up hierarchy
        if hasattr(attr_obj, "set_parent"):
            attr_obj.set_parent(parent_obj)
        if hasattr(attr_obj, "name"):
            attr_obj.name = attr_name

        # Mark as NOT_SET initially (from metadata defaults)
        if hasattr(parent_obj, "_value_states"):
            # Check if there's a default value in qualifiers
            if "default" in qualifiers and qualifiers["default"] is not None:
                parent_obj._value_states[attr_name] = ValueState.DEFAULT
                # Set the default value
                if hasattr(attr_obj, "set"):
                    attr_obj.set(qualifiers["default"])
                elif hasattr(attr_obj, "value"):
                    attr_obj.__dict__["value"] = qualifiers["default"]
            else:
                parent_obj._value_states[attr_name] = ValueState.NOT_SET

        return attr_obj

    @classmethod
    def _create_attribute_object(
        cls, class_name: str, attr_name: str, parent_obj, qualifiers: Dict[str, Any]
    ):
        """Create the appropriate attribute object based on class name."""
        # Import locally to avoid circular imports
        from .base_classes import CString

        # Normalize class name (remove module prefixes)
        clean_class_name = class_name.split(".")[-1]

        # Map to our implementations
        if clean_class_name in ["CInt"]:
            return cls._create_int_attribute(attr_name, parent_obj, qualifiers)
        elif clean_class_name in ["CFloat"]:
            return cls._create_float_attribute(attr_name, parent_obj, qualifiers)
        elif clean_class_name in ["CBoolean", "CBool"]:
            return cls._create_boolean_attribute(attr_name, parent_obj, qualifiers)
        elif clean_class_name in [
            "CString",
            "CFilePath",
            "CProjectId",
            "CUUID",
            "CJobTitle",
        ]:
            # All string-like types
            return CString(parent=parent_obj, name=attr_name)
        else:
            # Default to string for unknown types
            print(
                f"Warning: Unknown attribute type '{class_name}', defaulting to CString"
            )
            return CString(parent=parent_obj, name=attr_name)

    @classmethod
    def _create_int_attribute(cls, name: str, parent_obj, qualifiers: Dict[str, Any]):
        """Create a simple integer attribute."""
        from .base_classes import CData

        attr = CData(parent=parent_obj, name=name)

        # Set default value (0 or from qualifiers)
        default_value = (
            qualifiers.get("default", 0) if qualifiers.get("default") is not None else 0
        )
        attr.__dict__["value"] = default_value

        # Create methods for the attribute
        def set_value(val):
            attr.__dict__["value"] = val
            if hasattr(parent_obj, "_value_states"):
                parent_obj._value_states[name] = ValueState.EXPLICITLY_SET

        # Create isSet method that works like the fundamental types (optional field_name)
        def is_set(field_name: str = None) -> bool:
            if field_name is None:
                field_name = (
                    name  # Use the attribute name for the parent's _value_states
                )
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
    def _create_float_attribute(cls, name: str, parent_obj, qualifiers: Dict[str, Any]):
        """Create a simple float attribute."""
        from .base_classes import CData

        attr = CData(parent=parent_obj, name=name)

        # Set default value (0.0 or from qualifiers)
        default_value = (
            qualifiers.get("default", 0.0)
            if qualifiers.get("default") is not None
            else 0.0
        )
        attr.__dict__["value"] = default_value

        # Create methods for the attribute
        def set_value(val):
            attr.__dict__["value"] = float(val)
            if hasattr(parent_obj, "_value_states"):
                parent_obj._value_states[name] = ValueState.EXPLICITLY_SET

        # Create isSet method that works like the fundamental types (optional field_name)
        def is_set(field_name: str = None) -> bool:
            if field_name is None:
                field_name = (
                    name  # Use the attribute name for the parent's _value_states
                )
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
        cls, name: str, parent_obj, qualifiers: Dict[str, Any]
    ):
        """Create a simple boolean attribute."""
        from .base_classes import CData

        attr = CData(parent=parent_obj, name=name)

        # Set default value (False or from qualifiers)
        default_value = (
            qualifiers.get("default", False)
            if qualifiers.get("default") is not None
            else False
        )
        attr.__dict__["value"] = default_value

        # Create methods for the attribute
        def set_value(val):
            attr.__dict__["value"] = bool(val)
            if hasattr(parent_obj, "_value_states"):
                parent_obj._value_states[name] = ValueState.EXPLICITLY_SET

        # Create isSet method that works like the fundamental types (optional field_name)
        def is_set(field_name: str = None) -> bool:
            if field_name is None:
                field_name = (
                    name  # Use the attribute name for the parent's _value_states
                )
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
    def apply_metadata_to_instance(cls, instance, class_name: str = None):
        """Apply metadata to a CData instance, creating all required attributes.

        Args:
            instance: The CData instance to enhance
            class_name: Optional class name override (defaults to instance.__class__.__name__)
        """
        if class_name is None:
            class_name = instance.__class__.__name__

        contents = cls.get_class_contents(class_name)
        if not contents:
            return  # No metadata available

        for attr_name, attr_def in contents.items():
            # Create the attribute
            attr_obj = cls.create_attribute_from_metadata(instance, attr_name, attr_def)

            # Set it on the instance (avoid __setattr__ tracking)
            instance.__dict__[attr_name] = attr_obj
