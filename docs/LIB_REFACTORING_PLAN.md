# server/ccp4x/lib Refactoring Plan

## Executive Summary

The `server/ccp4x/lib` directory contains ~76 Python files with significant duplication between:
1. **Modern CData-aware utilities** ([cdata_utils.py](../server/ccp4x/lib/cdata_utils.py:1)) - 514 lines
2. **Legacy container traversal** ([utils/containers/find_objects.py](../server/ccp4x/lib/utils/containers/find_objects.py:1)) - 122 lines
3. **Two parameter setting implementations**:
   - [utils/parameters/set_param.py](../server/ccp4x/lib/utils/parameters/set_param.py:1) - 180 lines (CPluginScript + dbHandler architecture)
   - [utils/parameters/set_parameter.py](../server/ccp4x/lib/utils/parameters/set_parameter.py:1) - 178 lines (Direct container manipulation)

**Goal**: Eliminate duplication, move database-independent logic to core CData methods, consolidate to single source of truth for each operation.

---

## Current State Analysis

### Category 1: Container Traversal & Search

#### Duplicated Functionality

**Modern (cdata_utils.py)**:
- `find_all_files(container)` - Uses `children()` method, returns CDataFile list
- `find_objects_by_type(container, target_type)` - Uses `children()`, type-safe
- `find_objects_matching(container, predicate)` - Uses `childNames()`, predicate-based

**Legacy (utils/containers/find_objects.py)**:
- `find_objects(within, func, multiple)` - Uses `CONTENTS` attribute, lambda predicates
- `find_object_by_path(base_element, object_path)` - Dot-path navigation

#### Usage Analysis

**cdata_utils imports** (modern, database-aware):
- `server/ccp4x/lib/async_import_files.py` - file harvesting
- `server/ccp4x/db/async_db_handler.py` - DB synchronization

**find_objects imports** (legacy, still widely used):
- `server/ccp4x/lib/utils/parameters/set_input_by_context.py`
- `server/ccp4x/lib/utils/parameters/unset_output_data.py`
- `server/ccp4x/lib/utils/files/digest.py`
- `server/ccp4x/lib/utils/files/import_files.py`
- `server/ccp4x/lib/utils/jobs/i2run.py`
- `server/ccp4x/i2run/CCP4i2RunnerBase.py`

**Key Observation**: `find_object_by_path()` is heavily used in i2run and parameter setting. This is database-independent and should become a core CData/CContainer method.

---

### Category 2: Parameter Setting

#### Duplicate Implementations

**1. set_param.py** (Modern, DB-aware):
```python
def set_parameter(job: models.Job, object_path: str, value) -> Result[Dict]:
    """Uses CPluginScript + dbHandler for:
    - File handling with DB awareness (CDataFile.setFullPath())
    - Database synchronization (dbHandler.updateJobStatus())
    - XML persistence (saveDataToXml)
    """
```

**2. set_parameter.py** (Legacy, direct manipulation):
```python
def set_parameter(job: models.Job, object_path: str, value):
    """Direct container manipulation:
    - Calls set_parameter_container() directly
    - Saves params.xml directly
    - Returns JSON-encoded object
    """
```

#### Key Differences

| Feature | set_param.py (Modern) | set_parameter.py (Legacy) |
|---------|----------------------|---------------------------|
| **Architecture** | CPluginScript + dbHandler | Direct container access |
| **DB sync** | Yes (`dbHandler.updateJobStatus()`) | No |
| **File handling** | CDataFile.setFullPath() with DB | Direct .set() |
| **XML saving** | plugin.saveDataToXml() (filtered) | Direct XML write |
| **Return type** | `Result[Dict]` | JSON dict |
| **Error handling** | Structured Result pattern | Exception-based |

#### Usage

Both are imported by different parts of the codebase. **Recommendation**: Consolidate to `set_param.py` (modern) and deprecate `set_parameter.py`.

---

### Category 3: File Metadata Extraction

#### Modern Approach (cdata_utils.py)

```python
def extract_file_metadata(file_obj: CDataFile) -> Dict[str, Any]:
    """
    Uses CData metadata system:
    - get_qualifier() for guiLabel, toolTip
    - get_file_type_from_class() for MIME type mapping
    - isSet() checks for all attributes
    - Returns structured dict
    """
```

**Recommendation**: This is good as-is, but consider moving to CDataFile as an instance method:

```python
class CDataFile:
    def get_metadata_dict(self) -> Dict[str, Any]:
        """Extract all metadata as dict for serialization/DB storage"""
```

---

### Category 4: Container Utilities (database-independent)

