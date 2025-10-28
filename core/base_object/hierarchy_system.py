"""
Modern Python replacement for Qt's parent/child object hierarchy.

This module provides a clean, memory-safe object hierarchy system that can replace
Qt's QObject parent/child relationships in the CCP4i2 Django backend. It supports:

- Automatic lifecycle management
- Hierarchical object organization
- Event propagation through the hierarchy
- Automatic cleanup on parent destruction
- Weak references to prevent cycles
- Type-safe parent/child relationships
"""

import logging
import threading
import weakref
from abc import ABC
from typing import Any, Dict, List, Optional, Type, TypeVar, Callable, Set
from dataclasses import dataclass, field
from enum import Enum, auto

# Import will be done relatively when used as module
try:
    from .signal_system import Signal, SignalManager
except ImportError:
    # For standalone testing
    from signal_system import Signal, SignalManager

logger = logging.getLogger(__name__)

T = TypeVar("T", bound="HierarchicalObject")


class ObjectState(Enum):
    """Object lifecycle states."""

    CREATED = auto()
    INITIALIZED = auto()
    ACTIVE = auto()
    DESTROYING = auto()
    DESTROYED = auto()


@dataclass
class ObjectInfo:
    """Metadata about hierarchical objects."""

    name: str
    object_type: str
    created_at: float = field(default_factory=lambda: __import__("time").time())
    state: ObjectState = ObjectState.CREATED
    properties: Dict[str, Any] = field(default_factory=dict)


