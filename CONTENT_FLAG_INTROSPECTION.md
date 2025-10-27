# Content Flag Introspection Feature

**Date**: 2025-10-27
**Status**: ✅ COMPLETE

## Overview

CDataFile descendants can now automatically detect their `contentFlag` value by introspecting the actual file content. For MTZ files, this is done by reading column labels with gemmi and matching them against the class's `CONTENT_SIGNATURE_LIST`.

## Key Concepts

### Content Flag Indexing

**Important**: Content flag values are **1-indexed** (CONTENT_FLAG_IPAIR = 1, CONTENT_FLAG_FPAIR = 2, etc.), while Python arrays like `CONTENT_SIGNATURE_LIST` are **0-indexed**.

```python
# Content flag constants (1-indexed)
CONTENT_FLAG_IPAIR = 1   # Maps to CONTENT_SIGNATURE_LIST[0]
CONTENT_FLAG_FPAIR = 2   # Maps to CONTENT_SIGNATURE_LIST[1]
CONTENT_FLAG_IMEAN = 3   # Maps to CONTENT_SIGNATURE_LIST[2]
CONTENT_FLAG_FMEAN = 4   # Maps to CONTENT_SIGNATURE_LIST[3]

# Column signatures (0-indexed array)
CONTENT_SIGNATURE_LIST = [
    ['Iplus', 'SIGIplus', 'Iminus', 'SIGIminus'],  # [0] → contentFlag=1
    ['Fplus', 'SIGFplus', 'Fminus', 'SIGFminus'],  # [1] → contentFlag=2
    ['I', 'SIGI'],                                   # [2] → contentFlag=3
    ['F', 'SIGF']                                    # [3] → contentFlag=4
]
```

The introspection code correctly handles this by returning `idx + 1` when a match is found.

## Architecture

### Base Class (CDataFile)

**Location**: `core/base_object/base_classes.py:1193-1249`

```python
def setContentFlag(self, content_flag: Optional[int] = None):
    """
    Set or auto-detect the content flag for this file.

    Args:
        content_flag: If provided, sets contentFlag directly.
                     If None, attempts auto-detection via introspection.
    """
    if content_flag is not None:
        # Explicit assignment
        if hasattr(self, 'contentFlag') and hasattr(self.contentFlag, 'value'):
            self.contentFlag.value = content_flag  # CData wrapper
        else:
            self.contentFlag = content_flag  # Plain int
    else:
        # Auto-detection
        detected_flag = self._introspect_content_flag()
        if detected_flag is not None:
            # ... set contentFlag to detected_flag

def _introspect_content_flag(self) -> Optional[int]:
    """
    Auto-detect content flag by inspecting the file.
    Base implementation returns None (no introspection capability).
    Subclasses override to provide file-type-specific logic.
    """
    return None
```

### MTZ File Classes

**Location**: `core/CCP4XtalData.py`

#### CMiniMtzDataFile (lines 530-600)

```python
class CMiniMtzDataFile(CMiniMtzDataFileStub):
    def _introspect_content_flag(self) -> Optional[int]:
        """Auto-detect contentFlag by reading MTZ columns."""
        from pathlib import Path
        import gemmi

        file_path = self.getFullPath()
        if not file_path or not Path(file_path).exists():
            return None

        # Read MTZ and extract column labels
        mtz = gemmi.read_mtz_file(file_path)
        column_labels = [col.label for col in mtz.columns]
        column_set = set(column_labels)

        # Match against CONTENT_SIGNATURE_LIST
        signature_list = self.__class__.CONTENT_SIGNATURE_LIST
        for idx, required_columns in enumerate(signature_list):
            required_set = set(required_columns)
            if required_set.issubset(column_set):
                return idx + 1  # Convert 0-indexed to 1-indexed!

        return None
```

#### CFreeRDataFile (lines 329-390)

CFreeRDataFile has the same `_introspect_content_flag()` implementation because it **cannot inherit from CMiniMtzDataFile** due to definition order constraints.

### Class Hierarchy

