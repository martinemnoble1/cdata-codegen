# loadFile() Implementation Plan

## Executive Summary

This document outlines the systematic implementation of `loadFile()` methods for CDataFile and CDataFileContent classes, replacing legacy code that uses:
- **mmdb2** → **gemmi** for coordinates
- **hklfile (ccp4mg)** → **gemmi** for reflections
- **Direct `__dict__` manipulation** → **Proper CData attribute setters**

## Current Legacy Pattern (ccp4i2)

### CDataFile.loadFile() (CCP4File.py:714-736)

```python
def loadFile(self, initialise=False):
    rv = CErrorReport()
    if self.BLOCK_LOAD_FILES:
        return
    if self.qualifiers('fileContentClassName') is None:
        return

    # ⚠️ DIRECT __dict__ ACCESS
    if self.__dict__['_fileContent'] is None or initialise:
        self.__dict__['_fileContent'] = self.fileContentClass()(parent=self, name='fileContent')

    if self.fullPath.exists() and self.fullPath.isfile():
        try:
            # Delegates to content class
            self.__dict__['_fileContent'].loadFile(self.fullPath)
        except CException as e:
            rv.extend(e)
        except Exception as e:
            rv.append(self.__class__, 320, self.__str__() + '\n\n' + str(e), exc_info=sys.exc_info())
    else:
        self.__dict__['_fileContent'].unSet()
        self.__dict__['_lastLoadedFile'] = None

    self.dataLoaded.emit()
    return rv
```

**Issues**:
- Direct `__dict__` manipulation instead of using CData setters
- Uses `fileContentClass()` to dynamically get class from DATAMANAGER
- Requires global registration in DATAMANAGER

### File Content loadFile() Examples

#### CMmcifReflData.loadFile() (CCP4XtalData.py:767-828)

```python
def loadFile(self, fileName=None):
    if fileName is None or not os.path.exists(str(fileName)):
        self.unSet()
        self.__dict__['lastLoadedFile'] = None  # ⚠️ __dict__ access
        return

    fileName = str(fileName)
    err = CErrorReport()

    # Simple text parsing (first 500 lines)
    mmcifLines = CCP4Utils.readFile(fileName).split("\n")[0:500]

    # Manual parsing
    cell = {'a':None, 'b':None, 'c':None, 'alpha':None, 'beta':None, 'gamma':None}
    wavelength = None
    pyStrSpaceGroupName = ''
    # ... parse lines ...

    # ⚠️ DIRECT __dict__ ACCESS instead of using setters
    self.__dict__['_value']['cell'].set(cell)
    self.__dict__['_value']['wavelength'].set(wavelength)
    self.__dict__['_value']['spaceGroup'].set(pyStrSpaceGroupName)
    # ... etc ...

    self.__dict__['lastLoadedFile'] = fileName  # ⚠️ __dict__ access
    self.dataLoaded.emit()
    return err
```

**Issues**:
- Direct `__dict__` manipulation
- Manual text parsing (fragile)
- No use of proper CIF library
- Limited to first 500 lines

#### CUnmergedDataContent.loadFile() (CCP4XtalData.py:1152-1244)

```python
def loadFile(self, fileName=None):
    self.unSet()
    fileName = str(fileName)

    if fileName is None or not os.path.exists(fileName):
        return

    # Uses hklfile from ccp4mg (Python bindings to C++ clipper)
    try:
        import ccp4mg
        import hklfile
    except Exception as e:
        print('FAILED IMPORTING HKLFILE')
        print(e)

    # Detect format using hklfile
    reflectionList = hklfile.ReflectionList(fileName)
    ftype = reflectionList.FileType()

    # ⚠️ DIRECT __dict__ ACCESS
    self.__dict__['_value']['knowncell'].set(True)
    self.__dict__['_value']['knownwavelength'].set(True)

    # Extract metadata from hklfile's clipper objects
    self.__dict__['_value']['cell'].set(getClipperCell(reflectionList.Cell()))
    self.__dict__['_value']['spaceGroup'].set(hm)
    # ... etc ...
```

**Issues**:
- Uses hklfile (Python/SWIG bindings to C++ clipper) - heavyweight
- Direct `__dict__` manipulation
- Complex clipper API
- Requires ccp4mg module