class HierarchicalObject(ABC):
    """
    Base class providing Qt-like parent/child relationships and lifecycle management.

    This replaces Qt's QObject functionality with:
    - Parent/child hierarchy with automatic cleanup
    - Signal system integration
    - Property system
    - Event handling and propagation
    - Thread-safe operations
    - Memory leak prevention through weak references
    """

    def __init__(
        self, parent: Optional["HierarchicalObject"] = None, name: str = None
    ):
        self._parent_ref: Optional[weakref.ReferenceType] = None
        self._children: Set[weakref.ReferenceType] = set()
        self._name = name or f"{self.__class__.__name__}_{id(self)}"
        self._lock = threading.RLock()
        self._signal_manager = SignalManager()
        self._state = ObjectState.CREATED
        self._properties: Dict[str, Any] = {}
        self._event_handlers: Dict[str, List[Callable]] = {}

        # Core signals that all objects have
        self.destroyed = self._signal_manager.create_signal("destroyed", type(None))
        self.parent_changed = self._signal_manager.create_signal(
            "parent_changed", "HierarchicalObject"
        )
        self.child_added = self._signal_manager.create_signal(
            "child_added", "HierarchicalObject"
        )
        self.child_removed = self._signal_manager.create_signal(
            "child_removed", "HierarchicalObject"
        )

        # Set parent relationship
        if parent is not None:
            self.set_parent(parent)

        self._state = ObjectState.INITIALIZED
        logger.debug(f"Created {self._name}")

    @property
    def name(self) -> str:
        """Object name for identification and debugging."""
        return self._name

    @name.setter
    def name(self, value: str):
        old_name = self._name
        self._name = value
        logger.debug(f"Renamed object from {old_name} to {value}")

    @property
    def object_info(self) -> ObjectInfo:
        """Get metadata about this object."""
        return ObjectInfo(
            name=self._name,
            object_type=self.__class__.__name__,
            state=self._state,
            properties=self._properties.copy(),
        )

    @property
    def state(self) -> ObjectState:
        """Current object state."""
        return self._state

    @property
    def parent(self) -> Optional["HierarchicalObject"]:
        """Get the parent object (None if no parent or parent was destroyed)."""
        if self._parent_ref is None:
            return None
        parent = self._parent_ref()
        if parent is None:
            # Parent was garbage collected
            self._parent_ref = None
        return parent

    def set_parent(self, parent: Optional["HierarchicalObject"]) -> bool:
        """
        Set the parent object.

        Args:
            parent: New parent object or None to remove parent

        Returns:
            True if parent was successfully set
        """
        with self._lock:
            if self._state == ObjectState.DESTROYED:
                logger.warning(
                    f"Cannot set parent on destroyed object {self._name}"
                )
                return False

            old_parent = self.parent

            # Remove from old parent
            if old_parent is not None:
                old_parent._remove_child(self)

            # Set new parent
            if parent is not None:
                if parent._state == ObjectState.DESTROYED:
                    logger.warning(f"Cannot set destroyed object as parent")
                    return False

                self._parent_ref = weakref.ref(parent)
                parent._add_child(self)
            else:
                self._parent_ref = None

            # Emit signal (guard against GC ordering issues)
            if hasattr(self, 'parent_changed') and self.parent_changed is not None:
                self.parent_changed.emit(parent)
            logger.debug(
                f"Set parent of {self._name} to {parent._name if parent else None}"
            )
            return True

    def _add_child(self, child: "HierarchicalObject"):
        """Internal method to add a child (called by set_parent)."""
        with self._lock:
            # Clean up any dead references first
            self._cleanup_dead_children()

            child_ref = weakref.ref(child)
            self._children.add(child_ref)
            # Guard against GC ordering issues
            if hasattr(self, 'child_added') and self.child_added is not None:
                self.child_added.emit(child)
            logging.debug(f"Added child {child._name} to {self._name}")

    def _remove_child(self, child: "HierarchicalObject"):
        """Internal method to remove a child (called by set_parent)."""
        with self._lock:
            # Find and remove the child reference
            to_remove = None
            for child_ref in self._children:
                if child_ref() == child:
                    to_remove = child_ref
                    break

            if to_remove:
                self._children.remove(to_remove)
                # Guard against GC ordering issues - signal might be cleaned up already
                if hasattr(self, 'child_removed') and self.child_removed is not None:
                    self.child_removed.emit(child)
                logger.debug(
                    f"Removed child {child._name} from {self._name}"
                )

    def _cleanup_dead_children(self):
        """Remove weak references to destroyed children."""
        dead_refs = {ref for ref in self._children if ref() is None}
        self._children -= dead_refs

    def children(self) -> List["HierarchicalObject"]:
        """Get list of all child objects."""
        with self._lock:
            self._cleanup_dead_children()
            return [ref() for ref in self._children if ref() is not None]

    def find_child(
        self, name: str, recursive: bool = False
    ) -> Optional["HierarchicalObject"]:
        """Find a child by name."""
        children = self.children()

        # Direct children first
        for child in children:
            if child._name == name:
                return child

        # Recursive search if requested
        if recursive:
            for child in children:
                found = child.find_child(name, recursive=True)
                if found:
                    return found

        return None

    def find_children(
        self, object_type: Type[T] = None, recursive: bool = False
    ) -> List[T]:
        """Find children by type."""
        results = []
        children = self.children()

        for child in children:
            if object_type is None or isinstance(child, object_type):
                results.append(child)

            if recursive:
                results.extend(child.find_children(object_type, recursive=True))

        return results

    def ancestors(self) -> List["HierarchicalObject"]:
        """Get list of all ancestor objects (parents, grandparents, etc.)."""
        ancestors = []
        current = self.parent
        while current is not None:
            ancestors.append(current)
            current = current.parent
        return ancestors

    def root(self) -> "HierarchicalObject":
        """Get the root object (topmost ancestor)."""
        current = self
        while current.parent is not None:
            current = current.parent
        return current

    def path_from_root(self) -> List[str]:
        """Get the path from root to this object as list of names."""
        path = []
        current = self
        while current is not None:
            path.insert(0, current._name)
            current = current.parent
        return path

    def object_path(self) -> str:
        """Get the dot-separated path from root to this object."""
        return ".".join(self.path_from_root())

    def find_by_path(self, path: str) -> Optional["HierarchicalObject"]:
        """
        Find an object by dot-separated path with array indexing support.

        Supports:
        - Simple paths: "child.grandchild"
        - Array indexing: "children[0].property"
        - Mixed: "database.tables[2].columns[0]"

        Args:
            path: Dot-separated path string (e.g., "child.grandchild[0]")

        Returns:
            Found object or None
        """
        if not path:
            return self

        return self._resolve_path_segment(path.split("."), 0)

    def _resolve_path_segment(
        self, segments: List[str], index: int
    ) -> Optional["HierarchicalObject"]:
        """Recursively resolve path segments with array indexing."""
        if index >= len(segments):
            return self

        segment = segments[index]

        # Handle array indexing: "name[index]"
        if "[" in segment and segment.endswith("]"):
            name_part, bracket_part = segment.split("[", 1)
            array_index = bracket_part[:-1]  # Remove closing ']'

            try:
                idx = int(array_index)

                # Find child by name
                target_child = None
                if name_part:  # "child[0]"
                    target_child = self.find_child(name_part)
                else:  # "[0]" - use this object's children
                    children = self.children()
                    if 0 <= idx < len(children):
                        target_child = children[idx]

                if target_child is None:
                    return None

                # Handle array indexing on the found child
                if hasattr(target_child, "_indexed_children"):
                    # Custom array-like access
                    indexed_items = target_child._indexed_children()
                    if 0 <= idx < len(indexed_items):
                        next_obj = indexed_items[idx]
                    else:
                        return None
                elif name_part:  # Regular child with index - use the child itself
                    next_obj = target_child
                else:
                    return None

            except (ValueError, IndexError):
                return None

        else:
            # Simple name lookup
            next_obj = self.find_child(segment)

        if next_obj is None:
            return None

        # Continue with next segment
        return next_obj._resolve_path_segment(segments, index + 1)

    def set_by_path(self, path: str, value: Any) -> bool:
        """
        Set a property or child object by path.

        Args:
            path: Dot-separated path (e.g., "child.property" or "database.tables[0].name")
            value: Value to set

        Returns:
            True if successful
        """
        if not path:
            return False

        parts = path.split(".")
        if len(parts) == 1:
            # Setting property on this object
            self.set_property(parts[0], value)
            return True

        # Navigate to parent of target
        parent_path = ".".join(parts[:-1])
        target_parent = self.find_by_path(parent_path)

        if target_parent is None:
            return False

        property_name = parts[-1]
        target_parent.set_property(property_name, value)
        return True

    def get_by_path(self, path: str, default: Any = None) -> Any:
        """
        Get a property or object by path.

        Args:
            path: Dot-separated path
            default: Default value if path not found

        Returns:
            Found value/object or default
        """
        if not path:
            return self

        # Check if it's a property path (ends with property name)
        parts = path.split(".")

        # Try to find object first
        obj = self.find_by_path(path)
        if obj is not None:
            return obj

        # If not found as object, try as property path
        if len(parts) > 1:
            parent_path = ".".join(parts[:-1])
            parent_obj = self.find_by_path(parent_path)
            if parent_obj is not None:
                property_name = parts[-1]
                return parent_obj.get_property(property_name, default)

        return default

    def list_paths(self, max_depth: int = 3) -> List[str]:
        """
        Get all available paths from this object.

        Args:
            max_depth: Maximum depth to traverse

        Returns:
            List of dot-separated paths
        """
        paths = []
        self._collect_paths(paths, "", max_depth)
        return sorted(paths)

    def _collect_paths(self, paths: List[str], current_path: str, max_depth: int):
        """Recursively collect all paths."""
        if max_depth <= 0:
            return

        # Add current object path
        if current_path:
            paths.append(current_path)

        # Add property paths
        for prop_name in self.property_names():
            prop_path = f"{current_path}.{prop_name}" if current_path else prop_name
            paths.append(prop_path)

        # Add child paths
        children = self.children()
        for i, child in enumerate(children):
            # Regular child path
            child_path = (
                f"{current_path}.{child._name}"
                if current_path
                else child._name
            )
            child._collect_paths(paths, child_path, max_depth - 1)

            # Array index path
            array_path = f"{current_path}[{i}]" if current_path else f"[{i}]"
            child._collect_paths(paths, array_path, max_depth - 1)

    def descendant_count(self) -> int:
        """Count all descendants (children, grandchildren, etc.)."""
        count = 0
        for child in self.children():
            count += 1 + child.descendant_count()
        return count

    # Property system
    def set_property(self, name: str, value: Any):
        """Set a custom property on this object."""
        with self._lock:
            self._properties[name] = value

    def get_property(self, name: str, default: Any = None) -> Any:
        """Get a custom property value."""
        return self._properties.get(name, default)

    def has_property(self, name: str) -> bool:
        """Check if a property exists."""
        return name in self._properties

    def property_names(self) -> List[str]:
        """Get list of all property names."""
        return list(self._properties.keys())

    # Event system
    def install_event_handler(self, event_type: str, handler: Callable):
        """Install an event handler for a specific event type."""
        with self._lock:
            if event_type not in self._event_handlers:
                self._event_handlers[event_type] = []
            self._event_handlers[event_type].append(handler)

    def remove_event_handler(self, event_type: str, handler: Callable):
        """Remove an event handler."""
        with self._lock:
            if event_type in self._event_handlers:
                try:
                    self._event_handlers[event_type].remove(handler)
                    if not self._event_handlers[event_type]:
                        del self._event_handlers[event_type]
                except ValueError:
                    pass

    def emit_event(self, event_type: str, data: Any = None, propagate: bool = True):
        """Emit an event, optionally propagating to parent."""
        # Handle locally first
        with self._lock:
            handlers = self._event_handlers.get(event_type, [])
            for handler in handlers:
                try:
                    handler(self, event_type, data)
                except Exception as e:
                    logger.error(f"Event handler error: {e}")

        # Propagate to parent if requested
        if propagate:
            parent = self.parent
            if parent:
                parent.emit_event(event_type, data, propagate=True)

    # Signal system access
    def create_signal(self, name: str, signal_type: type = None) -> Signal:
        """Create a new signal for this object."""
        return self._signal_manager.create_signal(name, signal_type)

    def get_signal(self, name: str) -> Optional[Signal]:
        """Get a signal by name."""
        return self._signal_manager.get_signal(name)

    # Lifecycle management
    def destroy(self):
        """Destroy this object and all its children."""
        if self._state == ObjectState.DESTROYED:
            return

        logger.debug(f"Destroying {self._name}")
        self._state = ObjectState.DESTROYING

        # Destroy all children first
        for child in self.children():
            child.destroy()

        # Remove from parent
        parent = self.parent
        if parent:
            parent._remove_child(self)
            self._parent_ref = None

        # Emit destroyed signal if it exists
        destroyed_signal = getattr(self, 'destroyed', None)
        if destroyed_signal is not None:
            try:
                destroyed_signal.emit()
            except Exception:
                pass

        # Cleanup
        self._signal_manager.cleanup()
        self._children.clear()
        self._properties.clear()
        self._event_handlers.clear()

        self._state = ObjectState.DESTROYED
        logger.debug(f"Destroyed {self._name}")

    def __del__(self):
        """Ensure cleanup on garbage collection."""
        if self._state != ObjectState.DESTROYED:
            self.destroy()

    def __repr__(self) -> str:
        parent_name = self.parent._name if self.parent else "None"
        child_count = len(self.children())
        return (
            f"{self.__class__.__name__}(name={self._name}, "
            f"parent={parent_name}, children={child_count}, state={self._state.name})"
        )


