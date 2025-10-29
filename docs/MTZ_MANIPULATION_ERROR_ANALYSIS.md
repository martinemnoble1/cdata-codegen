# MTZ Manipulation Methods - Error Handling Analysis

## Executive Summary

**Status**: ⚠️ **Error handling in MTZ manipulation methods needs improvement**

The makeHklin/makeHklInput/splitHklout methods have **significantly less detailed error handling** compared to our converter implementation. They suffer from:
- Silent failures via bare `except: pass` blocks
- Vague error messages lacking context
- Missing file paths, column names, and exit codes
- No capture of subprocess error output
- Inconsistent error reporting patterns

## Methods Analyzed

### 1. makeHklin (line 1411)
**Purpose**: Merge multiple mini-MTZ files into a single hklin.mtz file

**Error handling**:
```python
def makeHklin(self, miniMtzsIn=[], hklin='hklin', ignoreErrorCodes=[]):
    error = CErrorReport()

    for miniMtz in miniMtzsIn:
        obj = self.container.inputData.get(mtzName)
        if obj is None:
            self.appendErrorReport(31, mtzName)
            error.append(self.__class__, 31, mtzName)
        elif not obj.isSet():
            self.appendErrorReport(30, mtzName)
            error.append(self.__class__, 30, mtzName)
        else:
            if targetContent is None:
                try:
                    infiles.append([str(obj.fullPath), obj.columnNames(True)])
                except:
                    pass  # ⚠️ SILENT FAILURE
            elif conversion == 'convert':
                rv = obj.convert(targetContent, parentPlugin=self)
                filePath, convertError = rv
                error.extend(convertError)
                if error.maxSeverity() <= SEVERITY_WARNING:  # ✅ GOOD
                    infiles.append([filePath, ...])

    status, ret = self.joinMtz(outfile, infiles)
    if status != CPluginScript.SUCCEEDED and ret not in ignoreErrorCodes:
        error.append(CPluginScript, ret, hklin)  # ⚠️ VAGUE
        self.appendErrorReport(ret, hklin, cls=CPluginScript)

    return outfile, error
```

**Issues**:
- ✅ Good: Creates CErrorReport, extends with converter errors, checks maxSeverity()
- ✅ Good: Dual reporting (local error + self.appendErrorReport)
- ⚠️ Problem: Bare `except: pass` at line 1437 silently swallows columnNames() failures
- ⚠️ Problem: Error code 32 ("failed running mtzjoin") provides no details about WHY
- ⚠️ Problem: No subprocess exit code or error output captured
- ⚠️ Problem: Only passes `hklin` as details, not full file paths or column info

### 2. makeHklInput (line 1466)
**Purpose**: Wrapper around makeHklin with flexible column naming options

**Error handling**:
```python
def makeHklInput(self, miniMtzsIn=[], hklin='hklin', ignoreErrorCodes=[],
                 extendOutputColnames=True, useInputColnames=False):
    error = CErrorReport()

    for miniMtz in miniMtzsIn:
        obj = self.container.inputData.get(mtzName)
        if obj is None:
            self.appendErrorReport(31, mtzName)
            error.append(self.__class__, 31, mtzName)
        elif not obj.isSet():
            self.appendErrorReport(30, mtzName)
            error.append(self.__class__, 30, mtzName)
        else:
            self._buildInputVector(obj, mtzName, targetContent, error, ...)

    status, ret = self.joinMtz(outfile, infiles)
    if status != CPluginScript.SUCCEEDED and ret not in ignoreErrorCodes:
        error.append(CPluginScript, ret, hklin)
        self.appendErrorReport(ret, hklin, cls=CPluginScript)

    return outfile, allColout.strip(','), error
```

**Issues**:
- ✅ Good: Similar pattern to makeHklin
- ⚠️ Problem: Delegates to _buildInputVector which has silent failures
- ⚠️ Problem: Same vague error reporting as makeHklin

### 3. _buildInputVector (line 1498)
**Purpose**: Helper to build input vector for joinMtz

