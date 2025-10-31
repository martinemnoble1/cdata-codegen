
"""Fundamental CCP4i2 data types that form the base of the type system."""

from typing import List, Any, Optional
from ..base_object.base_classes import CData, ValueState
from .class_metadata import cdata_class, attribute, AttributeType


@cdata_class(
    error_codes={
        "101": {"description": "below minimum"},
        "102": {"description": "above maximum"},
        "103": {"description": "not one of limited allowed values"}
    },
    qualifiers={
        "max": None,
        "min": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'
    ],
    qualifiers_definition={
        "default": {"type": int},
        "max": {"type": int, "description": "The inclusive minimum allowed value"},
        "min": {"type": int, "description": "The inclusive maximum allowed value"},
        "enumerators": {"type": list, "listItemType": "<class 'int'>", "description": "A Python list of allowed or recommended values - see onlyEnumerators"},
        "menuText": {"type": list, "listItemType": "<class 'str'>", "description": "A Python list of strings, matching items in enumerators list, to appear on GUI menu"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"}
    },
    gui_label="CInt",
)
class CInt(CData):
    def __hash__(self):
        return hash(self.value)

    """Integer value type."""

    def __init__(self, value: int = None, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)

        # Handle value setting with proper state tracking
        if value is None:
            # Default initialization - set value but mark as NOT_SET
            super().__setattr__("_value", 0)
            if hasattr(self, "_value_states"):
                self._value_states["value"] = ValueState.NOT_SET
        else:
            # Explicit value provided - mark as EXPLICITLY_SET
            self.value = value

    def _validate_value(self, val):
        """Validate value against min/max qualifiers."""
        # Skip validation if flag is set (used during .def.xml parsing)
        if getattr(self, '_skip_validation', False):
            return val

        min_val = self.get_qualifier("min")
        max_val = self.get_qualifier("max")

        if min_val is not None and val < min_val:
            raise ValueError(f"Value {val} is below minimum {min_val}")
        if max_val is not None and val > max_val:
            raise ValueError(f"Value {val} is above maximum {max_val}")

        return val

    @property
    def value(self):
        """Get the integer value."""
        return getattr(self, "_value", 0)

    @value.setter
    def value(self, val):
        """Set the integer value with validation."""
        validated = self._validate_value(int(val))
        super().__setattr__("_value", validated)
        if hasattr(self, "_value_states"):
            self._value_states["value"] = ValueState.EXPLICITLY_SET

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def set(self, value: int):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None, allowUndefined: bool = False,
              allowDefault: bool = False, allSet: bool = True) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.
            allowUndefined: If True, allow None/undefined values to be considered "set"
            allowDefault: If False, consider values that equal the default as "not set"
            allSet: For container types (unused for fundamental types)

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name, allowUndefined=allowUndefined,
                           allowDefault=allowDefault, allSet=allSet)

    def _is_value_type(self) -> bool:
        return True

    # Arithmetic operators
    def __add__(self, other):
        if isinstance(other, CInt):
            return CInt(self.value + other.value)
        elif isinstance(other, CFloat):
            return CFloat(self.value + other.value)
        elif isinstance(other, int):
            return CInt(self.value + other)
        elif isinstance(other, float):
            return CFloat(self.value + other)
        return int(self.value) + other

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, CInt):
            return CInt(self.value - other.value)
        elif isinstance(other, CFloat):
            return CFloat(self.value - other.value)
        elif isinstance(other, int):
            return CInt(self.value - other)
        elif isinstance(other, float):
            return CFloat(self.value - other)
        return int(self.value) - other

    def __rsub__(self, other):
        if isinstance(other, CInt):
            return CInt(other.value - self.value)
        elif isinstance(other, CFloat):
            return CFloat(other.value - self.value)
        elif isinstance(other, int):
            return CInt(other - self.value)
        elif isinstance(other, float):
            return CFloat(other - self.value)
        return other - int(self.value)

    def __mul__(self, other):
        if isinstance(other, CInt):
            return CInt(self.value * other.value)
        elif isinstance(other, CFloat):
            return CFloat(self.value * other.value)
        elif isinstance(other, int):
            return CInt(self.value * other)
        elif isinstance(other, float):
            return CFloat(self.value * other)
        return int(self.value) * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (CInt, int)):
            return CFloat(
                self.value / (other.value if isinstance(other, CInt) else other)
            )
        elif isinstance(other, (CFloat, float)):
            return CFloat(
                self.value / (other.value if isinstance(other, CFloat) else other)
            )
        return int(self.value) / other

    def __rtruediv__(self, other):
        if isinstance(other, (CInt, int)):
            return CFloat(
                (other.value if isinstance(other, CInt) else other) / self.value
            )
        elif isinstance(other, (CFloat, float)):
            return CFloat(
                (other.value if isinstance(other, CFloat) else other) / self.value
            )
        return other / int(self.value)

    def __floordiv__(self, other):
        if isinstance(other, CInt):
            return CInt(self.value // other.value)
        elif isinstance(other, int):
            return CInt(self.value // other)
        elif isinstance(other, CFloat):
            return CFloat(self.value // other.value)
        elif isinstance(other, float):
            return CFloat(self.value // other)
        return int(self.value) // other

    def __rfloordiv__(self, other):
        if isinstance(other, CInt):
            return CInt(other.value // self.value)
        elif isinstance(other, int):
            return CInt(other // self.value)
        elif isinstance(other, CFloat):
            return CFloat(other.value // self.value)
        elif isinstance(other, float):
            return CFloat(other // self.value)
        return other // int(self.value)

    def __mod__(self, other):
        if isinstance(other, CInt):
            return CInt(self.value % other.value)
        elif isinstance(other, int):
            return CInt(self.value % other)
        elif isinstance(other, CFloat):
            return CFloat(self.value % other.value)
        elif isinstance(other, float):
            return CFloat(self.value % other)
        return int(self.value) % other

    def __rmod__(self, other):
        if isinstance(other, CInt):
            return CInt(other.value % self.value)
        elif isinstance(other, int):
            return CInt(other % self.value)
        elif isinstance(other, CFloat):
            return CFloat(other.value % self.value)
        elif isinstance(other, float):
            return CFloat(other % self.value)
        return other % int(self.value)

    def __pow__(self, other):
        if isinstance(other, CInt):
            return CInt(self.value**other.value)
        elif isinstance(other, int):
            return CInt(self.value**other)
        elif isinstance(other, CFloat):
            return CFloat(self.value**other.value)
        elif isinstance(other, float):
            return CFloat(self.value**other)
        return int(self.value) ** other

    def __rpow__(self, other):
        if isinstance(other, CInt):
            return CInt(other.value**self.value)
        elif isinstance(other, int):
            return CInt(other**self.value)
        elif isinstance(other, CFloat):
            return CFloat(other.value**self.value)
        elif isinstance(other, float):
            return CFloat(other**self.value)
        return other ** int(self.value)

    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, CInt):
            return self.value == other.value
        elif isinstance(other, CFloat):
            return float(self.value) == other.value
        return int(self.value) == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, CInt):
            return self.value < other.value
        elif isinstance(other, CFloat):
            return float(self.value) < other.value
        return int(self.value) < other

    def __le__(self, other):
        if isinstance(other, CInt):
            return self.value <= other.value
        elif isinstance(other, CFloat):
            return float(self.value) <= other.value
        return int(self.value) <= other

    def __gt__(self, other):
        if isinstance(other, CInt):
            return self.value > other.value
        elif isinstance(other, CFloat):
            return float(self.value) > other.value
        return int(self.value) > other

    def __ge__(self, other):
        if isinstance(other, CInt):
            return self.value >= other.value
        elif isinstance(other, CFloat):
            return float(self.value) >= other.value
        return int(self.value) >= other

    def validity(self):
        """Validate the integer value against qualifiers.

        Returns:
            CErrorReport containing validation errors/warnings
        """
        from .error_reporting import (CErrorReport, SEVERITY_ERROR,
                                      SEVERITY_WARNING)

        report = CErrorReport()
        val = self.value

        # Check min/max constraints
        min_val = self.get_qualifier("min")
        if min_val is not None and val < min_val:
            report.append(
                "CInt", 101, f"Value {val} is below minimum {min_val}",
                self.objectName(), SEVERITY_ERROR
            )

        max_val = self.get_qualifier("max")
        if max_val is not None and val > max_val:
            report.append(
                "CInt", 102, f"Value {val} is above maximum {max_val}",
                self.objectName(), SEVERITY_ERROR
            )

        # Check enumerators if onlyEnumerators is True
        only_enumerators = self.get_qualifier("onlyEnumerators")
        enumerators = self.get_qualifier("enumerators")
        if only_enumerators and enumerators:
            if val not in enumerators:
                report.append(
                    "CInt", 103,
                    f"Value {val} not in allowed values {enumerators}",
                    self.objectName(), SEVERITY_ERROR
                )

        return report


@cdata_class(
    error_codes={
        "101": {"description": "below minimum"},
        "102": {"description": "above maximum"},
        "103": {"description": "not one of limited allowed values"}
    },
    qualifiers={
        "max": None,
        "min": None,
        "enumerators": [],
        "menuText": [],
        "onlyEnumerators": False
    },
    qualifiers_order=[
        'min',
        'max',
        'onlyEnumerators',
        'enumerators',
        'menuText'
    ],
    qualifiers_definition={
        "default": {"type": float},
        "max": {"description": "The inclusive maximum value"},
        "min": {"description": "The inclusive minimum value"},
        "enumerators": {"type": list, "description": "A Python list of allowed or recommended values - see onlyEnumerators"},
        "menuText": {"type": list, "listItemType": "<class 'str'>", "description": "A Python list of strings, matching items in enumerators list, to appear on GUI menu"},
        "onlyEnumerators": {"type": bool, "description": "If this is true then the enumerators are obligatory - otherwise they are treated as recommended values"}
    },
    gui_label="CFloat",
)
class CFloat(CData):
    def __hash__(self):
        return hash(self.value)

    """Float value type."""

    def __init__(self, value: float = None, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)

        # Handle value setting with proper state tracking
        if value is None:
            # Default initialization - set value but mark as NOT_SET
            super().__setattr__("_value", 0.0)
            if hasattr(self, "_value_states"):
                self._value_states["value"] = ValueState.NOT_SET
        else:
            # Explicit value provided - mark as EXPLICITLY_SET
            self.value = value

    def _validate_value(self, val):
        """Validate value against min/max qualifiers."""
        # Skip validation if flag is set (used during .def.xml parsing)
        if getattr(self, '_skip_validation', False):
            return val

        min_val = self.get_qualifier("min")
        max_val = self.get_qualifier("max")

        if min_val is not None and val < min_val:
            raise ValueError(f"Value {val} is below minimum {min_val}")
        if max_val is not None and val > max_val:
            raise ValueError(f"Value {val} is above maximum {max_val}")

        return val

    @property
    def value(self):
        """Get the float value."""
        return getattr(self, "_value", 0.0)

    @value.setter
    def value(self, val):
        """Set the float value with validation."""
        validated = self._validate_value(float(val))
        super().__setattr__("_value", validated)
        if hasattr(self, "_value_states"):
            self._value_states["value"] = ValueState.EXPLICITLY_SET

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return float(self.value)

    def set(self, value: float):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None, allowUndefined: bool = False,
              allowDefault: bool = False, allSet: bool = True) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.
            allowUndefined: If True, allow None/undefined values to be considered "set"
            allowDefault: If False, consider values that equal the default as "not set"
            allSet: For container types (unused for fundamental types)

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name, allowUndefined=allowUndefined,
                           allowDefault=allowDefault, allSet=allSet)

    def _is_value_type(self) -> bool:
        return True


    # Arithmetic operators
    def __add__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value + other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value + other.value)
        elif isinstance(other, float):
            return CFloat(self.value + other)
        elif isinstance(other, int):
            return CFloat(self.value + other)
        return float(self.value) + other

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value - other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value - other.value)
        elif isinstance(other, float):
            return CFloat(self.value - other)
        elif isinstance(other, int):
            return CFloat(self.value - other)
        return float(self.value) - other

    def __rsub__(self, other):
        if isinstance(other, CFloat):
            return CFloat(other.value - self.value)
        elif isinstance(other, CInt):
            return CFloat(other.value - self.value)
        elif isinstance(other, float):
            return CFloat(other - self.value)
        elif isinstance(other, int):
            return CFloat(other - self.value)
        return other - float(self.value)

    def __mul__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value * other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value * other.value)
        elif isinstance(other, float):
            return CFloat(self.value * other)
        elif isinstance(other, int):
            return CFloat(self.value * other)
        return float(self.value) * other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value / other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value / other.value)
        elif isinstance(other, float):
            return CFloat(self.value / other)
        elif isinstance(other, int):
            return CFloat(self.value / other)
        return float(self.value) / other

    def __rtruediv__(self, other):
        if isinstance(other, CFloat):
            return CFloat(other.value / self.value)
        elif isinstance(other, CInt):
            return CFloat(other.value / self.value)
        elif isinstance(other, float):
            return CFloat(other / self.value)
        elif isinstance(other, int):
            return CFloat(other / self.value)
        return other / float(self.value)

    def __floordiv__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value // other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value // other.value)
        elif isinstance(other, float):
            return CFloat(self.value // other)
        elif isinstance(other, int):
            return CFloat(self.value // other)
        return float(self.value) // other

    def __rfloordiv__(self, other):
        if isinstance(other, CFloat):
            return CFloat(other.value // self.value)
        elif isinstance(other, CInt):
            return CFloat(other.value // self.value)
        elif isinstance(other, float):
            return CFloat(other // self.value)
        elif isinstance(other, int):
            return CFloat(other // self.value)
        return other // float(self.value)

    def __mod__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value % other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value % other.value)
        elif isinstance(other, float):
            return CFloat(self.value % other)
        elif isinstance(other, int):
            return CFloat(self.value % other)
        return float(self.value) % other

    def __rmod__(self, other):
        if isinstance(other, CFloat):
            return CFloat(other.value % self.value)
        elif isinstance(other, CInt):
            return CFloat(other.value % self.value)
        elif isinstance(other, float):
            return CFloat(other % self.value)
        elif isinstance(other, int):
            return CFloat(other % self.value)
        return other % float(self.value)

    def __pow__(self, other):
        if isinstance(other, CFloat):
            return CFloat(self.value**other.value)
        elif isinstance(other, CInt):
            return CFloat(self.value**other.value)
        elif isinstance(other, float):
            return CFloat(self.value**other)
        elif isinstance(other, int):
            return CFloat(self.value**other)
        return float(self.value) ** other

    def __rpow__(self, other):
        if isinstance(other, CFloat):
            return CFloat(other.value**self.value)
        elif isinstance(other, CInt):
            return CFloat(other.value**self.value)
        elif isinstance(other, float):
            return CFloat(other**self.value)
        elif isinstance(other, int):
            return CFloat(other**self.value)
        return other ** float(self.value)

    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, CFloat):
            return self.value == other.value
        elif isinstance(other, CInt):
            return self.value == float(other.value)
        return float(self.value) == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if isinstance(other, CFloat):
            return self.value < other.value
        elif isinstance(other, CInt):
            return self.value < float(other.value)
        return float(self.value) < other

    def __le__(self, other):
        if isinstance(other, CFloat):
            return self.value <= other.value
        elif isinstance(other, CInt):
            return self.value <= float(other.value)
        return float(self.value) <= other

    def __gt__(self, other):
        if isinstance(other, CFloat):
            return self.value > other.value
        elif isinstance(other, CInt):
            return self.value > float(other.value)
        return float(self.value) > other

    def __ge__(self, other):
        if isinstance(other, CFloat):
            return self.value >= other.value
        elif isinstance(other, CInt):
            return self.value >= float(other.value)
        return float(self.value) >= other

    def validity(self):
        """Validate the float value against qualifiers.

        Returns:
            CErrorReport containing validation errors/warnings
        """
        from .error_reporting import (CErrorReport, SEVERITY_ERROR,
                                      SEVERITY_WARNING)

        report = CErrorReport()
        val = self.value

        # Check min/max constraints
        min_val = self.get_qualifier("min")
        if min_val is not None and val < min_val:
            report.append(
                "CFloat", 101, f"Value {val} is below minimum {min_val}",
                self.objectName(), SEVERITY_ERROR
            )

        max_val = self.get_qualifier("max")
        if max_val is not None and val > max_val:
            report.append(
                "CFloat", 102, f"Value {val} is above maximum {max_val}",
                self.objectName(), SEVERITY_ERROR
            )

        # Check enumerators if onlyEnumerators is True
        only_enumerators = self.get_qualifier("onlyEnumerators")
        enumerators = self.get_qualifier("enumerators")
        if only_enumerators and enumerators:
            if val not in enumerators:
                report.append(
                    "CFloat", 103,
                    f"Value {val} not in allowed values {enumerators}",
                    self.objectName(), SEVERITY_ERROR
                )

        return report


@cdata_class(
    error_codes={
        "101": {"description": "String too short"},
        "102": {"description": "String too long"},
        "103": {"description": "not one of limited allowed values"},
        "104": {"description": "Contains disallowed characters"}
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
        "charWidth": {"type": int, "description": "Width of the string in characters (for GUI layout)"},
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CString",
)
class CString(CData):
    """String value type with Python string dunder methods."""
    def __init__(self, value: str = "", parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)
        self.value = value

    def __hash__(self):
        """Make CString hashable for use in sets and as dict keys."""
        return hash(id(self))

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

    def __eq__(self, other):
        if isinstance(other, CString):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        if isinstance(other, CString):
            return self.value != other.value
        return self.value != other

    def __lt__(self, other):
        if isinstance(other, CString):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, CString):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, CString):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, CString):
            return self.value >= other.value
        return self.value >= other

    def __add__(self, other):
        if isinstance(other, CString):
            return CString(self.value + other.value)
        return CString(self.value + str(other))

    def __radd__(self, other):
        if isinstance(other, CString):
            return CString(other.value + self.value)
        return CString(str(other) + self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __contains__(self, item):
        return item in self.value

    def __len__(self):
        return len(self.value)

    def set(self, value: str):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None, allowUndefined: bool = False,
              allowDefault: bool = False, allSet: bool = True) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.
            allowUndefined: If True, allow None/undefined values to be considered "set"
            allowDefault: If False, consider values that equal the default as "not set"
            allSet: For container types (unused for fundamental types)

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name, allowUndefined=allowUndefined,
                           allowDefault=allowDefault, allSet=allSet)

    def _is_value_type(self) -> bool:
        return True

    def validity(self):
        """Validate the string value against qualifiers.

        Returns:
            CErrorReport containing validation errors/warnings
        """
        from .error_reporting import (CErrorReport, SEVERITY_ERROR,
                                      SEVERITY_WARNING)

        report = CErrorReport()
        val = self.value

        # Check minLength constraint
        min_length = self.get_qualifier("minLength")
        if min_length is not None and len(val) < min_length:
            report.append(
                "CString", 101,
                f"String length {len(val)} below minimum {min_length}",
                self.objectName(), SEVERITY_ERROR
            )

        # Check maxLength constraint
        max_length = self.get_qualifier("maxLength")
        if max_length is not None and len(val) > max_length:
            report.append(
                "CString", 102,
                f"String length {len(val)} above maximum {max_length}",
                self.objectName(), SEVERITY_ERROR
            )

        # Check enumerators if onlyEnumerators is True
        only_enumerators = self.get_qualifier("onlyEnumerators")
        enumerators = self.get_qualifier("enumerators")
        if only_enumerators and enumerators:
            if val not in enumerators:
                report.append(
                    "CString", 103,
                    f"Value '{val}' not in allowed values {enumerators}",
                    self.objectName(), SEVERITY_ERROR
                )

        return report

@cdata_class(
    error_codes={
        "101": {"description": "not allowed value"}
    },
    qualifiers={
        "menuText": ['NotImplemented', 'NotImplemented']
    },
    qualifiers_order=[
        'charWidth'
    ],
    qualifiers_definition={
        "default": {"type": bool},
        "menuText": {"type": list, "listItemType": "<class 'str'>", "description": "A list of two string descriptions for true and false"}
    },
    gui_label="CBoolean",
)
class CBoolean(CData):
    """Boolean value type."""

    def __init__(self, value: bool = None, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)

        # Handle value setting with proper state tracking
        if value is None:
            # Default initialization - set value but mark as NOT_SET
            super().__setattr__("value", False)
            if hasattr(self, "_value_states"):
                self._value_states["value"] = ValueState.NOT_SET
        else:
            # Explicit value provided - mark as EXPLICITLY_SET
            self.value = value

    def __hash__(self):
        """Make CBoolean hashable for use in sets and as dict keys."""
        return hash(id(self))

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return bool(self.value)

    def set(self, value: bool):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None, allowUndefined: bool = False,
              allowDefault: bool = False, allSet: bool = True) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.
            allowUndefined: If True, allow None/undefined values to be considered "set"
            allowDefault: If False, consider values that equal the default as "not set"
            allSet: For container types (unused for fundamental types)

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name, allowUndefined=allowUndefined,
                           allowDefault=allowDefault, allSet=allSet)

    def _is_value_type(self) -> bool:
        return True

    # Boolean and comparison operators
    def __eq__(self, other):
        return bool(self.value) == other

    def __ne__(self, other):
        return bool(self.value) != other

    def __and__(self, other):
        return bool(self.value) and other

    def __rand__(self, other):
        return other and bool(self.value)

    def __or__(self, other):
        return bool(self.value) or other

    def __ror__(self, other):
        return other or bool(self.value)

    def __invert__(self):
        return not bool(self.value)

    def validity(self):
        """Validate the boolean value.

        Returns:
            CErrorReport containing validation errors/warnings
        """
        from .error_reporting import CErrorReport

        # Boolean values are always valid
        report = CErrorReport()
        return report


