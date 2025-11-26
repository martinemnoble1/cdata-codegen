# Hierarchical Children and Value States in CData

This document explains how the `HierarchicalObject` and `CData` classes manage parent-child relationships, track whether values have been explicitly set, and how this state is used to understand pipeline parameters.

## Overview

The CData system provides a hierarchical object model where:
- Objects can have parent-child relationships (managed by `HierarchicalObject`)
- Each attribute tracks whether it has been explicitly set vs. using a default value (managed by `CData._value_states`)
- Both mechanisms work together to enable intelligent parameter handling in crystallographic pipelines

## HierarchicalObject: Managing Children

### Child Storage

`HierarchicalObject` maintains a set of weak references to its children:

```python
class HierarchicalObject:
    def __init__(self):
        self._children: Set[weakref.ReferenceType] = set()
        self._parent: Optional[weakref.ref] = None
        self._lock = threading.RLock()  # Thread-safe access
```

Key design decisions:
- **Weak references**: Children are stored as weak refs to prevent memory leaks in circular parent-child relationships
- **Thread-safe**: All operations on `_children` are protected by a reentrant lock
- **Automatic cleanup**: Dead references (objects that have been garbage collected) are cleaned up automatically

### Adding Children

When a CData attribute is assigned, the child is automatically added to the parent's children set via `__setattr__`:

```python
# In CData.__setattr__
if isinstance(value, HierarchicalObject):
    # Set parent relationship (this adds child to parent's _children)
    if value.get_parent() is None:
        value.set_parent(self)
    # Set the child's name within the hierarchy
    if value.objectName() is None:
        value._name = key
```

The `set_parent()` method handles adding the child to the parent:

```python
def set_parent(self, parent: "HierarchicalObject"):
    # Remove from old parent
    if self._parent is not None:
        old_parent = self._parent()
        if old_parent:
            old_parent._remove_child(self)

    # Add to new parent
    self._parent = weakref.ref(parent)
    parent._add_child(self)
```

### Iterating Over Children

The `children()` method returns a list of all current child objects:

```python
def children(self) -> List["HierarchicalObject"]:
    """Get list of all child objects."""
    with self._lock:
        self._cleanup_dead_children()
        return [ref() for ref in self._children if ref() is not None]
```

This is the preferred way to iterate over children because:
1. It only returns actual hierarchical children (not arbitrary `__dict__` entries)
2. It automatically cleans up dead references
3. It's thread-safe
4. It returns the actual objects, not names/keys

### Why Not Use `__dict__`?

Previously, code iterated over `self.__dict__` to find children:

```python
# OLD (problematic) approach:
for key, value in self.__dict__.items():
    if not key.startswith('_') and isinstance(value, CData):
        process(key, value)
```

Problems with this approach:
- `__dict__` contains internal attributes like `_value_states`, `_parent`, etc.
- It may contain non-CData values (signals, plain Python objects)
- It requires filtering logic that can be error-prone
- It doesn't respect the hierarchical structure

The new approach uses `children()`:

```python
# NEW (correct) approach:
for child in self.children():
    if isinstance(child, CData):
        key = child.objectName()
        process(key, child)
```

## ValueState: Tracking Explicitly Set Values

### The Three States

Each CData attribute can be in one of three states:

```python
class ValueState(Enum):
    NOT_SET = "not_set"           # Never assigned any value
    DEFAULT = "default"           # Using the default from class metadata
    EXPLICITLY_SET = "explicitly_set"  # User/code explicitly assigned a value
```

### State Storage

States are stored in a dictionary on each CData object:

```python
class CData:
    def __init__(self):
        self._value_states: Dict[str, ValueState] = {}
```

### State Transitions

1. **Initial State (NOT_SET)**:
   - When a CData object is created, attributes start as NOT_SET
   - The attribute may still have a value (from class metadata default), but it hasn't been explicitly set

