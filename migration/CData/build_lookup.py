"""
Build lookup data for CData-derived classes in the data_manager.

This module crawls through a directory tree, imports Python files, and builds
a lookup mapping of CData-derived classes. It captures:
- Class name and module
- CONTENTS class variable
- File path and other metadata

Similar to task_manager/build_lookup.py but focused on CData classes.
"""

import sys
import glob
import os
import importlib.util
import inspect
import logging
import json
import ast
import re
import pathlib
from typing import Dict, Any, List, Optional, Type
from pathlib import Path

from ccp4i2.googlecode import diff_match_patch_py3

CCP4I2_ROOT = str(pathlib.Path(diff_match_patch_py3.__file__).parent.parent)
if CCP4I2_ROOT not in sys.path:
    sys.path.insert(0, CCP4I2_ROOT)
print(CCP4I2_ROOT)


def setup_logger() -> logging.Logger:
    """Set up logging for the build process."""
    logger = logging.getLogger("data_build_lookup")
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(levelname)s %(asctime)s %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = setup_logger()

# Attributes to extract from CData classes
CDATA_ATTRIBUTES = [
    "CONTENTS",
    "CONTENTS_ORDER",
    "QUALIFIERS",
    "QUALIFIERS_ORDER",
    "QUALIFIERS_DEFINITION",
    "ERROR_CODES",
    "SUBITEM",
    "XMLNAME",
    "XMLTAG",
    "DATAPATH",
    "FILEFUNCTION",
    "CONTENTFLAG",
    "SUBTYPE",
]


def is_cdata_subclass(obj: Type) -> bool:
    """
    Return True if obj is a subclass of CData (by name, robust to import path).

    Args:
        obj: The class object to check

    Returns:
        bool: True if the class inherits from CData
    """
    try:
        if not inspect.isclass(obj):
            return False

        # Check method resolution order for CData
        for base in obj.__mro__:
            if base.__name__ == "CData":
                return True

        # Also check if it's a direct subclass of common CData types
        cdata_base_names = {
            "CData",
            "CDataFile",
            "CContainer",
            "CList",
            "CString",
            "CInt",
            "CFloat",
            "CBoolean",
        }

        for base in obj.__mro__:
            if base.__name__ in cdata_base_names:
                return True

        return False

    except Exception as e:
        logger.debug(f"Error checking CData inheritance for {obj}: {e}")
        return False


def discover_python_files(root_dir: str):
    """
    Yield (dirpath, filename, fullpath, module_name) for each candidate .py file.

    Args:
        root_dir: Root directory to search

    Yields:
        Tuple of (directory_path, filename, full_path, module_name)
    """

    filenames = glob.glob(os.path.join(root_dir, "*.py"))

    for fname in filenames:
        if (
            not fname.endswith(".py")
            or fname.startswith("__")
            or fname == "setup.py"
            or fname == "build_lookup.py"
        ):
            continue

        dirpath = os.path.dirname(fname)

        fpath = os.path.join(dirpath, fname)
        rel_path = os.path.relpath(fpath, root_dir)

        # Create module name from relative path
        module_name = "ccp4x.data_scan." + rel_path[:-3].replace(os.sep, ".")

        yield dirpath, fname, fpath, module_name


def import_module_from_file(module_name: str, fpath: str):
    """
    Import a module from a file path, returning the module object or None.

    Args:
        module_name: Name to assign to the imported module
        fpath: File path to import from

    Returns:
        The imported module or None if import failed
    """
    try:
        # Skip files that are likely to cause import issues
        skip_patterns = [
            "django",
            "models.py",
            "views.py",
            "urls.py",
            "admin.py",
            "migrations",
            "settings",
            "wsgi.py",
            "asgi.py",
            "CCP4WorkflowManager.py",
        ]

        if any(pattern in fpath.lower() for pattern in skip_patterns):
            logger.debug(f"Skipping Django/web file: {fpath}")
            return None

        spec = importlib.util.spec_from_file_location(module_name, fpath)
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)

            # Add to sys.modules to handle relative imports
            sys.modules[module_name] = mod
            spec.loader.exec_module(mod)

            return mod
        else:
            logger.warning(f"Could not create import spec for {fpath}")
    except Exception as e:
        logger.debug(f"Failed to import {fpath}: {e}")
    return None


