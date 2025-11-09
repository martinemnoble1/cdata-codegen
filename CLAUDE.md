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

**Plugin Registry Files (can be regenerated):**
- `core/task_manager/plugin_registry.py` (~67KB, 144 plugins)
- `core/task_manager/plugin_lookup.json` (~460KB, 144 plugins)

These files are generated from the local plugins in `wrappers/`, `wrappers2/`, and `pipelines/` directories. They can be safely regenerated:

```bash
export CCP4I2_ROOT=/Users/nmemn/Developer/cdata-codegen
.venv/bin/python core/task_manager/plugin_lookup.py
```

**Important Notes:**
- The registry contains ~145 plugins that can be successfully imported
- Legacy ccp4-python dependencies (`ccp4mg`, `mmdb2`, `ccp4srs`) are provided as minimal stubs in `stubs/` directory
- Plugins requiring Qt GUI components (`qtgui`) are skipped during import
- The registry automatically handles module paths relative to CCP4I2_ROOT
- See `core/task_manager/README.md` for full details on plugin discovery and registration

**Stub Modules:**
The `stubs/` directory contains minimal stub implementations for legacy ccp4-python modules:
- `ccp4mg.py` - CCP4 Molecular Graphics (imported but not used by acedrgNew)
- `mmdb2.py` - Macromolecular Database (provides constants and stub classes)
- `ccp4srs.py` - Structure Refinement Suite (provides stub Manager, Graph, GraphMatch)

These stubs allow plugins like `acedrgNew` to import successfully. The stubs raise `NotImplementedError` if their methods are actually called, which is acceptable since most tests don't exercise the atom matching functionality that requires them.

### CCP4I2_ROOT Environment Variable

**CRITICAL**: All tests and the plugin system require `CCP4I2_ROOT` to be set to the project root:

```bash
export CCP4I2_ROOT=/Users/nmemn/Developer/cdata-codegen
```

This allows the system to find plugins in `wrappers/`, `wrappers2/`, and `pipelines/` directories.

## Development Commands

### Environment Setup

**Flexible CCP4 Environment Configuration:**

The project supports testing with multiple Python/CCP4 versions via a `.env` configuration file:

```bash
# Check current environment
./switch_env.sh status

# Switch to Python 3.9 (CCP4-9, older stable)
./switch_env.sh py39

# Switch to Python 3.11 (CCP4-20251105, newer)
./switch_env.sh py311
```

**Environment Files:**
- `.env` - Active configuration (used by `run_test.sh`)
- `.env.py39` - Python 3.9 configuration (CCP4-9 at `/Applications/ccp4-9` + `.venv.old-py39`)
- `.env.py311` - Python 3.11 configuration (CCP4-20251105 at `../ccp4-20251105` + `.venv`)
- `.env.example` - Template with both options documented

**Initial Setup for Python 3.11:**
```bash
# Install dependencies
pip install autopep8 pytest

# Symlink mrbump module from CCP4 distribution
# Required for MrBUMP pipeline tests
ln -sf /Users/nmemn/Developer/ccp4-20251105/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/mrbump .venv/lib/python3.11/site-packages/mrbump
```

**Initial Setup for Python 3.9:**
```bash
# Create separate virtual environment
/Applications/ccp4-9/bin/ccp4-python -m venv .venv.old-py39
source .venv.old-py39/bin/activate

# Install dependencies
pip install autopep8 pytest

# Symlink mrbump module from CCP4-9
ln -sf /Applications/ccp4-9/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/mrbump .venv.old-py39/lib/python3.9/site-packages/mrbump
```

**Why Multiple Environments?**
- Compare test results between Python 3.9 and 3.11
- Identify version-specific bugs vs. code regressions
- Test against both older stable (CCP4-9) and newer (CCP4-20251105) CCP4 distributions

### Code Generation
```bash
# Generate stub files from cdata.json metadata
python migration/CData/generate_new_files.py

# Output: core/cdata_stubs/*Stub.py files with @cdata_class decorators
```

### Testing
```bash
# IMPORTANT: Always use ./run_test.sh for i2run tests to ensure CCP4 environment is set
./run_test.sh i2run/test_file.py::test_name

# i2run test examples (MUST use run_test.sh)
./run_test.sh i2run/test_csymmatch.py::test_8xfm
./run_test.sh i2run/test_parrot.py::test_parrot
./run_test.sh i2run/test_mrbump.py::test_mrbump
./run_test.sh i2run/test_servalcat.py::test_8xfm

# Run all tests (non-i2run)
pytest tests/

# Run specific test file
pytest tests/test_ccontainer.py

# Run single test
pytest tests/test_stubs.py::TestStubs::test_basic_import -v

# Run with output
pytest tests/ -v -s
```

**CRITICAL**: i2run tests MUST be run with `./run_test.sh` which:
- Sources CCP4 environment (`/Applications/ccp4-9/bin/ccp4.setup-sh`)
- Sets required environment variables ($CLIBD, $CCP4I2_ROOT, etc.)
- Activates the Python virtual environment
- Sets DJANGO_SETTINGS_MODULE