class ObjectRegistry:
    """
    Registry for managing global object relationships and lookup.
    Useful for debugging, monitoring, and finding objects across the hierarchy.
    """

    def __init__(self):
        self._objects: Dict[str, weakref.ReferenceType] = {}
        self._lock = threading.RLock()

    def register(self, obj: HierarchicalObject):
        """Register an object in the global registry."""
        with self._lock:
            self._objects[obj.name] = weakref.ref(obj)

    def unregister(self, name: str):
        """Unregister an object."""
        with self._lock:
            self._objects.pop(name, None)

    def find_by_name(self, name: str) -> Optional[HierarchicalObject]:
        """Find an object by name."""
        with self._lock:
            ref = self._objects.get(name)
            return ref() if ref else None

    def find_by_type(self, object_type: Type[T]) -> List[T]:
        """Find all objects of a specific type."""
        with self._lock:
            results = []
            dead_refs = []

            for name, ref in self._objects.items():
                obj = ref()
                if obj is None:
                    dead_refs.append(name)
                elif isinstance(obj, object_type):
                    results.append(obj)

            # Cleanup dead references
            for name in dead_refs:
                del self._objects[name]

            return results

    def all_objects(self) -> List[HierarchicalObject]:
        """Get all registered objects."""
        return self.find_by_type(HierarchicalObject)

    def object_count(self) -> int:
        """Get count of registered objects."""
        return len(self.all_objects())

    def cleanup(self):
        """Remove all dead references."""
        with self._lock:
            dead_refs = []
            for name, ref in self._objects.items():
                if ref() is None:
                    dead_refs.append(name)

            for name in dead_refs:
                del self._objects[name]


