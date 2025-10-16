"""Fundamental CCP4i2 data types that form the base of the type system."""

from typing import List, Any, Optional, Union
from .base_classes import CData, ValueState, CString


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


class CRange(CData):
    """Base class for range types."""

    def __init__(self, parent=None, name=None, **kwargs):
        super().__init__(parent=parent, name=name, **kwargs)


class CIntRange(CRange):
    """Integer range type."""

    def __init__(self, start: int = 0, end: int = 0, parent=None, name=None, **kwargs):
        self.start = start
        self.end = end
        super().__init__(parent=parent, name=name, **kwargs)

    def __str__(self):
        return f"{self.start}-{self.end}"

    def validate(self) -> List[str]:
        """Validate the range."""
        errors = []
        if self.start > self.end:
            errors.append("Start value cannot be greater than end value")
        return errors


class CFloatRange(CRange):
    """Float range type."""

    def __init__(
        self, start: float = 0.0, end: float = 0.0, parent=None, name=None, **kwargs
    ):
        self.start = start
        self.end = end
        super().__init__(parent=parent, name=name, **kwargs)

    def __str__(self):
        return f"{self.start}-{self.end}"

    def validate(self) -> List[str]:
        """Validate the range."""
        errors = []
        if self.start > self.end:
            errors.append("Start value cannot be greater than end value")
        return errors


# CString is now imported from base_classes.py


# Type aliases for commonly used types
CCellLength = CFloat
CCellAngle = CFloat
CWavelength = CFloat
CAngle = CFloat
CTime = CInt
CSpaceGroup = CString
CUUID = CString
CProjectId = CUUID
CUserId = CString
CVersion = CString
CProjectName = CString
CDatasetName = CString
CFilePath = CString
CHostName = CString
CJobStatus = CInt


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


# String type aliases
CJobTitle = CString
CRangeSelection = CString
CExperimentalDataType = CString
CFileFunction = CString
CI2DataType = CString
CCustomTaskFileFunction = CString
CCrystalName = CString
CShelxLabel = CString
CSequenceString = CString
COneWord = CString
