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
from core.base_object.error_reporting import CErrorReport
from core.task_manager.def_xml_handler import DefXmlParser
from core.task_manager.params_xml_handler import ParamsXmlHandler
from core.CCP4TaskManager import TASKMANAGER


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

        # Initialize infrastructure components
        self._def_parser = DefXmlParser()
        self._params_handler = ParamsXmlHandler()

        # Create main container with standard sub-containers
        # CPluginScript is now the parent of the container
        self.container = CContainer(parent=self, name="container")

        # Standard sub-containers as per CCP4i2 convention
        # Parent relationship established automatically when parent is set
        self.inputData = CContainer(parent=self.container, name="inputData")
        self.outputData = CContainer(parent=self.container, name="outputData")
        self.controlParameters = CContainer(
            parent=self.container, name="controlParameters")
        self.guiAdmin = CContainer(parent=self.container, name="guiAdmin")

        # Error report for tracking issues during execution
        self.errorReport = CErrorReport()

        # Process management
        self._process = None
        self._status = None

        # Working directory and file paths
        if workDirectory is not None:
            self.workDirectory = Path(workDirectory)
        else:
            self.workDirectory = Path.cwd()
        self.defFile = None
        self.paramsFile = None

        # Load DEF file if available (defines container structure)
        if self.TASKNAME:
            self._loadDefFile()

        # Load PARAMS file if provided (actual parameter values)
        if xmlFile:
            self.loadDataFromXml(xmlFile)

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

        # Use CTaskManager's locate_def_xml method
        return task_manager.locate_def_xml(
            task_name=self.TASKNAME,
            version=self.TASKVERSION
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
                self.inputData = parsed_container.inputData
                # Update parent to be our container (which is parented to self)
                self.inputData.set_parent(self.container)

            if hasattr(parsed_container, 'outputData'):
                self.outputData = parsed_container.outputData
                self.outputData.set_parent(self.container)

            if hasattr(parsed_container, 'controlParameters'):
                self.controlParameters = parsed_container.controlParameters
                self.controlParameters.set_parent(self.container)

            if hasattr(parsed_container, 'guiAdmin'):
                self.guiAdmin = parsed_container.guiAdmin
                self.guiAdmin.set_parent(self.container)

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
        error = self.processInputFiles()
        if error:
            self.errorReport.extend(error)
            return self.FAILED

        # Generate command and script
        error = self.makeCommandAndScript()
        if error:
            self.errorReport.extend(error)
            return self.FAILED

        # Start the process
        error = self.startProcess()
        if error:
            self.errorReport.extend(error)
            return self.FAILED

        return self.RUNNING

    def checkInputData(self) -> CErrorReport:
        """
        Validate that input data is correct and files exist.

        This method checks all items in the inputData container and
        verifies that files marked with mustExist actually exist.

        Returns:
            CErrorReport with any validation errors
        """
        error = CErrorReport()

        # Validate all input data items
        for name, obj in self.inputData.items():
            obj_error = obj.validity()
            if obj_error:
                error.extend(obj_error)

        return error

    def checkOutputData(self) -> CErrorReport:
        """
        Set output file names if not already set.

        This method generates appropriate file names for any output files
        that don't have names yet.

        Returns:
            CErrorReport with any issues (should fix rather than fail)
        """
        error = CErrorReport()

        # Auto-generate file names for output data
        # Subclasses can override for custom naming logic

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

    def makeCommandAndScript(self) -> CErrorReport:
        """
        Generate command line and command file for the program.

        Uses COMLINETEMPLATE and COMTEMPLATE class attributes to
        generate the command line and input file.

        Returns:
            CErrorReport with any errors
        """
        error = CErrorReport()

        # This would use CComTemplate to process templates
        # For now, placeholder implementation

        return error

    def startProcess(self) -> CErrorReport:
        """
        Start the external program process.

        Uses PROCESSMANAGER to start the program specified by TASKCOMMAND
        with the command line and file created by makeCommandAndScript().

        Returns:
            CErrorReport with any errors
        """
        error = CErrorReport()

        # This would use PROCESSMANAGER to start the process
        # For now, placeholder implementation

        return error

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
            error = self.processOutputFiles()
            if error:
                self.errorReport.extend(error)
                status = self.FAILED

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

        # Emit signal (placeholder)
        # In real implementation, would emit Qt signal

        self._status = status

    # =========================================================================
    # Utility methods for backward compatibility with old API
    # =========================================================================

    def makePluginObject(self, taskName: str, version: Optional[str] = None, **kwargs) -> Optional['CPluginScript']:
        """
        Create a sub-plugin (sub-job) instance using TASKMANAGER.

        This is used when a pipeline calls other wrappers as sub-jobs.

        Args:
            taskName: Name of the task to instantiate
            version: Optional version of the task (defaults to latest)
            **kwargs: Additional arguments passed to the plugin constructor

        Returns:
            New CPluginScript instance, or None if plugin not found
        """
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

        # Instantiate the plugin
        try:
            plugin_instance = plugin_class(**kwargs)
            return plugin_instance
        except Exception as e:
            self.errorReport.append(
                klass=self.__class__.__name__,
                code=109,
                details=f"Failed to instantiate plugin '{taskName}': {e}",
                name=taskName
            )
            return None

    def getErrorReport(self) -> CErrorReport:
        """Get the accumulated error report."""
        return self.errorReport

    def getContainer(self) -> CContainer:
        """Get the main container."""
        return self.container
