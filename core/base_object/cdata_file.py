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
import logging

from .cdata import CData

# Configure logger
logger = logging.getLogger(__name__)


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

        # File content instance (instantiated by loadFile())
        self.content = None

        # Set baseName if file_path provided
        if file_path is not None:
            self.setFullPath(file_path)

    def setFullPath(self, path: str):
        """Set the full path of the file.

        In non-database-connected mode, this sets the baseName attribute.
        In database-connected mode, this parses the path and sets project,
        relPath, baseName, and dbFileId appropriately.

        Args:
            path: Full file path as a string
        """
        from pathlib import Path

        logger.debug(
            "[setFullPath] Called for %s, input path: %s, hasattr baseName: %s",
            self.name if hasattr(self, 'name') else 'unnamed',
            path,
            hasattr(self, 'baseName')
        )
        if hasattr(self, 'baseName'):
            logger.debug("  baseName type: %s, has .value: %s", type(self.baseName), hasattr(self.baseName, 'value'))

        # Always set baseName first (basic functionality)
        if hasattr(self, 'baseName'):
            # If baseName is a CFilePath or similar, set its value
            if hasattr(self.baseName, 'value'):
                self.baseName.value = path
                logger.debug("  Set baseName.value = %s", path)
            else:
                # Otherwise set it directly
                self.baseName = path
                logger.debug("  Set baseName = %s", path)
        else:
            # baseName doesn't exist yet - store in file_path for now
            object.__setattr__(self, 'file_path', path)
            logger.debug("  Set file_path = %s (baseName doesn't exist)", path)

        # After setting, check the result
        if hasattr(self, 'baseName'):
            if hasattr(self.baseName, 'value'):
                logger.debug("  AFTER: baseName.value = %s", self.baseName.value)
                # Check value state
                if hasattr(self.baseName, '_value_states'):
                    logger.debug("  AFTER: baseName._value_states = %s", self.baseName._value_states)
                logger.debug("  AFTER: baseName.isSet('value') = %s",
                           self.baseName.isSet('value') if hasattr(self.baseName, 'isSet') else 'N/A')
            else:
                logger.debug("  AFTER: baseName = %s", self.baseName)

        logger.debug("  AFTER: dbFileId = %s",
                    self.dbFileId.value if hasattr(self, 'dbFileId') and hasattr(self.dbFileId, 'value') else 'N/A')
        logger.debug("  AFTER: relPath = %s",
                    self.relPath.value if hasattr(self, 'relPath') and hasattr(self.relPath, 'value') else 'N/A')
        logger.debug("  AFTER: project = %s",
                    self.project.value if hasattr(self, 'project') and hasattr(self.project, 'value') else 'N/A')

        # Database-aware logic: check if we're in a database context
        plugin = self._find_plugin_parent()
        if plugin and hasattr(plugin, 'get_db_job_id') and plugin.get_db_job_id():
            logger.debug("  DB-aware mode: plugin job ID = %s", plugin.get_db_job_id())
            try:
                self._update_from_database(path, plugin)
            except Exception as e:
                # Don't fail on database errors - just log and continue
                logger.debug("Failed to update file from database: %s", e)
        else:
            logger.debug("  Non-DB mode")

    def _find_plugin_parent(self):
        """Walk up the parent hierarchy to find the CPluginScript parent."""
        from core.CCP4PluginScript import CPluginScript
        current = self.parent
        while current:
            if isinstance(current, CPluginScript):
                return current
            current = getattr(current, 'parent', None)
        return None

    def _get_db_handler(self):
        """Get the database handler from the plugin parent, if available."""
        plugin = self._find_plugin_parent()
        if plugin and hasattr(plugin, '_db_handler'):
            return plugin._db_handler
        return None

    def _update_from_database(self, path: str, plugin):
        """Update file attributes from database if the file matches an existing database record.

        Uses the database handler attached to the plugin, if available. This keeps
        CDataFile decoupled from Django and allows for different database backends.

        Args:
            path: Full file path
            plugin: Parent CPluginScript instance
        """
        from pathlib import Path
        import re

        # Get database handler from plugin
        db_handler = self._get_db_handler()
        if not db_handler:
            return  # No database handler available

        abs_path = Path(path).resolve()

        # Try to extract job number from path
        # Path structure: .../project_dir/CCP4_JOBS/job_1/job_2/filename.ext
        # Should extract "1.2" from job_1/job_2
        path_str = str(abs_path)

        # Look for CCP4_JOBS directory pattern
        jobs_match = re.search(r'CCP4_JOBS/(job_\d+(?:/job_\d+)*)', path_str)
        if not jobs_match:
            return  # Not a job directory path

        # Extract job path like "job_1/job_2"
        job_path = jobs_match.group(1)
        # Convert to job number format: "job_1/job_2" → "1.2"
        job_numbers = re.findall(r'job_(\d+)', job_path)
        job_number = '.'.join(job_numbers)

        filename = abs_path.name

        # Query database via handler (returns dict, not Django model)
        try:
            file_info = db_handler.find_file_by_path_sync(
                file_path=str(abs_path),
                job_number=job_number,
                filename=filename
            )

            if file_info:
                # Update CDataFile attributes from database record
                if hasattr(self, 'dbFileId') and hasattr(self.dbFileId, 'value'):
                    self.dbFileId.value = file_info['uuid']

                # Set relPath if available
                if file_info.get('relative_path'):
                    if hasattr(self, 'relPath') and hasattr(self.relPath, 'value'):
                        self.relPath.value = file_info['relative_path']

                # Set project ID
                project_id = getattr(plugin, '_dbProjectId', None)
                if project_id:
                    if hasattr(self, 'project') and hasattr(self.project, 'value'):
                        self.project.value = str(project_id)

        except Exception as e:
            # Silently ignore errors - we're in a file setter
            import logging
            logger = logging.getLogger(__name__)
            logger.debug(f"Failed to update from database: {e}")

    def getFullPath(self) -> str:
        """Get the full file path as a string.

        Path construction logic:
        1. If baseName contains an absolute path → return it directly
        2. If dbFileId is set (database-aware) → retrieve from database
        3. If relPath is set → construct: workDirectory/relPath/baseName
           (This is the standard for output files: relPath = "CCP4_JOBS/job_n/job_m/job_y")
        4. If only baseName is set → return as-is (may be relative to CWD)
        5. Fallback to legacy file_path attribute

        For output files computed in checkOutputData():
        - relPath: "CCP4_JOBS/job_n/job_m/job_y"
        - baseName: just the filename (e.g., "refined.pdb")
        - fullPath: workDirectory + relPath + baseName

        For user-specified input files:
        - baseName: absolute or relative path (e.g., "/path/to/file.mtz" or "demo_data/test.mtz")
        - relPath: typically empty
        - fullPath: baseName as-is

        Returns:
            Full path to the file, or empty string if not set
        """
        from pathlib import Path

        # First, get baseName value if it exists
        basename_value = None
        if hasattr(self, 'baseName') and self.baseName is not None:
            if hasattr(self.baseName, 'value'):
                basename_value = self.baseName.value
            else:
                basename_value = self.baseName

        # If baseName is an absolute path, return it directly
        # This takes precedence over everything (user-specified absolute paths)
        if basename_value:
            basename_str = str(basename_value)
            if basename_str and Path(basename_str).is_absolute():
                logger.debug("Returning absolute path from baseName: %s", basename_str)
                return basename_str

        # Database-aware mode: Check if dbFileId is set
        if hasattr(self, 'dbFileId') and self.dbFileId is not None:
            db_file_id = None
            if hasattr(self.dbFileId, 'value') and self.dbFileId.value is not None:
                db_file_id = self.dbFileId.value
            elif isinstance(self.dbFileId, str):
                db_file_id = self.dbFileId

            if db_file_id:
                db_handler = self._get_db_handler()
                if db_handler:
                    try:
                        import uuid
                        file_uuid = uuid.UUID(str(db_file_id))
                        path = db_handler.get_file_path_sync(file_uuid)
                        if path:
                            logger.debug("Retrieved path from database via dbFileId: %s", path)
                            return path
                    except Exception as e:
                        logger.debug(f"Failed to retrieve path from database: {e}")

        # Standard path construction: workDirectory + relPath + baseName
        # This is used for output files where relPath = "CCP4_JOBS/job_n/job_m/job_y"
        relpath_value = None
        if hasattr(self, 'relPath') and self.relPath is not None:
            if hasattr(self.relPath, 'value'):
                relpath_value = self.relPath.value
            else:
                relpath_value = self.relPath

        if relpath_value:
            relpath_str = str(relpath_value).strip()
            if relpath_str:
                # Get workDirectory from plugin parent
                plugin = self._find_plugin_parent()
                if plugin and hasattr(plugin, 'workDirectory'):
                    work_dir = Path(plugin.workDirectory)
                    # Construct: workDirectory / relPath / baseName
                    if basename_value:
                        full_path = work_dir / relpath_str / str(basename_value)
                        logger.debug("Constructed path from workDir + relPath + baseName: %s", full_path)
                        return str(full_path)
                    else:
                        # Just workDirectory / relPath (no baseName)
                        full_path = work_dir / relpath_str
                        logger.debug("Constructed path from workDir + relPath: %s", full_path)
                        return str(full_path)

        # Return baseName as-is (may be relative path, or empty)
        if basename_value is not None:
            return str(basename_value) if basename_value else ""

        # Fallback to legacy file_path
        if hasattr(self, 'file_path') and self.file_path is not None:
            return str(self.file_path)

        return ""

    def exists(self) -> bool:
        """Check if the file exists on disk.

        Returns:
            True if the file exists, False otherwise
        """
        from pathlib import Path
        path = self.getFullPath()
        if path:
            return Path(path).exists()
        return False

    def isSet(self, field_name: str = None, allowUndefined: bool = False,
              allowDefault: bool = False, allSet: bool = True) -> bool:
        """Check if the file has been set.

        For CDataFile, a file is considered "set" if its baseName attribute is set.
        This overrides the base CData.isSet() to provide file-specific semantics.

        Args:
            field_name: If None, checks baseName. Otherwise delegates to parent.
            allowUndefined: If True, allow None/undefined values to be considered "set"
            allowDefault: If False, consider values that equal the default as "not set"
            allSet: For container types - if True, all children must be set

        Returns:
            True if baseName is set (has a non-None, non-empty value)
        """
        if field_name is None:
            # For files, check if baseName is set
            if hasattr(self, 'baseName'):
                if hasattr(self.baseName, 'value'):
                    # baseName is a CData wrapper - check its value
                    return self.baseName.value is not None and self.baseName.value != ""
                else:
                    # baseName is a plain value
                    return self.baseName is not None and self.baseName != ""
            # Fallback to legacy file_path
            if hasattr(self, 'file_path') and self.file_path is not None:
                return self.file_path != ""
            return False
        else:
            # For specific field names, delegate to parent
            return super().isSet(field_name, allowUndefined=allowUndefined,
                               allowDefault=allowDefault, allSet=allSet)

    @property
    def fullPath(self) -> str:
        """Property to access the full file path as a string.

        Returns:
            Full path to the file, or empty string if not set
        """
        return self.getFullPath()

    @fullPath.setter
    def fullPath(self, path: str):
        """Set the full file path.

        Args:
            path: Full file path as a string
        """
        self.setFullPath(path)

    def __str__(self) -> str:
        """Return string representation of the file (its path).

        Returns:
            Full path to the file, or empty string if not set
        """
        return self.getFullPath()

    def get(self) -> dict:
        """Get file attributes as a dict. Compatible with old CCP4i2 API.

        For file objects, this returns the fullPath as the primary value.
        Overrides base CData.get() to provide file-specific behavior.

        Returns:
            Dict with fullPath and other file attributes
        """
        # Get base attributes
        result = super().get()
        # Add fullPath as a convenience
        result['fullPath'] = self.getFullPath()
        return result

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

    def loadFile(self, initialise: bool = False):
        """
        Load file content by instantiating fileContentClassName and calling its loadFile().

        This base method:
        1. Gets fileContentClassName from qualifiers
        2. Instantiates that class if not already created
        3. Delegates to content class's loadFile() method
        4. Handles errors and emits dataLoaded signal

        Args:
            initialise: If True, recreate content object even if it exists

        Returns:
            CErrorReport with any errors encountered

        Example:
            >>> mtz_file = CMtzDataFile()
            >>> mtz_file.setFullPath('/path/to/data.mtz')
            >>> error = mtz_file.loadFile()
            >>> if error.count() == 0:
            ...     print(f"Cell: {mtz_file.content.cell}")
        """
        from core.base_object.error_reporting import CErrorReport, CException, SEVERITY_ERROR
        from pathlib import Path

        error = CErrorReport()

        # Check if file loading is blocked
        if hasattr(self, 'BLOCK_LOAD_FILES') and self.BLOCK_LOAD_FILES:
            return error

        # Get content class name from qualifiers
        content_class_name = self.get_qualifier('fileContentClassName')
        if content_class_name is None:
            return error  # No content class specified - not an error

        # Instantiate content object if needed
        if self.content is None or initialise:
            try:
                # Import the content class
                # Try local imports first (CCP4XtalData, CCP4ModelData, etc.)
                content_class = None
                for module_name in ['core.CCP4XtalData', 'core.CCP4ModelData', 'core.CCP4CootData']:
                    try:
                        module = __import__(module_name, fromlist=[content_class_name])
                        content_class = getattr(module, content_class_name, None)
                        if content_class is not None:
                            break
                    except (ImportError, AttributeError):
                        continue

                if content_class is None:
                    error.append(
                        klass=self.__class__.__name__,
                        code=105,
                        details=f"Content class '{content_class_name}' not found",
                        name=self.object_name() if hasattr(self, 'object_name') else ''
                    )
                    return error

                # Create content instance
                self.content = content_class(parent=self, name='fileContent')

            except Exception as e:
                error.append(
                    klass=self.__class__.__name__,
                    code=106,
                    details=f"Error instantiating content class '{content_class_name}': {e}",
                    name=self.object_name() if hasattr(self, 'object_name') else ''
                )
                return error

        # Get file path
        file_path = self.getFullPath()
        if not file_path:
            # No path set - unset content
            if self.content is not None:
                self.content.unSet()
            return error

        # Check file exists
        path_obj = Path(file_path)
        if path_obj.exists() and path_obj.is_file():
            try:
                # Delegate to content class's loadFile()
                content_error = self.content.loadFile(file_path)
                if content_error is not None:
                    error.extend(content_error)

            except CException as e:
                error.extend(e)

            except Exception as e:
                error.append(
                    klass=self.__class__.__name__,
                    code=320,
                    details=f"Unrecognised error loading file '{file_path}': {e}",
                    name=self.object_name() if hasattr(self, 'object_name') else ''
                )
        else:
            # File doesn't exist - unset content
            if self.content is not None:
                self.content.unSet()

        # Emit signal (if event system available)
        if hasattr(self, 'dataLoaded'):
            try:
                self.dataLoaded.emit()
            except:
                pass  # Signal system may not be available

        return error

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