#### CPdbDataContent.loadFile() (CCP4ModelData.py:1874-1909)

```python
def loadFile(self, fileName=None):
    self.unSet()
    if fileName is None or not os.path.exists(fileName):
        return

    # Uses mmdb2 (SWIG bindings to C++ MMDB library)
    try:
        import mmdb2 as mmdb
    except ImportError:
        raise CException(self.__class__, 101)

    # ⚠️ DIRECT __dict__ ACCESS to hold mmdb Manager
    self.__dict__['_molHnd'] = mmdb.Manager()

    rc = self.__dict__['_molHnd'].ReadCoorFile(str(fileName))
    if rc != 0:
        raise CException(self.__class__, 102, str(fileName))

    # No metadata extraction here - just holds reference to mmdb.Manager
    # Metadata accessed via properties that query self.__dict__['_molHnd']
```

**Issues**:
- Uses mmdb2 (SWIG bindings to C++ MMDB) - heavyweight, hard to install
- Direct `__dict__` to store `_molHnd` reference
- Metadata not extracted to CData attributes, only accessible via mmdb Manager
- Complex SWIG API

## New Pattern with Gemmi and CData

### Design Principles

1. **Use gemmi library** for coordinates and reflections (pure Python API)
2. **Use proper CData setters** instead of `__dict__` manipulation
3. **Extract metadata to CData attributes** for easy access without library reference
4. **Store library reference** for advanced queries
5. **Use fileContentClassName qualifier** to instantiate correct class
6. **Comprehensive error handling** with CException

### CDataFile.loadFile() - New Implementation

```python
# In core/CCP4File.py or base_classes.py

def loadFile(self, initialise: bool = False) -> CErrorReport:
    """
    Load file content by instantiating fileContentClassName and calling its loadFile().

    This base method:
    1. Gets fileContentClassName from qualifiers
    2. Instantiates that class if not already created
    3. Delegates to content class's loadFile() method
    4. Handles errors and emits dataLoaded signal

    Args:
        initialise: If True, recreate content object even if it exists

    Returns:
        CErrorReport with any errors encountered
    """
    from core.base_object.error_reporting import CErrorReport, CException, SEVERITY_ERROR
    from pathlib import Path

    error = CErrorReport()

    # Check if file loading is blocked
    if hasattr(self, 'BLOCK_LOAD_FILES') and self.BLOCK_LOAD_FILES:
        return error

    # Get content class name from qualifiers
    content_class_name = self.get_qualifier('fileContentClassName')
    if content_class_name is None:
        return error  # No content class specified - not an error

    # Instantiate content object if needed
    if not hasattr(self, 'content') or self.content is None or initialise:
        try:
            # Import the content class
            # Try local imports first (CCP4XtalData, CCP4ModelData, etc.)
            content_class = None
            for module_name in ['core.CCP4XtalData', 'core.CCP4ModelData', 'core.CCP4CootData']:
                try:
                    module = __import__(module_name, fromlist=[content_class_name])
                    content_class = getattr(module, content_class_name, None)
                    if content_class is not None:
                        break
                except (ImportError, AttributeError):
                    continue

            if content_class is None:
                error.append(
                    klass=self.__class__.__name__,
                    code=105,
                    details=f"Content class '{content_class_name}' not found",
                    name=self.object_name()
                )
                return error

            # Create content instance
            self.content = content_class(parent=self, name='fileContent')

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=106,
                details=f"Error instantiating content class '{content_class_name}': {e}",
                name=self.object_name()
            )
            return error

    # Get file path
    file_path = self.getFullPath()
    if not file_path:
        # No path set - unset content
        if hasattr(self, 'content') and self.content is not None:
            self.content.unSet()
        return error

    # Check file exists
    path_obj = Path(file_path)
    if path_obj.exists() and path_obj.is_file():
        try:
            # Delegate to content class's loadFile()
            content_error = self.content.loadFile(file_path)
            if content_error is not None:
                error.extend(content_error)

        except CException as e:
            error.extend(e)

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=320,
                details=f"Unrecognised error loading file '{file_path}': {e}",
                name=self.object_name()
            )
    else:
        # File doesn't exist - unset content
        if hasattr(self, 'content') and self.content is not None:
            self.content.unSet()

    # Emit signal (if event system available)
    if hasattr(self, 'dataLoaded'):
        self.dataLoaded.emit()

    return error
```

