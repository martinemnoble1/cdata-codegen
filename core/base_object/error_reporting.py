"""Error reporting and validation system for CData objects.

This module implements the CCP4i2-compatible error handling system, providing
error tracking, severity levels, and validation reporting capabilities.
"""

from typing import List, Optional, Dict, Any
from enum import IntEnum


class Severity(IntEnum):
    """Error severity levels for validation and error reporting."""
    OK = 0
    UNDEFINED = 1
    WARNING = 2
    UNDEFINED_ERROR = 3
    ERROR = 4


# Legacy compatibility constants
SEVERITY_OK = Severity.OK
SEVERITY_UNDEFINED = Severity.UNDEFINED
SEVERITY_WARNING = Severity.WARNING
SEVERITY_UNDEFINED_ERROR = Severity.UNDEFINED_ERROR
SEVERITY_ERROR = Severity.ERROR


class CErrorReport:
    """Error report container for tracking validation errors and warnings.

    CErrorReport holds a list of errors, each containing:
    - klass: The class name where the error occurred
    - code: Error code number (from ERROR_CODES dictionary)
    - details: Additional details about the error
    - name: Object name where error occurred
    - severity: Severity level (0=OK, 1=UNDEFINED, 2=WARNING, 3=UNDEFINED_ERROR, 4=ERROR)

    Example:
        >>> report = CErrorReport()
        >>> report.append("CInt", 101, "Value exceeds maximum", "myInt", Severity.ERROR)
        >>> print(report.maxSeverity())
        4
        >>> print(report.report())
        ERROR in CInt 'myInt': Value exceeds maximum (code 101)
    """

    def __init__(self):
        """Initialize an empty error report."""
        self._errors: List[Dict[str, Any]] = []

    def append(self, klass: str, code: int, details: str, name: str = "",
               severity: int = SEVERITY_ERROR):
        """Add a single error to the report.

        Args:
            klass: Class name where error occurred
            code: Error code number
            details: Error description/details
            name: Object name (optional)
            severity: Severity level (default: SEVERITY_ERROR)
        """
        self._errors.append({
            'class': klass,
            'code': code,
            'details': details,
            'name': name,
            'severity': severity
        })

    def extend(self, other: 'CErrorReport'):
        """Merge another error report into this one.

        Args:
            other: Another CErrorReport to merge
        """
        if isinstance(other, CErrorReport):
            self._errors.extend(other._errors)

    def count(self) -> int:
        """Return the number of errors in this report.

        Returns:
            Number of errors
        """
        return len(self._errors)

    def maxSeverity(self) -> int:
        """Return the maximum severity level of all errors.

        Returns:
            Maximum severity (0-4), or SEVERITY_OK if no errors
        """
        if not self._errors:
            return SEVERITY_OK
        return max(error['severity'] for error in self._errors)

    def report(self, severity_threshold: int = SEVERITY_WARNING) -> str:
        """Generate a formatted report of errors at or above severity threshold.

        Args:
            severity_threshold: Minimum severity to include (default: WARNING)

        Returns:
            Formatted error report string
        """
        if not self._errors:
            return "No errors"

        lines = []
        severity_names = {
            SEVERITY_OK: "OK",
            SEVERITY_UNDEFINED: "UNDEFINED",
            SEVERITY_WARNING: "WARNING",
            SEVERITY_UNDEFINED_ERROR: "UNDEFINED_ERROR",
            SEVERITY_ERROR: "ERROR"
        }

        for error in self._errors:
            if error['severity'] >= severity_threshold:
                severity_name = severity_names.get(error['severity'], "UNKNOWN")
                name_part = f" '{error['name']}'" if error['name'] else ""
                lines.append(
                    f"{severity_name} in {error['class']}{name_part}: "
                    f"{error['details']} (code {error['code']})"
                )

        return "\n".join(lines) if lines else f"No errors at or above severity {severity_threshold}"

    def __str__(self) -> str:
        """Return a string representation of the error report.

        Returns:
            Formatted error report
        """
        return self.report(SEVERITY_WARNING)

    def __bool__(self) -> bool:
        """Return True if there are errors with severity >= WARNING.

        Returns:
            True if there are warnings or errors
        """
        return self.maxSeverity() >= SEVERITY_WARNING

    def __len__(self) -> int:
        """Return the number of errors.

        Returns:
            Number of errors
        """
        return self.count()

    def getErrors(self) -> List[Dict[str, Any]]:
        """Get the list of all errors.

        Returns:
            List of error dictionaries
        """
        return self._errors.copy()

    def clear(self):
        """Clear all errors from the report."""
        self._errors.clear()


class CException(CErrorReport, Exception):
    """Exception class that combines CErrorReport functionality with Python exceptions.

    This allows errors to be both raised as exceptions and tracked in error reports.

    Example:
        >>> exc = CException("CInt", 101, "Value out of range", "myInt", Severity.ERROR)
        >>> raise exc
    """

    def __init__(self, klass: str = "", code: int = 0, details: str = "",
                 name: str = "", severity: int = SEVERITY_ERROR):
        """Initialize exception with error details.

        Args:
            klass: Class name where error occurred
            code: Error code number
            details: Error description
            name: Object name
            severity: Severity level
        """
        CErrorReport.__init__(self)
        Exception.__init__(self, details)

        if klass or code or details:
            self.append(klass, code, details, name, severity)
