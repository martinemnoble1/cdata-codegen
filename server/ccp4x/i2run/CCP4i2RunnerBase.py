import pathlib
import unittest
import argparse
import re
from core.CCP4Container import CContainer
from core.CCP4ErrorHandling import CException
from core.CCP4PluginScript import CPluginScript
from core import CCP4Container
from core.CCP4TaskManager import TASKMANAGER
from core import CCP4Data
from core import CCP4XtalData
import traceback
import os
import sys
import logging
import shlex
import numpy
from ..lib.utils.parameters.set_parameter import set_parameter_container
from ..lib.utils.containers.find_objects import find_object_by_path
from ..lib.utils.formats.gemmi_split_mtz import gemmi_split_mtz

# Get an instance of a logger
logger = logging.getLogger("root")


def get_leaf_paths(container):
    """
    Given a container, return a list of unique leaf element dictionaries.
    A leaf is any child that is not a CContainer or CCP4Container.CContainer.
    Paths are dot-separated objectName() values from the root to the leaf.
    Only one item is returned for each unique path.
    """

    def traverse(node, path_parts):
        leaf_paths = []
        for child in node.children():
            if isinstance(child, (CContainer, CCP4Container.CContainer)):
                leaf_paths.extend(traverse(child, path_parts + [child.objectName()]))
            else:
                # Get qualifiers dict from modern CData (attribute, not method)
                qualifiers_dict = getattr(child, 'qualifiers', {})
                leaf_paths.append(
                    {
                        "path": child.objectPath(),
                        "minimumPath": child.objectPath(),
                        "qualifiers": qualifiers_dict if isinstance(qualifiers_dict, dict) else {},
                        "className": type(child).__name__,
                        "object": child,
                    }
                )
        return leaf_paths

    all_leafs = traverse(container, [container.objectName()])
    # Filter so only one item per unique path is returned
    unique = {}
    for leaf in all_leafs:
        if leaf["path"] not in unique:
            unique[leaf["path"]] = leaf
    return list(unique.values())


def compute_minimum_paths(keywords):
    """
    For each keyword dict with a 'path' key, add a 'minimumPath' key containing the shortest
    suffix of the path that uniquely identifies the element among all keywords.
    """
    paths = [kw["path"].split(".") for kw in keywords]
    n = len(paths)
    for i, kw in enumerate(keywords):
        this_path = paths[i]
        # Try increasing suffix lengths until unique
        for suffix_len in range(1, len(this_path) + 1):
            candidate = ".".join(this_path[-suffix_len:])
            # Check if any other path shares this suffix
            matches = [
                j
                for j, other_path in enumerate(paths)
                if len(other_path) >= suffix_len
                and other_path[-suffix_len:] == this_path[-suffix_len:]
            ]
            if len(matches) == 1 and matches[0] == i:
                kw["minimumPath"] = candidate
                break
        else:
            # Fallback: use full path
            kw["minimumPath"] = ".".join(this_path)
    return keywords


