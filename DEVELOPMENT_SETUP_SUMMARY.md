# Package Management Summary

This document provides a quick reference for the hybrid package management strategy used in cdata-codegen.

## Environment
- **Python**: 3.11.11
- **CCP4 Distribution**: CCP4-20251105 (`/Users/nmemn/Developer/ccp4-20251105`)
- **Virtual Environment**: `.venv/` (Python 3.11)

## Pip-Installed Packages (56 total)

Installed via `pip install -r requirements.txt`:

### Web Framework & API
- `Django==5.2.8`
- `djangorestframework==3.16.1`
- `django-cors-headers==4.9.0`
- `django-filter==25.2`
- `whitenoise==6.11.0`

### Scientific Computing
- `numpy==1.26.4` (pinned < 2.0 for CCP4 compatibility)
- `scipy==1.16.3`
- `pandas==2.3.3`
- `matplotlib==3.10.7`

### Structural Biology (PyPI)
- `biopython==1.86`
- `gemmi==0.7.3`
- `mrcfile==1.5.4`
- `cctbx-base==2025.10` (CCTBX utilities, not full stack)

### Testing
- `pytest==8.4.2`
- `pytest-django==4.11.1`
- `pytest-asyncio==1.2.0`
- `pytest-xdist==3.8.0` (parallel testing)
- `pytest-ordering==0.6`

### Code Quality
- `autopep8==2.3.2`
- `mypy==1.18.2`

### Utilities
- `lxml==6.0.2`
- `PyYAML==6.0.3`
- `requests==2.32.5`
- `svgwrite==1.4.3`
- `psutil==7.1.3`

**Full list**: Run `.venv/bin/pip list --format=freeze`

## Symlinked CCP4 Modules (10 required)

Symlinked from CCP4-20251105 distribution at:
`/Users/nmemn/Developer/ccp4-20251105/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/`

### 1. Clipper (Crystallography)
```bash
ln -sf $CCP4_SITE_PACKAGES/clipper.py .venv/lib/python3.11/site-packages/
ln -sf $CCP4_SITE_PACKAGES/_clipper.so .venv/lib/python3.11/site-packages/
```
**Purpose**: Crystallographic calculations (FFT, map operations)
**Used by**: refmac, ctruncate, freerflag tests

### 2. CCP4MG (Molecular Graphics + MMDB2)
```bash
ln -sf $CCP4_SITE_PACKAGES/ccp4mg .venv/lib/python3.11/site-packages/
```
**Purpose**: Macromolecular database (mmdb2), coordinate manipulation
**Used by**: Model validation, structure manipulation tests

### 3. PyRVAPI (Report Viewing)
```bash
ln -sf $CCP4_SITE_PACKAGES/pyrvapi.so .venv/lib/python3.11/site-packages/
ln -sf $CCP4_SITE_PACKAGES/pyrvapi_ext .venv/lib/python3.11/site-packages/
```
**Purpose**: Interactive HTML report generation
**Used by**: All plugins with GUI reports

### 4. RDKit (Chemistry Toolkit) ⚠️ CRITICAL
```bash
ln -sf $CCP4_SITE_PACKAGES/rdkit .venv/lib/python3.11/site-packages/
```
**Purpose**: Chemical structure manipulation, SMILES parsing
**Version**: v2023.03.3 (CCP4-bundled)
**Why symlink?**:
- PyPI version v2025.09.1 incompatible with phaser's pickle implementation
- Phaser crashes with: `RuntimeError: Pickling of "rdkit.rdBase._vectd" instances is not enabled`
**Used by**: acedrg tests (8 tests), phaser tests (18 tests)

### 5. Phaser (Molecular Replacement)
```bash
ln -sf $CCP4_SITE_PACKAGES/phaser .venv/lib/python3.11/site-packages/
```
**Purpose**: Crystallographic phasing, molecular replacement
**Used by**: phaser_simple (4 tests), phaser_expert (2 tests), phaser_ep (1 test)

