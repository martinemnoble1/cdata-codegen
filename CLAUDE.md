# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**cdata-codegen** is a Python code generation framework for migrating legacy CCP4i2 crystallographic software from Qt-based C++/Python to modern, Qt-free Python. The system generates type-safe data classes from JSON metadata specifications while providing modern replacements for Qt's hierarchy, signal/slot, and event systems.

### Key Architectural Components

1. **Metadata-Driven Generation**: 212+ classes defined declaratively in `migration/CData/cdata.json`
2. **Base Object System**: `core/base_object/` provides the foundational architecture
   - `HierarchicalObject`: Parent-child relationships with weak references (replaces QObject)
   - `CData`: Base class with metadata-driven attribute management
   - Fundamental types: `CInt`, `CFloat`, `CString`, `CBoolean`, `CList`
3. **Modern Python Systems**: Qt-free replacements in `core/base_object/`
   - `signal_system.py`: Type-safe signals/slots with async support
   - `hierarchy_system.py`: Thread-safe object lifecycle management
   - `event_system.py`: Async event loop and task scheduling
4. **Plugin System**: 148 legacy ccp4i2 plugins accessible via lazy-loading registry
   - `wrappers/`, `wrappers2/`, `pipelines/` - **LOCKED legacy code, do not modify**
   - `core/task_manager/plugin_registry.py` - **LOCKED, pre-generated from legacy ccp4i2**

### IMPORTANT: Locked Directories

The following directories contain **locked legacy code** from ccp4i2 and should **NOT be modified**:

- **`wrappers/`** - 115+ plugin wrappers from legacy ccp4i2
- **`wrappers2/`** - Additional legacy plugin wrappers
- **`pipelines/`** - Multi-step pipeline plugins
- **`demo_data/`** - Test data files from legacy ccp4i2

**Plugin Registry Files (LOCKED - do not regenerate):**
- `core/task_manager/plugin_registry.py` (344KB, 148 plugins)
- `core/task_manager/plugin_lookup.json` (449KB, 148 plugins)

These were pre-generated from a full ccp4i2 environment and should remain unchanged. See `core/task_manager/README.md` for details.

### CCP4I2_ROOT Environment Variable

**CRITICAL**: All tests and the plugin system require `CCP4I2_ROOT` to be set to the project root:

```bash
export CCP4I2_ROOT=/Users/nmemn/Developer/cdata-codegen
```

This allows the system to find plugins in `wrappers/`, `wrappers2/`, and `pipelines/` directories.

## Development Commands

### Environment Setup
```bash
# Activate virtual environment (Python 3.11+)
source .venv/bin/activate

# Install dependencies
pip install autopep8 pytest
```

### Code Generation
```bash
# Generate stub files from cdata.json metadata
python migration/CData/generate_new_files.py

# Output: core/cdata_stubs/*Stub.py files with @cdata_class decorators
```

### Testing
```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_ccontainer.py

# Run single test
pytest tests/test_stubs.py::TestStubs::test_basic_import -v

# Run with output
pytest tests/ -v -s
```

### Code Quality
```bash
# Format generated code (automatically run by generate_new_files.py)
autopep8 --in-place <file>
```

## Code Architecture

### Base Class Hierarchy

```
HierarchicalObject (hierarchy_system.py)
  └── CData (base_classes.py)
       ├── CDataFileContent - Base for file content classes
       ├── CDataFile - File attributes and factory pattern
       ├── CContainer - List-like heterogeneous collections
       └── Fundamental Types:
           ├── CInt, CFloat, CString, CBoolean
           └── CList (homogeneous typed collections)
```

### Code Generation Workflow

1. **Source**: `migration/CData/cdata.json` contains comprehensive metadata for 212 classes:
   - `CONTENTS`: Field definitions with types
   - `QUALIFIERS`: Configuration parameters (constraints, defaults, GUI hints)
   - `ERROR_CODES`: Domain-specific error definitions
   - `QUALIFIERS_DEFINITION`: Type information and constraints

2. **Generation**: `migration/CData/generate_new_files.py`
   - Groups classes by source file (e.g., all ModelData classes together)
   - Topologically sorts to place base classes before subclasses
   - Renders Python with `@cdata_class()` decorators
   - Auto-formats with autopep8
   - **Output**: `core/cdata_stubs/*Stub.py`

3. **Manual Implementation**: Developers create `core/CCP4*.py` files
   - Extend stub classes with domain logic
   - Add file I/O operations
   - Implement business rules

### Critical Patterns

#### 1. Metadata Decorator System
All CData classes use the `@cdata_class()` decorator:

```python
@cdata_class(
    attributes={"field_name": attribute(AttributeType.STRING, tooltip="Help text")},
    qualifiers={"min": 0, "max": 100, "allowUndefined": True, "saveToDb": False},
    error_codes={"101": {"description": "File not found", "severity": 2}},
    qualifiers_definition={"min": {"type": int, "description": "Inclusive minimum"}},
    gui_label="Display Name"
)
class MyClass(CData):
    pass
```

**Important**: Decorators must be placed before class definitions. The decorator system registers metadata that drives validation, GUI generation, and serialization.

#### 2. Value State Tracking
Every field tracks three states:
- `ValueState.NOT_SET` - Never explicitly assigned
- `ValueState.DEFAULT` - Using default from qualifiers
- `ValueState.EXPLICITLY_SET` - Assigned by user

