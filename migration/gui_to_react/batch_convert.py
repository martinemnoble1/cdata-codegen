#!/usr/bin/env python3
"""
Batch convert all legacy CCP4i2 GUI files to React TSX.
Generates a report of successes and failures.
"""

import sys
import json
from pathlib import Path
from gui_parser import convert_gui_file, GuiParser

# All GUI file locations
GUI_DIRS = [
    Path(__file__).parent.parent.parent / "wrappers",
    Path(__file__).parent.parent.parent / "pipelines",
]

OUTPUT_DIR = Path(__file__).parent.parent.parent / "client/renderer/components/task/task-interfaces/generated"


def find_all_gui_files():
    """Find all *_gui.py files in wrappers and pipelines"""
    gui_files = []
    for base_dir in GUI_DIRS:
        if base_dir.exists():
            for gui_file in base_dir.glob("*/script/*_gui.py"):
                gui_files.append(gui_file)
    return sorted(gui_files)


def get_task_name_from_file(filepath: Path) -> str:
    """Extract task name by parsing the file"""
    try:
        parser = GuiParser(str(filepath))
        parsed = parser.parse()
        return parsed.task_name
    except Exception:
        # Fall back to filename-based guess
        name = filepath.stem.replace("_gui", "")
        return name


def main():
    gui_files = find_all_gui_files()
    print(f"Found {len(gui_files)} GUI files\n")

    results = {
        "success": [],
        "failed": [],
        "no_ctaskwidget": [],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for gui_file in gui_files:
        relative_path = gui_file.relative_to(gui_file.parent.parent.parent)
        try:
            parser = GuiParser(str(gui_file))
            parsed = parser.parse()
            task_name = parsed.task_name

            # Generate TSX
            tsx_code = convert_gui_file(str(gui_file))

            # Check if we got meaningful content (not just empty tabs)
            has_elements = "CCP4i2TaskElement" in tsx_code

            if has_elements:
                output_file = OUTPUT_DIR / f"{task_name}.tsx"
                output_file.write_text(tsx_code)
                results["success"].append({
                    "task_name": task_name,
                    "source": str(relative_path),
                    "output": str(output_file.name),
                    "element_count": tsx_code.count("CCP4i2TaskElement"),
                })
                print(f"✓ {task_name}: {tsx_code.count('CCP4i2TaskElement')} elements")
            else:
                results["failed"].append({
                    "task_name": task_name,
                    "source": str(relative_path),
                    "reason": "No elements extracted",
                })
                print(f"✗ {task_name}: No elements extracted")

        except ValueError as e:
            if "No CTaskWidget" in str(e):
                results["no_ctaskwidget"].append({
                    "source": str(relative_path),
                    "reason": str(e),
                })
                print(f"⚠ {relative_path.name}: No CTaskWidget class")
            else:
                results["failed"].append({
                    "source": str(relative_path),
                    "reason": str(e),
                })
                print(f"✗ {relative_path.name}: {e}")
        except Exception as e:
            results["failed"].append({
                "source": str(relative_path),
                "reason": str(e),
            })
            print(f"✗ {relative_path.name}: {e}")

    # Print summary
    print("\n" + "=" * 60)
    print("CONVERSION SUMMARY")
    print("=" * 60)
    print(f"Total GUI files: {len(gui_files)}")
    print(f"Successfully converted: {len(results['success'])}")
    print(f"Failed: {len(results['failed'])}")
    print(f"No CTaskWidget class: {len(results['no_ctaskwidget'])}")

    # Print list of successful conversions for task-container.tsx
    if results["success"]:
        print("\n" + "-" * 60)
        print("SUCCESSFUL CONVERSIONS (for task-container.tsx):")
        print("-" * 60)
        for item in results["success"]:
            print(f"  {item['task_name']}: {item['element_count']} elements")

    # Save detailed report
    report_file = OUTPUT_DIR / "conversion_report.json"
    with open(report_file, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed report saved to: {report_file}")

    return results


if __name__ == "__main__":
    main()