### 6. MrBUMP (MR Pipeline)
```bash
ln -sf $CCP4_SITE_PACKAGES/mrbump .venv/lib/python3.11/site-packages/
```
**Purpose**: Automated molecular replacement pipeline
**Used by**: mrbump test (1 test)

### 7. Iris Validation (Structure Validation)
```bash
ln -sf $CCP4_SITE_PACKAGES/iris_validation .venv/lib/python3.11/site-packages/
```
**Purpose**: Structure quality assessment
**Used by**: validate_protein tests (7 tests)

### 8. Chem_data (Top8000 Database)
```bash
ln -sf $CCP4_SITE_PACKAGES/chem_data .venv/lib/python3.11/site-packages/
```
**Purpose**: Ramachandran and rotamer reference database (Top8000)
**Used by**: MolProbity validation, iris_validation

## Verification

### Check Pip Packages
```bash
source .venv/bin/activate
pip list | wc -l  # Should show ~56 packages
```

### Check Symlinked Modules
```bash
ls -la .venv/lib/python3.11/site-packages/ | grep "^l" | wc -l  # Should show 10 symlinks
```

### Test Imports
```bash
# Core crystallography
python -c "import clipper; from ccp4mg import mmdb2; print('✓ clipper, mmdb2')"

# Critical RDKit version
python -c "import rdkit; print(f'RDKit: {rdkit.__version__}')"  # Must show 2023.03.3

# Molecular replacement
python -c "import phaser; import mrbump; print('✓ phaser, mrbump')"

# Validation
python -c "import iris_validation; print('✓ iris_validation')"
```

## Test Results

With all 56 pip packages + 10 symlinked modules:
- **53 passed** out of 69 tests
- **77% pass rate**
- Runtime: ~38 minutes
- Commit: `9187a41`

## Quick Setup

```bash
# 1. Create venv with CCP4's Python 3.11
/Users/nmemn/Developer/ccp4-20251105/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -m venv .venv

# 2. Install pip packages
source .venv/bin/activate
pip install -r requirements.txt

# 3. Symlink CCP4 modules
CCP4_SITE_PACKAGES="/Users/nmemn/Developer/ccp4-20251105/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages"
cd .venv/lib/python3.11/site-packages

ln -sf "$CCP4_SITE_PACKAGES/clipper.py" .
ln -sf "$CCP4_SITE_PACKAGES/_clipper.so" .
ln -sf "$CCP4_SITE_PACKAGES/ccp4mg" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi.so" .
ln -sf "$CCP4_SITE_PACKAGES/pyrvapi_ext" .
ln -sf "$CCP4_SITE_PACKAGES/rdkit" .
ln -sf "$CCP4_SITE_PACKAGES/phaser" .
ln -sf "$CCP4_SITE_PACKAGES/mrbump" .
ln -sf "$CCP4_SITE_PACKAGES/iris_validation" .
ln -sf "$CCP4_SITE_PACKAGES/chem_data" .

# 4. Verify
cd /Users/nmemn/Developer/cdata-codegen
python -c "import clipper, rdkit, phaser; print('✅ All modules OK')"
```

## Common Issues

### RDKit Version Conflict
**Symptom**: `RuntimeError: Pickling of "rdkit.rdBase._vectd" instances is not enabled`

**Cause**: Pip-installed RDKit v2025.09.1 instead of CCP4's v2023.03.3

**Fix**:
```bash
rm -rf .venv/lib/python3.11/site-packages/rdkit*
ln -sf "$CCP4_SITE_PACKAGES/rdkit" .venv/lib/python3.11/site-packages/
```

### Module Not Found
**Symptom**: `ModuleNotFoundError: No module named 'phaser'`

**Fix**: Check symlink exists and points to correct location:
```bash
ls -la .venv/lib/python3.11/site-packages/phaser
```

If broken, re-create symlink as shown above.
