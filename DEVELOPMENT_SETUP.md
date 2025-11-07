# Development Environment Setup

This guide walks through setting up a complete development environment for cdata-codegen with full CCP4 integration.

## Prerequisites

- **CCP4 Suite 9.x** installed on your system
- **Python 3.9** (must match CCP4's Python version)
- **Git** for version control
- **macOS, Linux, or WSL** (Unix-like environment)

## Overview

The cdata-codegen project requires integration with CCP4's crystallographic libraries (clipper, mmdb2, phaser, CCTBX stack). Since these are compiled Python extensions built for Python 3.9, we create a Python 3.9 virtual environment and symlink the CCP4 modules into it.

---

## Step 1: Locate Your CCP4 Installation

CCP4 installations vary by platform and installation method. Use these commands to find yours:

### macOS
```bash
# Standard installation
CCP4_ROOT=/Applications/ccp4-9

# Verify Python location
ls -la $CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/bin/python3.9
```

### Linux
```bash
# Common locations
CCP4_ROOT=/opt/ccp4-9.0
# Or
CCP4_ROOT=$HOME/ccp4-9.0

# Verify Python location
ls -la $CCP4_ROOT/bin/ccp4-python
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

CCP4 provides Python 3.9 with crystallographic libraries. We need to locate:
1. Python executable
2. site-packages directory
3. share directory

### macOS Paths
```bash
CCP4_PYTHON="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/bin/python3.9"
CCP4_SITE_PACKAGES="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages"
CCP4_SHARE="$CCP4_ROOT/Frameworks/Python.framework/Versions/3.9/share"
```

### Linux Paths
```bash
CCP4_PYTHON="$CCP4_ROOT/bin/ccp4-python"
CCP4_SITE_PACKAGES="$CCP4_ROOT/lib/python3.9/site-packages"
CCP4_SHARE="$CCP4_ROOT/share"
```

### Verify Paths
```bash
# Check Python version (must be 3.9.x)
$CCP4_PYTHON --version

# Check site-packages exists
ls "$CCP4_SITE_PACKAGES" | head -5

# Check for key modules
ls "$CCP4_SITE_PACKAGES" | grep -E "(clipper|phaser|cctbx|mmdb)"
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

### 5.1 Core Crystallographic Modules
```bash
cd .venv/lib/python3.9/site-packages

# Clipper (crystallographic library)
ln -sf "$CCP4_SITE_PACKAGES/clipper.py" .
ln -sf "$CCP4_SITE_PACKAGES/_clipper.so" .

# CCP4MG (includes mmdb2 for macromolecular database)
ln -sf "$CCP4_SITE_PACKAGES/ccp4mg" .

# PyRVAPI (Report Viewing API for interactive HTML reports)
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi.so" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi_ext" .
```

### 5.2 Full CCTBX Stack (for Phaser and advanced features)

Symlink all CCTBX-related modules:

```bash
cd .venv/lib/python3.9/site-packages

# List of all CCTBX modules to symlink
CCTBX_MODULES=(
    annlib_adaptbx
    boost_adaptbx
    cbflib_adaptbx
    ccp4io_adaptbx
    cctbx
    chiltbx
    cootbx
    dxtbx
    gltbx
    iotbx
    libtbx
    mmtbx
    omptbx
    phaser
    phaser_voyager
    phasertng
    rstbx
    scitbx
    serialtbx
    simtbx
    smtbx
    tbxx
    tntbx
    wxtbx
)

# Create symlinks
for module in "${CCTBX_MODULES[@]}"; do
    if [ -e "$CCP4_SITE_PACKAGES/$module" ]; then
        ln -sf "$CCP4_SITE_PACKAGES/$module" .
        echo "✓ Symlinked $module"
    else
        echo "⚠ Module $module not found (may not be needed)"
    fi
done
```

### 5.3 Additional CCP4 Modules (Optional - enables 158 plugins)

For maximum plugin discovery, symlink additional specialized modules:

```bash
cd .venv/lib/python3.9/site-packages

# Additional CCP4 modules for specialized plugins
ADDITIONAL_MODULES=(
    dials          # Diffraction Integration for Advanced Light Sources
    dials_data     # DIALS test data
    ample          # Ab-initio Molecular replacement Pipeline for Ensembles
    simbad         # Sequence Independent Molecular replacement Based on Available Database
    iris_validation # Structure validation tools
    onedep         # One-stop Data Entry and Processing
    pyjob          # Python job management (dependency for simbad/ample)
    docx           # Microsoft Word document generation (dependency for reporting)
)

# Create symlinks for additional modules
for module in "${ADDITIONAL_MODULES[@]}"; do
    if [ -e "$CCP4_SITE_PACKAGES/$module" ]; then
        ln -sf "$CCP4_SITE_PACKAGES/$module" .
        echo "✓ Symlinked $module"
    else
        echo "⚠ Module $module not found (skipping)"
    fi
done
```

**Note**: These additional modules enable 3 more plugins (155 → 158 total) but some (AMPLE, SIMBAD) require full CCP4 environment variables to be sourced at runtime.

### 5.4 CCTBX Build Configuration
```bash
cd /path/to/cdata-codegen

# Create share directory structure
mkdir -p .venv/share

# Symlink CCTBX build configuration
ln -sf "$CCP4_SHARE/cctbx" .venv/share/
```

**Verify symlinks:**
```bash
ls -la .venv/share/cctbx
file .venv/share/cctbx  # Should show it's a valid symlink
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

**Minimum Setup (basic tests):**
- Python 3.9 venv
- requirements.txt installed
- NumPy < 2
- Symlink: clipper.py, _clipper.so, ccp4mg, pyrvapi.so, pyrvapi_ext

**Full Setup (phaser/molecular replacement):**
- All of the above, plus:
- Symlink: 24 CCTBX modules
- Symlink: 8 additional CCP4 modules (dials, ample, simbad, etc.)
- Symlink: .venv/share/cctbx
- Install: svgwrite, chardet, mrcfile via pip
- Result: 158 plugins, phaser tests functional

**Verification Commands:**
```bash
# Quick check
python -c "import clipper; from ccp4mg import mmdb2; print('✓ Core modules OK')"

# Full check
python -c "import phaser; import cctbx; import iotbx; print('✓ Full stack OK')"

# Plugin count
python core/task_manager/plugin_lookup.py | grep "found.*plugins"

# Run tests
./run_test.sh i2run
```

---

## Next Steps

After setup:
1. Review [CLAUDE.md](CLAUDE.md) for project architecture
2. Check [RESMAX_FIX_SUMMARY.md](RESMAX_FIX_SUMMARY.md) for recent fixes
3. Run full test suite: `./run_test.sh i2run`
4. Expected baseline: **17 passed, 42 failed** (28.8% pass rate)

Good luck! 🚀