# Global registry instance
global_registry = ObjectRegistry()


# Example concrete implementations
class DataContainer(HierarchicalObject):
    """Example container class similar to CCP4's containers."""

    def __init__(self, parent: Optional[HierarchicalObject] = None, name: str = None):
        super().__init__(parent, name)
        self.data_changed = self.create_signal("data_changed", dict)
        self._data: Dict[str, Any] = {}

    def set_data(self, key: str, value: Any):
        """Set data and emit change signal."""
        old_value = self._data.get(key)
        self._data[key] = value
        self.data_changed.emit({"key": key, "old_value": old_value, "new_value": value})

    def get_data(self, key: str, default: Any = None) -> Any:
        """Get data value."""
        return self._data.get(key, default)

    def keys(self) -> List[str]:
        """Get all data keys."""
        return list(self._data.keys())


class TaskRunner(HierarchicalObject):
    """Example task runner class similar to CCP4's plugin system."""

    def __init__(self, task_name: str, parent: Optional[HierarchicalObject] = None):
        super().__init__(parent, f"TaskRunner_{task_name}")
        self.task_started = self.create_signal("task_started", str)
        self.task_finished = self.create_signal("task_finished", dict)
        self.task_failed = self.create_signal("task_failed", dict)
        self._task_name = task_name

    def run_task(self, parameters: Dict[str, Any]):
        """Run a task with given parameters."""
        try:
            self.task_started.emit(self._task_name)
            # Simulate task execution
            result = self._execute_task(parameters)
            self.task_finished.emit({"result": result, "parameters": parameters})
        except Exception as e:
            self.task_failed.emit({"error": str(e), "parameters": parameters})

    def _execute_task(self, parameters: Dict[str, Any]) -> Any:
        """Override in subclasses to implement actual task logic."""
        return {"status": "completed", "parameters": parameters}


