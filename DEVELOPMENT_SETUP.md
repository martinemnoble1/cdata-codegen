# Development Environment Setup

This guide walks through setting up a complete development environment for cdata-codegen with full CCP4 integration.

## Prerequisites

- **CCP4 Suite 2024/2025** installed on your system (tested with CCP4-20251105)
- **Python 3.11** (must match CCP4's Python version)
- **Git** for version control
- **macOS, Linux, or WSL** (Unix-like environment)

## Overview

The cdata-codegen project requires integration with CCP4's crystallographic libraries (clipper, mmdb2, phaser, RDKit, CCTBX stack). Since these are compiled Python extensions built for Python 3.11, we create a Python 3.11 virtual environment and symlink the CCP4 modules into it.

## Package Management Strategy

This project uses a **hybrid approach** combining pip-installed packages and symlinked CCP4 modules:

### Pip-Installed Packages (from PyPI)
Standard Python packages installed via `pip install -r requirements.txt`:
- **Web framework**: Django, djangorestframework, django-cors-headers
- **Scientific computing**: numpy, scipy, pandas, matplotlib
- **Structural biology**: biopython, gemmi, mrcfile
- **Testing**: pytest, pytest-django, pytest-asyncio, pytest-xdist
- **Utilities**: autopep8, lxml, PyYAML, requests, svgwrite

### Symlinked CCP4 Modules (from CCP4 distribution)
CCP4-specific modules that must be symlinked from the CCP4 installation:
- **Crystallography**: clipper, ccp4mg (includes mmdb2)
- **Chemistry**: rdkit (CCP4's v2023.03.3 for compatibility)
- **Molecular replacement**: phaser, mrbump
- **Validation**: iris_validation, chem_data (Top8000 database)
- **Reporting**: pyrvapi

**Why symlink?** These modules are either:
1. Compiled against CCP4's specific library versions
2. Not available on PyPI
3. Different versions than PyPI (e.g., RDKit v2023.03.3 vs v2025.09.1)

---

## Step 1: Locate Your CCP4 Installation

CCP4 installations vary by platform and installation method. Use these commands to find yours:

### macOS
```bash
# CCP4-20251105 (Python 3.11)
CCP4_ROOT=/Users/nmemn/Developer/ccp4-20251105

# Or standard installation location
CCP4_ROOT=/Applications/ccp4-20251105

# Verify Python location (should be 3.11.x)
ls -la $CCP4_ROOT/Frameworks/Python.framework/Versions/3.11/bin/python3.11
```

### Linux
```bash
# Common locations
CCP4_ROOT=/opt/ccp4-20251105
# Or
CCP4_ROOT=$HOME/ccp4-20251105

# Verify Python location
ls -la $CCP4_ROOT/bin/ccp4-python
$CCP4_ROOT/bin/ccp4-python --version  # Should show 3.11.x
```

### Finding CCP4 Automatically
```bash
# Method 1: Check environment after sourcing CCP4 setup
source /path/to/ccp4.setup-sh  # or ccp4.setup-csh
echo $CCP4

# Method 2: Find ccp4-python executable
which ccp4-python

# Method 3: Search common locations
find /Applications /opt $HOME -name "ccp4-python" -type f 2>/dev/null
```

**Set your CCP4_ROOT variable:**
```bash
export CCP4_ROOT=/path/to/your/ccp4-9
```

---

## Step 2: Determine CCP4 Python Paths

CCP4 provides Python 3.11 with crystallographic libraries. We need to locate:
1. Python executable
2. site-packages directory

### macOS Paths (CCP4-20251105)
```bash
CCP4_PYTHON="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.11/bin/python3.11"
CCP4_SITE_PACKAGES="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages"
```

### Linux Paths
```bash
CCP4_PYTHON="$CCP4_ROOT/bin/ccp4-python"
CCP4_SITE_PACKAGES="$CCP4_ROOT/lib/python3.11/site-packages"
```

### Verify Paths
```bash
# Check Python version (must be 3.11.x)
$CCP4_PYTHON --version

# Check site-packages exists
ls "$CCP4_SITE_PACKAGES" | head -5

# Check for key modules
ls "$CCP4_SITE_PACKAGES" | grep -E "(clipper|phaser|rdkit|mrbump|iris_validation)"
```

---

## Step 3: Create Python 3.9 Virtual Environment

### Option A: Use CCP4's Python (Recommended)
```bash
cd /path/to/cdata-codegen
$CCP4_PYTHON -m venv .venv
```

### Option B: Use System Python 3.9
```bash
# Install Python 3.9 if needed
# macOS:
brew install python@3.9

# Linux (Ubuntu/Debian):
sudo apt install python3.9 python3.9-venv

# Create venv
python3.9 -m venv .venv
```

### Activate and Upgrade pip
```bash
source .venv/bin/activate
pip install --upgrade pip
```

---

## Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Important**: After installation, downgrade NumPy for CCP4 compatibility:
```bash
pip install "numpy<2"
```

**Why?** CCP4's compiled modules (clipper, mmdb2) were built with NumPy 1.x and will crash with NumPy 2.x.

---

## Step 5: Symlink CCP4 Modules

### Summary of Required Symlinks

The following 10 symlinks are **required** for the comprehensive test suite (77% pass rate):

| Module | Type | Purpose | Test Impact |
|--------|------|---------|-------------|
| `clipper.py` + `_clipper.so` | Library | Crystallographic calculations | Core refmac, ctruncate tests |
| `ccp4mg/` | Package | Molecular graphics (includes mmdb2) | Model manipulation, validation |
| `pyrvapi.so` + `pyrvapi_ext/` | Library | Report viewing API | HTML report generation |
| `rdkit/` | Package | Chemistry toolkit (v2023.03.3) | **CRITICAL**: acedrg, phaser compatibility |
| `phaser/` | Package | Molecular replacement | phaser_* tests (18 tests) |
| `mrbump/` | Package | MR pipeline | mrbump tests |
| `iris_validation/` | Package | Structure validation | validate_protein tests |
| `chem_data/` | Data | Top8000 Ramachandran/rotamer database | MolProbity validation |

### 5.1 Core Crystallographic Modules
```bash
cd .venv/lib/python3.11/site-packages

# Clipper (crystallographic library)
ln -sf "$CCP4_SITE_PACKAGES/clipper.py" .
ln -sf "$CCP4_SITE_PACKAGES/_clipper.so" .

# CCP4MG (includes mmdb2 for macromolecular database)
ln -sf "$CCP4_SITE_PACKAGES/ccp4mg" .

# PyRVAPI (Report Viewing API for interactive HTML reports)
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi.so" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi_ext" .
```

### 5.2 Chemistry and Molecular Replacement
```bash
cd .venv/lib/python3.11/site-packages

# RDKit (CRITICAL: Use CCP4's v2023.03.3, not pip's v2025.09.1)
# Phaser's pickle implementation requires this specific version
ln -sf "$CCP4_SITE_PACKAGES/rdkit" .

# Phaser (molecular replacement)
ln -sf "$CCP4_SITE_PACKAGES/phaser" .

# MrBUMP (molecular replacement pipeline)
ln -sf "$CCP4_SITE_PACKAGES/mrbump" .
```

### 5.3 Validation and Data
```bash
cd .venv/lib/python3.11/site-packages

# Iris validation (structure validation tools)
ln -sf "$CCP4_SITE_PACKAGES/iris_validation" .

# Chem_data (Top8000 Ramachandran and rotamer database for MolProbity)
ln -sf "$CCP4_SITE_PACKAGES/chem_data" .
```

### 5.4 Verify All Symlinks
```bash
cd /path/to/cdata-codegen
ls -la .venv/lib/python3.11/site-packages/ | grep "^l"
```

**Expected output (10 symlinks):**
```
lrwxr-xr-x  _clipper.so -> /path/to/ccp4-20251105/.../site-packages/_clipper.so
lrwxr-xr-x  ccp4mg -> /path/to/ccp4-20251105/.../site-packages/ccp4mg
lrwxr-xr-x  chem_data -> /path/to/ccp4-20251105/.../site-packages/chem_data
lrwxr-xr-x  clipper.py -> /path/to/ccp4-20251105/.../site-packages/clipper.py
lrwxr-xr-x  iris_validation -> /path/to/ccp4-20251105/.../site-packages/iris_validation
lrwxr-xr-x  mrbump -> /path/to/ccp4-20251105/.../site-packages/mrbump
lrwxr-xr-x  phaser -> /path/to/ccp4-20251105/.../site-packages/phaser
lrwxr-xr-x  pyrvapi.so -> /path/to/ccp4-20251105/.../site-packages/pyrvapi.so
lrwxr-xr-x  pyrvapi_ext -> /path/to/ccp4-20251105/.../site-packages/pyrvapi_ext
lrwxr-xr-x  rdkit -> /path/to/ccp4-20251105/.../site-packages/rdkit
```

### Quick Setup Script
```bash
#!/bin/bash
# Quick symlink setup for cdata-codegen with CCP4-20251105

CCP4_ROOT="/Users/nmemn/Developer/ccp4-20251105"  # Adjust for your installation
CCP4_SITE_PACKAGES="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages"

cd .venv/lib/python3.11/site-packages

# Core modules (5 symlinks)
ln -sf "$CCP4_SITE_PACKAGES/clipper.py" .
ln -sf "$CCP4_SITE_PACKAGES/_clipper.so" .
ln -sf "$CCP4_SITE_PACKAGES/ccp4mg" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi.so" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi_ext" .

# Chemistry and MR (3 symlinks)
ln -sf "$CCP4_SITE_PACKAGES/rdkit" .
ln -sf "$CCP4_SITE_PACKAGES/phaser" .
ln -sf "$CCP4_SITE_PACKAGES/mrbump" .

# Validation (2 symlinks)
ln -sf "$CCP4_SITE_PACKAGES/iris_validation" .
ln -sf "$CCP4_SITE_PACKAGES/chem_data" .

echo "✅ All 10 CCP4 modules symlinked"
```

---

## Step 6: Verify Installation

### Test Core Modules
```bash
source .venv/bin/activate
python -c "import clipper; print('✓ clipper')"
python -c "from ccp4mg import mmdb2; print('✓ mmdb2')"
```

### Test CCTBX Stack (if installed)
```bash
python -c "import cctbx; print('✓ cctbx')"
python -c "import iotbx; print('✓ iotbx')"
python -c "import scitbx; print('✓ scitbx')"
python -c "import phaser; print('✓ phaser')"
```

### Test Full Stack
```bash
python -c "
import phaser
from ccp4mg import mmdb2
import clipper
import cctbx
import iotbx
import scitbx
print('✅ FULL CCTBX STACK WORKING!')
"
```

---

## Step 7: Regenerate Plugin Registry

```bash
export CCP4I2_ROOT=$(pwd)
python core/task_manager/plugin_lookup.py
```

Expected output (with full CCTBX stack + additional modules):
```
Building plugin lookup from: /path/to/cdata-codegen
  Found 102+ plugins in wrappers
  Found 2 plugins in wrappers2
  Found 50+ plugins in pipelines
Finished scanning, found 158 plugins
```

**Plugin Count Summary:**
- **Minimum setup** (core modules only): ~144 plugins
- **Full CCTBX stack**: 155 plugins
- **Full setup** (CCTBX + additional modules): 158 plugins

---

## Step 8: Run Tests

### Quick Test
```bash
./run_test.sh i2run/test_acedrg.py::test_from_cif_monomer_library
```

### Full Test Suite
```bash
./run_test.sh i2run
```

Expected: ~17+ tests passing (baseline: 17/59 = 28.8% pass rate)

---

## Troubleshooting

### Issue: NumPy Version Conflicts
**Error**: `AttributeError: _ARRAY_API not found` or `numpy.core.multiarray failed to import`

**Solution**: Downgrade NumPy
```bash
pip install "numpy<2"
```

### Issue: Module Not Found (phaser, scitbx, etc.)
**Error**: `ModuleNotFoundError: No module named 'phaser'`

**Check**:
1. Verify symlinks exist: `ls -la .venv/lib/python3.9/site-packages/phaser`
2. Check CCP4 has the module: `ls "$CCP4_SITE_PACKAGES/phaser"`
3. Re-run symlink commands from Step 5.2

### Issue: libtbx.env FileNotFoundError
**Error**: `FileNotFoundError: .venv/share/cctbx`

**Solution**: Ensure cctbx share directory is symlinked correctly
```bash
mkdir -p .venv/share
ln -sf "$CCP4_SHARE/cctbx" .venv/share/
ls -la .venv/share/cctbx  # Verify it's not a broken symlink
```

### Issue: Segmentation Fault on Import
**Error**: Exit code 139 or `Segmentation fault (core dumped)`

**Cause**: Python version mismatch. CCP4 modules are compiled for Python 3.9.

**Solution**:
1. Verify venv Python version: `python --version` (must be 3.9.x)
2. If not, recreate venv with correct Python version
3. Never try to use Python 3.10+ with CCP4's Python 3.9 modules

### Issue: Django Database Errors
**Error**: `Model class doesn't declare an explicit app_label`

**Solution**: Ensure `DJANGO_SETTINGS_MODULE` is set
```bash
export DJANGO_SETTINGS_MODULE=ccp4x.settings
```

The `run_test.sh` script sets this automatically.

---

## Platform-Specific Notes

### macOS (Intel vs ARM)
- Intel: Modules may be in `lib/python3.9/site-packages`
- ARM (M1/M2/M3): Same paths as shown above
- Universal binaries: CCP4 provides universal binaries that work on both

### Linux
- Distribution packages may place CCP4 in `/opt/ccp4-9.0`
- User installations typically go to `$HOME/ccp4-9.0`
- Check `$CCP4` environment variable after sourcing setup script

### WSL (Windows Subsystem for Linux)
- Follow Linux instructions
- CCP4 installation paths are Linux-style
- Performance note: File I/O may be slower across WSL boundary

---

## Automated Setup Script

Create a `setup_dev_env.sh` script for easy setup:

```bash
#!/bin/bash
set -e

# Detect CCP4 installation
if [ -d "/Applications/ccp4-9" ]; then
    # macOS
    CCP4_ROOT="/Applications/ccp4-9"
    CCP4_PYTHON="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/bin/python3.9"
    CCP4_SITE_PACKAGES="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages"
    CCP4_SHARE="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/share"
elif [ -d "/opt/ccp4-9.0" ]; then
    # Linux system install
    CCP4_ROOT="/opt/ccp4-9.0"
    CCP4_PYTHON="$CCP4_ROOT/bin/ccp4-python"
    CCP4_SITE_PACKAGES="$CCP4_ROOT/lib/python3.9/site-packages"
    CCP4_SHARE="$CCP4_ROOT/share"
elif [ -d "$HOME/ccp4-9.0" ]; then
    # Linux user install
    CCP4_ROOT="$HOME/ccp4-9.0"
    CCP4_PYTHON="$CCP4_ROOT/bin/ccp4-python"
    CCP4_SITE_PACKAGES="$CCP4_ROOT/lib/python3.9/site-packages"
    CCP4_SHARE="$CCP4_ROOT/share"
else
    echo "❌ CCP4 installation not found. Please install CCP4 Suite 9.x"
    exit 1
fi

echo "✓ Found CCP4 at: $CCP4_ROOT"
echo "✓ Python: $CCP4_PYTHON ($($CCP4_PYTHON --version))"

# Create venv
echo "Creating Python 3.9 virtual environment..."
$CCP4_PYTHON -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install "numpy<2"

# Symlink core modules
echo "Symlinking CCP4 core modules..."
cd .venv/lib/python3.9/site-packages
ln -sf "$CCP4_SITE_PACKAGES/clipper.py" .
ln -sf "$CCP4_SITE_PACKAGES/_clipper.so" .
ln -sf "$CCP4_SITE_PACKAGES/ccp4mg" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi.so" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi_ext" .

# Symlink CCTBX stack
echo "Symlinking CCTBX stack..."
CCTBX_MODULES=(
    annlib_adaptbx boost_adaptbx cbflib_adaptbx ccp4io_adaptbx cctbx chiltbx
    cootbx dxtbx gltbx iotbx libtbx mmtbx omptbx phaser phaser_voyager phasertng
    rstbx scitbx serialtbx simtbx smtbx tbxx tntbx wxtbx
)

for module in "${CCTBX_MODULES[@]}"; do
    if [ -e "$CCP4_SITE_PACKAGES/$module" ]; then
        ln -sf "$CCP4_SITE_PACKAGES/$module" .
    fi
done

# Symlink additional CCP4 modules (optional - enables 158 plugins)
echo "Symlinking additional CCP4 modules..."
ADDITIONAL_MODULES=(
    dials dials_data ample simbad iris_validation onedep pyjob docx
)

for module in "${ADDITIONAL_MODULES[@]}"; do
    if [ -e "$CCP4_SITE_PACKAGES/$module" ]; then
        ln -sf "$CCP4_SITE_PACKAGES/$module" .
    fi
done

# Symlink share directory
cd ../../..
mkdir -p share
ln -sf "$CCP4_SHARE/cctbx" share/

echo "✅ Development environment setup complete!"
echo ""
echo "To activate: source .venv/bin/activate"
echo "To test: ./run_test.sh i2run/test_acedrg.py::test_from_cif_monomer_library"
```

Make it executable:
```bash
chmod +x setup_dev_env.sh
./setup_dev_env.sh
```

---

## CI/CD Considerations

For continuous integration:
1. **Docker**: Install CCP4 in base image, cache the layer
2. **GitHub Actions**: Use matrix strategy for different CCP4 versions
3. **Environment Variables**: Set `CCP4I2_ROOT`, `DJANGO_SETTINGS_MODULE`
4. **Caching**: Cache pip packages and CCP4 installation separately

---

## Summary

### Package Inventory

**Pip-Installed Packages (56 total):**
- Core: Django, djangorestframework, pytest, numpy, scipy, pandas
- Structural biology: biopython, gemmi, mrcfile, cctbx-base
- Full list: Run `.venv/bin/pip list --format=freeze`

**Symlinked CCP4 Modules (10 required):**
1. `clipper.py` + `_clipper.so` - Crystallography
2. `ccp4mg/` - Molecular graphics (includes mmdb2)
3. `pyrvapi.so` + `pyrvapi_ext/` - Report viewing
4. `rdkit/` - Chemistry toolkit (v2023.03.3)
5. `phaser/` - Molecular replacement
6. `mrbump/` - MR pipeline
7. `iris_validation/` - Validation
8. `chem_data/` - Top8000 database

**Test Results with Full Setup:**
- **53 passed** out of 69 tests
- **77% pass rate**
- Runtime: ~38 minutes

**Verification Commands:**
```bash
# Quick check - Core modules
python -c "import clipper; from ccp4mg import mmdb2; print('✓ Core modules OK')"

# Critical check - RDKit version
python -c "import rdkit; print(f'RDKit: {rdkit.__version__}')"  # Should show 2023.03.3

# Full check - All symlinked modules
python -c "
import clipper
from ccp4mg import mmdb2
import rdkit
import phaser
import mrbump
import iris_validation
print('✅ ALL CCP4 MODULES OK')
"

# Run comprehensive tests
./run_test.sh tests/i2run
```

---

## Next Steps

After setup:
1. Review [CLAUDE.md](CLAUDE.md) for project architecture and development guidelines
2. Understand the migration: Qt-free CData system replacing Qt's QObject hierarchy
3. Run comprehensive test suite: `./run_test.sh tests/i2run`
4. Current baseline (as of commit 9187a41): **53 passed, 14 failed** (77% pass rate)

## Key Architecture Points

**CData System:** Metadata-driven data classes replacing Qt's property system
- Smart assignment with type coercion
- Hierarchical object system with weak references
- Signal/slot system without Qt dependencies

**Plugin System:** 148+ legacy ccp4i2 plugins via lazy-loading registry
- Locked legacy code in `wrappers/`, `wrappers2/`, `pipelines/`
- Modern Python wrappers in `core/`

**Test Strategy:** Django-based integration tests with CCP4 environment
- Use `./run_test.sh` for all i2run tests (sets up CCP4 environment)
- Clean test projects: `rm -rf tests/i2run/test_projects/*`

Good luck! 🚀
