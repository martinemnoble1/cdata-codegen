import os
import json
from typing import List, Dict, Any, Optional, Type
from pathlib import Path

import sys
import subprocess
import argparse


class CTaskManager:
    insts = None

    def __init__(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.task_manager_dir = os.path.join(dir_path, "task_manager")
        defxml_path = os.path.join(self.task_manager_dir, "defxml_lookup.json")
        plugin_path = os.path.join(self.task_manager_dir, "plugin_lookup.json")

        self.defxml_lookup: List[Dict[str, str]] = []
        self.plugin_lookup: Dict[str, Dict[str, Any]] = {}

        # Load defxml_lookup.json
        try:
            with open(defxml_path, "r") as f:
                self.defxml_lookup = json.load(f)
        except Exception as e:
            print(f"Error loading defxml_lookup.json: {e}")

        # Load plugin_lookup.json (for backward compatibility)
        try:
            with open(plugin_path, "r") as f:
                self.plugin_lookup = json.load(f)
        except Exception as e:
            print(f"Error loading plugin_lookup.json: {e}")

        # Set up CCP4I2_ROOT for plugin imports
        ccp4i2_root = os.environ.get("CCP4I2_ROOT")
        if ccp4i2_root and ccp4i2_root not in sys.path:
            sys.path.insert(0, ccp4i2_root)

        # Initialize plugin registry (lazy loading)
        self._plugin_registry = None

    @property
    def plugin_registry(self):
        """Get the plugin registry (lazy load on first access)."""
        if self._plugin_registry is None:
            from .task_manager.plugin_registry import get_registry
            self._plugin_registry = get_registry()
        return self._plugin_registry

    def get_plugin_class(self, task_name: str, version: Optional[str] = None) -> Optional[Type]:
        """
        Get a plugin class by name, with lazy loading.

        Args:
            task_name: Name of the task/plugin (e.g., "refmac", "pointless")
            version: Optional version (currently ignored - uses latest)

        Returns:
            Plugin class, or None if not found
        """
        return self.plugin_registry.get_plugin_class(task_name, version)

    def get_plugin_metadata(self, task_name: str) -> Optional[Dict[str, Any]]:
        """
        Get plugin metadata without importing the plugin.

        Args:
            task_name: Name of the task/plugin

        Returns:
            Dictionary of plugin metadata, or None if not found
        """
        return self.plugin_registry.get_plugin_metadata(task_name)

    def list_plugins(self) -> List[str]:
        """Get list of all available plugin names."""
        return self.plugin_registry.list_plugins()

    def locate_def_xml(self, task_name: str, version: Optional[str] = None) -> Optional[Path]:
        """
        Locate the .def.xml file for a task given its name and optional version.

        Args:
            task_name: Name of the task/plugin (e.g., "refmac", "pointless")
            version: Optional version string to match specific version

        Returns:
            Path to the .def.xml file if found, None otherwise
        """
        # Get CCP4I2_ROOT for resolving paths
        ccp4i2_root = os.environ.get("CCP4I2_ROOT")
        if not ccp4i2_root:
            # Fallback: try to detect from current file location
            # core/CCP4TaskManager.py -> core/../ = project root
            ccp4i2_root = str(Path(__file__).parent.parent)

        for entry in self.defxml_lookup:
            plugin_name = entry.get("pluginName", "")
            plugin_version = entry.get("pluginVersion", "")

            # Check if plugin name matches
            if plugin_name == task_name:
                # If version specified, check version match
                if version is not None and plugin_version != version:
                    continue

                # Get relative path from entry
                rel_path = entry.get("file_path", "")
                if rel_path:
                    # Legacy paths may point to ccp4i2 structure: ../../../ccp4i2/wrappers/...
                    # Current paths are relative: ../../wrappers/...
                    # Convert to our structure: wrappers/...
                    if "../../../ccp4i2/" in rel_path:
                        rel_path = rel_path.replace("../../../ccp4i2/", "")
                    elif "../../../" in rel_path:
                        # Assume it's a legacy path pointing to ccp4i2 root
                        rel_path = rel_path.replace("../../../", "")
                    elif "../../" in rel_path:
                        # Current path format from defxml_lookup.py: ../../wrappers/...
                        # Strip ../../ to get wrappers/...
                        rel_path = rel_path.replace("../../", "")

                    # Resolve relative to CCP4I2_ROOT
                    abs_path = Path(ccp4i2_root) / rel_path
                    abs_path = abs_path.resolve()  # Resolve any remaining .. in the path

                    if abs_path.exists():
                        return abs_path

        return None

    def getReportClass(self, name: str, version: Optional[str] = None) -> Optional[Type]:
        """
        Get the report class for a plugin/task.

        Args:
            name: Name of the task/plugin (e.g., "refmac", "pointless")
            version: Optional version string (currently ignored)

        Returns:
            Report class if found, None otherwise
        """
        # Get the plugin class first
        plugin_class = self.get_plugin_class(name, version)
        if plugin_class is None:
            return None

        # Check if the plugin class has a REPORT attribute
        if hasattr(plugin_class, "REPORT"):
            return plugin_class.REPORT

        return None

    def getReportAttribute(self, name: str, attribute: str, version: Optional[str] = None) -> Any:
        """
        Get an attribute from a plugin's report class.

        Args:
            name: Name of the task/plugin (e.g., "refmac", "pointless")
            attribute: Name of the attribute to retrieve (e.g., "WATCHED_FILE")
            version: Optional version string (currently ignored)

        Returns:
            Attribute value if found, None otherwise
        """
        report_class = self.getReportClass(name, version)
        if report_class is None:
            return None

        return getattr(report_class, attribute, None)

    def getTitle(self, name: str) -> Optional[str]:
        """
        Get the title of a plugin/task.

        Args:
            name: Name of the task/plugin (e.g., "refmac", "pointless")

        Returns:
            Task title if found, None otherwise
        """
        metadata = self.get_plugin_metadata(name)
        if metadata:
            return metadata.get("TASKTITLE")
        return None

    def getShortTitle(self, name: str) -> Optional[str]:
        """
        Get the short title of a plugin/task. Falls back to TASKNAME if no short title available.

        Args:
            name: Name of the task/plugin (e.g., "refmac", "pointless")

        Returns:
            Task short title or task name if found, None otherwise
        """
        metadata = self.get_plugin_metadata(name)
        if metadata:
            # Try SHORTTITLE first, fall back to TASKNAME
            return metadata.get("SHORTTITLE", metadata.get("TASKNAME"))
        return None


def TASKMANAGER():
    """Return a unique instance of CTaskManager."""
    if CTaskManager.insts is None:
        CTaskManager.insts = CTaskManager()
    return CTaskManager.insts


def main():
    """Main entry point for module. Use --rebuild to regenerate lookup files."""
    parser = argparse.ArgumentParser(description="CCP4 Task Manager Utility")
    parser.add_argument(
        "--rebuild", action="store_true", help="Regenerate lookup files"
    )
    args = parser.parse_args()

    if args.rebuild:
        dir_path = os.path.dirname(os.path.abspath(__file__))
        defxml_script = os.path.join(dir_path, "task_manager", "defxml_lookup.py")
        plugin_script = os.path.join(dir_path, "plugin_lookup.py")

        print("Regenerating defxml_lookup.json...")
        subprocess.run([sys.executable, defxml_script], check=True)
        print("Regenerating plugin_lookup.json...")
        subprocess.run([sys.executable, plugin_script], check=True)
        print("Lookup files regenerated.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