def extract_cdata_classes(mod, module_name: str) -> Dict[str, Any]:
    """
    Extract CData-derived classes from a module and return their metadata.

    Args:
        mod: The imported module
        module_name: Name of the module

    Returns:
        Dictionary mapping class names to their metadata
    """
    cdata_classes = {}

    try:
        for name, obj in inspect.getmembers(mod, inspect.isclass):
            # Skip the base CData class itself
            if obj.__name__ == "CData":
                continue

            # Only process classes defined in this module (not imported)
            if hasattr(obj, "__module__") and obj.__module__ != module_name:
                continue

            if is_cdata_subclass(obj):
                logger.debug(f"Found CData class: {name} in {module_name}")

                # Extract class metadata
                base_classes = [base.__name__ for base in obj.__bases__]
                immediate_parent = base_classes[0] if base_classes else None

                class_info = {
                    "module": module_name,
                    "class": name,
                    "file_path": getattr(mod, "__file__", "unknown"),
                    "docstring": inspect.getdoc(obj) or "",
                    "base_classes": base_classes,
                    "immediate_parent": immediate_parent,
                    "mro": [
                        cls.__name__ for cls in obj.__mro__[:-1]
                    ],  # Exclude 'object'
                }

                # Extract CData-specific attributes
                for attr in CDATA_ATTRIBUTES:
                    if hasattr(obj, attr):
                        try:
                            attr_value = getattr(obj, attr)
                            # Handle different types of attribute values
                            if attr_value is not None:
                                serialized_value = serialize_attribute(attr_value)
                                class_info[attr] = serialized_value
                            else:
                                class_info[attr] = None
                        except Exception as e:
                            logger.warning(f"Error extracting {attr} from {name}: {e}")
                            class_info[attr] = f"<Error: {str(e)}>"

                # Store by class name
                cdata_classes[name] = class_info
                logger.info(f"Registered CData class: {name} from {module_name}")

    except Exception as e:
        logger.warning(f"Error inspecting module {module_name}: {e}")

    return cdata_classes


def parse_file_for_classes(fpath: str) -> Dict[str, Any]:
    """
    Parse a Python file directly for class definitions when import fails.

    Args:
        fpath: Path to the Python file

    Returns:
        Dictionary of potentially interesting classes found
    """
    classes_found = {}

    try:
        with open(fpath, "r", encoding="utf-8") as f:
            content = f.read()

        # Use AST to parse the file safely
        import ast

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                class_name = node.name

                # Look for base classes that might indicate CData inheritance
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        # Handle cases like module.ClassName
                        base_names.append(
                            ast.unparse(base) if hasattr(ast, "unparse") else str(base)
                        )

                # Check if this might be a CData class
                cdata_indicators = {
                    "CData",
                    "CDataFile",
                    "CContainer",
                    "CList",
                    "CString",
                    "CInt",
                    "CFloat",
                    "CBoolean",
                }
                if any(
                    indicator in " ".join(base_names) for indicator in cdata_indicators
                ):

                    # Initialize attribute extraction
                    class_attributes = {}

                    # Extract immediate parent class
                    immediate_parent = base_names[0] if base_names else None

                    # Look for all CData-specific class variables
                    for class_node in node.body:
                        if isinstance(class_node, ast.Assign):
                            for target in class_node.targets:
                                if (
                                    isinstance(target, ast.Name)
                                    and target.id in CDATA_ATTRIBUTES
                                ):
                                    attr_name = target.id
                                    try:
                                        # Try to evaluate the attribute value safely
                                        attr_value = ast.literal_eval(class_node.value)
                                    except:
                                        attr_value = f"<Unparseable: {ast.unparse(class_node.value) if hasattr(ast, 'unparse') else 'complex'}>"

                                    # Parse unparseable content if needed
                                    if isinstance(
                                        attr_value, str
                                    ) and attr_value.startswith("<Unparseable:"):
                                        class_attributes[attr_name] = (
                                            parse_unparseable_contents(attr_value)
                                        )
                                    else:
                                        class_attributes[attr_name] = attr_value

                    classes_found[class_name] = {
                        "class": class_name,
                        "file_path": fpath,
                        "base_classes": base_names,
                        "immediate_parent": immediate_parent,
                        "parse_method": "AST",
                        "docstring": ast.get_docstring(node) or "",
                        **class_attributes,  # Add all extracted attributes
                    }

                    logger.info(
                        f"Found potential CData class via AST: {class_name} in {fpath}"
                    )

    except Exception as e:
        logger.debug(f"Failed to parse {fpath} with AST: {e}")

    return classes_found


def serialize_attribute(value: Any) -> Any:
    """
    Serialize an attribute value to JSON-compatible format.

    Args:
        value: The attribute value to serialize

    Returns:
        JSON-serializable representation of the value
    """
    if value is None:
        return None
    elif isinstance(value, (str, int, float, bool)):
        return value
    elif isinstance(value, (list, tuple)):
        return [serialize_attribute(item) for item in value]
    elif isinstance(value, dict):
        return {k: serialize_attribute(v) for k, v in value.items()}
    # elif inspect.isclass(type(value)):
    #    return {"type": "class", "className": value.__class__.__name__}
    elif hasattr(value, "__dict__"):
        return str(value)
    else:
        # Fall back to string representation
        return str(value)