### File Content Classes - New Pattern

Each file content class should follow this pattern:

```python
def loadFile(self, file_path: str) -> CErrorReport:
    """
    Load file content using appropriate library (gemmi for coordinates/reflections).

    1. Import library
    2. Read file
    3. Extract metadata to CData attributes
    4. Store library reference for advanced queries
    5. Return error report

    Args:
        file_path: Full path to file to load

    Returns:
        CErrorReport with any errors
    """
    from core.base_object.error_reporting import CErrorReport, CException
    from pathlib import Path
    import gemmi

    error = CErrorReport()

    # Unset all attributes first
    self.unSet()

    # Validate path
    if not file_path or not Path(file_path).exists():
        return error

    try:
        # Read file using gemmi
        # (specific method depends on file type)

        # Extract metadata to CData attributes using proper setters
        # NOT: self.__dict__['_value']['cell'].set(...)
        # BUT: self.cell.set(...) or self.cell = ...

        # Store library reference for advanced queries
        # Use a private attribute with proper naming

    except Exception as e:
        error.append(
            klass=self.__class__.__name__,
            code=101,
            details=f"Error loading file '{file_path}': {e}",
            name=self.object_name()
        )

    return error
```

## Systematic Implementation by File Type

### 1. MTZ Reflection Data (Merged)

**Legacy**: Uses `hklfile.ReflectionList` (clipper bindings)

**New**: Use `gemmi.read_mtz_file()`

**File content class**: `CMtzData` (in `CCP4XtalData.py`)

**Implementation**:

```python
class CMtzData(CDataFileContent):
    """Content of merged MTZ reflection file."""

    def loadFile(self, file_path: str) -> CErrorReport:
        """Load MTZ file using gemmi."""
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path
        import gemmi

        error = CErrorReport()
        self.unSet()

        if not file_path or not Path(file_path).exists():
            return error

        try:
            # Read MTZ using gemmi
            mtz = gemmi.read_mtz_file(str(file_path))

            # Extract metadata to CData attributes (NO __dict__ access)
            self.cell = {
                'a': mtz.cell.a,
                'b': mtz.cell.b,
                'c': mtz.cell.c,
                'alpha': mtz.cell.alpha,
                'beta': mtz.cell.beta,
                'gamma': mtz.cell.gamma
            }

            self.spaceGroup = mtz.spacegroup.hm
            self.nreflections = mtz.nreflections

            # Resolution limits
            self.lowRes = 1.0 / mtz.max_1_d2 ** 0.5 if mtz.max_1_d2 > 0 else 999.0
            self.highRes = 1.0 / mtz.min_1_d2 ** 0.5 if mtz.min_1_d2 > 0 else 0.0

            # Dataset information
            if len(mtz.datasets) > 0:
                dataset = mtz.datasets[0]
                self.datasetName = dataset.dataset_name
                self.crystalName = dataset.crystal_name
                self.wavelength = dataset.wavelength

            # Store gemmi Mtz object for advanced queries
            self._gemmi_mtz = mtz

            # Extract column information
            self.columns = [col.label for col in mtz.columns]

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=101,
                details=f"Error reading MTZ file '{file_path}': {e}",
                name=self.object_name()
            )

        return error
```

**Gemmi API**:
- `gemmi.read_mtz_file(path)` → `gemmi.Mtz`
- `mtz.cell` → `gemmi.UnitCell` with properties `a, b, c, alpha, beta, gamma`
- `mtz.spacegroup` → `gemmi.SpaceGroup` with property `hm` (Hermann-Mauguin symbol)
- `mtz.datasets` → list of `gemmi.Mtz.Dataset`
- `mtz.columns` → list of `gemmi.Mtz.Column`
- `mtz.nreflections` → int
- `mtz.min_1_d2`, `mtz.max_1_d2` → float (for resolution limits)

### 2. Unmerged Reflection Data

**Legacy**: Uses `hklfile.ReflectionList` with batch info