Methods: `isSet()`, `unSet()`, `getValueState()`, `setToDefault()`

#### 3. Smart Assignment
CData supports intelligent type conversions:

```python
# Primitive to wrapped type
cint_obj.value = 42

# Dict to CData
data_obj.config = {"key": "value"}  # Creates CData from dict

# CData to CData (updates in-place if exists)
data1.my_field = data2
```

#### 4. Hierarchical Object Paths
Objects maintain their position in the hierarchy:

```python
container = CContainer(name="root")
item = CInt(name="counter")
container.add_item(item)
print(item.object_path())  # "root.counter"
```

#### 5. Qualifier System
Qualifiers provide:
- **Constraints**: `min`, `max`, `minlength`, `maxlength`, `enumerators`
- **GUI Hints**: `guiLabel`, `toolTip`, `guiDefinition`
- **Persistence**: `saveToDb`, `allowUndefined`
- **File Handling**: `fileExtensions`, `mimeTypeName`, `mustExist`

Access via: `get_qualifier(key)`, `set_qualifier(key, value)`, `get_merged_metadata('qualifiers')`

## File Organization

### Key Directories

- **`core/base_object/`** - Base architecture (CData, HierarchicalObject, signals, events)
- **`core/cdata_stubs/`** - Auto-generated stub files (do not manually edit)
- **`core/CCP4*.py`** - Manual implementations extending stubs
- **`migration/CData/`** - Code generation tools and metadata source
- **`tests/`** - Test suite (pytest-based)
- **`generated_cdata_classes_by_file/`** - Alternative output format grouping by source file

### Important Files

- **`migration/CData/cdata.json`** - Source of truth (796KB, 212 classes)
- **`migration/CData/generate_new_files.py`** - Primary stub generator
- **`core/base_object/base_classes.py`** - CData, CContainer, CDataFile, CDataFileContent
- **`core/base_object/fundamental_types.py`** - CInt, CFloat, CString, CBoolean, CList
- **`core/base_object/class_metadata.py`** - `@cdata_class` decorator and registry
- **`core/base_object/hierarchy_system.py`** - HierarchicalObject (Qt replacement)
- **`core/base_object/signal_system.py`** - Signal/slot system (Qt replacement)

## Development Workflow

### Adding New CData Classes

1. Update `migration/CData/cdata.json` with class metadata
2. Run `python migration/CData/generate_new_files.py`
3. Review generated stub in `core/cdata_stubs/`
4. Create manual implementation in `core/` (if needed)
5. Write tests in `tests/`
6. Run `pytest tests/`

### Modifying Existing Classes

1. **For stub changes**: Update `cdata.json` and regenerate
2. **For implementation changes**: Edit manual files in `core/`
3. **Never manually edit stub files** - they will be overwritten

### Working with Hierarchies

- Use `HierarchicalObject` for parent-child relationships
- Always use weak references to prevent memory leaks
- Object lifecycle: CREATED → INITIALIZED → ACTIVE → DESTROYING → DESTROYED
- Call `set_parent()` or pass `parent=` in `__init__`
- Use `object_path()` for debugging hierarchies

### Signal System Usage

Replace Qt signals with modern Python:

```python
from core.base_object.signal_system import Signal

class MyClass(HierarchicalObject):
    def __init__(self):
        super().__init__()
        self.my_signal = Signal[dict]()

    def do_something(self):
        self.my_signal.emit({"status": "complete"})

# Connect
obj.my_signal.connect(lambda data: print(data))

# Async support
await obj.my_signal.emit_async({"status": "complete"})
```

## Common Pitfalls

1. **Don't manually edit stub files** - Changes will be overwritten on next generation
2. **Always activate venv** - Use `source .venv/bin/activate` before running commands
3. **Topological ordering matters** - Base classes must be defined before subclasses in stubs
4. **Weak references** - Use `weakref` for parent references to prevent memory leaks
5. **Value state semantics** - Check `isSet()` before assuming a field has a value
6. **Qualifier inheritance** - Subclasses inherit and can override parent qualifiers
7. **Import paths** - Generated stubs use absolute imports from `core.base_object`

## Testing Patterns

### Testing CData Classes
```python
def test_cdata_assignment():
    obj = CInt(10, name="test")
    assert obj.value == 10
    assert obj.isSet("value")
    obj.unSet("value")
    assert not obj.isSet("value")
```

### Testing Hierarchies
```python
def test_hierarchy():
    parent = CContainer(name="parent")
    child = CInt(5, name="child")
    parent.add_item(child)
    assert child.get_parent() == parent
    assert child.object_path() == "parent.child"
```

### Testing Qualifiers
```python
def test_qualifiers():
    obj = CInt(name="bounded")
    obj.set_qualifier("min", 0)
    obj.set_qualifier("max", 100)
    with pytest.raises(ValueError):
        obj.value = 150  # Should violate max
```

## Migration Context

This project migrates CCP4i2 from Qt dependencies to pure Python:

- **Qt signals/slots** → `signal_system.py` with async support
- **QObject hierarchy** → `HierarchicalObject` with weak references
- **QEventLoop** → `event_system.py` with asyncio
- **Qt property system** → Qualifier system with decorators
- **C++ types** → Python fundamental types (CInt, CFloat, etc.)

The goal is metadata-driven, type-safe data modeling without Qt overhead.