```
CDataFile (base_classes.py)
  ├─ setContentFlag() - Public API
  └─ _introspect_content_flag() - Override in subclasses

CMiniMtzDataFile (CCP4XtalData.py)
  ├─ Inherits: CMiniMtzDataFileStub
  └─ Overrides: _introspect_content_flag() with MTZ logic

CObsDataFile
  ├─ Inherits: CObsDataFileStub, CMiniMtzDataFile
  ├─ CONTENT_SIGNATURE_LIST with 4 signatures
  └─ Inherits _introspect_content_flag() from CMiniMtzDataFile ✓

CFreeRDataFile
  ├─ Inherits: CFreeRDataFileStub (cannot inherit CMiniMtzDataFile)
  ├─ CONTENT_SIGNATURE_LIST with 1 signature
  └─ Implements its own _introspect_content_flag() (duplicated)
```

## Usage

### Auto-Detection

```python
from core.CCP4XtalData import CObsDataFile

# Create file object
obs_file = CObsDataFile(file_path="/path/to/data.mtz")

# Auto-detect contentFlag from file
obs_file.setContentFlag()

# Access the detected value
print(f"Detected contentFlag: {obs_file.contentFlag}")  # Could be int or CData
```

### Explicit Assignment

```python
# Explicitly set contentFlag (backward compatibility)
obs_file.setContentFlag(4)  # Set to FMEAN
```

### Accessing contentFlag Value

The `contentFlag` attribute might be:
- A **CData wrapper** (CInt) with a `.value` attribute
- A **plain int** (depending on how it was assigned)

**Safe access pattern**:
```python
def get_content_flag_value(file_obj):
    """Safely get contentFlag value regardless of type."""
    if hasattr(file_obj.contentFlag, 'value'):
        return file_obj.contentFlag.value
    else:
        return file_obj.contentFlag
```

## Matching Algorithm

### How Introspection Works

1. **Read File**: Use gemmi to open MTZ and extract column labels
2. **Convert to Set**: `column_set = {'H', 'K', 'L', 'Iplus', 'SIGIplus', ...}`
3. **Match Signatures**: Loop through `CONTENT_SIGNATURE_LIST`
4. **Check Subset**: Does the required signature exist in the file's columns?
5. **Return 1-indexed**: If match at index `idx`, return `idx + 1`

### Example Matching

**File**: `/demo_data/gamma/merged_intensities_native.mtz`
**Columns**: `['H', 'K', 'L', 'Iplus', 'SIGIplus', 'Iminus', 'SIGIminus']`

```python
CONTENT_SIGNATURE_LIST = [
    ['Iplus', 'SIGIplus', 'Iminus', 'SIGIminus'],  # [0]
    ['Fplus', 'SIGFplus', 'Fminus', 'SIGFminus'],  # [1]
    ['I', 'SIGI'],                                   # [2]
    ['F', 'SIGF']                                    # [3]
]

# Check signature [0]
required = {'Iplus', 'SIGIplus', 'Iminus', 'SIGIminus'}
file_cols = {'H', 'K', 'L', 'Iplus', 'SIGIplus', 'Iminus', 'SIGIminus'}
required.issubset(file_cols) → True ✓

# Match found at index 0 → return 1 (CONTENT_FLAG_IPAIR)
```

## Classes with Introspection

### Implemented ✅

| Class | CONTENT_SIGNATURE_LIST | Introspection Method |
|-------|------------------------|---------------------|
| **CObsDataFile** | 4 signatures (IPAIR, FPAIR, IMEAN, FMEAN) | Inherits from CMiniMtzDataFile |
| **CPhsDataFile** | 2 signatures (HLA/HLB/HLC/HLD, PHI/FOM) | Inherits from CMiniMtzDataFile |
| **CFreeRDataFile** | 1 signature (FREER) | Own implementation |
| **CMapCoeffsDataFile** | 1 signature (F, PHI) | Inherits from CMiniMtzDataFile |

### Future Extensions

To add introspection to other MTZ file classes:

1. **If already inherits from CMiniMtzDataFile**: ✓ Already has introspection!
2. **If defined before CMiniMtzDataFile**: Add own `_introspect_content_flag()` method
3. **For non-MTZ files**: Override `_introspect_content_flag()` with file-type-specific logic

## Testing

### Test File

**Location**: `tests/test_content_flag_introspection.py`

### Test Data

| File | Type | Columns | Expected contentFlag |
|------|------|---------|---------------------|
| `/ccp4i2/demo_data/gamma/merged_intensities_native.mtz` | CObsDataFile | Iplus, SIGIplus, Iminus, SIGIminus | 1 (IPAIR) |
| `/ccp4i2/demo_data/gamma/freeR.mtz` | CFreeRDataFile | FREER | 1 (FREER) |