**New**: Use `gemmi.read_mtz_file()` (same as merged)

**File content class**: `CUnmergedDataContent`

**Implementation**:

```python
class CUnmergedDataContent(CDataFileContent):
    """Content of unmerged reflection file (MTZ, XDS, etc.)."""

    def loadFile(self, file_path: str) -> CErrorReport:
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path
        import gemmi
        import os

        error = CErrorReport()
        self.unSet()

        if not file_path or not Path(file_path).exists():
            return error

        # Determine format from extension
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext in ['.mtz']:
                # Use gemmi for MTZ
                mtz = gemmi.read_mtz_file(str(file_path))

                # Unmerged MTZ specific
                self.merged = 'unmerged'  # Could check mtz.is_merged() if available
                self.format = 'mtz'

                # Extract metadata
                self.cell = {
                    'a': mtz.cell.a,
                    'b': mtz.cell.b,
                    'c': mtz.cell.c,
                    'alpha': mtz.cell.alpha,
                    'beta': mtz.cell.beta,
                    'gamma': mtz.cell.gamma
                }
                self.spaceGroup = mtz.spacegroup.hm

                # Batch information
                if hasattr(mtz, 'batches') and len(mtz.batches) > 0:
                    self.batchs = [batch.number for batch in mtz.batches]
                    self.numberLattices = len(set(b.dataset_id for b in mtz.batches))

                # Resolution
                self.lowRes = 1.0 / mtz.max_1_d2 ** 0.5 if mtz.max_1_d2 > 0 else 999.0
                self.highRes = 1.0 / mtz.min_1_d2 ** 0.5 if mtz.min_1_d2 > 0 else 0.0

                # Store reference
                self._gemmi_mtz = mtz

            elif ext in ['.hkl', '.sca']:
                # SCA format - simpler parsing or use external tool
                self.format = 'sca'
                self.merged = 'unmerged'  # SCA usually unmerged
                self.knowncell = False  # SCA files may not have cell
                self.knownwavelength = False

                # Could implement basic SCA parser or use external tool
                error.append(
                    klass=self.__class__.__name__,
                    code=102,
                    details=f"SCA format not yet fully implemented with gemmi",
                    severity=SEVERITY_WARNING
                )

            else:
                error.append(
                    klass=self.__class__.__name__,
                    code=103,
                    details=f"Unknown file format: {ext}"
                )

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=101,
                details=f"Error reading unmerged file '{file_path}': {e}"
            )

        return error
```

### 3. mmCIF Reflection Data

**Legacy**: Manual text parsing (first 500 lines)

**New**: Use `gemmi.cif` module

**File content class**: `CMmcifReflData`

**Implementation**:

```python
class CMmcifReflData(CDataFileContent):
    """Content of mmCIF reflection file."""

    def loadFile(self, file_path: str) -> CErrorReport:
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path
        import gemmi

        error = CErrorReport()
        self.unSet()

        if not file_path or not Path(file_path).exists():
            return error

        try:
            # Read mmCIF using gemmi
            doc = gemmi.cif.read_file(str(file_path))
            block = doc.sole_block()  # Usually only one block

            # Extract unit cell
            cell_a = block.find_value('_cell.length_a')
            cell_b = block.find_value('_cell.length_b')
            cell_c = block.find_value('_cell.length_c')
            cell_alpha = block.find_value('_cell.angle_alpha')
            cell_beta = block.find_value('_cell.angle_beta')
            cell_gamma = block.find_value('_cell.angle_gamma')

            if all([cell_a, cell_b, cell_c, cell_alpha, cell_beta, cell_gamma]):
                self.cell = {
                    'a': float(cell_a),
                    'b': float(cell_b),
                    'c': float(cell_c),
                    'alpha': float(cell_alpha),
                    'beta': float(cell_beta),
                    'gamma': float(cell_gamma)
                }

            # Extract space group
            sg_hm = block.find_value('_symmetry.space_group_name_H-M')
            sg_number = block.find_value('_symmetry.Int_Tables_number')
            if sg_hm:
                self.spaceGroup = sg_hm.strip('"\'')
            elif sg_number:
                self.spaceGroup = int(sg_number)

            # Extract wavelength
            wavelength_val = block.find_value('_diffrn_radiation_wavelength.wavelength')
            if wavelength_val:
                self.wavelength = float(wavelength_val)

            # Check for column types (simplified)
            # Look for _refln category
            refln_loop = block.find_loop('_refln.index_h')
            if refln_loop:
                # Check which columns are present
                tags = [tag for tag in refln_loop.tags]
                self.haveFreeRColumn = '_refln.status' in tags
                self.haveFobsColumn = ('_refln.F_meas' in tags or '_refln.F_meas_au' in tags)
                self.haveFpmObsColumn = '_refln.pdbx_F_plus' in tags
                self.haveIobsColumn = ('_refln.intensity_meas' in tags or
                                      '_refln.F_squared_meas' in tags)
                self.haveIpmObsColumn = '_refln.pdbx_I_plus' in tags

            # Store reference for advanced queries
            self._gemmi_cif_doc = doc

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=102,
                details=f"Error reading mmCIF reflection file '{file_path}': {e}"
            )

        return error
```

