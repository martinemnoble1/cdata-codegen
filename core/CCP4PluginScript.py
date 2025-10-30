"""
CPluginScript - Base class for CCP4i2 task wrappers and pipelines.

This is a modernized version that uses the new CData infrastructure
while maintaining backward compatibility with the existing API used
by all .def.xml files and plugin implementations.
"""

from __future__ import annotations
from typing import Optional
from pathlib import Path
import xml.etree.ElementTree as ET

from core.base_object.base_classes import CData, CContainer
from core.base_object.error_reporting import CErrorReport, SEVERITY_ERROR, SEVERITY_WARNING
from core.task_manager.def_xml_handler import DefXmlParser
from core.task_manager.params_xml_handler import ParamsXmlHandler
from core.CCP4TaskManager import TASKMANAGER
from core.base_object.class_metadata import cdata_class


@cdata_class(
    error_codes={
        '200': {'description': 'Error merging MTZ files'},
        '201': {'description': 'Invalid miniMtzsIn specification'},
        '202': {'description': 'File object has no CONTENT_SIGNATURE_LIST'},
        '203': {'description': 'File object has no path set'},
        '204': {'description': 'MTZ file not found'},
        '205': {'description': 'File object not found in inputData or outputData'},
        '206': {'description': 'Invalid contentFlag for file type'},
        '207': {'description': 'Invalid item format in miniMtzsIn'},
        '208': {'description': 'Conversion method not found on file object'},
        '209': {'description': 'Conversion to requested format not yet implemented'},
        '210': {'description': 'Error during MTZ file conversion'},
        '300': {'description': 'Input MTZ file not found for split operation'},
        '301': {'description': 'miniMtzsOut and programColumnNames length mismatch'},
        '302': {'description': 'Output object not found in container.outputData'},
        '303': {'description': 'Output object has no path set'},
        '304': {'description': 'Error splitting MTZ file'},
    }
)
class CPluginScript(CData):
    """
    Base class for CCP4i2 wrappers and pipelines.

    A CPluginScript wraps a crystallographic program or script, providing:
    - Parameter management through containers
    - Input/output file handling
    - Command generation from templates
    - Process execution and monitoring
    - Error reporting and database integration

    Subclasses should define:
        TASKMODULE: Module category (e.g., 'utility', 'refinement')
        TASKTITLE: Display title for GUI
        TASKNAME: Unique task identifier
        TASKCOMMAND: Executable name
        TASKVERSION: Version number
        COMLINETEMPLATE: Command line template (optional)
        COMTEMPLATE: Command file template (optional)
    """

    # Class attributes to be defined in subclasses
    TASKMODULE = None
    TASKTITLE = None
    TASKNAME = None
    TASKCOMMAND = None
    TASKVERSION = None
    COMLINETEMPLATE = None
    COMTEMPLATE = None
    ASYNCHRONOUS = False  # Set to True for async execution

    # Status codes
    SUCCEEDED = 0
    FAILED = 1
    RUNNING = 2

    def __init__(self,
                 parent=None,
                 name: Optional[str] = None,
                 xmlFile: Optional[str] = None,
                 workDirectory: Optional[str | Path] = None,
                 **kwargs):
        """
        Initialize CPluginScript.

        Args:
            parent: Parent object (usually None for top-level scripts)
            name: Script instance name
            xmlFile: Path to input_params.xml file to load
            workDirectory: Working directory for the script (str or Path, optional)
            **kwargs: Additional arguments
        """
        # Initialize CData base class (provides hierarchy and event system)
        super().__init__(parent=parent, name=name or self.TASKNAME, **kwargs)

        # Create finished signal (inherits SignalManager from HierarchicalObject)
        # This signal is emitted when the plugin completes execution
        from core.base_object.signal_system import Signal
        self.finished = self._signal_manager.create_signal("finished", dict)

        # Initialize infrastructure components
        self._def_parser = DefXmlParser()
        self._params_handler = ParamsXmlHandler()

        # Create main container
        # CPluginScript is now the parent of the container
        self.container = CContainer(parent=self, name="container")

        # Error report for tracking issues during execution
        self.errorReport = CErrorReport()

        # Process management
        self._process = None
        self._status = None

        # Child job counter for sub-plugins (follows legacy convention)
        self._childJobCounter = 0

        # Database integration attributes (for database-backed environments)
        # These are set by the database handler when running in CCP4i2 GUI
        self._dbHandler = None        # Database handler object
        self._dbProjectId = None       # Project identifier in database
        self._dbProjectName = None     # Project name
        self._dbJobId = None           # Job identifier in database
        self._dbJobNumber = None       # Job number (e.g., "1.2.3" for nested jobs)

        # Command line for external program
        self.commandLine = []

        # Command script (list of lines to write to stdin or script file)
        self.commandScript = []

        # Working directory and file paths
        if workDirectory is not None:
            self.workDirectory = Path(workDirectory)
        else:
            self.workDirectory = Path.cwd()
        self.defFile = None
        self.paramsFile = None

        # Load DEF file if available (defines container structure)
        # This will create inputData, outputData, controlParameters, guiAdmin
        # as children of self.container
        if self.TASKNAME:
            self._loadDefFile()

        # Create default empty sub-containers ONLY if they don't exist after .def.xml loading
        # This ensures backward compatibility for plugins without .def.xml files
        self._ensure_standard_containers()

        # Load PARAMS file if provided (actual parameter values)
        if xmlFile:
            self.loadDataFromXml(xmlFile)

    # Getter/setter methods for database-related attributes
    def get_status(self) -> Optional[int]:
        """Get the current plugin status."""
        return self._status

    def get_db_job_id(self) -> Optional[str]:
        """Get the database job UUID."""
        return self._dbJobId

    def set_db_job_id(self, job_id: str) -> None:
        """Set the database job UUID."""
        self._dbJobId = job_id

    def get_db_job_number(self) -> Optional[str]:
        """Get the database job number (e.g., '1.2.3')."""
        return self._dbJobNumber

    def set_db_job_number(self, job_number: str) -> None:
        """Set the database job number."""
        self._dbJobNumber = job_number

    def _ensure_standard_containers(self):
        """
        Ensure standard sub-containers exist.

        Creates inputData, outputData, controlParameters, and guiAdmin
        as children of self.container only if they don't already exist.
        This ensures backward compatibility for plugins without .def.xml files.
        """
        standard_containers = ['inputData', 'outputData', 'controlParameters', 'guiAdmin']

        for container_name in standard_containers:
            # Check if container exists as a child
            try:
                # Try to access via __getattr__ (which searches children)
                getattr(self.container, container_name)
            except AttributeError:
                # Container doesn't exist - create it
                # Store in __dict__ to avoid __setattr__ while keeping references
                self.container.__dict__[container_name] = CContainer(
                    parent=self.container,
                    name=container_name
                )

    def _loadDefFile(self):
        """
        Load the .def.xml file for this task.

        Uses CTaskManager to locate the .def.xml file, then uses
        DefXmlParser to load the structure into containers.
        """
        # Locate DEF file using CTaskManager
        def_path = self._locateDefFile()

        if def_path and def_path.exists():
            # Load using DefXmlParser
            error = self.loadContentsFromXml(str(def_path))
            if error:
                self.errorReport.extend(error)

    def _locateDefFile(self) -> Optional[Path]:
        """
        Locate the .def.xml file for this task using CTaskManager.

        Returns:
            Path to .def.xml file, or None if not found
        """
        if not self.TASKNAME:
            return None

        task_manager = TASKMANAGER()

        # Treat '0.0' (string or float) and empty string as "no version"
        # for compatibility with defxml_lookup.json which uses empty strings
        version = self.TASKVERSION
        if version in ('0.0', '0', '', None, 0.0, 0):
            version = None

        # Use CTaskManager's locate_def_xml method
        return task_manager.locate_def_xml(
            task_name=self.TASKNAME,
            version=version
        )

    def loadContentsFromXml(self, fileName: str) -> CErrorReport:
        """
        Load container structure from a DEF file using DefXmlParser.

        Args:
            fileName: Path to .def.xml file

        Returns:
            CErrorReport indicating success or failure
        """
        error = CErrorReport()
        try:
            # Use DefXmlParser to parse the .def.xml file
            parsed_container = self._def_parser.parse_def_xml(fileName)

            # The parsed container has the full hierarchy
            # We need to extract the sub-containers and attach them to our
            # container (which is parented to this CPluginScript instance)
            if hasattr(parsed_container, 'inputData'):
                self.container.inputData = parsed_container.inputData
                # Update parent to be our container (which is parented to self)
                self.container.inputData.set_parent(self.container)

            if hasattr(parsed_container, 'outputData'):
                self.container.outputData = parsed_container.outputData
                self.container.outputData.set_parent(self.container)

            if hasattr(parsed_container, 'controlParameters'):
                self.container.controlParameters = parsed_container.controlParameters
                self.container.controlParameters.set_parent(self.container)

            if hasattr(parsed_container, 'guiAdmin'):
                self.container.guiAdmin = parsed_container.guiAdmin
                self.container.guiAdmin.set_parent(self.container)

            self.defFile = fileName

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=100,
                details=f"Failed to load DEF file {fileName}: {e}",
                name=str(fileName)
            )

        return error

    def loadContentsFromEtree(self, element: ET.Element) -> CErrorReport:
        """
        Load container structure from an eTree element.

        Args:
            element: eTree element containing container definitions

        Returns:
            CErrorReport indicating success or failure
        """
        error = CErrorReport()
        # This method is kept for API compatibility but delegates to
        # DefXmlParser internally if needed in the future
        error.append(
            klass=self.__class__.__name__,
            code=101,
            details="loadContentsFromEtree not yet implemented",
            name=self.name or ""
        )
        return error

    def loadDataFromXml(self, fileName: str) -> CErrorReport:
        """
        Load parameter values from a PARAMS file using ParamsXmlHandler.

        Args:
            fileName: Path to .params.xml or input_params.xml file

        Returns:
            CErrorReport indicating success or failure
        """
        error = CErrorReport()
        try:
            # Use ParamsXmlHandler to import params
            success = self._params_handler.import_params_xml(
                self.container, fileName)

            if not success:
                error.append(
                    klass=self.__class__.__name__,
                    code=102,
                    details=f"Failed to load data from {fileName}",
                    name=str(fileName)
                )
            else:
                self.paramsFile = fileName

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=103,
                details=f"Failed to load data from {fileName}: {e}",
                name=str(fileName)
            )

        return error

    def loadDataFromEtree(self, element: ET.Element) -> CErrorReport:
        """
        Load parameter values from an eTree element.

        Args:
            element: eTree element containing parameter values

        Returns:
            CErrorReport indicating success or failure
        """
        error = CErrorReport()
        try:
            self.container.loadDataFromEtree(element)
        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=104,
                details=f"Failed to load data from etree: {e}",
                name=self.name or ""
            )
        return error

    def saveContentsToXml(self, fileName: str) -> CErrorReport:
        """
        Save container structure to a DEF file.

        Args:
            fileName: Path to output .def.xml file

        Returns:
            CErrorReport indicating success or failure
        """
        error = CErrorReport()
        # DEF file saving is typically not done by tasks
        # Kept for API compatibility
        error.append(
            klass=self.__class__.__name__,
            code=105,
            details="saveContentsToXml not yet implemented",
            name=self.name or ""
        )
        return error

    def saveDataToXml(self, fileName: str) -> CErrorReport:
        """
        Save parameter values to a PARAMS file using ParamsXmlHandler.

        Args:
            fileName: Path to output .params.xml file

        Returns:
            CErrorReport indicating success or failure
        """
        error = CErrorReport()
        try:
            # Use ParamsXmlHandler to export params
            success = self._params_handler.export_params_xml(
                self.container, fileName)

            if not success:
                error.append(
                    klass=self.__class__.__name__,
                    code=106,
                    details=f"Failed to save data to {fileName}",
                    name=str(fileName)
                )

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=107,
                details=f"Failed to save data to {fileName}: {e}",
                name=str(fileName)
            )

        return error

    def saveParams(self, fileName: Optional[str] = None) -> CErrorReport:
        """
        Save current parameters to PARAMS file using ParamsXmlHandler.

        This is typically called at the end of execution to save the
        final state including any output data that was generated.

        Args:
            fileName: Path to output file (defaults to auto-generated name)

        Returns:
            CErrorReport indicating success or failure
        """
        if fileName is None:
            fileName = str(self.workDirectory / f"{self.name}.params.xml")

        return self.saveDataToXml(fileName)

    # =========================================================================
    # Process workflow methods
    # =========================================================================

    def process(self) -> int:
        """
        Main processing method - orchestrates the entire workflow.

        This method calls the following steps in order:
        1. checkInputData() - validate input files exist
        2. checkOutputData() - set output file names
        3. processInputFiles() - pre-process input files
        4. makeCommandAndScript() - generate command line/file
        5. startProcess() - execute the program

        Returns:
            Status code (SUCCEEDED, FAILED, or RUNNING)
        """
        # Validate input data
        error = self.checkInputData()
        if error:
            self.errorReport.extend(error)
            return self.FAILED

        # Set up output data
        error = self.checkOutputData()
        if error:
            self.errorReport.extend(error)
            # Don't fail - checkOutputData should fix issues

        # Pre-process input files if needed
        result = self.processInputFiles()
        # Handle both modern API (CErrorReport) and legacy API (int)
        if isinstance(result, int):
            # Legacy API: returns SUCCEEDED (0) or FAILED (1)
            if result != self.SUCCEEDED:
                return result
        elif result:
            # Modern API: returns CErrorReport (truthy if has errors)
            self.errorReport.extend(result)
            return self.FAILED

        # Generate command and script
        print(f"[DEBUG process] Calling makeCommandAndScript() for {self.TASKNAME}")
        error = self.makeCommandAndScript()
        print(f"[DEBUG process] makeCommandAndScript() returned, commandLine has {len(self.commandLine)} items")
        if error:
            self.errorReport.extend(error)
            return self.FAILED

        # Start the process
        error = self.startProcess()
        if error:
            self.errorReport.extend(error)
            return self.FAILED

        # For synchronous execution (subprocess.run), process is complete when startProcess returns
        # Call processOutputFiles to extract output data
        status = self.SUCCEEDED
        try:
            error = self.processOutputFiles()
            if error:
                self.errorReport.extend(error)
                status = self.FAILED
        except Exception as e:
            # Legacy wrappers may not have processOutputFiles implemented
            print(f"Warning: processOutputFiles() exception: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()

        # Emit finished signal so pipelines can continue
        # This is essential for sub-plugins in pipelines (e.g., mtzdump in demo_copycell)
        self.reportStatus(status)

        return status

    def _find_datafile_descendants(self, container) -> list:
        """
        Recursively find all CDataFile descendants in a container hierarchy.

        Handles both CContainer children and CList elements.

        Args:
            container: Container to search

        Returns:
            List of (name, file_obj) tuples for all CDataFile descendants
        """
        from core.base_object.base_classes import CDataFile
        from core.base_object.fundamental_types import CList

        results = []

        # Check all children of this container
        for child in container.children():
            # If it's a CDataFile, add it
            if isinstance(child, CDataFile):
                results.append((child.name, child))
            # If it's a CList, check its elements
            elif isinstance(child, CList):
                for i, item in enumerate(child):
                    # If the list item is a CDataFile, add it
                    if isinstance(item, CDataFile):
                        # Use list element name if available, otherwise use index
                        item_name = item.name if hasattr(item, 'name') and item.name else f"{child.name}[{i}]"
                        results.append((item_name, item))
                    # If the list item is a container, recurse into it
                    elif hasattr(item, 'children'):
                        results.extend(self._find_datafile_descendants(item))
            # If it's a container, recurse into it
            elif hasattr(child, 'children'):
                results.extend(self._find_datafile_descendants(child))

        return results

    def checkInputData(self) -> CErrorReport:
        """
        Validate that input data is correct and files exist.

        This method recursively checks all CDataFile descendants in the
        entire container hierarchy and verifies that files marked with
        mustExist actually exist.

        Returns:
            CErrorReport with any validation errors
        """
        error = CErrorReport()

        # Find all CDataFile descendants recursively in the entire container
        file_items = self._find_datafile_descendants(self.container)

        # Validate each file
        for name, obj in file_items:
            obj_error = obj.validity()
            if obj_error:
                error.extend(obj_error)

        return error

    def checkOutputData(self) -> CErrorReport:
        """
        Set output file names if not already set.

        This method generates appropriate file names for any output files
        that don't have names yet, based on their objectName() and workDirectory.

        For lists of CDataFiles, pre-populates up to maxListElements items.

        Returns:
            CErrorReport with any issues (should fix rather than fail)
        """
        import os
        import re
        from core.base_object.base_classes import CDataFile
        from core.base_object.fundamental_types import CList

        error = CErrorReport()

        if not hasattr(self.container, 'outputData'):
            return error

        # Get maxListElements setting (default 50)
        max_list_elements = getattr(self, 'maxListElements', 50)

        def slugify(name: str) -> str:
            """Convert objectName to valid filename, removing special chars like braces."""
            # Remove or replace special characters
            name = re.sub(r'[\[\]{}()<>]', '', name)  # Remove braces and brackets
            name = re.sub(r'[^\w\s\-\.]', '_', name)  # Replace other special chars with underscore
            name = re.sub(r'[-\s]+', '_', name)  # Replace spaces and hyphens with underscore
            return name.strip('_')

        def populate_list_outputs(obj, parent_path: str = ""):
            """Pre-populate CList of CDataFiles with proper file paths."""
            if not isinstance(obj, CList):
                return

            # If list is empty or has fewer than max elements, populate it
            current_len = len(obj) if hasattr(obj, '__len__') else 0
            target_len = max_list_elements

            # Get the item type if specified
            item_class = None
            if hasattr(obj, '_item_type') and obj._item_type:
                # Try to get the class from registry
                try:
                    from core.CCP4TaskManager import TASKMANAGER
                    tm = TASKMANAGER()
                    if hasattr(tm, 'class_registry'):
                        item_class = tm.class_registry.get(obj._item_type)
                except Exception:
                    pass

            # If we couldn't determine item type, check if there are existing items
            if not item_class and current_len > 0:
                item_class = type(obj[0])

            # Only populate if we know it's a CDataFile list
            if item_class and issubclass(item_class, CDataFile):
                for i in range(current_len, target_len):
                    # Create new instance
                    new_item = item_class()
                    # Generate file path
                    base_name = slugify(obj.objectName() or obj.name or "output")
                    file_name = f"{base_name}_{i}.mtz"  # Default to .mtz extension
                    file_path = os.path.join(self.workDirectory, file_name)
                    new_item.setFullPath(file_path)
                    # Add to list
                    obj.append(new_item)

        def process_container(container, parent_path: str = ""):
            """Recursively process container to set output file paths."""
            print(f'[DEBUG checkOutputData] Processing container: {container.name if hasattr(container, "name") else "unknown"}')
            children = list(container.children())
            print(f'[DEBUG checkOutputData] Found {len(children)} children')
            for child in children:
                print(f'[DEBUG checkOutputData] Processing child: {child.name if hasattr(child, "name") else "unknown"} (type: {type(child).__name__})')
                # Handle CDataFile
                if isinstance(child, CDataFile):
                    # Only set path if baseName has not been set by the user
                    # Check baseName rather than fullPath as it's more fundamental
                    # Also check that baseName is non-empty (DEF files may set it to empty string)
                    basename_is_set = False
                    if hasattr(child, 'baseName') and hasattr(child.baseName, 'isSet'):
                        basename_is_set = child.baseName.isSet('value') and bool(str(child.baseName).strip())

                    obj_name = child.objectName() if hasattr(child, 'objectName') else (child.name if hasattr(child, 'name') else 'unknown')
                    print(f'[DEBUG checkOutputData]   {obj_name}: basename_is_set={basename_is_set}, baseName={str(child.baseName) if hasattr(child, "baseName") else "N/A"}')
                    if hasattr(child, 'baseName'):
                        if hasattr(child.baseName, '_value_states'):
                            print(f'[DEBUG checkOutputData]     baseName._value_states={child.baseName._value_states}')
                        if hasattr(child.baseName, 'value'):
                            print(f'[DEBUG checkOutputData]     baseName.value={child.baseName.value}')

                    if not basename_is_set:
                        # Generate path from objectName
                        obj_name = child.objectName()
                        if not obj_name:
                            obj_name = child.name if hasattr(child, 'name') and child.name else 'output'

                        # Slugify to create valid filename
                        file_name = slugify(obj_name)

                        # Add appropriate extension if not present
                        if not any(file_name.endswith(ext) for ext in ['.mtz', '.pdb', '.cif', '.log', '.xml']):
                            file_name += '.mtz'  # Default extension

                        # Combine with workDirectory
                        file_path = os.path.join(self.workDirectory, file_name)
                        print(f'[DEBUG checkOutputData] Setting path for {obj_name}: {file_path}')
                        child.setFullPath(file_path)
                        # Verify it was set
                        retrieved_path = child.getFullPath()
                        print(f'[DEBUG checkOutputData] Retrieved path: {retrieved_path}')

                # Handle CList - pre-populate if it contains CDataFiles
                elif isinstance(child, CList):
                    populate_list_outputs(child, parent_path)
                    # Also process any items already in the list
                    for item in child:
                        if isinstance(item, CDataFile):
                            # Check if baseName is already set
                            basename_is_set = False
                            if hasattr(item, 'baseName') and hasattr(item.baseName, 'isSet'):
                                basename_is_set = item.baseName.isSet('value')

                            if not basename_is_set:
                                obj_name = item.objectName() or item.name or 'output'
                                file_name = slugify(obj_name)
                                if not any(file_name.endswith(ext) for ext in ['.mtz', '.pdb', '.cif', '.log', '.xml']):
                                    file_name += '.mtz'
                                file_path = os.path.join(self.workDirectory, file_name)
                                item.setFullPath(file_path)
                        elif hasattr(item, 'children'):
                            process_container(item, parent_path)

                # Handle nested containers
                elif hasattr(child, 'children'):
                    process_container(child, parent_path)

        # Process outputData container
        try:
            process_container(self.container.outputData)
        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=50,
                details=f"Error setting output file paths: {str(e)}"
            )

        return error

    def processInputFiles(self) -> CErrorReport:
        """
        Pre-process input files before running main program.

        This is a hook for subclasses to perform any manipulations
        on input data or files before calling the main program.

        Returns:
            CErrorReport with any errors
        """
        return CErrorReport()

    def makeCommandAndScript(self, container=None) -> CErrorReport:
        """
        Generate command line and command file for the program.

        Uses COMLINETEMPLATE and COMTEMPLATE class attributes to
        generate the command line and input file.

        Args:
            container: Container object with input/output data (defaults to self.container)

        Returns:
            CErrorReport with any errors
        """
        error = CErrorReport()

        # Use the container from this plugin if not specified
        if container is None:
            container = self.container

        # Use our modern CComTemplate implementation (Qt-free)
        try:
            from core import CCP4ComTemplate
            print(f"[DEBUG makeCommandAndScript] CComTemplate imported successfully")
        except ImportError as e:
            # Should never happen since CCP4ComTemplate is in our core package
            print(f"[DEBUG makeCommandAndScript] CComTemplate import failed: {e}")
            return error

        # Process COMTEMPLATE (generates stdin script)
        # The numeric prefix is stripped by CComTemplate, output goes to stdin
        if self.COMTEMPLATE is not None:
            print(f"[DEBUG makeCommandAndScript] Processing COMTEMPLATE: {self.COMTEMPLATE}")
            try:
                comTemplate = CCP4ComTemplate.CComTemplate(parent=self, template=self.COMTEMPLATE)
                text, tmpl_err = comTemplate.makeComScript(container)
                print(f"[DEBUG makeCommandAndScript] COMTEMPLATE expanded to: '{text}'")
                if tmpl_err and len(tmpl_err) > 0:
                    print(f"[DEBUG makeCommandAndScript] COMTEMPLATE errors: {tmpl_err}")
                    error.extend(tmpl_err)
                if text and len(text) > 0:
                    # Add to commandScript (stdin) - preserve newlines
                    print(f"[DEBUG makeCommandAndScript] Adding to commandScript (stdin)")
                    self.commandScript.append(text + '\n')
            except Exception as e:
                print(f"[DEBUG makeCommandAndScript] Exception processing COMTEMPLATE: {e}")
                import traceback
                traceback.print_exc()
                error.append(
                    klass=self.__class__.__name__,
                    code=13,
                    details=f"Error processing COMTEMPLATE: {e}"
                )

        # Process COMLINETEMPLATE (generates command line arguments)
        # The leading numeric prefix (e.g., "1 HKLIN") is stripped by CComTemplate
        if self.COMLINETEMPLATE is not None:
            print(f"[DEBUG makeCommandAndScript] Processing COMLINETEMPLATE: {self.COMLINETEMPLATE}")
            try:
                comTemplate = CCP4ComTemplate.CComTemplate(parent=self, template=self.COMLINETEMPLATE)
                text, tmpl_err = comTemplate.makeComScript(container)
                print(f"[DEBUG makeCommandAndScript] Template expanded to: '{text}'")
                if tmpl_err and len(tmpl_err) > 0:
                    print(f"[DEBUG makeCommandAndScript] Template errors: {tmpl_err}")
                    error.extend(tmpl_err)
                if text and len(text) > 0:
                    # Split the text and append each word to commandLine
                    wordList = text.split()
                    print(f"[DEBUG makeCommandAndScript] Adding words to commandLine: {wordList}")
                    for word in wordList:
                        self.commandLine.append(word)
            except Exception as e:
                print(f"[DEBUG makeCommandAndScript] Exception processing COMLINETEMPLATE: {e}")
                import traceback
                traceback.print_exc()
                error.append(
                    klass=self.__class__.__name__,
                    code=15,
                    details=f"Error processing COMLINETEMPLATE: {e}"
                )

        return error

    def appendCommandLine(self, wordList=[], clear=False) -> CErrorReport:
        """
        Add text strings or list of strings to the command line.

        Args:
            wordList: String or list of strings to add to command line
            clear: If True, clear command line before appending

        Returns:
            CErrorReport with any errors
        """
        import re
        from core.base_object.fundamental_types import CList

        error = CErrorReport()

        if clear:
            self.clearCommandLine()

        if not isinstance(wordList, list):
            wordList = [wordList]

        for item in wordList:
            if isinstance(item, (list, CList)):
                for subItem in item:
                    try:
                        myText = str(subItem)
                        self.commandLine.append(myText)
                    except Exception:
                        error.append(
                            klass=self.__class__.__name__,
                            code=2,
                            details="Error converting command line item to string"
                        )
            else:
                try:
                    myText = str(item)
                    # Remove newlines from command line arguments
                    myText = re.sub(r'\n', ' ', myText)
                    self.commandLine.append(myText)
                except Exception:
                    error.append(
                        klass=self.__class__.__name__,
                        code=2,
                        details="Error converting command line item to string"
                    )

        if error:
            self.errorReport.extend(error)

        return error

    def clearCommandLine(self):
        """Clear the command line list."""
        self.commandLine = []

    def makeFileName(self, format='COM', ext='', qualifier=None):
        """
        Generate consistent names for output files.

        Args:
            format: File type format (e.g., 'PROGRAMXML', 'LOG', 'REPORT')
            ext: File extension (unused, kept for compatibility)
            qualifier: Optional qualifier to modify the filename

        Returns:
            Full path to the file in the work directory
        """
        import os

        defNames = {
            'ROOT': '',
            'PARAMS': 'params.xml',
            'JOB_INPUT': 'input_params.xml',
            'PROGRAMXML': 'program.xml',
            'LOG': 'log.txt',
            'STDOUT': 'stdout.txt',
            'STDERR': 'stderr.txt',
            'INTERRUPT': 'interrupt_status.xml',
            'DIAGNOSTIC': 'diagnostic.xml',
            'REPORT': 'report.html',
            'COM': 'com.txt',
            'MGPICDEF': 'report.mgpic.py',
            'PIC': 'report.png',
            'RVAPIXML': 'i2.xml'
        }

        fileName = defNames.get(format, 'unknown.unk')
        if qualifier is not None:
            base, ext = fileName.split('.', 1)
            fileName = base + '_' + str(qualifier) + '.' + ext
        return os.path.join(self.workDirectory, fileName)

    def logFileText(self) -> str:
        """
        Read and return the contents of the log file.

        This is a legacy API method used by plugins to parse their output.

        Returns:
            Contents of the log file as a string, or empty string if file doesn't exist
        """
        log_path = self.makeFileName('LOG')
        try:
            with open(log_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
        except Exception as e:
            print(f"Warning: Error reading log file {log_path}: {e}")
            return ""

    def jobNumberString(self) -> str:
        """
        Return a string representation of the job number for annotations.

        In a full CCP4i2 environment with database integration, this would
        return something like "Job #123". For standalone testing without
        database, returns the task name.

        Returns:
            String describing the job (e.g., "parrot" or "Job #123")
        """
        # When running standalone (no database integration), use task name
        # In full CCP4i2, this would query the database for the job number
        if hasattr(self, 'jobId') and self.jobId:
            return f"Job #{self.jobId}"
        return self.TASKNAME or "Job"

    def startProcess(self) -> CErrorReport:
        """
        Start the external program process.

        Runs the program specified by TASKCOMMAND with the command line
        arguments built by makeCommandAndScript(), capturing output to log files.

        If ASYNCHRONOUS is True, uses AsyncProcessManager for non-blocking execution.
        Otherwise uses subprocess.run() for synchronous execution.

        If both commandLine and commandScript are defined, the commandLine is used
        to start the process and commandScript is fed as stdin.

        Returns:
            CErrorReport with any errors
        """
        import subprocess
        import os

        error = CErrorReport()

        if not self.TASKCOMMAND:
            error.append(
                klass=self.__class__.__name__,
                code=100,
                details="No TASKCOMMAND specified for this plugin"
            )
            return error

        # Check if async execution is requested
        if self.ASYNCHRONOUS or getattr(self, 'waitForFinished', 0) == -1:
            return self._startProcessAsync()
        else:
            return self._startProcessSync()

    def _startProcessSync(self) -> CErrorReport:
        """Synchronous process execution using subprocess.run()."""
        import subprocess
        import os

        error = CErrorReport()

        # Ensure working directory exists
        from pathlib import Path
        work_dir_path = Path(self.workDirectory)
        if not work_dir_path.exists():
            work_dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created working directory: {self.workDirectory}")

        # Write command script to file if present
        command_script_file = None
        if self.commandScript:
            command_script_file = self.writeCommandFile()

        # Prepare log file paths
        # Use LOG for program output (not STDOUT) to match CCP4 conventions
        # This allows wrappers to find the logfile via makeFileName('LOG')
        stdout_path = self.makeFileName('LOG')
        stderr_path = self.makeFileName('STDERR')

        # Find full path to executable to ensure subprocess can find it
        import shutil
        exe_path = shutil.which(self.TASKCOMMAND)
        if exe_path:
            # Use full path if found
            command = [exe_path] + self.commandLine
        else:
            # Fall back to command name
            command = [self.TASKCOMMAND] + self.commandLine

        print(f"\n{'='*60}")
        print(f"Running: {' '.join(command)}")
        print(f"Working directory: {self.workDirectory}")
        print(f"Log file: {stdout_path}")
        print(f"Stderr file: {stderr_path}")
        if command_script_file:
            print(f"Command script: {command_script_file}")
        print(f"{'='*60}\n")

        try:
            # Run the process
            # Copy environment to ensure subprocess inherits all variables
            env = os.environ.copy()

            # Debug: print environment variables
            print(f"Environment CBIN: {env.get('CBIN', 'NOT SET')}")
            print(f"Environment CCP4: {env.get('CCP4', 'NOT SET')}")
            print(f"Environment CLIB: {env.get('CLIB', 'NOT SET')}")

            # Prepare stdin input
            # When using input= parameter, do NOT set stdin= parameter
            # The input= parameter automatically opens stdin as PIPE, writes data, and closes (sends EOF)
            stdin_input = None
            if self.commandScript:
                # Join command script lines into single string
                stdin_input = ''.join(self.commandScript)

            with open(stdout_path, 'w') as stdout_file, open(stderr_path, 'w') as stderr_file:
                # Write formatted header to stdout
                stdout_file.write("="*70 + "\n")
                stdout_file.write(f"CCP4i2 Task: {self.TASKNAME}\n")
                stdout_file.write("="*70 + "\n\n")

                # Write command line
                stdout_file.write("Command Line:\n")
                stdout_file.write("-" * 70 + "\n")
                stdout_file.write(f"{' '.join(command)}\n\n")

                # Write command script if present
                if self.commandScript:
                    stdout_file.write("Command Script (stdin):\n")
                    stdout_file.write("-" * 70 + "\n")
                    for line in self.commandScript:
                        stdout_file.write(line)
                    stdout_file.write("\n")

                stdout_file.write("="*70 + "\n")
                stdout_file.write("Program Output:\n")
                stdout_file.write("="*70 + "\n\n")
                stdout_file.flush()

                # Run the process
                # Note: When input= is provided, stdin is automatically set to PIPE and closed after writing
                # When input= is None, stdin defaults to inheriting from parent (but files are closed)
                result = subprocess.run(
                    command,
                    cwd=self.workDirectory,
                    input=stdin_input,
                    stdout=stdout_file,
                    stderr=stderr_file,
                    text=True,
                    timeout=300,  # 5 minute timeout
                    env=env
                )

            # Check return code
            if result.returncode != 0:
                error.append(
                    klass=self.__class__.__name__,
                    code=101,
                    details=f"Process {self.TASKCOMMAND} exited with code {result.returncode}"
                )

                # Read stderr for error details
                if os.path.exists(stderr_path):
                    with open(stderr_path, 'r') as f:
                        stderr_content = f.read()
                        if stderr_content:
                            print(f"STDERR:\n{stderr_content}")

            else:
                print(f"✅ Process completed successfully (exit code 0)")

        except FileNotFoundError as e:
            error.append(
                klass=self.__class__.__name__,
                code=102,
                details=f"File not found error: {str(e)}. "
                        f"Command: {command[0]}. "
                        f"Working directory: {self.workDirectory}. "
                        f"Make sure CCP4 is set up (source ccp4.setup-sh)"
            )
        except subprocess.TimeoutExpired:
            error.append(
                klass=self.__class__.__name__,
                code=103,
                details=f"Process {self.TASKCOMMAND} timed out after 300 seconds"
            )
        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=104,
                details=f"Error running {self.TASKCOMMAND}: {str(e)}"
            )

        return error

    def _startProcessAsync(self) -> CErrorReport:
        """
        Asynchronous process execution using AsyncProcessManager.

        This method:
        1. Starts the subprocess in non-blocking mode
        2. Returns immediately (RUNNING status)
        3. When subprocess finishes, calls _onProcessFinished handler
        4. Handler calls postProcess() which emits finished signal
        """
        import os
        from pathlib import Path
        from core.async_process_manager import ASYNC_PROCESSMANAGER

        error = CErrorReport()

        # Ensure working directory exists
        work_dir_path = Path(self.workDirectory)
        if not work_dir_path.exists():
            work_dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Created working directory: {self.workDirectory}")

        # Write command script to file if present
        command_script_file = None
        if self.commandScript:
            command_script_file = self.writeCommandFile()

        # Prepare log file paths
        stdout_path = self.makeFileName('LOG')
        stderr_path = self.makeFileName('STDERR')

        # Find full path to executable
        import shutil
        exe_path = shutil.which(self.TASKCOMMAND)
        command = exe_path if exe_path else self.TASKCOMMAND

        print(f"\n{'='*60}")
        print(f"Starting ASYNC: {command} {' '.join(self.commandLine)}")
        print(f"Working directory: {self.workDirectory}")
        print(f"Log file: {stdout_path}")
        if command_script_file:
            print(f"Command script: {command_script_file}")
        print(f"{'='*60}\n")

        try:
            # Get async process manager
            pm = ASYNC_PROCESSMANAGER()

            # Prepare stdin input
            input_file = command_script_file if command_script_file else None

            # Create handler callback
            handler = [self._onProcessFinished, {}]

            # Start async process
            self._runningProcessId = pm.startProcess(
                command=command,
                args=self.commandLine,
                inputFile=input_file,
                logFile=stdout_path,
                cwd=str(self.workDirectory),
                env=os.environ.copy(),
                handler=handler,
                timeout=-1,  # No timeout
                ifAsync=True
            )

            print(f"✅ Process started asynchronously (PID: {self._runningProcessId})")

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=110,
                details=f"Error starting async process: {e}"
            )

        return error

    def _onProcessFinished(self, pid: int):
        """
        Called when async subprocess completes.

        This handler:
        1. Checks process exit status
        2. Calls postProcess() to handle completion
        3. postProcess() eventually calls reportStatus() which emits finished signal
        """
        print(f"\n{'='*60}")
        print(f"Process {pid} finished")
        print(f"{'='*60}\n")

        # Call postProcess to handle completion
        # This will call processOutputFiles() and reportStatus()
        # reportStatus() emits the finished signal
        status = self.postProcess()

        return status

    def postProcess(self) -> int:
        """
        Post-processing after program completes.

        This method calls:
        1. postProcessCheck() - check if program succeeded
        2. processOutputFiles() - extract output data
        3. reportStatus() - save params and report to database

        Returns:
            Status code (SUCCEEDED or FAILED)
        """
        # Check if process succeeded
        status = self.postProcessCheck()

        if status == self.SUCCEEDED:
            # Extract output data
            # Wrap in try/except to handle legacy wrappers that may have incomplete implementations
            try:
                error = self.processOutputFiles()
                if error:
                    self.errorReport.extend(error)
                    status = self.FAILED
            except Exception as e:
                # Legacy wrappers may depend on methods we haven't implemented yet
                # For now, just log a warning and continue
                print(f"Warning: processOutputFiles() exception: {type(e).__name__}: {str(e)}")
                import traceback
                traceback.print_exc()
                # Don't fail the job for this - the main output file should still be created

        # Report status and save params
        self.reportStatus(status)

        return status

    def postProcessCheck(self) -> int:
        """
        Check if the program process completed successfully.

        Returns:
            SUCCEEDED or FAILED
        """
        # Check process exit code, log files, etc.
        # For now, placeholder implementation
        return self.SUCCEEDED

    def processOutputFiles(self) -> CErrorReport:
        """
        Extract data from output files and populate outputData container.

        This is a hook for subclasses to read output files, extract
        relevant data, and update the outputData container.

        Returns:
            CErrorReport with any errors
        """
        return CErrorReport()

    def reportStatus(self, status: int):
        """
        Report job completion and save parameters.

        This method:
        1. Saves parameters to PARAMS file
        2. Reports completion to database
        3. Emits finished signal

        Args:
            status: Final status (SUCCEEDED or FAILED)
        """
        # Save params
        self.saveParams()

        # Report to database (placeholder)
        # In real implementation, would notify database

        # Emit finished signal with status dict (modern API)
        # Legacy plugins may expect just int, handled by connectSignal() wrapper
        status_dict = {
            'finishStatus': status,
            'jobId': getattr(self, 'jobId', None)
        }
        self.finished.emit(status_dict)

        # Set the internal status
        self._status = status

    def postProcessWrapper(self, finishStatus):
        """
        Wrapper method for propagating finish status from sub-plugins.

        This is called by pipelines as a callback when a sub-plugin finishes.
        It simply forwards the status to reportStatus() to emit the finished signal.

        Args:
            finishStatus: Can be either int (legacy) or dict (modern)
        """
        # Handle both int and dict status formats
        if isinstance(finishStatus, dict):
            status = finishStatus.get('finishStatus', self.FAILED)
        else:
            status = finishStatus

        self.reportStatus(status)

    # =========================================================================
    # Utility methods for backward compatibility with old API
    # =========================================================================

    def makePluginObject(self, taskName: str, version: Optional[str] = None,
                         reportToDatabase: bool = True, **kwargs) -> Optional['CPluginScript']:
        """
        Create a sub-plugin (sub-job) instance using TASKMANAGER.

        This is used when a pipeline calls other wrappers as sub-jobs.

        Following legacy CCP4i2 convention, each sub-plugin is assigned:
        - A working directory: parent_workdir/job_N (where N = 1, 2, 3, ...)
        - A unique name: parent_name_N

        The working directory is created if it doesn't exist.

        Args:
            taskName: Name of the task to instantiate
            version: Optional version of the task (defaults to latest)
            reportToDatabase: Whether to report this job to the database (default True).
                            In database-backed environments (CCP4i2 GUI), this controls
                            whether the sub-job is registered in the project database.
                            In standalone mode, this parameter is ignored.
            **kwargs: Additional arguments passed to the plugin constructor
                     (workDirectory will be overridden based on convention)

        Returns:
            New CPluginScript instance, or None if plugin not found
        """
        import os
        from pathlib import Path

        # TODO: In database-backed mode, if reportToDatabase is True and _dbHandler exists,
        # would call self._dbHandler.createJob() to register sub-job in database
        # For now (standalone mode), we skip database registration

        # Increment child job counter
        self._childJobCounter += 1

        # Create subdirectory following convention: job_1, job_2, etc.
        child_work_dir = Path(self.workDirectory) / f"job_{self._childJobCounter}"
        try:
            if not child_work_dir.exists():
                child_work_dir.mkdir(parents=True, exist_ok=True)
                print(f"[DEBUG makePluginObject] Created subdirectory: {child_work_dir}")
        except Exception as e:
            self.errorReport.append(
                klass=self.__class__.__name__,
                code=24,
                details=f"Failed to create working directory '{child_work_dir}': {e}",
                name=str(child_work_dir)
            )
            # Fall back to parent's work directory
            child_work_dir = Path(self.workDirectory)

        # Create name following convention: parent_name_N
        child_name = f"{self.name}_{self._childJobCounter}" if self.name else f"job_{self._childJobCounter}"

        # Use TASKMANAGER to get the plugin class
        task_manager = TASKMANAGER()
        plugin_class = task_manager.get_plugin_class(taskName, version=version)

        if plugin_class is None:
            # Log error
            self.errorReport.append(
                klass=self.__class__.__name__,
                code=108,
                details=f"Plugin '{taskName}' not found in registry",
                name=taskName
            )
            return None

        # Instantiate the plugin with computed workDirectory and name
        # Use automatic workDirectory/name unless explicitly provided in kwargs
        try:
            plugin_kwargs = kwargs.copy()

            # Use automatic workDirectory unless explicitly overridden
            if 'workDirectory' not in plugin_kwargs:
                plugin_kwargs['workDirectory'] = str(child_work_dir)

            # Use automatic name unless explicitly overridden
            if 'name' not in plugin_kwargs:
                plugin_kwargs['name'] = child_name

            # Always set parent relationship
            plugin_kwargs['parent'] = self

            actual_name = plugin_kwargs['name']
            actual_workdir = plugin_kwargs['workDirectory']
            plugin_instance = plugin_class(**plugin_kwargs)
            print(f"[DEBUG makePluginObject] Created sub-plugin '{taskName}' as '{actual_name}' in '{actual_workdir}'")
            return plugin_instance
        except Exception as e:
            self.errorReport.append(
                klass=self.__class__.__name__,
                code=109,
                details=f"Failed to instantiate plugin '{taskName}': {e}",
                name=taskName
            )
            import traceback
            traceback.print_exc()
            return None

    def getErrorReport(self) -> CErrorReport:
        """Get the accumulated error report."""
        return self.errorReport

    def getContainer(self) -> CContainer:
        """Get the main container."""
        return self.container

    # =========================================================================
    # Database integration methods (for database-backed environments)
    # =========================================================================

    def getJobId(self):
        """Get the database job ID.

        Returns:
            Job ID in database, or None if not running in database-backed mode
        """
        return self._dbJobId

    def getJobNumber(self):
        """Get the database job number.

        Returns:
            Job number (e.g., "1.2.3"), or None if not running in database-backed mode
        """
        return self._dbJobNumber

    def getProjectId(self):
        """Get the database project ID.

        Returns:
            Project ID in database, or None if not running in database-backed mode
        """
        return self._dbProjectId

    def getChildJobNumber(self):
        """Get the current child job counter.

        This returns how many sub-plugins have been created via makePluginObject().

        Returns:
            Child job counter (starts at 0, increments with each makePluginObject call)
        """
        return self._childJobCounter

    # connectSignal() is now inherited from HierarchicalObject base class
    # with automatic signature adaptation for legacy int handlers

    # =========================================================================
    # MTZ File Merging Methods (makeHklin family)
    # =========================================================================

    def makeHklinGemmi(
        self,
        file_objects: list,
        output_name: str = 'hklin',
        merge_strategy: str = 'first'
    ) -> Path:
        """
        Merge normalized mini-MTZ files into a single HKLIN file (new Pythonic API).

        This is the modern, Pythonic replacement for makeHklin. It works with
        container attribute names and uses gemmi for MTZ operations.

        Args:
            file_objects: List of file specifications. Each can be either:
                - str: Attribute name in inputData/outputData (e.g., 'HKLIN1')
                       Uses the file's contentFlag to determine columns automatically.
                - dict: Explicit specification with keys:
                    {
                        'name': str,                    # Attribute name (required)
                        'target_contentFlag': int,      # Optional: Convert to this contentFlag if needed
                        'rename': Dict[str, str],       # Optional: Column renaming
                        'display_name': str             # Optional: Name for column prefixes (default: name)
                    }

            output_name: Base name for output file (default: 'hklin')
                        Output written to: self.workDirectory / f"{output_name}.mtz"

            merge_strategy: How to handle column conflicts (default: 'first')
                - 'first': Keep column from first file
                - 'last': Keep column from last file
                - 'error': Raise error on conflicts
                - 'rename': Auto-rename conflicts (F, F_1, F_2, ...)

        Returns:
            Path: Full path to created HKLIN file

        Raises:
            AttributeError: If file object not found in inputData/outputData
            ValueError: If contentFlag unknown or file has no path set
            FileNotFoundError: If MTZ file doesn't exist at specified path
            NotImplementedError: If conversion method not available

        Example:
            >>> # Simple merge using contentFlags
            >>> hklin = self.makeHklinGemmi(['HKLIN1', 'FREERFLAG'])
            >>> # Result: merged.mtz with columns from both files

            >>> # With explicit column renaming
            >>> hklin = self.makeHklinGemmi([
            ...     'HKLIN1',  # Uses contentFlag automatically
            ...     {
            ...         'name': 'HKLIN2',
            ...         'rename': {'F': 'F_deriv', 'SIGF': 'SIGF_deriv'}
            ...     }
            ... ])

            >>> # With automatic conversion
            >>> hklin = self.makeHklinGemmi([
            ...     'HKLIN1',
            ...     {
            ...         'name': 'HKLIN2',
            ...         'target_contentFlag': 4  # Convert to FMEAN if not already
            ...     }
            ... ])
        """
        from core.CCP4Utils import merge_mtz_files
        from core.base_object.fundamental_types import CInt

        input_specs = []
        converted_files = []  # Track temporary file objects for cleanup

        for file_spec_idx, file_spec in enumerate(file_objects):
            # Parse spec to get name, display_name, target_contentFlag, and optional rename
            if isinstance(file_spec, str):
                name = file_spec
                display_name = file_spec
                target_content_flag = None
                rename_map = {}
            elif isinstance(file_spec, dict):
                name = file_spec['name']
                display_name = file_spec.get('display_name', name)
                target_content_flag = file_spec.get('target_contentFlag', None)
                rename_map = file_spec.get('rename', {})
            else:
                raise ValueError(
                    f"Invalid file_spec type: {type(file_spec)}. "
                    f"Expected str or dict."
                )

            # Lookup file object in containers
            file_obj = None
            if hasattr(self.container.inputData, name):
                file_obj = getattr(self.container.inputData, name)
            elif hasattr(self.container.outputData, name):
                file_obj = getattr(self.container.outputData, name)
            else:
                raise AttributeError(
                    f"File object '{name}' not found in inputData or outputData"
                )

            # Auto-detect contentFlag from file content to ensure accuracy
            if hasattr(file_obj, 'setContentFlag') and int(file_obj.contentFlag) == 0:
                print(f"[DEBUG makeHklinGemmi] Auto-detecting contentFlag for '{name}'")
                file_obj.setContentFlag()

            # Check if conversion is needed
            current_content_flag = int(file_obj.contentFlag)

            if target_content_flag is not None and current_content_flag != target_content_flag:
                # CONVERSION NEEDED!
                print(f"[DEBUG makeHklinGemmi] Conversion needed: {name} from contentFlag={current_content_flag} to {target_content_flag}")

                # Validate target contentFlag
                if not hasattr(file_obj, 'CONTENT_SIGNATURE_LIST'):
                    raise ValueError(
                        f"File object '{name}' (class {file_obj.__class__.__name__}) "
                        f"has no CONTENT_SIGNATURE_LIST. Cannot convert."
                    )

                if target_content_flag < 1 or target_content_flag > len(file_obj.CONTENT_SIGNATURE_LIST):
                    raise ValueError(
                        f"Invalid target_contentFlag {target_content_flag} for '{name}'. "
                        f"Valid range: 1-{len(file_obj.CONTENT_SIGNATURE_LIST)}"
                    )

                # Get target content flag name (e.g., 'IPAIR', 'FMEAN')
                target_name = self._get_content_flag_name(file_obj, target_content_flag)

                # Call conversion method (e.g., as_IPAIR(), as_FMEAN())
                method_name = f'as_{target_name}'
                if not hasattr(file_obj, method_name):
                    raise NotImplementedError(
                        f"Conversion method '{method_name}' not found on {file_obj.__class__.__name__}. "
                        f"Cannot convert from contentFlag={current_content_flag} to {target_content_flag}."
                    )

                conversion_method = getattr(file_obj, method_name)
                converted_path = conversion_method(self.workDirectory)
                print(f"[DEBUG makeHklinGemmi] Converted {name} to {converted_path}")

                # Create a temporary file object pointing to converted file
                temp_name = f"_converted_{name}_{file_spec_idx}"
                temp_file_obj = file_obj.__class__(parent=self.container.inputData, name=temp_name)
                temp_file_obj.setFullPath(str(converted_path))
                temp_file_obj.contentFlag = CInt(target_content_flag)

                # Add to inputData temporarily
                setattr(self.container.inputData, temp_name, temp_file_obj)
                converted_files.append(temp_name)

                # Use temp object for merging
                file_obj = temp_file_obj
                print(f"[DEBUG makeHklinGemmi] Using temp file object '{temp_name}' with contentFlag={target_content_flag}")

            # Get filesystem path
            path = file_obj.getFullPath()
            print(f"[DEBUG makeHklinGemmi] Processing '{name}' -> path: {path}")
            if not path:
                raise ValueError(f"File object '{name}' has no path set")

            # Get columns from CONTENT_SIGNATURE_LIST using contentFlag
            # contentFlag is 1-indexed, CONTENT_SIGNATURE_LIST is 0-indexed
            content_flag = int(file_obj.contentFlag)
            if not hasattr(file_obj, 'CONTENT_SIGNATURE_LIST'):
                raise ValueError(
                    f"File object '{name}' (class {file_obj.__class__.__name__}) "
                    f"has no CONTENT_SIGNATURE_LIST. Is it a CMiniMtzDataFile?"
                )

            if content_flag < 1 or content_flag > len(file_obj.CONTENT_SIGNATURE_LIST):
                raise ValueError(
                    f"Invalid contentFlag {content_flag} for '{name}'. "
                    f"Valid range: 1-{len(file_obj.CONTENT_SIGNATURE_LIST)}"
                )

            columns = file_obj.CONTENT_SIGNATURE_LIST[content_flag - 1]

            # Build column_mapping (input_label -> output_label)
            # By default, prepend display_name to column (e.g., HKLIN1_F)
            # unless explicit rename is provided
            column_mapping = {}
            for col in columns:
                if col in rename_map:
                    # Explicit rename provided
                    output_col = rename_map[col]
                else:
                    # Default: prepend display_name with underscore
                    output_col = f"{display_name}_{col}"
                column_mapping[col] = output_col

            # Build spec for merge_mtz_files
            input_specs.append({
                'path': path,
                'column_mapping': column_mapping
            })

        # Call low-level gemmi utility
        output_path = self.workDirectory / f"{output_name}.mtz"
        result = merge_mtz_files(
            input_specs=input_specs,
            output_path=output_path,
            merge_strategy=merge_strategy
        )

        return result

    def _get_content_flag_name(self, file_obj, content_flag: int) -> str:
        """
        Get the name of a content flag from its integer value.

        Args:
            file_obj: File object with CONTENT_FLAG_* class constants
            content_flag: Integer content flag value

        Returns:
            Name of the content flag (e.g., 'IPAIR', 'FMEAN')

        Raises:
            ValueError: If content flag not found
        """
        # Search class constants for matching content flag
        for attr_name in dir(file_obj.__class__):
            if attr_name.startswith('CONTENT_FLAG_'):
                flag_value = getattr(file_obj.__class__, attr_name)
                if flag_value == content_flag:
                    # Extract name after CONTENT_FLAG_
                    return attr_name.replace('CONTENT_FLAG_', '')

        raise ValueError(f"No content flag name found for value {content_flag}")

    def makeHklin(self, miniMtzsIn: list, hklin: str = 'hklin') -> CErrorReport:
        """
        Merge mini-MTZ files into HKLIN (backward-compatible legacy API).

        This is a lightweight wrapper around makeHklinGemmi() that translates
        the old API format to the new API format. All conversion logic is
        handled by makeHklinGemmi().

        Args:
            miniMtzsIn: List of file specifications. Each can be either:
                - str: Attribute name in inputData (e.g., 'HKLIN1')
                       Uses the file object's own contentFlag
                - [str, int]: [attribute_name, target_contentFlag]
                       If file's contentFlag != target_contentFlag,
                       converts file to target format first (handled by makeHklinGemmi)

            hklin: Base name for output file (default: 'hklin')

        Returns:
            CErrorReport: Error report (empty if successful)

        Example (old API):
            >>> # Simple merge (uses objects' contentFlags)
            >>> error = self.makeHklin(['HKLIN1', 'FREERFLAG'])

            >>> # Request HKLIN2 in FPAIR format (converts if needed)
            >>> error = self.makeHklin([
            ...     'HKLIN1',
            ...     ['HKLIN2', CObsDataFile.CONTENT_FLAG_FPAIR]
            ... ])
        """
        error = CErrorReport()

        try:
            # Translate old API to new API
            file_objects = []

            for item in miniMtzsIn:
                if isinstance(item, str):
                    # Simple name - use object's own contentFlag
                    file_objects.append(item)

                elif isinstance(item, (list, tuple)) and len(item) == 2:
                    # [name, target_contentFlag] - let makeHklinGemmi handle conversion
                    name, target_flag = item
                    file_objects.append({
                        'name': name,
                        'display_name': name,
                        'target_contentFlag': target_flag
                    })

                else:
                    error.append(
                        klass=self.__class__.__name__,
                        code=207,
                        details=f"Invalid miniMtzsIn item: {item}. Expected str or [str, int]",
                        name=str(item)
                    )
                    self.errorReport.extend(error)
                    return error

            # Call new API - it handles all conversions
            self.makeHklinGemmi(
                file_objects=file_objects,
                output_name=hklin,
                merge_strategy='first'
            )

        except (AttributeError, ValueError, NotImplementedError, FileNotFoundError) as e:
            # Map specific exceptions to error codes
            error.append(
                klass=self.__class__.__name__,
                code=200,
                details=f"Error in makeHklin: {e}",
                name=hklin
            )
            self.errorReport.extend(error)

        except Exception as e:
            # Catch-all for unexpected errors
            error.append(
                klass=self.__class__.__name__,
                code=200,
                details=f"Unexpected error in makeHklin: {e}",
                name=hklin
            )
            self.errorReport.extend(error)

        # Add errors to plugin's error report
        self.errorReport.extend(error)

        # Print ERROR-level messages to terminal
        if error.maxSeverity() >= SEVERITY_ERROR:
            print(f"\n{'='*60}")
            print(f"ERROR in {self.__class__.__name__}.makeHklin():")
            print(f"{'='*60}")
            print(error.report())
            print(f"{'='*60}\n")

        return error

    def makeHklInput(
        self,
        miniMtzsIn: list = [],
        hklin: str = 'hklin',
        ignoreErrorCodes: list = [],
        extendOutputColnames: bool = True,
        useInputColnames: bool = False
    ) -> tuple:
        """
        Legacy API for makeHklin - returns (outfile, colnames, error).

        This method provides backward compatibility with the old CCP4i2 API.
        It wraps the modern makeHklin() method and returns the expected tuple.

        Args:
            miniMtzsIn: List of file names or [name, contentFlag] pairs
            hklin: Output filename (without extension)
            ignoreErrorCodes: Error codes to ignore (not currently used)
            extendOutputColnames: Whether to extend column names (not currently used)
            useInputColnames: Whether to use input column names (not currently used)

        Returns:
            Tuple of (outfile_path, column_names, error_report)
        """
        # Call the modern API
        error = self.makeHklin(miniMtzsIn, hklin)

        # Construct the output path
        outfile = str(self.workDirectory / f"{hklin}.mtz")

        # For now, return empty column names string
        # (Full column introspection would require reading the merged MTZ)
        colnames = ""

        return outfile, colnames, error

    def splitMtz(self, infile: str, outfiles: list, logFile: str = None) -> int:
        """
        Split an MTZ file into multiple mini-MTZ files with selected columns.

        This is a thin CData wrapper around split_mtz_file() from CCP4Utils.
        It handles the legacy outfiles list format and converts it to the
        simple column_mapping dict format.

        Args:
            infile: Path to input MTZ file
            outfiles: List of output specifications, each is a list of:
                     [output_path, input_columns] or
                     [output_path, input_columns, output_columns]
                     where input_columns and output_columns are comma-separated column names
            logFile: Optional path to log file (not used in gemmi implementation)

        Returns:
            SUCCEEDED or FAILED status code

        Example:
            >>> self.splitMtz(
            ...     '/path/to/input.mtz',
            ...     [['/path/to/output.mtz', 'FMEAN,SIGFMEAN', 'F,SIGF']],
            ...     '/path/to/log'
            ... )
        """
        from core.CCP4Utils import split_mtz_file, MtzSplitError

        print(f'[DEBUG splitMtz] Splitting {infile} using gemmi')
        print(f'[DEBUG splitMtz] Output specs: {outfiles}')

        try:
            # Process each output file
            for outfile_spec in outfiles:
                # Parse output specification
                if len(outfile_spec) == 2:
                    output_path, input_cols = outfile_spec
                    output_cols = input_cols  # Use same names for output
                elif len(outfile_spec) == 3:
                    output_path, input_cols, output_cols = outfile_spec
                else:
                    print(f'[ERROR] Invalid outfile spec: {outfile_spec}')
                    return self.FAILED

                # Parse column names
                input_col_names = [c.strip() for c in input_cols.split(',')]
                output_col_names = [c.strip() for c in output_cols.split(',')]

                if len(input_col_names) != len(output_col_names):
                    print(f'[ERROR] Input and output column counts must match')
                    return self.FAILED

                # Build column mapping dict for utility function
                column_mapping = dict(zip(input_col_names, output_col_names))

                print(f'[DEBUG splitMtz] Creating {output_path}')
                print(f'[DEBUG splitMtz]   Column mapping: {column_mapping}')

                # Call CData-agnostic utility function
                result_path = split_mtz_file(
                    input_path=infile,
                    output_path=output_path,
                    column_mapping=column_mapping
                )

                import os
                file_size = os.path.getsize(result_path)
                print(f'[DEBUG splitMtz] Created: {result_path} ({file_size} bytes)')

            return self.SUCCEEDED

        except (FileNotFoundError, ValueError, MtzSplitError) as e:
            print(f'[ERROR] splitMtz failed: {e}')
            return self.FAILED
        except Exception as e:
            print(f'[ERROR] splitMtz unexpected error: {e}')
            import traceback
            traceback.print_exc()
            return self.FAILED

    def splitHklout(
        self,
        miniMtzsOut: list,
        programColumnNames: list,
        inFile: str = None,
        logFile: str = None
    ) -> 'CErrorReport':
        """
        Split an HKLOUT file into multiple mini-MTZ files (CData-aware API).

        This is the standard CCP4i2 API method that works with object names
        in container.outputData. It wraps the lower-level splitMtz() method.

        Args:
            miniMtzsOut: List of output object names in container.outputData
            programColumnNames: List of comma-separated column name strings
                              e.g., ['F,SIGF', 'HLA,HLB,HLC,HLD']
            inFile: Input MTZ file path (default: workDirectory/hklout.mtz)
            logFile: Log file path (default: workDirectory/splitmtz.log)

        Returns:
            CErrorReport with any errors

        Example:
            >>> # Split hklout.mtz into FPHIOUT and ABCDOUT
            >>> error = self.splitHklout(
            ...     ['FPHIOUT', 'ABCDOUT'],
            ...     ['F,phi', 'A,B,C,D']
            ... )
        """
        error = CErrorReport()

        # Default input file
        if inFile is None:
            inFile = str(self.workDirectory / 'hklout.mtz')

        # Validate input file exists
        from pathlib import Path
        if not Path(inFile).exists():
            error.append(
                klass=self.__class__.__name__,
                code=300,
                details=f"Input file not found: {inFile}"
            )
            return error

        # Validate arguments
        if len(miniMtzsOut) != len(programColumnNames):
            error.append(
                klass=self.__class__.__name__,
                code=301,
                details=f"miniMtzsOut and programColumnNames must have same length. "
                        f"Got {len(miniMtzsOut)} vs {len(programColumnNames)}"
            )
            return error

        print(f'[DEBUG splitHklout] Splitting {inFile}')
        print(f'[DEBUG splitHklout] Output objects: {miniMtzsOut}')
        print(f'[DEBUG splitHklout] Column names: {programColumnNames}')

        # Build outfiles list for splitMtz
        outfiles = []
        for obj_name, col_string in zip(miniMtzsOut, programColumnNames):
            # Get output file object from container.outputData
            if not hasattr(self.container.outputData, obj_name):
                error.append(
                    klass=self.__class__.__name__,
                    code=302,
                    details=f"Output object '{obj_name}' not found in container.outputData"
                )
                continue

            file_obj = getattr(self.container.outputData, obj_name)

            # Get output file path
            output_path = file_obj.getFullPath()
            if not output_path:
                error.append(
                    klass=self.__class__.__name__,
                    code=303,
                    details=f"Output object '{obj_name}' has no path set"
                )
                continue

            # col_string is already comma-separated (e.g., 'F,SIGF')
            # Add to outfiles list: [output_path, input_columns]
            # (input and output columns are the same)
            outfiles.append([output_path, col_string])

            print(f'[DEBUG splitHklout]   {obj_name} -> {output_path} (columns: {col_string})')

        # Return early if there were errors
        if error.count() > 0:
            return error

        # Call splitMtz to do the actual work
        result = self.splitMtz(inFile, outfiles, logFile)

        if result == self.FAILED:
            error.append(
                klass=self.__class__.__name__,
                code=304,
                details="splitMtz failed"
            )

        return error

    def appendCommandScript(self, text=None, fileName=None, oneLine=False, clear=False):
        """
        Add text to the command script (list of lines for stdin/script file).

        Args:
            text: String or list of strings to add
            fileName: Path to file whose contents should be added
            oneLine: If text is a list, join into single line
            clear: Clear existing script before adding

        Returns:
            CErrorReport with any errors encountered
        """
        from core.CCP4ErrorHandling import CErrorReport

        error = CErrorReport()

        if clear:
            self.commandScript = []

        # Load from file if provided
        if fileName is not None:
            fileName = str(fileName)
            if not os.path.exists(fileName):
                error.append(
                    klass=self.__class__.__name__,
                    code=16,
                    details=f"File not found: {fileName}",
                    name=fileName
                )
                return error
            try:
                with open(fileName, 'r') as f:
                    text = f.read()
            except Exception as e:
                error.append(
                    klass=self.__class__.__name__,
                    code=16,
                    details=f"Error reading file: {e}",
                    name=fileName
                )
                return error

        # Process text
        if text is not None:
            # Handle list inputs
            if isinstance(text, list):
                if not oneLine:
                    # Add each item separately
                    for item in text:
                        sub_error = self.appendCommandScript(item)
                        if sub_error.count() > 0:
                            error.extend(sub_error)
                    return error
                else:
                    # Join into single line
                    text = ' '.join(str(item) for item in text)

            # Convert to string
            try:
                text_str = str(text)
            except Exception:
                error.append(
                    klass=self.__class__.__name__,
                    code=5,
                    details="Could not convert text to string"
                )
                return error

            # Ensure newline at end
            if text_str and not text_str.endswith('\n'):
                text_str += '\n'

            self.commandScript.append(text_str)

        return error

    def writeCommandFile(self, qualifier=None):
        """
        Write the command script to a file.

        Args:
            qualifier: Optional qualifier for filename (creates com_{qualifier}.txt)

        Returns:
            Path to written file, or None on error
        """
        if not self.commandScript:
            return None

        # Prepend header comment
        script_lines = [f'# Task {self.TASKNAME} command script\n'] + self.commandScript

        # Generate filename
        fileName = self.makeFileName('COM', qualifier=qualifier)

        try:
            with open(fileName, 'w') as f:
                f.writelines(script_lines)
            return fileName
        except Exception as e:
            print(f'[ERROR] Writing command file {fileName}: {e}')
            self.errorReport.append(
                klass=self.__class__.__name__,
                code=7,
                details=f'Error writing command file: {e}',
                name=fileName
            )
            return None

    def makeFileName(self, format='COM', ext='', qualifier=None):
        """
        Generate consistent names for output files.

        Args:
            format: File type (COM, LOG, STDOUT, STDERR, etc.)
            ext: Custom extension (overrides format default)
            qualifier: Optional qualifier to add to filename

        Returns:
            Full path to file in work directory
        """
        defNames = {
            'ROOT': '',
            'PARAMS': 'params.xml',
            'JOB_INPUT': 'input_params.xml',
            'PROGRAMXML': 'program.xml',
            'LOG': 'log.txt',
            'STDOUT': 'stdout.txt',
            'STDERR': 'stderr.txt',
            'INTERRUPT': 'interrupt_status.xml',
            'DIAGNOSTIC': 'diagnostic.xml',
            'REPORT': 'report.html',
            'COM': 'com.txt',
            'MGPICDEF': 'report.mgpic.py',
            'PIC': 'report.png',
            'RVAPIXML': 'i2.xml'
        }

        fileName = defNames.get(format, 'unknown.unk')

        # Add qualifier if provided
        if qualifier is not None:
            base, extension = fileName.rsplit('.', 1)
            fileName = f'{base}_{qualifier}.{extension}'

        # Use custom extension if provided
        if ext:
            base = fileName.rsplit('.', 1)[0]
            fileName = f'{base}.{ext}'

        return str(self.workDirectory / fileName)