### Running Tests

```bash
python -m pytest tests/test_content_flag_introspection.py -v
```

**Result**: ✅ 9 tests passed

### Test Coverage

- ✅ Auto-detection for IPAIR (CObsDataFile)
- ✅ Auto-detection for FREER (CFreeRDataFile)
- ✅ Explicit contentFlag setting
- ✅ Graceful handling of non-existent files
- ✅ Graceful handling of no-match scenarios
- ✅ Annotation lookup matches contentFlag
- ✅ CONTENT_SIGNATURE_LIST structure verification

## Backward Compatibility

### Explicit Setting Still Works

```python
# Old way (still works)
obs_file = CObsDataFile(file_path="/path/to/file.mtz")
obs_file.contentFlag = 4  # Direct assignment

# New way (recommended)
obs_file.setContentFlag(4)  # Explicit via method

# New feature (auto-detection)
obs_file.setContentFlag()  # Auto-detects from file
```

### No Breaking Changes

- Existing code that assigns `contentFlag` directly continues to work
- `setContentFlag()` is a new method that enhances functionality
- Auto-detection is opt-in (only happens when called without arguments)

## Error Handling

The introspection is designed to **fail gracefully**:

1. **File doesn't exist** → Returns `None`, contentFlag unchanged
2. **File can't be read** → Returns `None`, contentFlag unchanged
3. **gemmi not available** → Returns `None`, contentFlag unchanged
4. **No signature matches** → Returns `None`, contentFlag unchanged
5. **Class has no CONTENT_SIGNATURE_LIST** → Returns `None`, contentFlag unchanged

**No exceptions are raised** - introspection silently fails and leaves contentFlag unchanged.

## Implementation Details

### Why Duplicate Code for CFreeRDataFile?

CFreeRDataFile is defined at line 329, but CMiniMtzDataFile is defined at line 530. Python doesn't allow forward references in inheritance, so CFreeRDataFile cannot inherit from CMiniMtzDataFile.

**Solutions considered**:
1. **Reorder classes** - Would break existing code/imports
2. **Split into separate files** - Too much refactoring
3. **Duplicate the method** ← Chosen (pragmatic, low risk)

The duplication is **intentional and documented** with a comment in the code.

### Definition Order Constraints

From `MULTIPLE_INHERITANCE_APPLIED.md`, we know that 27 classes cannot use multiple inheritance due to definition order. CFreeRDataFile is one of them (line 80 in that document).

## Future Enhancements

### 1. Support More File Types

Add `_introspect_content_flag()` to:
- **CPdbDataFile**: Check for ATOM/HETATM records, determine if ensemble
- **CCifDataFile**: Parse mmCIF categories
- **CImageFileFormats**: Determine detector type from headers

### 2. More Sophisticated Matching

Current matching uses simple subset matching. Could be enhanced with:
- **Column type checking** (not just labels)
- **Weighted scoring** (prefer matches with more required columns)
- **Ambiguity detection** (warn if multiple signatures match)

### 3. Logging Support

Currently errors are silently ignored. Could add:
```python
import logging
logger = logging.getLogger(__name__)

try:
    mtz = gemmi.read_mtz_file(file_path)
except Exception as e:
    logger.debug(f"Failed to read MTZ file: {e}")
    return None
```

## Related Documentation

- **BASE_CLASS_DECISION.md** - Why CDataFile remains hand-written
- **MTZ_CONVERSION_SYSTEM.md** - MTZ file conversion methods
- **CONTENT_FLAGS_SUBTYPES_COMPLETE.md** - All content flags and subtypes
- **STUB_IMPLEMENTATION_INHERITANCE_PATTERN.md** - Multiple inheritance pattern
- **MULTIPLE_INHERITANCE_APPLIED.md** - Which classes use multiple inheritance

## Summary

✅ **Complete Implementation** of automatic content flag introspection:
- Generic `setContentFlag()` method in CDataFile base class
- MTZ-specific `_introspect_content_flag()` in CMiniMtzDataFile and CFreeRDataFile
- Correctly handles 1-indexed content flags vs 0-indexed signature arrays
- 9 comprehensive tests covering all scenarios
- Backward compatible with existing code
- Graceful error handling

The feature enables **intelligent file auto-detection** while maintaining **backward compatibility** and **safety**.