**Gemmi CIF API**:
- `gemmi.cif.read_file(path)` → `gemmi.cif.Document`
- `doc.sole_block()` → `gemmi.cif.Block` (most files have one block)
- `block.find_value('_tag')` → str or None
- `block.find_loop('_tag')` → `gemmi.cif.Loop` or None
- `loop.tags` → list of tag names

### 4. PDB Coordinate Files

**Legacy**: Uses `mmdb.Manager()` from mmdb2

**New**: Use `gemmi.read_structure()`

**File content class**: `CPdbDataContent`

**Implementation**:

```python
class CPdbDataContent(CDataFileContent):
    """Content of PDB coordinate file."""

    def loadFile(self, file_path: str) -> CErrorReport:
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path
        import gemmi

        error = CErrorReport()
        self.unSet()

        if not file_path or not Path(file_path).exists():
            return error

        try:
            # Read structure using gemmi (auto-detects PDB vs mmCIF)
            structure = gemmi.read_structure(str(file_path))

            # Extract metadata
            if structure.cell:
                self.cell = {
                    'a': structure.cell.a,
                    'b': structure.cell.b,
                    'c': structure.cell.c,
                    'alpha': structure.cell.alpha,
                    'beta': structure.cell.beta,
                    'gamma': structure.cell.gamma
                }

            if structure.spacegroup_hm:
                self.spaceGroup = structure.spacegroup_hm

            # Count atoms, residues, chains
            if len(structure) > 0:
                model = structure[0]
                self.nChains = len(model)
                self.nResidues = sum(len(chain) for chain in model)
                self.nAtoms = sum(sum(len(res) for res in chain) for chain in model)

            # Store gemmi Structure for advanced queries
            # This is the key object - everything can be queried from it
            self._gemmi_structure = structure

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=102,
                details=f"Error reading PDB file '{file_path}': {e}"
            )

        return error

    # Example advanced query method
    def get_chain(self, chain_id: str):
        """Get a chain by ID using gemmi structure."""
        if not hasattr(self, '_gemmi_structure'):
            return None
        if len(self._gemmi_structure) == 0:
            return None
        model = self._gemmi_structure[0]
        return model.find_chain(chain_id)

    def select_atoms(self, selection_string: str):
        """Select atoms using gemmi's selection syntax."""
        if not hasattr(self, '_gemmi_structure'):
            return []

        # gemmi has a Selection class for atom selection
        # Much simpler than mmdb's SWIG-wrapped selection API
        sel = gemmi.Selection(selection_string)
        return sel.models(self._gemmi_structure[0])
```

**Gemmi Structure API**:
- `gemmi.read_structure(path)` → `gemmi.Structure` (auto-detects format)
- `structure.cell` → `gemmi.UnitCell`
- `structure.spacegroup_hm` → str (Hermann-Mauguin symbol)
- `structure[i]` → `gemmi.Model` (usually just one model)
- `model[i]` or `model.find_chain(name)` → `gemmi.Chain`
- `chain[i]` → `gemmi.Residue`
- `residue[i]` → `gemmi.Atom`
- `gemmi.Selection(string)` → Simple selection language

### 5. mmCIF Coordinate Files

