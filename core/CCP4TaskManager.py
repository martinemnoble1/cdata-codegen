import os
import json
from typing import List, Dict, Any

import sys
import subprocess
import argparse


class CTaskManager:
    insts = None

    def __init__(self):
        dir_path = os.path.dirname(os.path.abspath(__file__))
        defxml_path = os.path.join(dir_path, "task_manager", "defxml_lookup.json")
        plugin_path = os.path.join(dir_path, "task_manager", "plugin_lookup.json")

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
