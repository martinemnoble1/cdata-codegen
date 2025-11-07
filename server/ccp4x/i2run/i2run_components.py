"""
i2run_components.py

Clean, separated components for i2run functionality.
Provides keyword extraction, argument building, and plugin population.

This refactored architecture separates concerns for better maintainability:
- KeywordExtractor: Extracts parameters from plugin definitions
- ArgumentBuilder: Builds argparse arguments with backward-compatible aliases
- PluginPopulator: Populates plugin instances with parsed arguments
"""

import logging
from pathlib import Path
from typing import List, Dict, Any

from core.CCP4Container import CContainer
from core.CCP4PluginScript import CPluginScript
from core import CCP4Data

logger = logging.getLogger(__name__)


# ============================================================================
# KeywordExtractor: Extract parameters from plugin definitions
# ============================================================================

class KeywordExtractor:
    """
    Extracts keyword metadata from plugin container hierarchies.

    Responsibilities:
    - Traverse container structure to find all leaf parameters
    - Compute minimum unique paths for each parameter
    - Identify ambiguous simple names for backward compatibility
    """

    @staticmethod
    def extract_from_plugin(plugin: CPluginScript) -> List[Dict[str, Any]]:
        """
        Extract all keywords from a plugin instance.

        Args:
            plugin: CPluginScript instance

        Returns:
            List of keyword dictionaries with metadata
        """
        keywords = KeywordExtractor._get_leaf_paths(plugin.container)
        keywords = KeywordExtractor._compute_minimum_paths(keywords)
        return keywords

    @staticmethod
    def extract_from_task_name(task_name: str) -> List[Dict[str, Any]]:
        """
        Extract all keywords for a task by name.

        Creates a temporary plugin instance to extract keywords.

        Args:
            task_name: Name of the task/plugin

        Returns:
            List of keyword dictionaries with metadata
        """
        from core.CCP4TaskManager import TASKMANAGER

        # Instantiate plugin to get its structure
        plugin_class = TASKMANAGER().get_plugin_class(task_name)
        plugin = plugin_class(parent=None)

        return KeywordExtractor.extract_from_plugin(plugin)

    @staticmethod
    def _get_leaf_paths(container: CContainer) -> List[Dict[str, Any]]:
        """
        Traverse container hierarchy and collect all leaf parameters.

        Args:
            container: Root container to traverse

        Returns:
            List of keyword dictionaries with path, object, and qualifiers
        """
        def traverse(node, path_parts):
            results = []

            if isinstance(node, CContainer):
                # Traverse children
                for child in node.children():
                    child_path = path_parts + [child.objectName()]
                    results.extend(traverse(child, child_path))
            else:
                # Leaf node - create keyword entry
                path = ".".join(path_parts)
                qualifiers = {}

                if hasattr(node, "get_merged_metadata"):
                    meta = node.get_merged_metadata("qualifiers")
                    if meta:
                        qualifiers = meta

                results.append({
                    "path": path,
                    "object": node,
                    "qualifiers": qualifiers
                })

            return results

        # Start traversal from container
        all_leaves = traverse(container, [container.objectName()])

        # Deduplicate by path (keep first occurrence)
        unique = {}
        for leaf in all_leaves:
            if leaf["path"] not in unique:
                unique[leaf["path"]] = leaf

        return list(unique.values())

    @staticmethod
    def _compute_minimum_paths(keywords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Compute minimum unique paths and identify ambiguous simple names.

        For each keyword:
        - minimumPath: Shortest suffix that uniquely identifies it
        - simpleName: Just the last path element
        - isAmbiguousSimpleName: Whether this simple name appears multiple times
        - isShortestForSimpleName: Whether this is the shortest path for its simple name

        Args:
            keywords: List of keyword dictionaries

        Returns:
            Enhanced keyword list with path metadata
        """
        paths = [kw["path"].split(".") for kw in keywords]

        # Build simple name mapping
        simple_name_map = {}
        for i, kw in enumerate(keywords):
            this_path = paths[i]
            simple_name = this_path[-1]
            kw["simpleName"] = simple_name

            if simple_name not in simple_name_map:
                simple_name_map[simple_name] = []
            simple_name_map[simple_name].append(i)

        # Mark ambiguous simple names and identify shortest path
        for simple_name, indices in simple_name_map.items():
            if len(indices) > 1:
                # Ambiguous - find shortest path
                shortest_idx = min(indices, key=lambda idx: len(paths[idx]))
                for idx in indices:
                    keywords[idx]["isAmbiguousSimpleName"] = True
                    keywords[idx]["isShortestForSimpleName"] = (idx == shortest_idx)
            else:
                # Unique
                keywords[indices[0]]["isAmbiguousSimpleName"] = False
                keywords[indices[0]]["isShortestForSimpleName"] = True

        # Compute minimum unique paths
        for i, kw in enumerate(keywords):
            this_path = paths[i]

            # Try increasing suffix lengths until unique
            for suffix_len in range(1, len(this_path) + 1):
                candidate = ".".join(this_path[-suffix_len:])

                # Check if any other path shares this suffix
                matches = [
                    j for j, other_path in enumerate(paths)
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


# ============================================================================
# ArgumentBuilder: Build argparse arguments with aliases
# ============================================================================

class ArgumentBuilder:
    """
    Builds argparse arguments from keyword metadata.

    Responsibilities:
    - Add arguments with minimum unique paths
    - Add backward-compatible simple name aliases
    - Handle CList types with append action
    """

    @staticmethod
    def build_arguments(parser, keywords: List[Dict[str, Any]]) -> None:
        """
        Add all arguments to the parser.

        Args:
            parser: argparse.ArgumentParser instance
            keywords: List of keyword dictionaries from KeywordExtractor
        """
        # First pass: Add arguments with minimum unique paths
        for keyword in keywords:
            ArgumentBuilder._add_argument(parser, keyword)

        # Second pass: Add simple name aliases for backward compatibility
        for keyword in keywords:
            if keyword.get("isAmbiguousSimpleName", False) and \
               keyword.get("isShortestForSimpleName", False):
                ArgumentBuilder._add_alias(parser, keyword)

    @staticmethod
    def _add_argument(parser, keyword: Dict[str, Any]) -> None:
        """
        Add a single argument to the parser.

        Args:
            parser: argparse.ArgumentParser instance
            keyword: Keyword dictionary with metadata
        """
        arg_name = f"--{keyword['minimumPath']}"
        kwargs = {
            "required": False,
            "dest": keyword["minimumPath"],
            "nargs": "+",
            "metavar": keyword["object"].__class__.__name__
        }

        # Extract help text and defaults from qualifiers
        qualifiers = keyword.get("qualifiers", {})
        if "toolTip" in qualifiers and qualifiers["toolTip"] != NotImplemented:
            kwargs["help"] = qualifiers["toolTip"]

        if "default" in qualifiers and qualifiers["default"] and \
           qualifiers["default"] != NotImplemented:
            kwargs["default"] = qualifiers["default"]

        # CList types use append action
        if isinstance(keyword["object"], CCP4Data.CList):
            kwargs["action"] = "append"

        try:
            parser.add_argument(arg_name, **kwargs)
        except TypeError as err:
            logger.error(f"TypeError adding argument {arg_name}: {err}")
        except Exception as err:
            logger.error(f"Error adding argument {arg_name}: {err}")

    @staticmethod
    def _add_alias(parser, keyword: Dict[str, Any]) -> None:
        """
        Add a simple name alias for backward compatibility.

        For ambiguous names, adds --XYZIN as an alias to --inputData.XYZIN
        (the shortest path).

        Args:
            parser: argparse.ArgumentParser instance
            keyword: Keyword dictionary for the shortest path
        """
        simple_arg = f"--{keyword['simpleName']}"

        try:
            parser.add_argument(
                simple_arg,
                dest=keyword["minimumPath"],
                required=False,
                nargs="+",
                metavar=keyword["object"].__class__.__name__,
                help=f"(Alias for --{keyword['minimumPath']}, shortest match)"
            )
            logger.debug(f"Added alias: {simple_arg} -> --{keyword['minimumPath']}")
        except Exception as err:
            # Alias conflicts or already exists - skip silently
            logger.debug(f"Could not add alias {simple_arg}: {err}")


# ============================================================================
# PluginPopulator: Populate plugin instances with parsed arguments
# ============================================================================

class PluginPopulator:
    """
    Populates plugin instances with values from parsed command-line arguments.

    Responsibilities:
    - Map parsed arguments to plugin parameters
    - Handle special syntaxes (fullPath=, columnLabels=, etc.)
    - Manage lists and file objects
    """

    @staticmethod
    def populate(plugin: CPluginScript, parsed_args, keywords: List[Dict[str, Any]]) -> None:
        """
        Populate plugin with parsed arguments.

        Args:
            plugin: CPluginScript instance to populate
            parsed_args: Namespace from argparse
            keywords: List of keyword dictionaries (for path mapping)
        """
        for kw in keywords:
            minpath = kw["minimumPath"]
            val = getattr(parsed_args, minpath, None)

            if val is not None:
                PluginPopulator._handle_item(plugin, kw["path"], val)

    @staticmethod
    def _handle_item(plugin: CPluginScript, object_path: str, value: Any) -> None:
        """
        Set a value on a plugin parameter.

        Handles special syntax like:
        - fullPath=/path/to/file
        - columnLabels=/*/*/[F,SIGF]
        - selection/text=(chain A)

        Args:
            plugin: CPluginScript instance
            object_path: Dot-separated path to parameter (e.g., "inputData.XYZIN")
            value: Value(s) to set (may be list)
        """
        # Navigate to the target object
        path_parts = object_path.split(".")
        current = plugin

        for part in path_parts[:-1]:  # Navigate to parent
            current = getattr(current, part, None)
            if current is None:
                logger.warning(f"Could not navigate to {part} in {object_path}")
                return

        # Get the target object
        target_name = path_parts[-1]
        target = getattr(current, target_name, None)

        if target is None:
            logger.warning(f"Could not find {target_name} in {object_path}")
            return

        # Handle list of values
        if isinstance(value, list):
            PluginPopulator._handle_item_or_list(plugin, current, target, value)
        else:
            PluginPopulator._handle_single_value(target, value)

    @staticmethod
    def _handle_item_or_list(plugin: CPluginScript, parent, target, values: List[Any]) -> None:
        """
        Handle setting a list of values.

        Args:
            plugin: CPluginScript instance
            parent: Parent container
            target: Target parameter object
            values: List of values to set
        """
        from core.CCP4File import CDataFile

        # For CList, add each item
        if isinstance(target, CCP4Data.CList):
            logger.debug(f"Handling CList {type(target).__name__} with {len(values)} values")
            for val in values:
                # Create a new item for the list
                new_item = target.makeItem()
                logger.debug(f"Created list item: {type(new_item).__name__}, setting value: {val}")
                # Set the value on the new item (not on the CList itself)
                PluginPopulator._handle_single_value(new_item, val, is_list=False)
                # Add the item to the list
                target.append(new_item)
                logger.debug(f"Appended item to list, list now has {len(target)} items")
        # For single-value file objects, process all subvalues
        elif isinstance(target, CDataFile):
            PluginPopulator._handle_file_with_subvalues(target, values)
        else:
            # Single value object - take first value
            if len(values) > 0:
                PluginPopulator._handle_single_value(target, values[0])

    @staticmethod
    def _handle_single_value(target, value, is_list: bool = False) -> None:
        """
        Handle setting a single value.

        Parses special syntax like fullPath=, columnLabels=, selection/text=

        Args:
            target: Target parameter object
            value: Value to parse and set (string, list, or dict)
            is_list: Whether this is being added to a CList
        """
        from core.CCP4File import CDataFile

        # Handle list values - join them or convert to appropriate format
        if isinstance(value, list):
            # For CData objects with .set(), convert list to string (comma-separated)
            # or try to set as individual attributes
            if hasattr(target, "set"):
                # If it's a single-item list, unwrap it
                if len(value) == 1:
                    value = value[0]
                else:
                    # Multiple items - join as comma-separated string
                    value = ",".join(str(v) for v in value)
            elif hasattr(target, "value"):
                # For simple value objects, use first item or join
                value = value[0] if len(value) == 1 else ",".join(str(v) for v in value)
            else:
                logger.warning(f"Don't know how to set list value {value} on {type(target).__name__}")
                return

        # Parse key=value syntax
        if "=" in str(value):
            parts = str(value).split("=", 1)
            key = parts[0]
            val = parts[1] if len(parts) > 1 else ""

            # Handle nested paths like "selection/text"
            if "/" in key:
                nested_parts = key.split("/")
                current = target
                for nested_key in nested_parts[:-1]:
                    current = getattr(current, nested_key, None)
                    if current is None:
                        logger.warning(f"Could not navigate to {nested_key}")
                        return

                final_key = nested_parts[-1]
                if hasattr(current, final_key):
                    setattr(current, final_key, val)
            else:
                # Direct attribute
                if hasattr(target, key):
                    attr = getattr(target, key, None)
                    # Handle CDataFile attributes specially
                    if isinstance(attr, CDataFile):
                        attr.setFullPath(val)
                    else:
                        setattr(target, key, val)
        else:
            # No key=value syntax - set the value directly
            if isinstance(target, CDataFile):
                target.setFullPath(value)
            elif hasattr(target, "value"):
                target.value = value
            elif hasattr(target, "set") and isinstance(value, (dict, type(target))):
                target.set(value)
            else:
                logger.warning(f"Don't know how to set value on {type(target).__name__}")

    @staticmethod
    def _handle_file_with_subvalues(target, values: List[str]) -> None:
        """
        Handle file objects with multiple subvalues.

        Example: --XYZIN fullPath=/path selection/text=(A)

        Special handling:
        1. If an MTZ file is provided with columnLabels, automatically splits
           the MTZ using gemmi_split_mtz and imports with standardized column names.
        2. If seqFile= is provided for CAsuDataFile, converts the sequence file
           to ASU XML format on the fly.

        Args:
            target: CDataFile instance
            values: List of key=value strings
        """
        from core.CCP4File import CDataFile

        # Parse all key=value pairs first to check for special handling opportunities
        parsed_values = {}
        has_key_value_syntax = False
        for value in values:
            if "=" in value:
                key, val = value.split("=", 1)
                parsed_values[key] = val
                has_key_value_syntax = True

        # Special handling for sequence files with seqFile= (CAsuDataFile)
        if has_key_value_syntax and "seqFile" in parsed_values:
            from ccp4x.lib.utils.formats.seq_to_asu import convert_sequence_file_to_asu
            import tempfile
            import os

            seq_file_path = Path(parsed_values["seqFile"])
            logger.info(f"seqFile parameter detected: {seq_file_path.name}, converting to ASU XML")

            try:
                # Determine destination directory using parent hierarchy
                dest_dir = None
                plugin_parent = target._find_plugin_parent() if hasattr(target, '_find_plugin_parent') else None

                if plugin_parent and hasattr(plugin_parent, 'workDirectory'):
                    # Use the plugin's work directory
                    work_dir = plugin_parent.workDirectory
                    dest_dir = Path(str(work_dir))
                    logger.debug(f"Using plugin workDirectory for ASU XML: {dest_dir}")
                else:
                    # Fallback: use temp directory
                    dest_dir = Path(tempfile.gettempdir())
                    logger.debug(f"No plugin workDirectory found, using temp dir: {dest_dir}")

                # Generate unique filename for ASU XML
                fd, temp_path = tempfile.mkstemp(
                    suffix=".asu.xml",
                    prefix=f"{seq_file_path.stem}_",
                    dir=dest_dir
                )
                os.close(fd)
                asu_xml_path = Path(temp_path)

                # Convert sequence file to ASU XML
                logger.info(f"Converting {seq_file_path} to ASU XML: {asu_xml_path}")
                convert_sequence_file_to_asu(
                    input_file=seq_file_path,
                    output_file=asu_xml_path,
                    project_name=getattr(plugin_parent, 'projectName', 'i2run_project') if plugin_parent else 'i2run_project',
                    project_id=getattr(plugin_parent, 'projectId', '00000000000000000000000000000000') if plugin_parent else '00000000000000000000000000000000'
                )

                # Replace seqFile with fullPath to the generated ASU XML
                parsed_values["fullPath"] = str(asu_xml_path)
                del parsed_values["seqFile"]
                logger.info(f"Converted sequence file to ASU XML: {asu_xml_path.name}")

            except Exception as e:
                logger.error(
                    f"Failed to convert sequence file {seq_file_path} to ASU XML: {e}. "
                    f"The seqFile parameter will be ignored."
                )
                # Remove seqFile from parsed_values to avoid setting it as an attribute
                if "seqFile" in parsed_values:
                    del parsed_values["seqFile"]

        # Special handling for MTZ files with columnLabels
        if has_key_value_syntax and "fullPath" in parsed_values and "columnLabels" in parsed_values:
            file_path = Path(parsed_values["fullPath"])
            if file_path.suffix.lower() == ".mtz" and file_path.exists():
                try:
                    from ccp4x.lib.utils.formats.gemmi_split_mtz import gemmi_split_mtz
                    import tempfile
                    import os

                    logger.info(
                        f"MTZ file with columnLabels detected: {file_path.name}, "
                        f"columns={parsed_values['columnLabels']}"
                    )

                    # Determine destination directory using parent hierarchy
                    # This works in both database and non-database contexts
                    dest_dir = None
                    plugin_parent = target._find_plugin_parent() if hasattr(target, '_find_plugin_parent') else None

                    if plugin_parent and hasattr(plugin_parent, 'workDirectory'):
                        # Use the plugin's work directory
                        work_dir = plugin_parent.workDirectory
                        # workDirectory might be a Path or a CString - use str() to handle both
                        dest_dir = Path(str(work_dir))
                        logger.debug(f"Using plugin workDirectory for MTZ split: {dest_dir}")
                    else:
                        # Fallback: use temp directory
                        dest_dir = Path(tempfile.gettempdir())
                        logger.debug(f"No plugin workDirectory found, using temp dir: {dest_dir}")

                    # Generate unique filename to avoid collisions
                    fd, temp_path = tempfile.mkstemp(
                        suffix=".mtz",
                        prefix=f"{file_path.stem}_split_",
                        dir=dest_dir
                    )
                    os.close(fd)  # Close the file descriptor, we just need the unique name
                    split_dest = Path(temp_path)

                    logger.info(f"Splitting MTZ to: {split_dest}")

                    # Split the MTZ with specified columns
                    split_file = gemmi_split_mtz(
                        input_file_path=file_path,
                        input_column_path=parsed_values["columnLabels"],
                        preferred_dest=split_dest
                    )

                    # Use the split file instead of original
                    parsed_values["fullPath"] = str(split_file)
                    logger.info(f"Using split MTZ file with standardized columns: {split_file.name}")

                except Exception as e:
                    logger.warning(
                        f"Failed to split MTZ file {file_path}: {e}. "
                        f"Continuing with original file."
                    )

        # Now apply all values using original behavior
        # If we modified parsed_values (MTZ splitting), reconstruct the values list
        if has_key_value_syntax and parsed_values:
            for key, val in parsed_values.items():
                PluginPopulator._handle_single_value(target, f"{key}={val}")
        else:
            # No key=value syntax or no modifications - use original behavior
            for value in values:
                PluginPopulator._handle_single_value(target, value)