**Legacy**: Uses `mmdb.Manager()` (same as PDB)

**New**: Use `gemmi.read_structure()` (same as PDB - auto-detects format)

**File content class**: `CMmcifDataContent`

**Implementation**: Essentially the same as `CPdbDataContent` - gemmi auto-detects format:

```python
class CMmcifDataContent(CDataFileContent):
    """Content of mmCIF coordinate file."""

    def loadFile(self, file_path: str) -> CErrorReport:
        # Same implementation as CPdbDataContent
        # gemmi.read_structure() handles both PDB and mmCIF
        return self._load_coordinate_file(file_path)

    def _load_coordinate_file(self, file_path: str) -> CErrorReport:
        """Common loading for PDB and mmCIF coordinate files."""
        # Same as CPdbDataContent.loadFile()
        # Could be factored into a base class method
```

### 6. Sequence Files

**Legacy**: Uses BioPython

**New**: Keep BioPython (works well, no need to change)

**File content class**: `CSequence`

**Implementation**: Keep existing implementation but fix `__dict__` usage:

```python
class CSequence(CDataFileContent):
    """Protein/DNA sequence content."""

    def loadFile(self, file_path: str, format: str = 'unknown') -> CErrorReport:
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path

        error = CErrorReport()

        if format == 'internal':
            self._loadInternalFile(file_path)
        elif format == 'uniprot':
            self._loadUniprotFile(file_path)
        else:
            # Use BioPython
            from Bio import SeqIO
            try:
                seq_record = SeqIO.read(str(file_path), format)

                # Use proper setters instead of __dict__
                self.sequence = str(seq_record.seq)
                self.identifier = seq_record.id

            except Exception as e:
                error.append(
                    klass=self.__class__.__name__,
                    code=101,
                    details=f"Error reading sequence file '{file_path}': {e}"
                )

        return error
```

## Migration Strategy

### Phase 1: Core Infrastructure ✅

1. **Implement CDataFile.loadFile()** base method (new pattern)
2. **Add `content` attribute** to CDataFile base class
3. **Update ERROR_CODES** for loadFile operations

### Phase 2: Reflection Files (High Priority)

1. **CMtzData** - Merged MTZ files
   - Replace `hklfile.ReflectionList` with `gemmi.read_mtz_file()`
   - Extract all metadata to CData attributes
   - Store `_gemmi_mtz` for advanced queries

2. **CUnmergedDataContent** - Unmerged data
   - Use `gemmi.read_mtz_file()` for MTZ
   - Handle SCA/XDS formats (may need custom parsers)

3. **CMmcifReflData** - mmCIF reflections
   - Replace text parsing with `gemmi.cif.read_file()`
   - Use proper CIF parsing API

### Phase 3: Coordinate Files (High Priority)

1. **CPdbDataContent** - PDB coordinates
   - Replace `mmdb.Manager()` with `gemmi.read_structure()`
   - Extract metadata to CData attributes
   - Store `_gemmi_structure` for queries

2. **CMmcifDataContent** - mmCIF coordinates
   - Use same `gemmi.read_structure()` (auto-detects)
   - Share implementation with CPdbDataContent

### Phase 4: Other Files (Medium Priority)

1. **Map files** - CCP4 maps, CryoEM maps
   - Use `gemmi.read_ccp4_map()`

2. **Dictionary files** - CIF dictionaries
   - Use `gemmi.cif.read_file()`

3. **Sequence files** - Keep BioPython, fix `__dict__` usage

### Phase 5: Testing and Refinement

1. **Unit tests** for each content class
2. **Integration tests** with real files
3. **Performance comparison** vs legacy (gemmi should be faster)
4. **Memory profiling** (gemmi should use less memory)

## Benefits of New Approach

### 1. Simplified Dependencies ✅

**Before**:
- mmdb2 (SWIG bindings, C++, hard to install)
- hklfile/ccp4mg (SWIG bindings, clipper dependency)
- BioPython (sequence files)

**After**:
- gemmi (pure Python bindings, pip installable)
- BioPython (sequence files only)

### 2. Cleaner Code ✅

