"""
CDataFile - Base class for file-related CData classes.

Provides file path management with:
- setFullPath() / getFullPath() for file path operations
- fullPath property for convenient access
- __str__() returns the file path
- Automatic contentFlag introspection
- File I/O placeholder methods (load_from_file, save_to_file)

File path handling:
- In standalone mode: Uses baseName attribute
- In database mode (future): Uses project + relPath + baseName
"""

from typing import Optional, Any
from pathlib import Path

from .cdata import CData


class CDataFile(CData):
    """Base class for file-related CData classes.

    Attributes are automatically created from embedded metadata:
    - project: CProjectId - Project identifier
    - baseName: CFilePath - Base filename
    - relPath: CFilePath - Relative path to file
    - annotation: CString - File annotation
    - dbFileId: CUUID - Database file identifier
    - subType: CInt - File subtype (optional)
    - contentFlag: CInt - Content flag (min=0, optional)

    CDataFile has special behavior for file path handling:
    - Assigning a string to a CDataFile sets the baseName attribute
    - __str__() returns the file path (baseName when not database-connected)
    - fullPath property and getFullPath() method return the full path
    """

    def __init__(self, file_path: str = None, parent=None, name=None, **kwargs):
        # Pass per-instance metadata overrides to base
        super().__init__(parent=parent, name=name, **kwargs)

        # Legacy compatibility
        self.file_path = file_path

        # Set baseName if file_path provided
        if file_path is not None:
            self.setFullPath(file_path)

    def setFullPath(self, path: str):
        """Set the full path of the file.

        In non-database-connected mode, this sets the baseName attribute.
        In database-connected mode (future), this would parse the path
        and set project, relPath, and baseName appropriately.

        Args:
            path: Full file path as a string
        """
        # For now (non-database mode), just set baseName
        if hasattr(self, 'baseName'):
            # If baseName is a CFilePath or similar, set its value
            if hasattr(self.baseName, 'value'):
                self.baseName.value = path
            else:
                # Otherwise set it directly
                self.baseName = path
        else:
            # baseName doesn't exist yet - store in file_path for now
            object.__setattr__(self, 'file_path', path)

    def getFullPath(self) -> str:
        """Get the full file path as a string.

        Returns:
            Full path to the file, or empty string if not set
        """
        # Non-database mode: return baseName
        if hasattr(self, 'baseName') and self.baseName is not None:
            # If baseName has a value attribute, return that
            if hasattr(self.baseName, 'value'):
                return str(self.baseName.value) if self.baseName.value is not None else ""
            # Otherwise convert baseName directly
            return str(self.baseName)

        # Fallback to legacy file_path
        if hasattr(self, 'file_path') and self.file_path is not None:
            return str(self.file_path)

        return ""

    @property
    def fullPath(self) -> str:
        """Property to access the full file path as a string.

        Returns:
            Full path to the file, or empty string if not set
        """
        return self.getFullPath()

    def __str__(self) -> str:
        """Return string representation of the file (its path).

        Returns:
            Full path to the file, or empty string if not set
        """
        return self.getFullPath()

    def set(self, value={}, **kw):
        """Set file attributes. Compatible with old CCP4i2 API.

        Args:
            value: Can be:
                - str: File path (calls setFullPath)
                - dict: Dict of attributes to set
                - CDataFile: Another file object to copy from
            **kw: Additional keyword arguments passed to parent
        """
        if isinstance(value, str):
            # String argument: set as file path
            self.setFullPath(value)
        elif isinstance(value, CDataFile):
            # Another CDataFile: copy its attributes
            super().set(value.get())
        elif isinstance(value, dict):
            # Dict: handle special cases for file paths
            if 'fullPath' in value:
                self.setFullPath(value['fullPath'])
            else:
                # Regular dict - pass to parent
                super().set(value)
        else:
            # Fallback to parent implementation
            super().set(value)

    def load_from_file(self, file_path: str):
        """Load data from file."""
        self.setFullPath(file_path)
        # TODO: Implement file loading logic

    def save_to_file(self, file_path: str = None):
        """Save data to file."""
        path = file_path or self.getFullPath()
        if not path:
            raise ValueError("No file path specified")
        # TODO: Implement file saving logic

    def _get_conversion_output_path(
        self,
        target_content_type: str,
        target_extension: Optional[str] = None,
        work_directory: Optional[Any] = None
    ) -> str:
        """
        Calculate output path for converted file (generic for all file types).

        This is a base class method used by as_CONTENTTYPE() conversion methods
        in subclasses. It generates output paths following the pattern:
        {inputroot}_as_{CONTENT_TYPE}{extension}

        Naming pattern: {inputroot}_as_{CONTENT_TYPE}{extension}
        Location: Input file's directory (if writable), else work_directory

        Args:
            target_content_type: Name of target content type (e.g., 'FMEAN', 'MMCIF')
            target_extension: Optional extension override (e.g., '.cif').
                            If None, uses input file's extension.
            work_directory: Fallback directory if input dir not writable

        Returns:
            Full path to output file

        Examples:
            >>> # MTZ conversion (same extension)
            >>> obs_file._get_conversion_output_path('FMEAN')
            '/data/input_as_FMEAN.mtz'

            >>> # PDB to mmCIF (different extension)
            >>> pdb_file._get_conversion_output_path('MMCIF', '.cif')
            '/data/model_as_MMCIF.cif'
        """
        from pathlib import Path

        input_path = Path(self.getFullPath())
        input_dir = input_path.parent
        input_stem = input_path.stem  # Filename without extension

        # Use target_extension if provided, otherwise preserve input extension
        extension = target_extension if target_extension else input_path.suffix

        # Calculate output filename
        output_name = f"{input_stem}_as_{target_content_type}{extension}"

        # Try input directory first (if it exists and we can write there)
        if input_dir.exists() and input_dir.is_dir():
            output_path = input_dir / output_name
            # Check if we can write there (basic check)
            try:
                # Try to create a test file
                test_file = input_dir / f".write_test_{id(self)}"
                test_file.touch()
                test_file.unlink()
                return str(output_path)
            except (PermissionError, OSError):
                # Not writable, fall through to work_directory
                pass

        # Fall back to work directory
        if work_directory:
            work_dir = Path(work_directory)
            return str(work_dir / output_name)

        # Last resort: same as input (may fail at write time if not writable)
        return str(input_dir / output_name)

    def setContentFlag(self, content_flag: Optional[int] = None):
        """
        Set or auto-detect the content flag for this file.

        For backward compatibility, this method can be called without arguments
        to trigger automatic introspection of the file's content.

        Args:
            content_flag: If provided, sets contentFlag to this value directly.
                         If None, attempts to auto-detect by inspecting the file
                         (behavior depends on subclass implementation).

        Examples:
            >>> # Explicit assignment
            >>> obs_file.setContentFlag(4)  # Set to FMEAN

            >>> # Auto-detection (for MTZ files)
            >>> obs_file.setContentFlag()  # Introspects file, sets based on columns
        """
        if content_flag is not None:
            flag_value = content_flag
        else:
            # Auto-detection: delegate to subclass-specific implementation
            flag_value = self._introspect_content_flag()
            if flag_value is None:
                return  # No detection, don't change contentFlag

        # Set the value, handling both CData wrappers and plain values
        if hasattr(self, 'contentFlag') and hasattr(self.contentFlag, 'value'):
            # contentFlag is a CData wrapper - set its .value attribute
            self.contentFlag.value = flag_value
        else:
            # contentFlag doesn't exist or isn't a proper CData wrapper
            # Use simple assignment and hope smart assignment works
            # (If contentFlag is CInt with _is_value_type(), smart assign will work)
            # (If contentFlag is generic CData without _is_value_type(), it will be replaced)
            # TODO: Fix metadata system to create CInt instead of CData
            self.contentFlag = flag_value

    def _introspect_content_flag(self) -> Optional[int]:
        """
        Auto-detect the content flag by inspecting the file.

        This is the base implementation that does nothing. Subclasses
        (like CMiniMtzDataFile) override this to provide file-type-specific
        introspection logic.

        Returns:
            Detected content flag value, or None if cannot be determined
        """
        # Base implementation: no introspection capability
        return None
