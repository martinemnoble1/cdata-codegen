# MTZ Manipulation Error Handling - Quick Summary

## Status: ⚠️ Needs Improvement

The MTZ manipulation methods (makeHklin, splitHklout, etc.) have **less detailed error handling** than our converters.

## Critical Issues Found

### 1. Silent Failures (Lines 1437, 1506)

**Current code**:
```python
try:
    infiles.append([str(obj.fullPath), obj.columnNames(True)])
except:
    pass  # ⚠️ SWALLOWS ERRORS SILENTLY
```

**Comment in code**: "Keep this (unfortunately). Trying to avoid any changes cascading through i2."

**Impact**: Users get no indication when column name retrieval fails.

### 2. Missing Exit Code Context

**Current code** (joinMtz, line 1569):
```python
exitCode = CCP4Modules.PROCESSMANAGER().getJobData(pid, 'exitCode')
# exitCode retrieved but NOT included in error messages!

if status != 0:
    return CPluginScript.FAILED, 32  # Just error code 32
```

**Impact**: Error says "failed running mtzjoin" but not WHY (exit code, reason).

### 3. No Subprocess Error Capture

**Current code**:
```python
pid = CCP4Modules.PROCESSMANAGER().startProcess(bin, arglist, logFile=logFile)
# ...
# Log file created but never parsed for errors
return CPluginScript.FAILED, 32
```

**Impact**: cmtzjoin/cmtzsplit error messages not surfaced to user.

### 4. Vague Error Messages

**Current ERROR_CODES**:
- Code 27: "Error interpreting output data for split MTZ"
- Code 28: "Error interpreting input data for join MTZ"
- Code 32: "Error converting miniMTZ to HKLIN - failed running mtzjoin"
- Code 34: "Error converting HKLOUT to miniMTZ - failed running mtzsplit"

**Impact**: No details about WHAT went wrong (file paths, columns, exit codes).

## Quick Comparison

| Feature | Our Converters | MTZ Methods |
|---------|---------------|-------------|
| Specific error codes | ✅ 6-10 per converter | ⚠️ 7 generic codes |
| Silent failures | ✅ 0 | ❌ 2+ |
| Exit codes in errors | ✅ Yes | ❌ No |
| Plugin error capture | ✅ Yes | ❌ No |
| File paths in errors | ✅ Full paths | ⚠️ Filename only |
| Column details | ✅ Yes | ❌ No |
| Input validation | ✅ Yes | ❌ No |
| Binary existence checks | ✅ Yes | ❌ No |

## Recommended Fixes

### Priority 1: Fix Silent Failures

Replace:
```python
except:
    pass
```

With:
```python
except Exception as e:
    error.append(self.__class__, 37,
                 details=f"Cannot get column names for {obj.fullPath}: {str(e)}")
    self.appendErrorReport(37, f"{obj.fullPath}: {str(e)}")
```

### Priority 2: Include Exit Codes

Replace:
```python
if status != 0:
    return CPluginScript.FAILED, 32
```

With:
```python
if status != 0:
    error_details = f"cmtzjoin failed with exit code {exitCode}\n"
    error_details += f"Output file: {outfile}\n"
    error_details += f"Check logs in {logFile}"
    self.appendErrorReport(32, error_details)
    return CPluginScript.FAILED, 32
```

### Priority 3: Parse Log Files

After subprocess failure:
```python
if os.path.exists(logFile):
    try:
        with open(logFile, 'r') as f:
            lines = f.readlines()
            error_lines = [l for l in lines if 'error' in l.lower()]
            if error_lines:
                error_details += f"\nLog errors:\n{''.join(error_lines[-5:])}"
    except:
        pass
```

## Methods Analyzed

1. **makeHklin** (line 1411) - Merge mini-MTZs into hklin.mtz
   - ⚠️ Silent failure at line 1437
   - ⚠️ No exit code in error 32

2. **makeHklInput** (line 1466) - Wrapper with flexible column naming
   - ⚠️ Delegates to _buildInputVector with silent failures

3. **_buildInputVector** (line 1498) - Helper for joinMtz input
   - ❌ Silent failure at line 1506 with apologetic comment

4. **joinMtz** (line 1541) - Run cmtzjoin to merge
   - ⚠️ Creates CErrorReport() but never uses it
   - ⚠️ No exit code in errors
   - ⚠️ No log file parsing

5. **splitHklout** (line 1654) - Split hklout.mtz to mini-MTZs
   - ⚠️ No exit code in error 34
   - ⚠️ No log file parsing

6. **splitHkloutList** (line 1677) - Split multiple files
   - ⚠️ Error 34 has NO details at all

7. **splitMtz** (line 1722) - Run cmtzsplit to split
   - ⚠️ No CErrorReport used
   - ⚠️ No exit code in errors
   - ⚠️ No indication of which output file missing

**Note**: No makeHklinGemmi method exists in current codebase.

## Impact on Users

**Current situation**:
- User sees: "Error converting miniMTZ to HKLIN - failed running mtzjoin"
- User doesn't know:
  - Which input file caused the problem
  - What exit code cmtzjoin returned
  - What error message cmtzjoin output
  - Which column names were incompatible
  - Where to find the log file

**After improvements**:
- User sees: "Error merging MTZ files with cmtzjoin (exit code 1)"
- User knows:
  - Full path to output file attempted
  - Exit code from cmtzjoin
  - Key error lines from cmtzjoin log
  - Path to full log file for debugging
  - Which columns were being merged

## Next Steps

1. ✅ **Documentation complete** - This analysis documents all issues
2. ⬜ **Decide on approach** - Incremental fixes vs. full refactor?
3. ⬜ **Add error codes** - Define new codes 37-41 for specific failures
4. ⬜ **Fix silent failures** - Replace bare except: pass blocks
5. ⬜ **Enhance error details** - Include exit codes, file paths, columns
6. ⬜ **Add tests** - Verify error handling improvements
7. ⬜ **Update ERROR_CODES** - Make descriptions more specific

## Recommendation

**Incremental improvement approach**:

- **Phase 1** (2-4 hours): Fix silent failures + add exit codes
- **Phase 2** (2-4 hours): Add binary checks + input validation
- **Phase 3** (4-8 hours): Refactor to match converter pattern + tests

This brings MTZ manipulation to the same error handling standard as our converters, addressing the user's concern about surfacing failure reasons.

---

*Analysis completed: 2025-01-15*
*See MTZ_MANIPULATION_ERROR_ANALYSIS.md for detailed analysis*
