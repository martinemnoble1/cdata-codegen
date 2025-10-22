"""
Params XML Handler for CCP4i2 Task Parameters

This module handles .params.xml files that capture user-specified parameter values
for CCP4i2 tasks. It provides bidirectional functionality:

1. Export: Create .params.xml from a task hierarchy (only explicitly set parameters)
2. Import: Parse .params.xml and overlay values onto a task hierarchy

The params XML format uses simple tag names that correspond to the parameter names
in the task hierarchy, with values stored as text content or structured data for files.
"""

import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Union, List
from pathlib import Path
from datetime import datetime
import socket
import os

from ..new_cdata.base_classes import CData, CContainer
from ..new_cdata.fundamental_types import *


class ParamsXmlHandler:
    """Handler for CCP4i2 .params.xml files."""

    def __init__(self):
        self.namespace = "http://www.ccp4.ac.uk/ccp4ns"
        self.namespace_prefix = "ccp4"

    def export_params_xml(
        self, task: CData, output_path: str, user_id: str = None
    ) -> bool:
        """
        Export explicitly set parameters from a task hierarchy to a .params.xml file.

        Args:
            task: The root task object (from .def.xml parsing)
            output_path: Path where to save the .params.xml file
            user_id: User ID for the header (defaults to current user)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create root element with namespace
            root = ET.Element(f"{{{self.namespace}}}ccp4i2")
            root.set(f"xmlns:{self.namespace_prefix}", self.namespace)

            # Create header
            header = ET.SubElement(root, "ccp4i2_header")

            # Add header information
            ET.SubElement(header, "function").text = "PARAMS"
            ET.SubElement(header, "userId").text = user_id or os.getenv(
                "USER", "unknown"
            )
            ET.SubElement(header, "hostName").text = socket.gethostname()
            ET.SubElement(header, "creationTime").text = datetime.now().strftime(
                "%H:%M %d/%b/%y"
            )
            ET.SubElement(header, "ccp4iVersion").text = (
                "alpha_rev_90011"  # Could be configurable
            )
            ET.SubElement(header, "pluginName").text = getattr(
                task, "name", "unknown_task"
            )

            # Create body
            body = ET.SubElement(root, "ccp4i2_body")

            # Export all containers and their explicitly set parameters
            self._export_container(task, body)

            # Write to file with proper formatting
            self._write_formatted_xml(root, output_path)

            print(f"✅ Exported params to: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Error exporting params XML: {e}")
            import traceback

            traceback.print_exc()
            return False

    def import_params_xml(self, task: CData, params_xml_path: str) -> bool:
        """
        Import parameter values from a .params.xml file and overlay them onto a task hierarchy.

        Args:
            task: The root task object (from .def.xml parsing)
            params_xml_path: Path to the .params.xml file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not Path(params_xml_path).exists():
                print(f"❌ Params file not found: {params_xml_path}")
                return False

            # Parse the XML
            tree = ET.parse(params_xml_path)
            root = tree.getroot()

            # Find the body element
            body = root.find(".//ccp4i2_body")
            if body is None:
                print("❌ No ccp4i2_body found in params XML")
                return False

            # Import all parameter values
            imported_count = self._import_container_values(body, task)

            print(f"✅ Imported {imported_count} parameters from: {params_xml_path}")
            return True

        except Exception as e:
            print(f"❌ Error importing params XML: {e}")
            import traceback

            traceback.print_exc()
            return False

    def _export_container(self, container: CData, parent_elem: ET.Element):
        """Recursively export container contents, only including explicitly set values."""
        # Get all attributes that are CData objects
        for attr_name in sorted(dir(container)):
            if (
                not attr_name.startswith("_")
                and not callable(getattr(container, attr_name))
                and attr_name
                not in [
                    "child_added",
                    "child_removed",
                    "destroyed",
                    "object_info",
                    "parent_changed",
                    "state",
                ]
            ):

                try:
                    attr = getattr(container, attr_name)
                    if hasattr(attr, "name"):  # It's a CData object

                        if isinstance(attr, CContainer):
                            # Create container element and recurse
                            container_elem = ET.SubElement(parent_elem, attr_name)
                            self._export_container(attr, container_elem)

                            # Remove empty containers
                            if len(container_elem) == 0:
                                parent_elem.remove(container_elem)

                        else:
                            # Check if this parameter has been explicitly set
                            if self._is_explicitly_set(attr):
                                param_elem = ET.SubElement(parent_elem, attr_name)
                                self._export_parameter_value(attr, param_elem)

                except Exception as e:
                    print(f"Warning: Error processing {attr_name}: {e}")
                    continue

    def _is_explicitly_set(self, param: CData) -> bool:
        """Check if a parameter has been explicitly set by the user."""
        try:
            # Check if it has set state tracking
            if hasattr(param, "getValueState"):
                from .new_cdata.base_classes import ValueState

                state = param.getValueState("value")
                return state == ValueState.EXPLICITLY_SET

            # Fallback: check if it has a value attribute that's not default
            if hasattr(param, "value"):
                # For now, consider any non-empty value as explicitly set
                # This could be refined with better default tracking
                value = param.value
                if isinstance(value, bool):
                    return True  # Booleans are always considered set if present
                elif isinstance(value, (int, float)):
                    return True  # Numbers are always considered set if present
                elif isinstance(value, str):
                    return len(value.strip()) > 0
                else:
                    return value is not None

            return False

        except Exception:
            return False

    def _export_parameter_value(self, param: CData, elem: ET.Element):
        """Export the value of a parameter to an XML element."""
        try:
            if hasattr(param, "value"):
                value = param.value

                # Handle different data types
                if isinstance(value, bool):
                    elem.text = str(value)
                elif isinstance(value, (int, float)):
                    elem.text = str(value)
                elif isinstance(value, str):
                    elem.text = value
                else:
                    elem.text = str(value)

            # Handle file objects (they have structured data)
            elif self._is_file_object(param):
                self._export_file_data(param, elem)

            # Handle performance indicators and other complex objects
            elif hasattr(param, "__dict__"):
                self._export_complex_object(param, elem)

        except Exception as e:
            print(f"Warning: Error exporting value for {param.name}: {e}")
            elem.text = ""

    def _is_file_object(self, param: CData) -> bool:
        """Check if this is a file-type object."""
        type_name = type(param).__name__
        return "File" in type_name or "DataFile" in type_name

    def _export_file_data(self, file_obj: CData, elem: ET.Element):
        """Export file object data in the structured format."""
        # For file objects, we need to export structured data
        # This is a placeholder - you'd need to implement based on your file object structure
        file_attrs = [
            "project",
            "baseName",
            "relPath",
            "annotation",
            "dbFileId",
            "subType",
            "contentFlag",
        ]

        for attr in file_attrs:
            if hasattr(file_obj, attr):
                value = getattr(file_obj, attr)
                if value is not None:
                    sub_elem = ET.SubElement(elem, attr)
                    sub_elem.text = str(value)

    def _export_complex_object(self, obj: CData, elem: ET.Element):
        """Export complex objects with multiple attributes."""
        # For objects like PERFORMANCEINDICATOR
        for attr_name in dir(obj):
            if (
                not attr_name.startswith("_")
                and not callable(getattr(obj, attr_name))
                and attr_name not in ["name", "parent"]
            ):

                try:
                    value = getattr(obj, attr_name)
                    if value is not None and not isinstance(value, CData):
                        sub_elem = ET.SubElement(elem, attr_name)
                        sub_elem.text = str(value)
                except Exception:
                    continue

    def _import_container_values(
        self, xml_container: ET.Element, cdata_container: CData
    ) -> int:
        """Recursively import values from XML into CData container."""
        imported_count = 0

        for child_elem in xml_container:
            elem_name = child_elem.tag

            # Check if this corresponds to an attribute in the CData container
            if hasattr(cdata_container, elem_name):
                attr = getattr(cdata_container, elem_name)

                if isinstance(attr, CContainer):
                    # Recurse into nested containers
                    imported_count += self._import_container_values(child_elem, attr)

                else:
                    # Import parameter value
                    if self._import_parameter_value(child_elem, attr):
                        imported_count += 1
            else:
                print(f"Warning: No attribute '{elem_name}' found in container")

        return imported_count

    def _import_parameter_value(self, xml_elem: ET.Element, param: CData) -> bool:
        """Import a value from XML element into a CData parameter."""
        try:
            # Handle simple values
            if xml_elem.text is not None and len(list(xml_elem)) == 0:
                # Simple text value
                text_value = xml_elem.text.strip()

                if hasattr(param, "value"):
                    # Convert to appropriate type
                    if isinstance(param, CBoolean):
                        param.value = text_value.lower() in ("true", "1", "yes")
                    elif isinstance(param, CInt):
                        param.value = int(text_value)
                    elif isinstance(param, CFloat):
                        param.value = float(text_value)
                    elif isinstance(param, CString):
                        param.value = text_value
                    else:
                        # Generic assignment
                        param.value = text_value

                    return True

            # Handle structured data (like file objects)
            elif len(list(xml_elem)) > 0:
                return self._import_structured_data(xml_elem, param)

            return False

        except Exception as e:
            print(f"Warning: Error importing value for {param.name}: {e}")
            return False

    def _import_structured_data(self, xml_elem: ET.Element, param: CData) -> bool:
        """Import structured data from XML into a parameter."""
        try:
            imported_any = False

            for child in xml_elem:
                attr_name = child.tag
                if child.text is not None:
                    value = child.text.strip()
                    # Set attribute if it exists
                    if hasattr(param, attr_name):
                        # Convert to appropriate type if needed
                        try:
                            existing_value = getattr(param, attr_name)
                            if isinstance(existing_value, bool):
                                setattr(
                                    param,
                                    attr_name,
                                    value.lower() in ("true", "1", "yes"),
                                )
                            elif isinstance(existing_value, int):
                                setattr(param, attr_name, int(value))
                            elif isinstance(existing_value, float):
                                setattr(param, attr_name, float(value))
                            else:
                                setattr(param, attr_name, value)

                            imported_any = True

                        except (ValueError, TypeError):
                            # Just set as string if conversion fails
                            setattr(param, attr_name, value)
                            imported_any = True

            return imported_any

        except Exception as e:
            print(f"Warning: Error importing structured data: {e}")
            return False

    def _write_formatted_xml(self, root: ET.Element, output_path: str):
        """Write XML with proper formatting and indentation."""
        # Create the tree
        tree = ET.ElementTree(root)

        # Add XML declaration and format
        self._indent_xml(root)

        # Write to file
        tree.write(output_path, encoding="utf-8", xml_declaration=True)

    def _indent_xml(self, elem: ET.Element, level: int = 0):
        """Add proper indentation to XML elements."""
        indent = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = indent + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = indent
            for child in elem:
                self._indent_xml(child, level + 1)
            if not child.tail or not child.tail.strip():
                child.tail = indent
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = indent


def export_task_params(task: CData, output_path: str, user_id: str = None) -> bool:
    """
    Convenience function to export task parameters to .params.xml file.

    Args:
        task: Task hierarchy (from .def.xml parsing)
        output_path: Where to save the .params.xml file
        user_id: User ID for the header

    Returns:
        bool: True if successful
    """
    handler = ParamsXmlHandler()
    return handler.export_params_xml(task, output_path, user_id)


def import_task_params(task: CData, params_xml_path: str) -> bool:
    """
    Convenience function to import parameters from .params.xml file into task.

    Args:
        task: Task hierarchy (from .def.xml parsing)
        params_xml_path: Path to .params.xml file

    Returns:
        bool: True if successful
    """
    handler = ParamsXmlHandler()
    return handler.import_params_xml(task, params_xml_path)


# Example usage
if __name__ == "__main__":
    # This would typically be used with a task loaded from .def.xml
    print("Params XML Handler - use export_task_params() and import_task_params()")