**Before**:
```python
self.__dict__['_value']['cell'].set(cell)  # Fragile
self.__dict__['_molHnd'] = mmdb.Manager()  # Direct access
```

**After**:
```python
self.cell = cell  # Clear, uses CData setters
self._gemmi_structure = structure  # Explicit naming
```

### 3. Better Error Handling ✅

**Before**: Many bare `except:` blocks, `print()` statements

**After**: Proper CException with error codes, detailed messages

### 4. Modern API ✅

**Before**: SWIG-wrapped C++ APIs (verbose, unintuitive)

**After**: Pythonic gemmi API (clean, well-documented)

### 5. Performance ✅

- gemmi is faster than mmdb/clipper for most operations
- Lower memory overhead
- No SWIG marshalling overhead

### 6. Type Safety ✅

- Can add type hints to all methods
- CData attributes have defined types
- gemmi has Python stubs for type checking

## Example Usage

### Loading MTZ File

```python
from core.CCP4XtalData import CMtzDataFile

# Create file object
mtz_file = CMtzDataFile()
mtz_file.setFullPath('/path/to/data.mtz')

# Load file (new pattern)
error = mtz_file.loadFile()

if error.count() > 0:
    print("Errors:", error.report())
else:
    # Access metadata via CData attributes
    print(f"Space group: {mtz_file.content.spaceGroup}")
    print(f"Cell: {mtz_file.content.cell}")
    print(f"Resolution: {mtz_file.content.highRes:.2f} Å")
    print(f"Columns: {mtz_file.content.columns}")

    # Advanced queries via gemmi reference
    if hasattr(mtz_file.content, '_gemmi_mtz'):
        mtz = mtz_file.content._gemmi_mtz
        for dataset in mtz.datasets:
            print(f"Dataset: {dataset.dataset_name}, λ={dataset.wavelength}")
```

### Loading PDB File

```python
from core.CCP4ModelData import CPdbDataFile

# Create and load
pdb_file = CPdbDataFile()
pdb_file.setFullPath('/path/to/model.pdb')
error = pdb_file.loadFile()

if error.count() == 0:
    # Access metadata
    print(f"Chains: {pdb_file.content.nChains}")
    print(f"Atoms: {pdb_file.content.nAtoms}")

    # Advanced queries via gemmi
    if hasattr(pdb_file.content, '_gemmi_structure'):
        structure = pdb_file.content._gemmi_structure

        # Iterate chains
        for chain in structure[0]:
            print(f"Chain {chain.name}: {len(chain)} residues")

        # Select atoms (gemmi selection syntax)
        from gemmi import Selection
        sel = Selection("CA")  # All CA atoms
        ca_atoms = sel.to_list(structure[0])
        print(f"Found {len(ca_atoms)} CA atoms")
```

## Implementation Checklist

- [ ] Implement CDataFile.loadFile() base method
- [ ] Add `content` attribute to CDataFile
- [ ] CMtzData.loadFile() using gemmi.read_mtz_file()
- [ ] CUnmergedDataContent.loadFile() using gemmi
- [ ] CMmcifReflData.loadFile() using gemmi.cif
- [ ] CPdbDataContent.loadFile() using gemmi.read_structure()
- [ ] CMmcifDataContent.loadFile() using gemmi.read_structure()
- [ ] CSequence.loadFile() fix __dict__ usage
- [ ] Write unit tests for each class
- [ ] Integration tests with real files
- [ ] Update documentation
- [ ] Performance benchmarks
- [ ] Deprecate legacy code

## References

- **Gemmi documentation**: https://gemmi.readthedocs.io/
- **Gemmi mol.rst**: `/Users/nmemn/Developer/gemmi/docs/mol.rst`
- **Gemmi hkl.rst**: `/Users/nmemn/Developer/gemmi/docs/hkl.rst`
- **Legacy CCP4File.py**: `/Users/nmemn/Developer/ccp4i2/core/CCP4File.py`
- **Legacy CCP4XtalData.py**: `/Users/nmemn/Developer/ccp4i2/core/CCP4XtalData.py`
- **Legacy CCP4ModelData.py**: `/Users/nmemn/Developer/ccp4i2/core/CCP4ModelData.py`

---

*Plan created: 2025-01-15*
*Ready for implementation*