@cdata_class(
    error_codes={
        "101": {"description": "List shorter than required minimum length"},
        "102": {"description": "List longer than required maximum length"},
        "103": {"description": "Consecutive values in list fail comparison test"},
        "104": {"description": "Attempting to add object of wrong type"},
        "105": {"description": "Attempting to add object of correct type but wrong qualifiers"},
        "106": {"description": "Attempting to add data which does not satisfy the qualifiers for a list item"},
        "107": {"description": "Deleting item will reduce list below minimum length"},
        "108": {"description": "Adding item will extend list beyond maximum length"},
        "109": {"description": "Invalid item class"},
        "110": {"description": "etree (XML) list item of wrong type"},
        "112": {"description": "No list item object set for list"}
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
    gui_label="CList",
)
class CList(CData):
    """List container type for collections of CData objects."""

    def __init__(
        self, items: Optional[List[Any]] = None, parent=None, name=None, **kwargs
    ):
        super().__init__(parent=parent, name=name, **kwargs)
        object.__setattr__(self, '_items', items or [])
        object.__setattr__(self, '_item_type', None)
        object.__setattr__(self, '_item_qualifiers', {})

        # Register existing items as children
        for i, item in enumerate(self._items):
            if isinstance(item, CData):
                item.set_parent(self)
                item.name = f"{self.name}[{i}]"

    def append(self, item: Any) -> None:
        """Add an item to the list."""
        from ..base_object.base_classes import ValueState
        index = len(self._items)

        # If item is CData, register as child
        if isinstance(item, CData):
            item.set_parent(self)
            item.name = f"{self.name}[{index}]"

        self._items.append(item)

        # Mark as explicitly set
        self._value_states["_items"] = ValueState.EXPLICITLY_SET

    def insert(self, index: int, item: Any) -> None:
        """Insert an item at specified index."""
        if isinstance(item, CData):
            item.set_parent(self)
            item.name = f"{self.name}[{index}]"

        self._items.insert(index, item)

        # Update names of subsequent items
        for i in range(index + 1, len(self._items)):
            if isinstance(self._items[i], CData):
                self._items[i].name = f"{self.name}[{i}]"

        # Mark as explicitly set
        self._value_states["_items"] = self.ValueState.EXPLICITLY_SET

    def remove(self, item: Any) -> None:
        """Remove an item from the list."""
        index = self._items.index(item)
        self._items.remove(item)

        # Update names of subsequent items
        for i in range(index, len(self._items)):
            if isinstance(self._items[i], CData):
                self._items[i].name = f"{self.name}[{i}]"

        # Mark as explicitly set
        self._value_states["_items"] = self.ValueState.EXPLICITLY_SET

    def pop(self, index: int = -1) -> Any:
        """Remove and return item at index."""
        item = self._items.pop(index)

        # Update names of subsequent items if needed
        if index >= 0:
            for i in range(index, len(self._items)):
                if isinstance(self._items[i], CData):
                    self._items[i].name = f"{self.name}[{i}]"

        # Mark as explicitly set
        self._value_states["_items"] = self.ValueState.EXPLICITLY_SET
        return item

    def clear(self) -> None:
        """Remove all items from the list."""
        self._items.clear()
        self._value_states["_items"] = self.ValueState.EXPLICITLY_SET

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, index: int) -> Any:
        return self._items[index]

    def __setitem__(self, index: int, value: Any) -> None:
        if isinstance(value, CData):
            value.set_parent(self)
            value.name = f"{self.name}[{index}]"

        self._items[index] = value
        self._value_states["_items"] = self.ValueState.EXPLICITLY_SET

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, item: Any) -> bool:
        return item in self._items

    def __str__(self) -> str:
        return f"CList({len(self._items)} items)"


# NOTE: Type aliases removed - all custom types now have proper stub classes
# in core/cdata_stubs/ and implementation classes in core/
# (COneWord, CUUID, CProjectId, CCellLength, CWavelength, etc. are all
# regular custom classes derived from fundamental types)
#CProjectName = CString
#CDatasetName = CString
#CFilePath = CString
#CHostName = CString
#CJobStatus = CInt