**Error handling**:
```python
def _buildInputVector(self, obj, mtzName, targetContent, error, ...):
    if targetContent is None:
        try:
            infile = str(obj.fullPath)
            colin, ext_outputCol = self.makeColinColout(mtzName, obj)
            colout = obj.columnNames(True)
        except:
            pass  # ⚠️ SILENT FAILURE with comment "Keep this (unfortunately)"
    else:
        obj.setContentFlag()
        conversion, targetContent = obj.conversion(targetContent)
        if conversion == 'no':
            error.append(self.__class__, 35, mtzName)
        elif conversion == 'convert':
            rv = obj.convert(targetContent, parentPlugin=self)
            filePath, convertError = rv
            error.extend(convertError)
            if error.maxSeverity() <= SEVERITY_WARNING:  # ✅ GOOD
                colin, ext_outputCol = self.makeColinColout(...)
```

**Issues**:
- ⚠️ **Critical**: Bare `except: pass` at line 1506 with comment acknowledging it's a problem
- ⚠️ Problem: Comment says "Keep this (unfortunately). Trying to avoid any changes cascading through i2"
- ✅ Good: Conversion errors are extended, maxSeverity checked
- ⚠️ Problem: Silent failure means missing columns won't be reported

### 4. joinMtz (line 1541)
**Purpose**: Run cmtzjoin to merge MTZ files

**Error handling**:
```python
def joinMtz(self, outfile, infiles):
    from core import CCP4Utils
    error = CErrorReport()  # ⚠️ Created but never used!
    logFile = self.makeFileName('LOG', qualifier='mtzjoin')

    bin = os.path.join(CCP4Utils.getOSDir(), 'bin', exe)
    arglist = ['-mtzout', outfile]

    try:
        if len(infiles[0]) == 2:
            for name, cols in infiles:
                arglist.extend(('-mtzin', name))
                if len(cols) > 0:
                    arglist.extend(('-colout', cols))
        else:
            for name, colin, colout in infiles:
                arglist.extend(('-mtzin', name))
                arglist.extend(('-colin', colin))
                arglist.extend(('-colout', colout))
    except:
        self.appendErrorReport(28, str(infiles))  # ⚠️ GENERIC

    pid = CCP4Modules.PROCESSMANAGER().startProcess(bin, arglist, logFile=logFile)
    status = CCP4Modules.PROCESSMANAGER().getJobData(pid)
    exitCode = CCP4Modules.PROCESSMANAGER().getJobData(pid, 'exitCode')

    # ⚠️ No checking of logFile for error details
    # ⚠️ No checking if cmtzjoin binary exists
    # ⚠️ exitCode retrieved but not used in error reporting

    if status in [0, 101] and os.path.exists(outfile):
        return CPluginScript.SUCCEEDED, None
    elif status in [101]:
        return CPluginScript.UNSATISFACTORY, 36
    else:
        return CPluginScript.FAILED, 32
```

**Issues**:
- ⚠️ Problem: Creates `error = CErrorReport()` but never uses it or returns it
- ⚠️ Problem: Bare `except:` at line 1564 with generic error code 28
- ⚠️ Problem: Error 28 only includes str(infiles), not which specific file failed
- ⚠️ Problem: exitCode retrieved but not included in error reporting
- ⚠️ Problem: No checking if cmtzjoin binary exists before running
- ⚠️ Problem: No parsing of logFile for detailed error messages
- ⚠️ Problem: Returns status codes instead of CErrorReport
- ⚠️ Problem: Hardcoded handling of status 101 without explanation

### 5. splitHklout (line 1654)
**Purpose**: Split hklout.mtz into multiple mini-MTZ output files

**Error handling**:
```python
def splitHklout(self, miniMtzsOut=[], programColumnNames=[], infile=None, logFile=None):
    error = CErrorReport()
    if infile is None:
        infile = os.path.join(self.workDirectory, 'hklout.mtz')

    outfiles = []
    for ii in range(min(len(miniMtzsOut), len(programColumnNames))):
        obj = self.container.outputData.get(mtzName)
        if obj is None:
            error.append(self.__class__, 33, mtzName)
            self.appendErrorReport(33, mtzName)  # ✅ GOOD: Dual reporting
        elif not obj.isSet():
            pass  # ⚠️ Silent skip
        else:
            outfiles.append([str(obj.fullPath), programColumnNames[ii], obj.columnNames(True)])

    status = self.splitMtz(infile, outfiles, logFile)
    if status != CPluginScript.SUCCEEDED:
        error.append(self.__class__, 34, str(outfiles))  # ⚠️ VAGUE
        self.appendErrorReport(34, str(outfiles))
        return error

    print('splitHklout DONE')
    return error
```