Running i2run tests directly with pytest will fail due to missing CCP4 environment variables.

**Test Directory Structure - Sub-jobs:**
Pipelines create sub-jobs with nested directory structures:
```
CCP4_JOBS/job_1/           # Main pipeline job
  job_1/                   # First sub-job (e.g., acedrgNew called by LidiaAcedrgNew)
    MOLOUT.mol            # Sub-job output files
  job_2/                   # Second sub-job (if any)
  input_params.xml         # Main job parameters
  params.xml
```

**IMPORTANT for debugging**: Paths like `/job_1/job_1/MOLOUT.mol` are CORRECT - not a bug! The first `job_1` is the pipeline, the second `job_1` is the sub-job created by `makePluginObject()`. Don't be confused by the apparent duplication when debugging file-not-found errors.

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

#### 3a. Legacy API Compatibility
CData provides legacy camelCase method aliases for backward compatibility with ccp4i2 plugin code:

```python
# Modern API (preferred)
obj.set_qualifier('allowUndefined', True)
obj.get_qualifier('allowUndefined')

# Legacy API (for compatibility)
obj.setQualifier('allowUndefined', True)  # Alias for set_qualifier()
obj.qualifiers('allowUndefined')           # Shorthand for get_qualifier()
```

**Note**: New code should use the modern underscore API (`set_qualifier`, `get_qualifier`). The camelCase methods (`setQualifier`) are provided only for backward compatibility with locked legacy plugin code.

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

## Legacy Code Type Coercion

**IMPORTANT - Post-Migration TODO**: The CData system currently performs **automatic type conversion** when assigning string values to typed fields (CInt, CFloat, CBoolean). This was implemented to support legacy plugin code patterns like:

```python
# Legacy code pattern (BAD PRACTICE - found in molrep_pipe.py:280)
self.refmac.container.controlParameters.NCYCLES = str(self.container.inputData.REFMAC_NCYC)
```

Where `NCYCLES` is defined as a `CInt`, but the code explicitly converts to string before assignment.

**Current Behavior** (implemented in `core/base_object/cdata.py:905-953`):
- Assigning `"10"` (string) to a CInt field → automatically converts to `10` (int)
- Assigning `"3.14"` (string) to a CFloat field → automatically converts to `3.14` (float)
- Assigning `"true"` (string) to a CBoolean field → automatically converts to `True` (bool)

**Why This Is Questionable**:
1. **Hides bugs** - Code should fail loudly when types don't match
2. **Unclear intent** - Why is the legacy code doing `str(int_value)` in the first place?
3. **Python philosophy violation** - "Explicit is better than implicit"
4. **Type safety erosion** - The whole point of CInt/CFloat is type enforcement

**Post-Migration Action Items**:
1. **Audit locked legacy code** - Find all instances of explicit string conversion (`str(...)`) before assignment
2. **Understand intent** - Was this for XML serialization? String formatting? Or just confused?
3. **Decision point**:
   - Option A: Keep automatic conversion with deprecation warnings
   - Option B: Make it strict and fix all legacy code violations
   - Option C: Add a migration flag to control behavior (strict vs. permissive)

**Current Status**: Being **permissive** to enable test passage during migration. After migration is complete, revisit this design decision.

**Example of proper code**:
```python
# Good - direct integer assignment
self.refmac.container.controlParameters.NCYCLES = self.container.inputData.REFMAC_NCYC.value

# Also good - explicit int
self.refmac.container.controlParameters.NCYCLES = 10
```

## Known Limitations and Missing Dependencies

### Legacy CCP4-Python Dependencies

**Stub Modules Solution:**
Legacy ccp4-python dependencies are provided as minimal stubs in the `stubs/` directory, allowing plugins like `acedrgNew` to import successfully:
- `ccp4mg` - CCP4 Molecular Graphics (imported but not actually used)
- `mmdb2` - Macromolecular Database (stub constants and classes)
- `ccp4srs` - Structure Refinement Suite (stub Manager, Graph, GraphMatch)

The stubs are sufficient for basic plugin operation but raise `NotImplementedError` if atom-matching functionality is actually invoked.

**Plugins requiring `qtgui` (Qt GUI components):**
- Various GUI-related plugins are skipped during registry generation
- These were only needed for the Qt-based CCP4i2 GUI
- Backend functionality works without them

**Plugins requiring `mmut` (mmCIF utilities):**
- Some phasing pipelines (`phaser_rnp_pipeline`, `phaser_simple`)
- Use alternative wrappers or pipelines when available

### Known Test Limitations

1. **Wrapper-specific issues** - Some wrappers may have legacy code assumptions
   - Example: `freerflag` writing invalid `RESOL 0.0` for unset parameters causing segfaults
   - Status: Legacy wrapper behavior - cannot modify locked code

2. **Atom matching functionality** - Tests that use acedrgNew's atom matching features will fail
   - The stub modules allow import but don't implement full ccp4srs graph matching
   - Most basic acedrg tests work fine without atom matching

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