**Files in `server/ccp4x/lib/utils/containers/`**:
- `get_container.py` - `get_job_container(job)` - **DB-dependent**, keep in lib
- `json_encoder.py` - CCP4i2JsonEncoder - **Core serialization**, move to core?
- `json_for_container.py` - JSON conversion - **Core serialization**, move to core?
- `validate.py` - Container validation - **Could be CContainer method**
- `remove_defaults.py` - Filter unset values - **Could be CContainer method**

---

## Refactoring Strategy

### Phase 1: Consolidate Path Navigation (Database-Independent)

**Action**: Move `find_object_by_path()` to core as a CContainer method

**Rationale**:
- Used in 10+ files across server/ccp4x
- Pure CData hierarchy traversal (no DB dependency)
- Natural fit as instance method on CContainer

**Implementation**:
```python
# In core/CCP4Container.py
class CContainer(CData):
    def find_by_path(self, path: str, skip_first: bool = True):
        """
        Find a descendant object by dot-separated path.

        Args:
            path: Dot-separated path (e.g., "controlParameters.NCYCLES")
            skip_first: If True, skip first element (legacy task name compatibility)

        Returns:
            The found CData object

        Raises:
            AttributeError: If path not found
        """
        # Move logic from find_object_by_path here
```

**Migration**:
1. Add method to CContainer
2. Update `find_objects.py` to call container.find_by_path() (backward compat wrapper)
3. Gradually migrate call sites to use method directly

---

### Phase 2: Consolidate Parameter Setting (Migrate to Modern)

**Action**: Deprecate `set_parameter.py`, consolidate to `set_param.py`

**Rationale**:
- `set_param.py` has proper DB synchronization via dbHandler
- Uses CPluginScript architecture (correct lifecycle)
- Returns structured Result type
- Handles file parameters correctly with DB awareness

**Migration**:
1. Audit all imports of `set_parameter.py`
2. Replace with `set_param.py` imports
3. Update call sites to handle Result type
4. Mark `set_parameter.py` as deprecated with migration notice

---

### Phase 3: Promote Container Search to Core

**Action**: Add search methods to CContainer/CData base classes

**Rationale**:
- `find_all_files()`, `find_objects_by_type()` are generic CData operations
- No database dependency
- Natural instance methods

**Implementation**:
```python
# In core/CCP4Container.py or core/base_object/cdata.py
class CData:
    def find_children_by_type(self, target_type: Type) -> List[Any]:
        """Find all descendant objects of specific type"""

    def find_children_matching(self, predicate: Callable) -> List[Any]:
        """Find all descendants matching predicate"""

class CContainer(CData):
    def find_all_files(self) -> List[CDataFile]:
        """Find all CDataFile descendants in hierarchy"""
```

**Migration**:
1. Add methods to core classes
2. Update `cdata_utils.py` to call these methods (backward compat wrappers)
3. Gradually migrate direct call sites

---

### Phase 4: Move Metadata Extraction to CDataFile

**Action**: Convert `extract_file_metadata()` to instance method

**Implementation**:
```python
# In core/base_object/cdata_file.py
class CDataFile(CData):
    def to_metadata_dict(self) -> Dict[str, Any]:
        """
        Extract complete metadata as dict for DB storage/serialization.

        Replaces cdata_utils.extract_file_metadata().
        """
        # Move logic from cdata_utils.py here
```

**Benefits**:
- More discoverable (obj.to_metadata_dict() vs util function)
- Encapsulation (metadata extraction logic lives with file object)
- Easier testing (mock file object, call method)

---

### Phase 5: Container Utilities Assessment

**Review each file in `utils/containers/` for core migration**:

#### Keep in server/ccp4x/lib (DB-dependent):
- `get_container.py` - Loads from Job model + XML files
- Anything using Django models

#### Consider moving to core:
- `json_encoder.py` - CCP4i2JsonEncoder (core serialization)
- `json_for_container.py` - JSON conversion utilities
- `validate.py` - Container validation (if DB-independent)
- `remove_defaults.py` - Filter unset values (pure CData logic)

**Criterion**: If it doesn't touch Django models or database, it belongs in core.

---

## Migration Path Summary

### Step 1: Core CData Enhancements (No Breaking Changes)
```python
# Add new methods to core classes (backward compatible)
CContainer.find_by_path(path)
CContainer.find_all_files()
CData.find_children_by_type(type)
CData.find_children_matching(predicate)
CDataFile.to_metadata_dict()
```

### Step 2: Update server/ccp4x/lib Wrappers
```python
# Update cdata_utils.py to call core methods
def find_all_files(container):
    """Deprecated: Use container.find_all_files() instead"""
    return container.find_all_files()

# Update find_objects.py to call core methods
def find_object_by_path(base_element, object_path):
    """Deprecated: Use container.find_by_path() instead"""
    return base_element.find_by_path(object_path)
```

