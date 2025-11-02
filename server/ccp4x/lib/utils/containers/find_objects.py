import logging
import re
from xml.etree import ElementTree as ET
from core import CCP4Container
from core import CCP4ModelData
from core import CCP4Data
from core.base_object.cdata import CData
from core import CCP4File
from core.CCP4Container import CContainer
from core.base_object.fundamental_types import CList

logger = logging.getLogger(f"ccp4x:{__name__}")


def find_objects(within, func, multiple=False, growing_list=None, growing_name=None):
    """
    Recursively searches for objects within a container or list that match a given condition.

    Args:
        within (CCP4Container.CContainer or list): The container or list to search within.
        func (callable): A function that takes an object and returns True if the object matches the condition.
        multiple (bool, optional): If True, find all matching objects. If False, stop after finding the first match. Defaults to True.
        growing_list (list, optional): A list to accumulate the matching objects. If None, a new list is created. Defaults to None.

    Returns:
        list: A list of objects that match the given condition.
    """
    if growing_list is None:
        growing_list = []
    original_length = len(growing_list)

    if growing_name is None:
        growing_name = within.objectPath()

    search_domain = (
        within._value
        if isinstance(within, (CCP4Data.CList, CList))
        else within.CONTENTS
    )
    for ichild, child_ref in enumerate(search_domain):
        child = (
            child_ref
            if isinstance(within, (CCP4Data.CList, CList))
            else getattr(within, child_ref, None)
        )
        current_name = (
            f"{growing_name}[{ichild}]"
            if isinstance(within._value, (CCP4Data.CList, CList, list))
            else f"{growing_name}.{child.objectName()}"
        )

        if func(child):
            growing_list.append(child)
            if not multiple:
                logger.debug("Match for %s", child.objectName())
                return growing_list
        elif isinstance(child, (CCP4Data.CList, CList, list)) or hasattr(
            child, "CONTENTS"
        ):
            find_objects(child, func, multiple, growing_list, current_name)
            if not multiple and len(growing_list) > original_length:
                return growing_list

    return growing_list


def find_object_by_path(base_element: CData, object_path: str):
    """
    Find a descendent CData item from a root element given a dot-separated path.

    This is a thin wrapper around built-in CData hierarchy traversal that handles
    the legacy path format where the first element is the task/plugin name.

    Args:
        base_element: The container to search in (usually plugin.container)
        object_path: Dot-separated path (e.g., "prosmart_refmac.controlParameters.NCYCLES")
                    The first element (task name) is skipped since base_element is already
                    the container, not the plugin.

    Returns:
        The found CData object

    Raises:
        AttributeError: If the path is not found

    Example:
        >>> container = plugin.container  # name="container"
        >>> obj = find_object_by_path(container, "prosmart_refmac.controlParameters.NCYCLES")
        # Skips "prosmart_refmac", then uses getattr() and .find() to navigate:
        # container.controlParameters.NCYCLES

    Implementation:
        Uses getattr() first (which triggers CContainer.__getattr__ to search children),
        then falls back to .find() (which does depth-first recursive search).
    """
    path_elements = object_path.split(".")

    # Skip the first element (task/plugin name) since base_element is the container
    # Legacy paths are like: "prosmart_refmac.controlParameters.NCYCLES"
    # But base_element is already plugin.container, so we search for "controlParameters.NCYCLES"
    if len(path_elements) > 1:
        path_to_search = path_elements[1:]
    else:
        # Single element path - use as-is
        path_to_search = [object_path]

    # Navigate the path using built-in hierarchy traversal methods
    current = base_element
    for segment in path_to_search:
        # Try getattr() first - triggers CContainer.__getattr__ which searches children
        next_obj = getattr(current, segment, None)

        # Fall back to .find() - does depth-first recursive search through hierarchy
        if next_obj is None and hasattr(current, 'find'):
            next_obj = current.find(segment)

        if next_obj is None:
            raise AttributeError(f"Element '{segment}' not found in '{current}'")

        current = next_obj

    return current