**Issues**:
- ✅ Good: Dual reporting (local error + self.appendErrorReport)
- ⚠️ Problem: Error 34 only includes str(outfiles), not exit code or reason
- ⚠️ Problem: No checking if infile exists before splitting
- ⚠️ Problem: Silent skip when obj.isSet() is False (line 1666)
- ⚠️ Problem: No validation of programColumnNames vs miniMtzsOut lengths

### 6. splitHkloutList (line 1677)
**Purpose**: Split multiple input files into output file lists

**Error handling**:
```python
def splitHkloutList(self, miniMtzsOut=[], programColumnNames=[],
                    outputBaseName=[], outputContentFlags=[], infileList=[], logFile=None):
    error = CErrorReport()

    # ... setup code ...

    for infile in infileList:
        outfiles = []
        for ii in range(min(len(miniMtzsOut), len(programColumnNames))):
            # ... build outfiles ...

        status = self.splitMtz(infilePath, outfiles, logFile)
        if status != CPluginScript.SUCCEEDED:
            error.append(self.__class__, 34)  # ⚠️ VAGUE, no hklout variable
            self.appendErrorReport(34)
            return error

    return error
```

**Issues**:
- ✅ Good: Dual reporting
- ⚠️ Problem: Error 34 has no details at all (comment notes hklout doesn't exist)
- ⚠️ Problem: First failure aborts all remaining files
- ⚠️ Problem: No indication of WHICH file in the list failed

### 7. splitMtz (line 1722)
**Purpose**: Run cmtzsplit to split MTZ file

**Error handling**:
```python
def splitMtz(self, infile, outfiles, logFile=None):
    print('CPluginScript.splitMtz', infile, outfiles)
    from core import CCP4Utils

    if logFile is None:
        logFile = self.makeFileName('LOG', qualifier='mtzsplit')

    bin = os.path.join(CCP4Utils.getOSDir(), 'bin', 'cmtzsplit')
    arglist = ['-mtzin', infile]

    try:
        for outfile in outfiles:
            if len(outfile) == 2:
                name, colin = outfile
                colout = ''
            else:
                name, colin, colout = outfile
            arglist.append('-mtzout')
            arglist.append(name)
            # ... build arglist ...
    except:
        self.appendErrorReport(27, str(outfiles))  # ⚠️ GENERIC

    pid = CCP4Modules.PROCESSMANAGER().startProcess(bin, arglist, logFile=logFile)
    status = CCP4Modules.PROCESSMANAGER().getJobData(pid)
    exitCode = CCP4Modules.PROCESSMANAGER().getJobData(pid, 'exitCode')

    # ⚠️ exitCode retrieved but not used
    # ⚠️ No checking of logFile for error details

    if status == CPluginScript.SUCCEEDED:
        for outfile in outfiles:
            if not os.path.exists(outfile[0]):
                return CPluginScript.FAILED  # ⚠️ No error details
        return CPluginScript.SUCCEEDED
    else:
        return CPluginScript.FAILED  # ⚠️ No error details
```

**Issues**:
- ⚠️ Problem: No CErrorReport created or returned
- ⚠️ Problem: Bare `except:` at line 1747 with generic error code 27
- ⚠️ Problem: Returns status code only, no error details
- ⚠️ Problem: exitCode retrieved but not used in error reporting
- ⚠️ Problem: No checking if cmtzsplit binary exists
- ⚠️ Problem: When output file missing, returns FAILED with zero context
- ⚠️ Problem: No indication of WHICH output file is missing

## CPluginScript ERROR_CODES

**Relevant error codes** from CPluginScript.ERROR_CODES (lines 55-114):

| Code | Description | Context | Severity | Issues |
|------|-------------|---------|----------|--------|
| 27 | Error interpreting output data for split MTZ | str(outfiles) | ERROR | Too vague, no specific file/column |
| 28 | Error interpreting input data for join MTZ | str(infiles) | ERROR | Too vague, no specific file/column |
| 30 | Warning converting miniMTZ to HKLIN - data not set | mtzName | WARNING | ✅ Clear |
| 31 | Error converting miniMTZ to HKLIN - data name not recognised | mtzName | ERROR | ✅ Clear |
| 32 | Error converting miniMTZ to HKLIN - failed running mtzjoin | hklin | ERROR | No exit code, no reason |
| 33 | Error converting HKLOUT to miniMTZ - data name not recognised | mtzName | ERROR | ✅ Clear |
| 34 | Error converting HKLOUT to miniMTZ - failed running mtzsplit | str(outfiles) | ERROR | No exit code, no reason |
| 35 | Error converting miniMTZ to HKLIN - data type conversion not possible | mtzName | ERROR | ✅ Reasonably clear |
| 36 | Error merging in FreeR flags - insufficient data | hklin | ERROR | ✅ Clear |

## Comparison with Our Converters

### Our Converter Pattern (ObsDataConverter, PhaseDataConverter)

✅ **Structured ERROR_CODES** with specific failure modes:
```python
ERROR_CODES = {
    1: {'description': 'Input file does not exist', 'severity': SEVERITY_ERROR},
    2: {'description': 'Cannot determine contentFlag from input file', 'severity': SEVERITY_ERROR},
    3: {'description': 'Unsupported conversion path', 'severity': SEVERITY_ERROR},
    4: {'description': 'ctruncate plugin not available', 'severity': SEVERITY_ERROR},
    5: {'description': 'ctruncate conversion failed', 'severity': SEVERITY_ERROR},
    6: {'description': 'Output file not created after conversion', 'severity': SEVERITY_ERROR},
    7: {'description': 'Required anomalous data columns not found', 'severity': SEVERITY_ERROR},
    8: {'description': 'Invalid sigma values in anomalous data', 'severity': SEVERITY_ERROR},
}
```

✅ **Detailed error context**:
```python
if wrapper.errorReport.count() > 0:
    error_msg += f"\nErrors:\n{wrapper.errorReport.report()}"
    error_msg += f"\nCheck logs in {ctruncate_work}"
    raise CException(ObsDataConverter, 5, details=error_msg)
```

✅ **Early validation**:
```python
@staticmethod
def _validate_input_file(obs_file):
    from pathlib import Path
    input_path = obs_file.getFullPath()

    if not Path(input_path).exists():
        raise CException(ObsDataConverter, 1, details=f"File: {input_path}")

    content_flag = int(obs_file.contentFlag) if obs_file.contentFlag.isSet() else 0
    if content_flag == 0:
        raise CException(ObsDataConverter, 2, details=f"File: {input_path}")
```

✅ **Plugin error capture**:
```python
if not Path(output_path).exists():
    error_details = f"Output file: {output_path}"
    if hasattr(wrapper, 'errorReport') and wrapper.errorReport.count() > 0:
        error_details += f"\nPlugin errors: {wrapper.errorReport.report()}"
    raise CException(PhaseDataConverter, 6, details=error_details)
```

### MTZ Manipulation Pattern

⚠️ **Generic ERROR_CODES** with minimal context:
```python
ERROR_CODES = {
    27: {'description': 'Error interpreting output data for split MTZ'},
    28: {'description': 'Error interpreting input data for join MTZ'},
    32: {'description': 'Error converting miniMTZ to HKLIN - failed running mtzjoin'},
    34: {'description': 'Error converting HKLOUT to miniMTZ - failed running mtzsplit'},
}
```

⚠️ **Minimal error context**:
```python
if status != CPluginScript.SUCCEEDED:
    error.append(CPluginScript, ret, hklin)  # Just the filename
    self.appendErrorReport(ret, hklin, cls=CPluginScript)
```

⚠️ **No validation**:
```python
# No checking if binary exists
# No checking if input files exist
# No checking column compatibility
```

⚠️ **No subprocess error capture**:
```python
pid = CCP4Modules.PROCESSMANAGER().startProcess(bin, arglist, logFile=logFile)
status = CCP4Modules.PROCESSMANAGER().getJobData(pid)
exitCode = CCP4Modules.PROCESSMANAGER().getJobData(pid, 'exitCode')
# exitCode retrieved but NOT included in error reporting!
```

## Summary of Issues

### Critical Issues

1. **Silent Failures** (Lines 1437, 1506)
   - Bare `except: pass` blocks swallow errors
   - No indication to user that something went wrong
   - Makes debugging extremely difficult

2. **Missing Exit Codes** (Lines 1569, 1752)
   - Exit codes retrieved but not included in error messages
   - Users can't tell if program crashed, had bad input, or other failure

3. **No Subprocess Error Capture**
   - Log files generated but not parsed for errors
   - cmtzjoin/cmtzsplit error messages not surfaced
   - Users told "failed running mtzjoin" with no context

### Moderate Issues

4. **Vague Error Messages**
   - Error 32: "failed running mtzjoin" - WHY did it fail?
   - Error 34: "failed running mtzsplit" - WHY did it fail?
   - Error 27/28: "Error interpreting data" - WHAT was wrong?

5. **Missing File Path Context**
   - Only filename passed, not full path
   - No indication of which input file caused issue
   - No column names when column mismatch occurs

6. **No Binary Existence Checks**
   - Assumes cmtzjoin/cmtzsplit exist
   - Cryptic errors if binaries missing
   - No helpful "cmtzjoin not found" message

7. **Inconsistent Return Patterns**
   - Some return (outfile, error)
   - Some return status code
   - Some return just error
   - Callers must handle multiple patterns

### Minor Issues

8. **Unused Variables**
   - joinMtz creates CErrorReport() but never uses it
   - exitCode retrieved but not reported

9. **Missing Input Validation**
   - No check if input files exist before joining
   - No validation of column name compatibility
   - No check for empty infiles list

## Recommendations

### High Priority

**1. Replace Silent Failures**

Replace bare `except: pass` blocks with proper error handling:

```python
# Current (line 1437):
try:
    infiles.append([str(obj.fullPath), obj.columnNames(True)])
except:
    pass  # SILENT FAILURE

# Recommended:
try:
    infiles.append([str(obj.fullPath), obj.columnNames(True)])
except Exception as e:
    error.append(self.__class__, 37,
                 details=f"Cannot get column names for {obj.fullPath}: {str(e)}")
    self.appendErrorReport(37, f"{obj.fullPath}: {str(e)}")
```

**2. Capture Exit Codes and Subprocess Errors**

Include exit codes and parse log files:

```python
# Current (line 1567-1578):
pid = CCP4Modules.PROCESSMANAGER().startProcess(bin, arglist, logFile=logFile)
status = CCP4Modules.PROCESSMANAGER().getJobData(pid)
exitCode = CCP4Modules.PROCESSMANAGER().getJobData(pid, 'exitCode')
if status in [0, 101] and os.path.exists(outfile):
    return CPluginScript.SUCCEEDED, None
else:
    return CPluginScript.FAILED, 32

# Recommended:
pid = CCP4Modules.PROCESSMANAGER().startProcess(bin, arglist, logFile=logFile)
status = CCP4Modules.PROCESSMANAGER().getJobData(pid)
exitCode = CCP4Modules.PROCESSMANAGER().getJobData(pid, 'exitCode')

if status in [0, 101] and os.path.exists(outfile):
    return CPluginScript.SUCCEEDED, None
else:
    error_details = f"cmtzjoin failed with exit code {exitCode}\n"
    error_details += f"Command: {' '.join([bin] + arglist)}\n"
    error_details += f"Output file: {outfile}\n"
    error_details += f"Check logs in {logFile}"

    # Optionally parse log file for specific errors
    if os.path.exists(logFile):
        try:
            with open(logFile, 'r') as f:
                lines = f.readlines()
                error_lines = [l for l in lines if 'error' in l.lower() or 'fatal' in l.lower()]
                if error_lines:
                    error_details += f"\nLog errors:\n{''.join(error_lines[-5:])}"
        except:
            pass

    self.appendErrorReport(32, error_details)
    return CPluginScript.FAILED, 32
```

**3. Add Detailed ERROR_CODES**

Expand ERROR_CODES to be more specific:

```python
ERROR_CODES = {
    # ... existing codes ...
    32: {'description': 'Error merging MTZ files with cmtzjoin', 'severity': SEVERITY_ERROR},
    34: {'description': 'Error splitting MTZ file with cmtzsplit', 'severity': SEVERITY_ERROR},
    37: {'description': 'Cannot retrieve column names from MTZ file', 'severity': SEVERITY_ERROR},
    38: {'description': 'cmtzjoin binary not found', 'severity': SEVERITY_ERROR},
    39: {'description': 'cmtzsplit binary not found', 'severity': SEVERITY_ERROR},
    # Add more specific codes...
}
```

### Medium Priority

**4. Add Binary Existence Checks**

```python
def joinMtz(self, outfile, infiles):
    from core import CCP4Utils
    error = CErrorReport()

    bin = os.path.join(CCP4Utils.getOSDir(), 'bin', exe)
    if not os.path.exists(bin):
        bin = os.path.join(CCP4Utils.getCCP4Dir(), 'bin', exe)

    # Add check:
    if not os.path.exists(bin):
        error_details = f"cmtzjoin binary not found\n"
        error_details += f"Searched in:\n"
        error_details += f"  {os.path.join(CCP4Utils.getOSDir(), 'bin', exe)}\n"
        error_details += f"  {os.path.join(CCP4Utils.getCCP4Dir(), 'bin', exe)}"
        self.appendErrorReport(38, error_details)
        return CPluginScript.FAILED, 38
```

**5. Add Input Validation**

```python
def splitMtz(self, infile, outfiles, logFile=None):
    # Add validation:
    if not os.path.exists(infile):
        error_details = f"Input file does not exist: {infile}"
        self.appendErrorReport(40, error_details)
        return CPluginScript.FAILED

    if not outfiles or len(outfiles) == 0:
        error_details = "No output files specified for MTZ split"
        self.appendErrorReport(41, error_details)
        return CPluginScript.FAILED

    # ... rest of method ...
```

### Low Priority

**6. Consistent Return Patterns**

Standardize to return (status, error) tuples consistently:

```python
# Instead of returning just status:
return CPluginScript.FAILED

# Return tuple:
return CPluginScript.FAILED, error
```

**7. Remove Unused Variables**

```python
# In joinMtz (line 1543):
error = CErrorReport()  # Remove if not using, or actually use it!
```

## Comparison Table

| Aspect | Our Converters | MTZ Manipulation Methods |
|--------|---------------|-------------------------|
| **Structured ERROR_CODES** | ✅ 6-10 specific codes per converter | ⚠️ 7 generic codes shared |
| **Error details** | ✅ File paths, columns, plugin errors, logs | ⚠️ Minimal (just filename) |
| **Silent failures** | ✅ None - all exceptions raised | ❌ 2 bare `except: pass` blocks |
| **Input validation** | ✅ _validate_input_file() checks existence | ❌ No validation |
| **Plugin error capture** | ✅ wrapper.errorReport included | ❌ Not captured |
| **Exit codes in errors** | ✅ Included when available | ❌ Retrieved but not reported |
| **Binary checks** | ✅ Check plugin availability | ❌ No checks |
| **Log file parsing** | ✅ Suggest log locations | ⚠️ Generated but not parsed |
| **Context in errors** | ✅ Work dirs, columns, file paths | ⚠️ Minimal context |
| **Severity levels** | ✅ All SEVERITY_ERROR | ⚠️ Mix of ERROR/WARNING |

## Test Coverage Needed

To bring MTZ manipulation methods to the same standard as converters, we'd need:

1. **Error handling tests**:
   - Test bare `except` blocks are replaced
   - Test exit codes appear in error messages
   - Test missing binary is detected
   - Test missing input files are detected
   - Test column mismatch errors are clear

2. **Integration tests**:
   - Test joinMtz with invalid column names
   - Test splitMtz with missing input file
   - Test error messages contain full context

3. **Regression tests**:
   - Ensure existing functionality still works
   - Verify error handling doesn't break existing code

## Conclusion

**Gap Analysis**: The MTZ manipulation methods have **significantly less error handling granularity** than our converters:

| Metric | Our Converters | MTZ Methods | Gap |
|--------|---------------|-------------|-----|
| Specific error codes | 6-10 per converter | 7 total | **Low granularity** |
| Silent failures | 0 | 2+ | **Critical gap** |
| Context in errors | High (paths, columns, logs) | Low (filename only) | **Moderate gap** |
| Exit code reporting | Yes | No | **Moderate gap** |
| Plugin error capture | Yes | No | **Moderate gap** |
| Input validation | Yes | No | **Moderate gap** |

**Recommendation**: **Incrementally improve** MTZ manipulation error handling:

1. **Phase 1** (High priority): Fix silent failures, add exit codes
2. **Phase 2** (Medium priority): Add binary checks, input validation
3. **Phase 3** (Low priority): Refactor return patterns, add tests

This would bring them to the same standard as our converter implementation and address the user's concern about surfacing failure reasons.

---

*Analysis completed: 2025-01-15*
*Methods analyzed: makeHklin, makeHklInput, _buildInputVector, joinMtz, splitHklout, splitHkloutList, splitMtz*
*Note: No makeHklinGemmi method found in codebase*
