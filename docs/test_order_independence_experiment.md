# Test Order Independence Experiment

**Date**: 2025-11-23
**Objective**: Verify that underlying fixes have made tests truly order-independent, not just passing due to forced test ordering.

## Background

After implementing forced test ordering (phaser tests first) to work around RDKit/pickle contamination issues, we discovered and fixed several underlying problems:

1. **Job numbering issues** - Jobs were not being numbered consistently
2. **Sub-directory naming** - CCP4_JOBS subdirectories had naming conflicts
3. **RDKit pickle cleanup** - Added module unloading in conftest.py cleanup
4. **Concurrent test safety** - Added random suffixes to prevent directory collisions

## Hypothesis

The forced test ordering was a workaround. If our underlying fixes are correct, tests should pass in **any order**, including alphabetical order.

## Methodology

### Previous Test Configuration (conftest.py lines 70-89)
```python
def pytest_collection_modifyitems(items):
    # FORCED ORDERING: phaser tests first
    phaser_tests = []
    other_tests = []
    for item in items:
        test_file = item.nodeid.lower()
        if 'phaser' in test_file or 'substitute_ligand' in test_file:
            phaser_tests.append(item)
        else:
            other_tests.append(item)
    items[:] = phaser_tests + other_tests
```

### New Test Configuration (Order-Independent)
```python
def pytest_collection_modifyitems(items):
    """Automatically add django_db marker to all test items."""
    for item in items:
        item.add_marker(pytest.mark.django_db(transaction=True))

    # NOTE: Test reordering DISABLED to verify order-independence
    # (Original reordering logic commented out)
```

### Test Execution
```bash
# Run tests in TRUE alphabetical order (no forced reordering)
gtimeout 2700 ./run_test.sh tests/i2run/ > /tmp/truly_alphabetical.txt 2>&1
```

**Key Difference**: Tests now run in alphabetical order:
- test_acedrg.py (RDKit-using tests) run **FIRST**
- test_phaser_*.py (pickle-using tests) run **LATER**

This is the **opposite** of our previous forced ordering!

## Concurrent Test Safety Enhancement

Added random suffix to project directory names (conftest.py lines 169-175):

```python
# Generate random suffix for uniqueness (6 alphanumeric chars)
# This prevents directory collisions in concurrent test runs
random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# Build consistent project name with random suffix
if test_function and test_file:
    project_name = f"tmp_{test_file}_{test_function}_{random_suffix}"
```

**Before**: `tmp_acedrg_test_from_smiles` (deterministic, collides in parallel runs)
**After**: `tmp_acedrg_test_from_smiles_x7k2p9` (unique, safe for parallel execution)

## Expected Results

### Success Criteria (Order-Independent)
If underlying fixes are correct:
- **Pass rate**: Similar to previous 82% (55/67 tests)
- **No RDKit contamination**: Phaser tests should pass even when run after acedrg
- **No directory collisions**: Random suffixes prevent concurrent test conflicts

### Failure Indicators (Still Order-Dependent)
If tests are still order-dependent:
- **Phaser pickle errors**: "rdkit.rdBase._vectd instances cannot be pickled"
- **Lower pass rate**: Significantly worse than 82%
- **File-not-found errors**: Indicates job numbering/directory issues

## Test Status

- **Start time**: ~11:00 (estimated)
- **Current progress**: 30% (test_editbfac) as of 11:22:51
- **Monitor log**: `/tmp/alphabetical_monitor.log`
- **Results file**: `/tmp/truly_alphabetical.txt`

## Files Modified

1. **tests/i2run/conftest.py**
   - Lines 70-89: Disabled forced test reordering
   - Lines 169-175: Added random suffix for concurrent safety
   - Lines 224-246: Enhanced RDKit cleanup (already present)

2. **core/CCP4XtalData.py**
   - Lines 1468-1601: Improved clipperSameCell() (Clipper reciprocal space algorithm)
   - Lines 2675-2808: CUnmergedDataContent.clipperSameCell() (duplicate implementation)

## Next Steps (After Test Completion)

1. **Analyze pass/fail rate** - Compare to previous 82% baseline
2. **Check for RDKit errors** - Grep for "rdkit" or "pickle" failures
3. **Identify new failures** - Any tests that fail in alphabetical order but passed in forced order
4. **Decision point**:
   - If tests pass: Remove forced ordering permanently (tests are truly order-independent)
   - If tests fail: Re-enable forced ordering and investigate remaining issues

## Relevant Documentation

- **pytest_collection_modifyitems**: [pytest docs](https://docs.pytest.org/en/stable/reference/reference.html#pytest.hookspec.pytest_collection_modifyitems)
- **RDKit pickle issue**: See conftest.py lines 220-246 comments
- **Concurrent test safety**: See conftest.py lines 156-171 comments
