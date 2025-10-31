"""
Result type for standardized operation returns.

Provides a consistent way to return success/failure from library functions
that can be easily consumed by both API endpoints and management commands.
"""

from typing import TypeVar, Generic, Optional, Dict, Any
from dataclasses import dataclass, field

T = TypeVar('T')


@dataclass
class Result(Generic[T]):
    """
    Standardized result type for library operations.

    Encapsulates either a successful result with data, or a failure with
    error information. This provides a consistent interface for both
    API endpoints and CLI commands to handle operation outcomes.

    Attributes:
        success: Whether the operation succeeded
        data: Result data (if successful)
        error: Error message (if failed)
        error_details: Additional error context (if failed)

    Example:
        >>> result = Result.ok({"job_id": 123})
        >>> if result.success:
        ...     print(result.data)

        >>> result = Result.fail("Job not found", {"job_id": 999})
        >>> print(result.error)  # "Job not found"
    """

    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    error_details: Optional[Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def ok(cls, data: T) -> 'Result[T]':
        """
        Create a successful result.

        Args:
            data: The result data

        Returns:
            Result with success=True and the provided data
        """
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str, details: Optional[Dict[str, Any]] = None) -> 'Result[T]':
        """
        Create a failed result.

        Args:
            error: Error message
            details: Optional additional error context

        Returns:
            Result with success=False and error information
        """
        return cls(
            success=False,
            error=error,
            error_details=details or {}
        )

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for API/CLI responses.

        Returns:
            Dictionary with status, data/reason, and optional details

        Example:
            Success: {"status": "Success", "data": {...}}
            Failure: {"status": "Failed", "reason": "...", "details": {...}}
        """
        if self.success:
            return {
                "status": "Success",
                "data": self.data
            }
        else:
            result = {
                "status": "Failed",
                "reason": self.error
            }
            if self.error_details:
                result["details"] = self.error_details
            return result

    def unwrap(self) -> T:
        """
        Unwrap the result, raising an exception if failed.

        Returns:
            The data if successful

        Raises:
            ValueError: If the result is a failure

        Example:
            >>> result = Result.ok(42)
            >>> value = result.unwrap()  # 42

            >>> result = Result.fail("Error")
            >>> value = result.unwrap()  # Raises ValueError
        """
        if self.success:
            return self.data
        else:
            raise ValueError(f"Cannot unwrap failed result: {self.error}")

    def unwrap_or(self, default: T) -> T:
        """
        Unwrap the result or return a default value.

        Args:
            default: Value to return if result is a failure

        Returns:
            The data if successful, otherwise the default
        """
        return self.data if self.success else default

    def map(self, func):
        """
        Map a function over the result data.

        If the result is successful, applies func to the data.
        If the result is a failure, returns the failure unchanged.

        Args:
            func: Function to apply to successful data

        Returns:
            New Result with transformed data or original failure
        """
        if self.success:
            return Result.ok(func(self.data))
        else:
            return self


# Convenience alias for clarity in some contexts
OperationResult = Result