class CCP4i2RunnerBase(object):
    def __init__(self, the_args=None, command_line=None, parser=None, parent=None):
        self.parent = parent

        assert (
            the_args is not None or command_line is not None
        ), "Need to provide one of args or command_line"
        if the_args is None and command_line is not None:
            the_args = [os.path.expandvars(a) for a in shlex.split(command_line)]
        self.args = the_args

        if parser is None:
            self.parser = argparse.ArgumentParser(usage="i2run")
        else:
            self.parser = parser

        self.task_name = self.args[0]
        self.parser.add_argument("task_name")
        self.parser.add_argument("--project_name", default=None)
        self.parser.add_argument("--project_path", default=None)
        self.parser.add_argument("--delay", action="store_true")
        self.parser.add_argument("--batch", action="store_true")
        self.parsed_args = None
        self.job_id = None
        self.project_id = None
        self.list_map = {}

    def keywordsOfTask(self):
        return self.keywordsOfTaskName(self.task_name)

    def parseArgs(self, arguments_parsed=False):
        """
        Parse command-line arguments for the task.

        Args:
            arguments_parsed: If True, skip adding task arguments (already done)

        Returns:
            Parsed arguments namespace
        """
        if not arguments_parsed:
            CCP4i2RunnerBase.addTaskArguments(
                self.parser, self.task_name, parent=None
            )
        if self.parsed_args is None:
            self.parsed_args = self.parser.parse_args(self.args)
        return self.parsed_args

    def getPlugin(self, jobId=None, arguments_parsed=False):
        parsed_args = self.parseArgs(arguments_parsed)
        logger.debug(f"parsed_args is {parsed_args}")
        sys.stdout.flush()
        if parsed_args.project_name is not None:
            self.projectId = self.projectWithName(
                parsed_args.project_name, parsed_args.project_path
            )
            self.jobId = self.projectJobWithTask(
                projectId=self.projectId, task_name=self.task_name
            )
            jobId = self.jobId
        return self.pluginWithArgs(parsed_args=parsed_args, jobId=jobId)

    def projectWithName(self, project_name):
        raise Exception(
            f"CCP4i2RunnerBase class does not provide projectWithName - implemented in subclasses"
        )

    def projectJobWithTask(self, projectId, task_name=None):
        raise Exception(
            f"CCP4i2RunnerBase class does not provide projectJobWithTask - implemented in subclasses"
        )

    def execute(self):
        raise Exception(
            f"CCP4i2RunnerBase class does not provide execute - implemented in subclasses"
        )

    @staticmethod
    def keywordsOfContainer(container: CContainer, growingList=None):
        return get_leaf_paths(container)

    @staticmethod
    def getCandidatePath(currentPath):
        pathElements = currentPath.split(".")
        return ".".join(pathElements[1:])

    @staticmethod
    def minimisePaths(allKeywords):
        compute_minimum_paths(allKeywords)
        return allKeywords

    @staticmethod
    def keywordsOfTaskName(task_name, parent=None):
        """
        Get all keywords (parameters) for a task by instantiating its plugin.

        Modern approach: Instantiate CPluginScript which automatically:
        - Locates and loads .def.xml (with inheritance support via DefXmlParser)
        - Creates container hierarchy (inputData, outputData, controlParameters)
        - Sets up all parameters with qualifiers

        Args:
            task_name: Name of the task/plugin
            parent: Parent object (unused in modern approach, kept for compatibility)

        Returns:
            List of keyword dicts with paths, minimumPaths, qualifiers, etc.
        """
        # Get plugin class from task manager
        plugin_class = TASKMANAGER().get_plugin_class(task_name)

        # Instantiate plugin - this automatically loads .def.xml with modern DefXmlParser
        # (which includes inheritance support we added in Phase 1)
        thePlugin = plugin_class(parent=None, workDirectory=None)

        # Extract keywords from the loaded container
        allKeywords = CCP4i2RunnerBase.keywordsOfContainer(thePlugin.container, [])

        # Compute minimum paths for concise CLI arguments
        return CCP4i2RunnerBase.minimisePaths(allKeywords)

    @staticmethod
    def addTaskArguments(theParser, task_name, parent=None):
        """
        Add command-line arguments to parser based on task parameters.

        Args:
            theParser: argparse.ArgumentParser instance
            task_name: Name of the task/plugin
            parent: Unused (kept for backward compatibility)
        """
        keywords = CCP4i2RunnerBase.keywordsOfTaskName(task_name, parent=None)
        logger.debug(str(keywords))

        for keyword in keywords:
            logger.debug(keyword["path"])
            # sys.stdout.flush()
            args = ["--{}".format(keyword["minimumPath"])]
            kwargs = {"required": False}
            for key, value in keyword["qualifiers"].items():
                if key == "toolTip" and value != NotImplemented:
                    kwargs["help"] = value
                elif key == "default" and value and value != NotImplemented:
                    # True  Here a hack to make no properties "required" from command line
                    kwargs["default"] = value
                kwargs["nargs"] = "+"
                kwargs["metavar"] = keyword["object"].__class__.__name__
            if isinstance(keyword["object"], CCP4Data.CList):
                # print("Found append action", keyword["object"].objectPath())
                kwargs["action"] = "append"
            try:
                # print(args, kwargs)
                theParser.add_argument(*args, **kwargs)
            except TypeError as err:
                print("TypeError Exception ", err, " for ", args, kwargs)
            except argparse.ArgumentError as err:
                print("argparse.ArgumentError Exception ", err, " for ", args, kwargs)
        return theParser

    @staticmethod
    def slugify_variable(variable):
        # Remove any non-alphanumeric characters except for commas and hyphens
        variable = re.sub(r"[/*\[\] ,]+", "-", variable)

        # Convert to lowercase
        variable = variable.lower()

        # Remove leading/trailing hyphens, if any
        variable = variable.strip("-")

        return variable

    @staticmethod
    def gemmiSplitMTZ(
        input_path_str: str = None,
        inputColumnPath: str = None,
        output_path_str: str = None,
        intoDirectory: str = None,
    ):
        if output_path_str is not None and intoDirectory is not None:
            raise Exception(
                "smartSplitMTZ Exception:",
                "Provide *either* full output path for file, or name of directory where file should be placed",
            )
        if output_path_str is None and intoDirectory is None:
            raise Exception(
                "smartSplitMTZ Exception:",
                "Provide either full output path for file, or name of directory where file should be placed",
            )
        input_path = pathlib.Path(input_path_str)

        if output_path_str is None:
            output_path_str = (
                CCP4i2RunnerBase.slugify_variable(inputColumnPath) + "_split.mtz"
            )
        output_path = pathlib.Path(intoDirectory) / output_path_str

        final_dest = gemmi_split_mtz(input_path, inputColumnPath, output_path)
        return str(final_dest)

    def handleItem(self, thePlugin: CPluginScript, objectPath, value):
        """
        Set a parameter value on the plugin container.

        Args:
            thePlugin: Plugin instance
            objectPath: Full object path (e.g., "prosmart_refmac.container.controlParameters.WEIGHT")
            value: Value to set

        Note:
            The objectPath from keywords includes the full hierarchy, but find_object_by_path
            expects a path relative to the container. We need to strip the task name and
            "container" prefix.
        """
        # Strip task name and "container" from path
        # e.g., "prosmart_refmac.container.controlParameters.WEIGHT" -> "controlParameters.WEIGHT"
        path_parts = objectPath.split(".")
        if len(path_parts) >= 3 and path_parts[1] == "container":
            # Remove task name (path_parts[0]) and "container" (path_parts[1])
            relative_path = ".".join(path_parts[2:])
        else:
            # Fallback: use path as-is
            relative_path = objectPath

        the_object = find_object_by_path(thePlugin.container, relative_path)
        if the_object is None:
            return
        is_complex_object = (
            hasattr(the_object, "children")
            and callable(the_object.children)
            and len(the_object.children()) > 0
        )
        if is_complex_object and isinstance(value, str) and "=" in value:
            subPath, subValue = value.split("=", 1)
            # Intercept some things to do with (e.g.) columnLabels
            if subPath == "columnLabels":
                theObject = find_object_by_path(
                    thePlugin.container, relative_path
                )  # PluginUtils.locateElement(thePlugin.container, relative_path)
                splitFilePath = CCP4i2RunnerBase.gemmiSplitMTZ(
                    input_path_str=theObject.fullPath.__str__(),
                    inputColumnPath=subValue,
                    intoDirectory=thePlugin.workDirectory,
                )
                print(f"Post split file path is {splitFilePath}")
                set_parameter_container(thePlugin.container, relative_path, splitFilePath)
            elif subPath == "fileUse":
                # print(f'In handleItem fileUse {relative_path}')
                sys.stdout.flush()
                fileUseDict = CCP4i2RunnerBase.parseFileUse(subValue)
                fileUseDict["projectId"] = thePlugin.projectId()
                fileDict = self.fileForFileUse(**fileUseDict)
                set_parameter_container(thePlugin.container, relative_path, fileDict)
            elif subPath == "fullPath":
                logger.info("Setting parameter to %s %s", relative_path, subValue)
                set_parameter_container(thePlugin.container, relative_path, subValue)
            else:
                # For composite paths, also strip the task.container prefix from the base
                compositePath = ".".join(relative_path.split(".") + subPath.split("/"))
                logger.info("Setting parameter to %s %s", compositePath, subValue)
                set_parameter_container(thePlugin.container, compositePath, subValue)
        elif value is not None:
            # Handle Python lists being set on CList objects (from argparse nargs)
            from core.base_object.fundamental_types import CList

            if isinstance(the_object, CList) and isinstance(value, list):
                # For CList objects, populate with items from the Python list
                the_object.clear()
                for item_value in value:
                    new_item = the_object.makeItem()
                    new_item.value = item_value
                    the_object.append(new_item)
                logger.info("Setting CList parameter %s with %d items", relative_path, len(value))
            elif not isinstance(the_object, CList) and isinstance(value, list):
                # For non-CList objects, if argparse returned a list (nargs), unwrap it
                # This happens when argparse uses nargs for a simple parameter
                if len(value) == 1:
                    actual_value = value[0]
                    logger.info("Setting parameter to %s %s (unwrapped from list)", relative_path, actual_value)
                    set_parameter_container(thePlugin.container, relative_path, actual_value)
                else:
                    # Multiple values for non-list parameter - this shouldn't happen
                    logger.warning("Got multiple values %s for non-list parameter %s, using first", value, relative_path)
                    set_parameter_container(thePlugin.container, relative_path, value[0])
            else:
                logger.info("Setting parameter to %s %s", relative_path, value)
                set_parameter_container(thePlugin.container, relative_path, value)

    def fileForFileUse(
        self,
        projectName=None,
        projectId=None,
        task_name=None,
        jobIndex=None,
        jobParamName=None,
        paramIndex=-1,
    ):
        # Base class stub method, to be overloaded by derived classes
        return {}

    def handleItemOrList(self, thePlugin, objectPath, value):
        # print(f"In handleItemOrList {objectPath} {value}")
        if isinstance(value, list):
            for item in value:
                self.handleItem(thePlugin, objectPath, item)
        else:
            self.handleItem(thePlugin, objectPath, value)

    def pluginWithArgs(self, parsed_args, workDirectory=None, jobId=None):
        """
        Create plugin instance and populate with command-line arguments.

        Modern approach: Plugin instantiation with parent=None (no Qt dependency).

        Args:
            parsed_args: Parsed command-line arguments
            workDirectory: Working directory for the plugin
            jobId: Optional job ID for database integration

        Returns:
            Configured plugin instance
        """
        if jobId is not None:
            workDirectory = CCP4Modules.PROJECTSMANAGER().jobDirectory(jobId=jobId)
        # Modern approach: No Qt parent needed
        thePlugin = TASKMANAGER().get_plugin_class(
            parsed_args.task_name
        )(jobId=jobId, workDirectory=workDirectory, parent=None)
        self.work_directory = workDirectory
        if jobId is not None:
            jobInfo = (
                CCP4Modules.PROJECTSMANAGER()
                .db()
                .getJobInfo(
                    mode=["projectname", "projectid", "jobnumber"],
                    jobId=jobId,
                    returnType=dict,
                )
            )
            # print('jobInfo', jobInfo)
            thePlugin.setDbData(
                jobId=jobId,
                projectName=jobInfo["projectname"],
                projectId=jobInfo["projectid"],
                jobNumber=jobInfo["jobnumber"],
            )
        # PluginUtils.removeDefaults(thePlugin.container)
        allKeywords = CCP4i2RunnerBase.keywordsOfContainer(thePlugin.container, [])

        def predicate(item):
            return (
                f"{parsed_args.task_name}.inputData.temporary" not in item["path"]
                and f"{parsed_args.task_name}.outputData" not in item["path"]
            )

        allKeywords = list(filter(predicate, allKeywords))
        mappedKeywords = {
            taskKeyword["minimumPath"]: taskKeyword
            for taskKeyword in CCP4i2RunnerBase.minimisePaths(allKeywords)
        }
        for keyword, value in vars(parsed_args).items():
            if value is not NotImplemented and keyword in mappedKeywords:
                theObject = mappedKeywords[keyword]["object"]
                try:
                    if isinstance(theObject, CCP4Data.CList):
                        # Here handling lists that might or might not start out with a "dummy" entry
                        if theObject.objectPath() not in self.list_map:
                            self.list_map[theObject.objectPath()] = 1
                            if len(theObject) == 0:
                                theObject.append(theObject.makeItem())
                        else:
                            theObject.append(theObject.makeItem())
                        theItem = theObject[-1]
                        if value is not None:
                            for iItem, item in enumerate(value):
                                self.handleItemOrList(
                                    thePlugin, theItem.objectPath(), item
                                )
                                if iItem < len(value) - 1:
                                    theObject.append(theObject.makeItem())
                                    theItem = theObject[-1]
                        # Delete known unset exemplars
                        theObject.removeUnsetListItems()
                    elif value is not None:
                        self.handleItemOrList(thePlugin, theObject.objectPath(), value)
                except Exception as err:
                    print(
                        f"Failed to set {theObject.objectPath()} to {value} with err {err}"
                    )
                    traceback.print_exc()
        return thePlugin

    @staticmethod
    def parseFileUse(fileUse):
        fileUseParser_tN_jI_jP_pI = re.compile(
            r"^(?P<task_name>.+)\[(?P<jobIndex>.+)\]\.(?P<jobParamName>.+)\[(?P<paramIndex>.+)\].*$"
        )
        fileUseParser_jI_jP_pI = re.compile(
            r"^(?P<jobIndex>.+)\.(?P<jobParamName>.*)\[(?P<paramIndex>.+)\].*$"
        )
        fileUseParser_tN_jI_jP = re.compile(
            r"^(?P<task_name>.+)\[(?P<jobIndex>.+)\]\.(?P<jobParamName>.+).*$"
        )
        fileUseParser_jI_jP = re.compile(r"^(?P<jobIndex>.+)\.(?P<jobParamName>.+).*$")
        # task_name[jobIndex].jobParamName[paramIndex] returns dict containing task_name, jobIndex, jobParamName, paramIndex
        result = {
            "task_name": None,
            "jobIndex": None,
            "jobParamName": None,
            "paramIndex": -1,
        }
        print(f"Trying to match [{fileUse}]")
        try:
            matches = fileUseParser_tN_jI_jP_pI.match(fileUse)
            result.update(matches.groupdict())
            # print(f'Fileuse {fileUse} matched tN_jI_jP_pI')
            result["jobIndex"] = int(result["jobIndex"])
            result["paramIndex"] = int(result["paramIndex"])
            return result
        except AttributeError as err:
            try:
                matches = fileUseParser_jI_jP_pI.match(fileUse)
                result.update(matches.groupdict())
                # print(f'Fileuse {fileUse} matched jI_jP_pI')
                result["jobIndex"] = int(result["jobIndex"])
                result["paramIndex"] = int(result["paramIndex"])
                return result
            except AttributeError as err:
                try:
                    matches = fileUseParser_tN_jI_jP.match(fileUse)
                    result.update(matches.groupdict())
                    # print(f'Fileuse {fileUse} matched tN_jI_jP')
                    result["jobIndex"] = int(result["jobIndex"])
                    result["paramIndex"] = int(result["paramIndex"])
                    return result
                except AttributeError as err:
                    matches = fileUseParser_jI_jP.match(fileUse)
                    result.update(matches.groupdict())
                    # print(f'Fileuse {fileUse} matched jI_jP')
                    result["jobIndex"] = int(result["jobIndex"])
                    result["paramIndex"] = int(result["paramIndex"])
                    return result


