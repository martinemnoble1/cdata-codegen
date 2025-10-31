import logging
from xml.etree import ElementTree as ET
from core import CCP4Container
from core import CCP4ErrorHandling


logger = logging.getLogger(f"ccp4x:{__name__}")

# Severity level to text mapping
SEVERITY_TEXT = {
    CCP4ErrorHandling.SEVERITY_OK: "OK",
    CCP4ErrorHandling.SEVERITY_UNDEFINED: "UNDEFINED",
    CCP4ErrorHandling.SEVERITY_WARNING: "WARNING",
    CCP4ErrorHandling.SEVERITY_UNDEFINED_ERROR: "UNDEFINED_ERROR",
    CCP4ErrorHandling.SEVERITY_ERROR: "ERROR"
}


def getEtree(error_report: CCP4ErrorHandling.CErrorReport):
    """Convert CErrorReport to XML ElementTree.

    Args:
        error_report: CErrorReport instance containing validation errors

    Returns:
        ET.Element: XML tree with error reports
    """
    element = ET.Element("errorReportList")

    # Get errors using public API (getErrors() returns list of error dicts)
    for item in error_report.getErrors():
        try:
            ele = ET.Element("errorReport")

            # className - in new API, item["class"] is already the class name string
            e = ET.Element("className")
            class_name = item["class"]
            # Handle both class objects and string class names
            e.text = class_name.__name__ if hasattr(class_name, '__name__') else str(class_name)
            ele.append(e)

            # code
            e = ET.Element("code")
            e.text = str(item["code"])
            ele.append(e)

            # description - in new API, details field contains the description
            e = ET.Element("description")
            e.text = item["details"]
            ele.append(e)

            # severity - in new API, severity is directly in the item dict
            e = ET.Element("severity")
            severity = item["severity"]
            e.text = SEVERITY_TEXT.get(severity, f"UNKNOWN({severity})")
            ele.append(e)

            # name (object name) - new field in new API
            if item.get("name"):
                e = ET.Element("objectName")
                e.text = str(item["name"])
                ele.append(e)

            # time (if present)
            if item.get("time", None) is not None:
                e = ET.Element("time")
                e.text = str(item["time"])
                ele.append(e)

            # stack (if present)
            if item.get("stack", None) is not None:
                e = ET.Element("stack")
                stack = item["stack"]
                if isinstance(stack, list):
                    text = "".join(stack)
                else:
                    text = str(stack)
                e.text = text
                ele.append(e)

            element.append(ele)

        except Exception as e:
            logger.exception("Error processing error report item: %s", e)

    return element


def validate_container(
    container: CCP4Container.CContainer,
) -> ET.Element:
    error_report: CCP4ErrorHandling.CErrorReport = container.validity()
    error_etree: ET.Element = getEtree(error_report)

    # Remove stacks (too nasty to live with)
    namespace = ""
    error_reports = error_etree.findall(".//{0}errorReport".format(namespace))
    for error_report in error_reports:
        stack_children = error_report.findall("./stack")
        for stack_child in stack_children:
            error_report.remove(stack_child)
        description_children = error_report.findall("./description")

        for description_child in description_children:
            description_text = description_child.text
            broken_text = description_text.split(":")
            if len(broken_text) > 1:
                object_element = ET.Element("objectPath")
                object_element.text = broken_text[0].strip()
                error_report.append(object_element)

    ET.indent(error_etree, " ")
    # print(error_log)
    return error_etree