# Example usage and testing
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Create a hierarchy
    root = DataContainer(name="RootContainer")

    child1 = DataContainer(parent=root, name="Child1")
    child2 = TaskRunner("test_task", parent=root)

    grandchild = DataContainer(parent=child1, name="GrandChild")

    # Test signals
    def on_data_changed(data):
        print(f"Data changed: {data}")

    child1.data_changed.connect(on_data_changed)
    child1.set_data("test_key", "test_value")

    # Test hierarchy
    print(f"Root children: {[c.name for c in root.children()]}")
    print(f"Child1 path: {child1.path_from_root()}")
    print(f"Descendant count: {root.descendant_count()}")

    # Test path-based access
    print("\n=== Path-Based Access Examples ===")

    # Set up a more complex hierarchy for path testing
    app = DataContainer(name="Application")
    db = DataContainer(parent=app, name="Database")
    tables = DataContainer(parent=db, name="Tables")

    # Create some tables
    users_table = DataContainer(parent=tables, name="Users")
    jobs_table = DataContainer(parent=tables, name="Jobs")

    # Set properties
    users_table.set_property("row_count", 150)
    jobs_table.set_property("row_count", 45)

    # Test path access
    print(f"App path: '{app.object_path()}'")
    print(f"Users table path: '{users_table.object_path()}'")

    # Find by path
    found_table = app.find_by_path("Database.Tables.Users")
    print(f"Found by path: {found_table.name if found_table else 'None'}")

    # Array indexing
    first_table = app.find_by_path("Database.Tables[0]")
    print(f"First table: {first_table.name if first_table else 'None'}")

    # Property access via path
    row_count = app.get_by_path("Database.Tables.Users.row_count")
    print(f"Users row count: {row_count}")

    # Set via path
    app.set_by_path("Database.Tables.Users.description", "User accounts table")
    desc = app.get_by_path("Database.Tables.Users.description")
    print(f"Users description: {desc}")

    # List all paths
    print("\nAll available paths (max depth 3):")
    for path in app.list_paths(max_depth=2):
        print(f"  {path}")

    # Test cleanup
    print("\nDestroying root...")
    app.destroy()
    print("Done!")
