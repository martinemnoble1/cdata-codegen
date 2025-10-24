import os
import json
from typing import List, Dict, Any, Optional
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

        # Load plugin_lookup.json
        try:
            with open(plugin_path, "r") as f:
                self.plugin_lookup = json.load(f)
        except Exception as e:
            print(f"Error loading plugin_lookup.json: {e}")

    def locate_def_xml(self, task_name: str, version: Optional[str] = None) -> Optional[Path]:
        """
        Locate the .def.xml file for a task given its name and optional version.

        Args:
            task_name: Name of the task/plugin (e.g., "refmac", "pointless")
            version: Optional version string to match specific version

        Returns:
            Path to the .def.xml file if found, None otherwise
        """
        for entry in self.defxml_lookup:
            plugin_name = entry.get("pluginName", "")
            plugin_version = entry.get("pluginVersion", "")

            # Check if plugin name matches
            if plugin_name == task_name:
                # If version specified, check version match
                if version is not None and plugin_version != version:
                    continue

                # Get relative path and convert to absolute
                rel_path = entry.get("file_path", "")
                if rel_path:
                    # Path is relative to task_manager directory
                    abs_path = Path(self.task_manager_dir) / rel_path
                    abs_path = abs_path.resolve()  # Resolve any .. in the path

                    if abs_path.exists():
                        return abs_path

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
