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
            super().__setattr__("value", 0)
            if hasattr(self, "_value_states"):
                self._value_states["value"] = ValueState.NOT_SET
        else:
            # Explicit value provided - mark as EXPLICITLY_SET
            self.value = value

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def set(self, value: int):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name)

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
            super().__setattr__("value", 0.0)
            if hasattr(self, "_value_states"):
                self._value_states["value"] = ValueState.NOT_SET
        else:
            # Explicit value provided - mark as EXPLICITLY_SET
            self.value = value

    def __str__(self):
        return str(self.value)

    def __float__(self):
        return float(self.value)

    def set(self, value: float):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name)

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

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        return bool(self.value)

    def set(self, value: bool):
        """Set the value directly using .set() method."""
        self.value = value
        return self

    def isSet(self, field_name: str = None) -> bool:
        """Check if the value has been set.

        Args:
            field_name: Optional field name. If not provided, checks if 'value' is set.

        Returns:
            True if the value (or specified field) has been set, False otherwise.
        """
        if field_name is None:
            field_name = "value"
        return super().isSet(field_name)

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
        self._items = items or []
        self._item_type = None
        self._item_qualifiers = {}

        # Register existing items as children
        for i, item in enumerate(self._items):
            if isinstance(item, CData):
                item.set_parent(self)
                item.name = f"{self.name}[{i}]"

    def append(self, item: Any) -> None:
        """Add an item to the list."""
        index = len(self._items)

        # If item is CData, register as child
        if isinstance(item, CData):
            item.set_parent(self)
            item.name = f"{self.name}[{index}]"

        self._items.append(item)

        # Mark as explicitly set
        self._value_states["_items"] = self.ValueState.EXPLICITLY_SET

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

    def __repr__(self) -> str:
        return f"CList({self._items!r})"



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
        "allowedCharsCode": {"type": int, "description": "Flag if the text is limited to set of allowed characters"}
    },
    gui_label="CString",
)
class CString(CData):
    def __hash__(self):
        return hash(self.value)

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
        return str(self.value)[key]

    def __contains__(self, item):
        return item in str(self.value)

    def __len__(self):
        return len(str(self.value))

    """A string value type for testing smart assignment."""

    def __init__(self, value: str = "", parent=None, name=None, **kwargs):
        self.value = value
        super().__init__(parent=parent, name=name, **kwargs)

    def __str__(self):
        return str(self.value)

    def set(self, value: str):
        """Set the value directly using .set() method."""
        self.value = value
        # Mark as explicitly set in parent if we have one
        if self.parent and hasattr(self.parent, "_value_states") and self.name:
            self.parent._value_states[self.name] = ValueState.EXPLICITLY_SET
        return self

    def isSet(self, field_name: str = None) -> bool:
        """Check if this string value has been set.

        Args:
            field_name: Optional field name (for compatibility with parent's isSet interface)
                       If None, uses this object's name in its parent

        Returns:
            True if value has been explicitly set, False otherwise
        """
        if self.parent and hasattr(self.parent, "_value_states"):
            # Use provided field_name or fall back to this object's name
            check_name = field_name if field_name is not None else self.name
            if check_name:
                return (
                    self.parent._value_states.get(check_name, ValueState.NOT_SET)
                    == ValueState.EXPLICITLY_SET
                )

        # Fallback: check if we have a non-empty value (basic heuristic)
        return bool(self.value) if self.value != "" else False

    def _is_value_type(self) -> bool:
        return True

# Type aliases for commonly used types
#CCellLength = CFloat
#CWavelength = CFloat
#CCellAngle = CFloat
#CAngle = CFloat
#CTime = CInt
#CSpaceGroup = CString
#CUUID = CString
#CProjectId = CUUID
#CUserId = CString
#CVersion = CString
#CProjectName = CString
#CDatasetName = CString
#CFilePath = CString
#CHostName = CString
#CJobStatus = CInt