class TestParse(unittest.TestCase):
    modelPdb = os.path.join(
        os.path.expandvars("$CCP4I2_TOP/demo_data/gamma/gamma_model.pdb")
    )
    gammaMtz = os.path.join(
        os.path.expandvars("$CCP4I2_TOP/demo_data/gamma/merged_intensities_Xe.mtz")
    )
    betaPdb = os.path.join(
        os.path.expandvars("$CCP4I2_TOP/demo_data/beta_blip/beta.pdb")
    )
    blipPdb = os.path.join(
        os.path.expandvars("$CCP4I2_TOP/demo_data/beta_blip/blip.pdb")
    )

    def setUp(self):
        self.application = CCP4Modules.QTAPPLICATION(graphical=False)

    def test1(self):
        args = ["prosmart_refmac"]
        runner = CCP4i2RunnerBase(args, parent=self.application)
        taskKeywords = runner.keywordsOfTask()
        print(len(taskKeywords))
        assert len(taskKeywords) == 150

    def test2(self):
        args = ["prosmart_refmac", "--XYZIN", "test.pdb"]
        runner = CCP4i2RunnerBase(args, parent=self.application)
        parsed_args = runner.parseArgs()
        # print(parsed_args.XYZIN)
        assert len(parsed_args.XYZIN) == 1
        assert parsed_args.XYZIN[0] == "test.pdb"

    def test3(self):
        args = [
            "phaser_pipeline",
            "--ENSEMBLES",
            "use=True",
            "pdbItemList[0]/identity_to_target=0.8",
            "pdbItemList[0]/structure={}".format(TestParse.betaPdb),
            "--ENSEMBLES",
            "use=True",
            "pdbItemList[0]/identity_to_target=0.9",
            "pdbItemList[0]/structure={}".format(TestParse.blipPdb),
        ]
        runner = CCP4i2RunnerBase(args, parent=self.application)
        # theParser.print_help()
        thePlugin = runner.getPlugin()
        theEtree = thePlugin.container.getEtree(excludeUnset=True)
        assert len(theEtree.findall("//identity_to_target")) == 2
        assert theEtree.findall("//identity_to_target")[0].text == "0.8"
        assert theEtree.findall("//identity_to_target")[1].text == "0.9"
        # ET.indent(theEtree)
        # print(ET.tostring(theEtree))

    def test4(self):
        args = [
            "prosmart_refmac",
            "--XYZIN",
            TestParse.modelPdb,
            'selection/text="A/"',
            "--F_SIGF",
            TestParse.gammaMtz,
            "columnLabels=/*/*/[Iplus,SIGIplus,Iminus,SIGIminus]",
        ]
        runner = CCP4i2RunnerBase(args, parent=self.application)
        thePlugin = runner.getPlugin()
        theEtree = thePlugin.container.getEtree(excludeUnset=True)
        assert len(theEtree.findall(".//selection/text")) == 1

    def test5(self):
        # self.assertDictEqual(CCP4i2RunnerBase.parseFileUse("prosmart_refmac[-1].XYZOUT[2]"),
        #                     {"task_name": "prosmart_refmac", "jobIndex": "-1", "jobParamName": "XYZOUT", "paramIndex": "2"})
        self.assertDictEqual(
            CCP4i2RunnerBase.parseFileUse("refmac[-1].XYZOUT[2]"),
            {
                "task_name": "refmac",
                "jobIndex": -1,
                "jobParamName": "XYZOUT",
                "paramIndex": 2,
            },
        )
        self.assertDictEqual(
            CCP4i2RunnerBase.parseFileUse("[-1].XYZOUT[2]"),
            {
                "task_name": None,
                "jobIndex": -1,
                "jobParamName": "XYZOUT",
                "paramIndex": 2,
            },
        )
        self.assertDictEqual(
            CCP4i2RunnerBase.parseFileUse("[-1].XYZOUT"),
            {
                "task_name": None,
                "jobIndex": -1,
                "jobParamName": "XYZOUT",
                "paramIndex": -1,
            },
        )
        self.assertDictEqual(
            CCP4i2RunnerBase.parseFileUse("refmac[-1].XYZOUT"),
            {
                "task_name": "refmac",
                "jobIndex": -1,
                "jobParamName": "XYZOUT",
                "paramIndex": -1,
            },
        )

    def test6(self):
        args = [
            "prosmart_refmac",
            "--XYZIN",
            TestParse.modelPdb,
            'selection/text="A/"',
            "--F_SIGF",
            'fileUse="aimless_pipeline[-1].HKLOUT[0]"',
        ]
        theRunner = CCP4i2RunnerBase(args, parent=self.application)
        thePlugin = theRunner.getPlugin()
        theEtree = thePlugin.container.getEtree(excludeUnset=True)
