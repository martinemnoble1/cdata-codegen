"""
Standardized response types for CCP4i2 operations.

This module provides consistent result and error handling across
the library, API, and CLI layers.
"""

from .result import Result, OperationResult
from .exceptions import (
    CCP4OperationError,
    JobNotFoundError,
    ProjectNotFoundError,
    ValidationError,
    FileOperationError,
    ParameterError,
)

__all__ = [
    'Result',
    'OperationResult',
    'CCP4OperationError',
    'JobNotFoundError',
    'ProjectNotFoundError',
    'ValidationError',
    'FileOperationError',
    'ParameterError',
]