def build_lookup_from_dir(root_dir: str) -> Dict[str, Any]:
    """
    Crawl a directory tree, import .py files, and build a lookup mapping
    of CData-derived classes.

    Args:
        root_dir: Root directory to scan

    Returns:
        Dictionary containing the lookup data with metadata
    """
    # Add root directory to Python path for imports
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    lookup = {}
    scan_stats = {
        "files_scanned": 0,
        "files_imported": 0,
        "classes_found": 0,
        "import_errors": 0,
    }

    logger.info(f"Building CData lookup from: {root_dir}")

    for dirpath, fname, fpath, module_name in discover_python_files(root_dir):
        scan_stats["files_scanned"] += 1
        logger.debug(f"Scanning file: {fpath}")

        mod = import_module_from_file(module_name, fpath)
        if mod:
            scan_stats["files_imported"] += 1
            cdata_classes = extract_cdata_classes(mod, module_name)
            lookup.update(cdata_classes)
            scan_stats["classes_found"] += len(cdata_classes)

            # Clean up module from sys.modules to avoid conflicts
            if module_name in sys.modules:
                del sys.modules[module_name]
        else:
            print("Failed to import module: {module_name} from {fpath}")
            scan_stats["import_errors"] += 1

            # Try AST parsing as fallback for files that can't be imported
            logger.debug(f"Trying AST parsing for {fpath}")
            ast_classes = parse_file_for_classes(fpath)
            if ast_classes:
                lookup.update(ast_classes)
                scan_stats["classes_found"] += len(ast_classes)

    # Build final result with metadata
    result = {
        "scan_info": {
            "root_directory": root_dir,
            "scan_timestamp": None,  # Could add if needed
            **scan_stats,
        },
        "classes": lookup,
    }

    logger.info(
        f"Scan complete: {scan_stats['classes_found']} CData classes found "
        f"from {scan_stats['files_imported']}/{scan_stats['files_scanned']} files"
    )

    return result


def save_lookup_to_json(lookup_data: Dict[str, Any], output_file: str):
    """
    Save lookup data to a JSON file.

    Args:
        lookup_data: The lookup data to save
        output_file: Path to output JSON file
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(lookup_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Lookup data saved to: {output_file}")
    except Exception as e:
        logger.error(f"Failed to save lookup data to {output_file}: {e}")


def print_summary(lookup_data: Dict[str, Any]):
    """
    Print a summary of the discovered classes.

    Args:
        lookup_data: The lookup data to summarize
    """
    classes = lookup_data.get("classes", {})
    scan_info = lookup_data.get("scan_info", {})

    print(f"\nCData Class Discovery Summary:")
    print(f"=" * 40)
    print(f"Root directory: {scan_info.get('root_directory', 'unknown')}")
    print(f"Files scanned: {scan_info.get('files_scanned', 0)}")
    print(f"Files imported: {scan_info.get('files_imported', 0)}")
    print(f"Import errors: {scan_info.get('import_errors', 0)}")
    print(f"Classes found: {scan_info.get('classes_found', 0)}")

    if classes:
        print(f"\nDiscovered Classes:")
        print(f"-" * 20)

        # Group by base class
        by_base_class = {}
        for class_name, class_info in classes.items():
            base_classes = class_info.get("base_classes", ["unknown"])
            base_class = base_classes[0] if base_classes else "unknown"

            if base_class not in by_base_class:
                by_base_class[base_class] = []
            by_base_class[base_class].append(class_name)

        for base_class, class_list in sorted(by_base_class.items()):
            print(f"\n{base_class} subclasses ({len(class_list)}):")
            for class_name in sorted(class_list):
                class_info = classes[class_name]
                has_contents = "CONTENTS" in class_info and class_info["CONTENTS"]
                contents_indicator = " [CONTENTS]" if has_contents else ""
                print(f"  • {class_name}{contents_indicator}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Build lookup data for CData-derived classes"
    )
    parser.add_argument(
        "directory",
        nargs="?",
        default=os.path.join(CCP4I2_ROOT, "core"),
        help="Directory to scan for CData classes (default: current directory)",
    )
    parser.add_argument("--output", "-o", help="Output JSON file path")
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress summary output"
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    elif args.quiet:
        logger.setLevel(logging.WARNING)

    # Build the lookup
    root_directory = os.path.abspath(args.directory)
    logger.info(f"Starting CData class discovery in: {root_directory}")

    result = build_lookup_from_dir(root_directory)

    # Save to file if requested
    if args.output:
        save_lookup_to_json(result, args.output)

    # Print summary unless quiet
    if not args.quiet:
        print_summary(result)

    # Print JSON to stdout if no output file
    if not args.output and not args.quiet:
        print(f"\nJSON Output:")
        print(f"=" * 15)
        print(json.dumps(result, indent=2))