2. **Default State (DEFAULT)**:
   - When `setToDefault()` is called
   - When reading from XML without an explicit value

3. **Explicitly Set (EXPLICITLY_SET)**:
   - When a value is assigned via `__setattr__`
   - When `set()` is called with a value
   - When loading from XML with an explicit value

### The `isSet()` Method

The `isSet()` method checks whether a value has been explicitly set:

```python
def isSet(self, field_name=None, allowUndefined=True, allowDefault=True, allSet=False):
    """Check if a field has been set.

    Args:
        field_name: Field to check, or None to check the object itself
        allowUndefined: If True, NOT_SET is considered "set" (legacy compatibility)
        allowDefault: If True, DEFAULT is considered "set"
        allSet: If True, require ALL children to be set (not just any)

    Returns:
        True if the field(s) meet the "set" criteria
    """
```

Key behaviors:

1. **Checking a specific field**:
   ```python
   if obj.isSet('NCYCLES'):  # Is NCYCLES explicitly set?
   ```

2. **Checking the object itself**:
   ```python
   if obj.isSet():  # Does this object have any set values?
   ```

3. **Strict checking (no defaults)**:
   ```python
   if obj.isSet('NCYCLES', allowDefault=False):  # Ignore default values
   ```

4. **Checking all children**:
   ```python
   if obj.isSet(allSet=True):  # Are ALL children set?
   ```

### Hierarchical `isSet()` Checking

When checking if a container is set, `isSet()` recursively checks children:

```python
# In isSet()
for child in self.children():
    if isinstance(child, CData) and hasattr(child, 'isSet'):
        if child.isSet(field_name=None, allowUndefined=allowUndefined,
                      allowDefault=allowDefault, allSet=allSet):
            return True
```

This allows checking container states like:
- "Does inputData have any set parameters?" - `inputData.isSet()`
- "Are all required parameters set?" - `inputData.isSet(allSet=True)`

## Use in Pipeline Parameters

### Parameter Serialization

When writing params.xml, `isSet()` controls what gets serialized:

```python
def toEtree(self, excludeUnset=False, ...):
    for child in self.children():
        if excludeUnset and not child.isSet(allowDefault=False):
            continue  # Skip unset/default-only values
        # Serialize the child...
```

This ensures:
- Only explicitly set parameters appear in XML
- Default values don't clutter the output
- Pipelines can distinguish user input from defaults

### Parameter Copying

When copying parameters between pipeline stages, `isSet()` prevents accidental overwrites:

```python
def __setattr__(self, key, value):
    # Only copy if source value is actually set
    if isinstance(value, CData) and not value.isSet():
        if not value._has_any_set_children():
            return  # Skip - source has no meaningful data
```

This prevents issues like:
- Overwriting user-set values with empty containers
- Marking fields as "set" when they only contain defaults
- Losing track of which parameters came from user input

### Performance Indicators Example

Consider copying RFactor from refmac's output:

```python
# Pipeline copies performance indicator
self.container.outputData.PERFORMANCEINDICATOR = refmac.container.outputData.PERFORMANCEINDICATOR
```

The system checks:
1. Is `PERFORMANCEINDICATOR` set on the source? (`isSet()`)
2. Do any children have values? (`_has_any_set_children()`)
3. If yes, copy the data and mark as EXPLICITLY_SET
4. If no, skip the assignment to preserve any existing values

## Summary

The HierarchicalObject + CData system provides:

1. **Clean parent-child relationships** via `children()` method
2. **Three-state value tracking** (NOT_SET, DEFAULT, EXPLICITLY_SET)
3. **Intelligent `isSet()` checking** with hierarchical support
4. **Safe parameter serialization** that excludes unset/default values
5. **Smart assignment** that respects value states during copying

This enables pipelines to:
- Know exactly which parameters were user-specified
- Distinguish between "not set" and "set to default"
- Copy parameters safely without losing state information
- Generate clean XML with only meaningful values