### Step 3: Parameter Setting Consolidation
```python
# Deprecate set_parameter.py, use set_param.py everywhere
# Add deprecation warnings to old module
```

### Step 4: Gradual Migration
- Update call sites file-by-file
- Run tests after each migration
- Keep deprecated wrappers for compatibility during transition

### Step 5: Cleanup
- Remove deprecated modules
- Update imports
- Add migration guide to CLAUDE.md

---

## Benefits

### 1. Single Source of Truth
- One implementation per operation
- Easier to maintain and debug
- No confusion about which version to use

### 2. Better Encapsulation
- Core CData operations live in core classes
- Database-specific logic stays in server/ccp4x
- Clear architectural boundaries

### 3. Improved Discoverability
```python
# Before (scattered utilities)
from server.ccp4x.lib.cdata_utils import find_all_files
files = find_all_files(container)

# After (instance methods)
files = container.find_all_files()  # IDE autocomplete works!
```

### 4. Easier Testing
```python
# Test core methods without database
def test_find_by_path():
    container = CContainer()
    # ... setup ...
    obj = container.find_by_path("child.grandchild")
    assert obj.name == "grandchild"
```

### 5. Reduced Duplication
- ~300 lines of duplicated traversal code consolidated
- Single parameter setting implementation
- Metadata extraction as instance method

---

## Risks and Mitigation

### Risk 1: Breaking Changes
**Mitigation**: Keep backward-compat wrappers during transition, deprecate gradually

### Risk 2: Performance Regression
**Mitigation**: Benchmark before/after, optimize core methods if needed

### Risk 3: Incomplete Migration
**Mitigation**: Track migration progress, use deprecation warnings to find stragglers

### Risk 4: Test Coverage Gaps
**Mitigation**: Add tests for new core methods before removing old utilities

---

## Implementation Timeline

### Week 1: Core Method Addition
- Add find_by_path() to CContainer
- Add search methods to CData
- Add to_metadata_dict() to CDataFile
- Write tests for new methods

### Week 2: Wrapper Updates
- Update cdata_utils.py wrappers
- Update find_objects.py wrappers
- Add deprecation warnings
- Update documentation

### Week 3: Parameter Setting Consolidation
- Audit set_parameter.py usage
- Migrate to set_param.py
- Test all parameter setting paths

### Week 4: Gradual Call Site Migration
- Migrate high-traffic files first
- Run comprehensive tests
- Monitor for regressions

### Week 5: Cleanup
- Remove deprecated modules
- Update CLAUDE.md with migration guide
- Final testing

---

## Files to Modify

### Core (add methods, no breaking changes):
- `core/CCP4Container.py` - add find_by_path(), find_all_files()
- `core/base_object/cdata.py` - add find_children_by_type(), find_children_matching()
- `core/base_object/cdata_file.py` - add to_metadata_dict()

### Server (deprecate/consolidate):
- `server/ccp4x/lib/cdata_utils.py` - convert to wrappers with deprecation warnings
- `server/ccp4x/lib/utils/containers/find_objects.py` - convert to wrappers
- `server/ccp4x/lib/utils/parameters/set_parameter.py` - deprecate, redirect to set_param.py
- Update all import sites (~20+ files)

### Documentation:
- `CLAUDE.md` - add refactoring migration guide
- This document - track progress

---

## Success Criteria

1. ✅ All container traversal uses core CData methods
2. ✅ Single parameter setting implementation (set_param.py)
3. ✅ No duplication between cdata_utils.py and find_objects.py
4. ✅ All tests passing after migration
5. ✅ Clear deprecation path for old utilities
6. ✅ Updated documentation

---

## Questions for User

1. **Timeline**: Should we proceed with this refactoring incrementally (backward-compatible wrappers), or do a coordinated migration?

2. **Parameter Setting**: Confirm that `set_param.py` (CPluginScript + dbHandler architecture) is the correct modern approach to keep?

3. **JSON Serialization**: Should `CCP4i2JsonEncoder` move to core, or stay in server/ccp4x/lib? (It's currently DB-independent but server-specific)

4. **Priority**: Which category should we tackle first?
   - Container traversal (most widely used)
   - Parameter setting (two implementations)
   - Metadata extraction (cleanest to migrate)

5. **Testing**: Do we need additional integration tests before starting migration?

---

## Next Steps

After user confirmation:
1. Create feature branch `refactor/lib-consolidation`
2. Start with Phase 1 (path navigation to core)
3. Write tests for new core methods
4. Migrate one high-traffic file as proof-of-concept
5. Get feedback before proceeding to other phases
