"""
Modern utility functions for working with CData objects in database-backed execution.

These utilities replace legacy container introspection with type-safe CData metadata access.
"""

import logging
from typing import List, Dict, Any, Optional, Type, Callable
from pathlib import Path

from core import CCP4Data
from core.base_object.cdata_file import CDataFile

logger = logging.getLogger(__name__)


def get_file_type_from_class(file_obj: CDataFile) -> str:
    """
    Get the proper file type (MIME type) from a CDataFile using ccp4i2_static_data.py mapping.

    The mapping works as follows:
    1. Get the class name (e.g., "CMtzDataFile")
    2. Strip the leading "C" → "MtzDataFile"
    3. Apply special case mappings (e.g., UnmergedMtzDataFile → UnmergedDataFile)
    4. Find the index in FILETYPES_CLASS
    5. Return FILETYPES_TEXT[index]

    Args:
        file_obj: CDataFile object

    Returns:
        MIME type string (e.g., "application/CCP4-mtz")

    Example:
        >>> file_type = get_file_type_from_class(mtz_file)
        >>> print(file_type)  # "application/CCP4-mtz"
    """
    from ccp4x.db.ccp4i2_static_data import FILETYPES_CLASS, FILETYPES_TEXT

    # Get the class name and strip leading 'C'
    class_name = file_obj.__class__.__name__
    if class_name.startswith('C'):
        class_name = class_name[1:]  # Remove leading 'C'

    # Special case mappings for legacy compatibility
    # CUnmergedMtzDataFile → UnmergedDataFile (legacy ccp4i2 had no separate UnmergedMtzDataFile)
    special_mappings = {
        'UnmergedMtzDataFile': 'UnmergedDataFile',
    }

    if class_name in special_mappings:
        original_name = class_name
        class_name = special_mappings[class_name]
        logger.debug(f"Applied special mapping: {original_name} → {class_name}")

    # Find the index in FILETYPES_CLASS
    try:
        index = FILETYPES_CLASS.index(class_name)
        file_type = FILETYPES_TEXT[index]
        logger.debug(f"Mapped {file_obj.__class__.__name__} → {class_name} → index {index} → {file_type}")
        return file_type
    except (ValueError, IndexError) as e:
        logger.warning(f"Could not map class {file_obj.__class__.__name__} to file type: {e}")
        return "unknown"


def find_all_files(container) -> List[CDataFile]:
    """
    Find all CDataFile objects in a container hierarchy using CData introspection.

    This replaces the legacy find_objects() with lambda predicates by using
    CData's hierarchical object system and childNames() method.

    Args:
        container: Root CData object to search (e.g., plugin.outputData)

    Returns:
        List of all CDataFile objects found in the hierarchy (deduplicated by object id)

    Example:
        >>> output_files = find_all_files(plugin.outputData)
        >>> for file_obj in output_files:
        ...     print(f"Found {file_obj.objectName()}: {file_obj.object_path()}")
    """
    files = []
    visited = set()  # Track visited object IDs to prevent duplicates
    logger.debug(f"[DEBUG find_all_files] Starting search from {container}")
    logger.debug(f"[DEBUG find_all_files] Container type: {type(container)}")

    def traverse(obj, depth=0):
        """Recursively traverse the CData hierarchy using children()"""
        # Skip if already visited (prevents cycles)
        obj_id = id(obj)
        if obj_id in visited:
            return
        visited.add(obj_id)

        indent = "  " * depth
        logger.debug(f"{indent}[DEBUG traverse] obj={obj.objectName() if hasattr(obj, 'objectName') else 'unnamed'}, type={type(obj).__name__}")

        # Check if this object itself is a file
        if isinstance(obj, CDataFile):
            files.append(obj)
            logger.debug(f"{indent}  -> IS A FILE! Added to list")

        # Use standardized children() method for all CData objects
        # This is the canonical way to access children after the refactoring
        if hasattr(obj, 'children'):
            try:
                children = obj.children()
                logger.debug(f"{indent}  children() returned {len(children)} children")
                for child in children:
                    if child is not None:
                        traverse(child, depth + 1)
            except Exception as e:
                logger.debug(f"{indent}  EXCEPTION traversing children: {e}")

    traverse(container)
    return files


def find_objects_by_type(container, target_type: Type) -> List[Any]:
    """
    Find all objects of a specific type in a container hierarchy.

    Args:
        container: Root CData object to search
        target_type: Type to search for (e.g., CPerformanceIndicator)

    Returns:
        List of objects matching the target type

    Example:
        >>> kpis = find_objects_by_type(plugin.outputData, CPerformanceIndicator)
        >>> for kpi in kpis:
        ...     print(f"KPI: {kpi.object_path()}")
    """
    objects = []

    def traverse(obj):
        """Recursively traverse the CData hierarchy"""
        if isinstance(obj, target_type):
            objects.append(obj)

        # Use children() method from HierarchicalObject for proper traversal
        if hasattr(obj, 'children'):
            try:
                for child in obj.children():
                    traverse(child)
            except Exception as e:
                logger.debug(f"Error traversing object: {e}")

    traverse(container)
    return objects


def find_objects_matching(container, predicate: Callable[[Any], bool]) -> List[Any]:
    """
    Find all objects matching a predicate function.

    This is a modern replacement for legacy find_objects() that uses CData's
    hierarchical traversal instead of string-based searches.

    Args:
        container: Root CData object to search
        predicate: Function that returns True for matching objects

    Returns:
        List of objects matching the predicate

    Example:
        >>> # Find all set data files
        >>> set_files = find_objects_matching(
        ...     plugin.outputData,
        ...     lambda obj: isinstance(obj, CDataFile) and obj.isSet()
        ... )
    """
    matches = []

    def traverse(obj):
        if predicate(obj):
            matches.append(obj)

        if hasattr(obj, 'childNames'):
            try:
                child_names = obj.childNames()
                for child_name in child_names:
                    child = getattr(obj, child_name, None)
                    if child is not None:
                        traverse(child)
            except Exception as e:
                logger.debug(f"Error traversing object: {e}")

    traverse(container)
    return matches


def extract_file_metadata(file_obj: CDataFile) -> Dict[str, Any]:
    """
    Extract complete metadata from a CDataFile object using CData's metadata system.

    This replaces legacy string-based qualifier access with type-safe metadata retrieval.

    Args:
        file_obj: CDataFile object to extract metadata from

    Returns:
        Dictionary containing all relevant file metadata

    Example:
        >>> file_info = extract_file_metadata(plugin.outputData.HKLOUT)
        >>> print(f"File type: {file_info['file_type']}")
        >>> print(f"Content flag: {file_info['content_flag']}")
    """
    # Get qualifiers using get_qualifier() method
    metadata = {
        'name': file_obj.objectName(),
        'object_path': file_obj.object_path(),
        'file_type': get_file_type_from_class(file_obj),
        'gui_label': file_obj.get_qualifier('guiLabel', ''),
        'tooltip': file_obj.get_qualifier('toolTip', ''),
        'is_set': file_obj.isSet(),
        'exists': file_obj.exists() if hasattr(file_obj, 'exists') else False,
    }

    # Extract optional attributes with type safety
    if hasattr(file_obj, 'subType'):
        if hasattr(file_obj.subType, 'isSet') and file_obj.subType.isSet():
            metadata['sub_type'] = file_obj.subType.value

    if hasattr(file_obj, 'contentFlag'):
        if hasattr(file_obj.contentFlag, 'isSet') and file_obj.contentFlag.isSet():
            metadata['content_flag'] = file_obj.contentFlag.value

    if hasattr(file_obj, 'annotation'):
        annotation_obj = file_obj.annotation
        if hasattr(annotation_obj, 'isSet') and annotation_obj.isSet():
            metadata['annotation'] = str(annotation_obj)

    if hasattr(file_obj, 'baseName'):
        base_name_obj = file_obj.baseName
        if hasattr(base_name_obj, 'isSet') and base_name_obj.isSet():
            metadata['base_name'] = str(base_name_obj)

    if hasattr(file_obj, 'relPath'):
        rel_path_obj = file_obj.relPath
        if hasattr(rel_path_obj, 'isSet') and rel_path_obj.isSet():
            metadata['rel_path'] = str(rel_path_obj)

    if hasattr(file_obj, 'dbFileId'):
        db_file_id_obj = file_obj.dbFileId
        if hasattr(db_file_id_obj, 'isSet') and db_file_id_obj.isSet():
            metadata['db_file_id'] = str(db_file_id_obj)

    return metadata


def extract_parameter_name(obj) -> str:
    """
    Extract the parameter name from a CData object.

    This replaces legacy regex-based parsing of objectPath() strings.

    Args:
        obj: CData object

    Returns:
        Parameter name (e.g., "HKLOUT")

    Example:
        >>> param_name = extract_parameter_name(plugin.outputData.HKLOUT)
        >>> print(param_name)  # "HKLOUT"
    """
    # Simple approach: use the object's name
    if hasattr(obj, 'name'):
        return obj.name

    # Fallback: parse object_path()
    if hasattr(obj, 'object_path'):
        full_path = obj.object_path()
        parts = full_path.split('.')
        return parts[-1]

    # Last resort: use class name
    return obj.__class__.__name__


def extract_kpi_values(kpi_container) -> Dict[str, Any]:
    """
    Extract key performance indicator values from a CPerformanceIndicator object.

    Uses CData's childNames() to iterate through KPI values with type safety.

    Args:
        kpi_container: CPerformanceIndicator object

    Returns:
        Dictionary of KPI name -> value

    Example:
        >>> kpis = extract_kpi_values(plugin.outputData.PROGRAMXML.performanceIndicator)
        >>> print(f"R-factor: {kpis.get('Rfactor')}")
    """
    values = {}

    # Use children() method from HierarchicalObject for proper traversal
    if not hasattr(kpi_container, 'children'):
        return values

    try:
        for child in kpi_container.children():
            # Get the child's name using objectName()
            param_name = child.objectName() if hasattr(child, 'objectName') else None
            if not param_name:
                continue

            # Extract value based on CData type
            if isinstance(child, CCP4Data.CFloat):
                if child.isSet():
                    values[param_name] = float(child)

            elif isinstance(child, CCP4Data.CInt):
                if child.isSet():
                    values[param_name] = int(child)

            elif isinstance(child, CCP4Data.CString):
                if child.isSet() and len(str(child)) > 0:
                    values[param_name] = str(child)

            elif isinstance(child, CCP4Data.CBoolean):
                if child.isSet():
                    values[param_name] = bool(child)

    except Exception as e:
        logger.exception(f"Error extracting KPI values from {kpi_container.object_path()}: {e}")

    return values


def check_file_attributes(file_obj: CDataFile) -> Dict[str, bool]:
    """
    Check which standard file attributes are present and set on a file object.

    Useful for debugging and understanding file object state.

    Args:
        file_obj: CDataFile object to check

    Returns:
        Dictionary of attribute_name -> is_set

    Example:
        >>> attrs = check_file_attributes(plugin.outputData.HKLOUT)
        >>> if attrs['contentFlag']:
        ...     print(f"Content flag is set: {file_obj.contentFlag.value}")
    """
    standard_attrs = [
        'baseName', 'relPath', 'dbFileId', 'annotation',
        'subType', 'contentFlag', 'project'
    ]

    status = {}
    for attr_name in standard_attrs:
        if hasattr(file_obj, attr_name):
            attr_obj = getattr(file_obj, attr_name)
            status[attr_name] = (
                hasattr(attr_obj, 'isSet') and attr_obj.isSet()
            )
        else:
            status[attr_name] = False

    return status


def get_file_full_path(file_obj: CDataFile, project_directory: Optional[Path] = None) -> Optional[Path]:
    """
    Get the full filesystem path for a file object.

    Args:
        file_obj: CDataFile object
        project_directory: Optional project directory (if not set in file object)

    Returns:
        Full Path to the file, or None if cannot be determined

    Example:
        >>> full_path = get_file_full_path(plugin.outputData.HKLOUT)
        >>> print(f"Output file at: {full_path}")
    """
    try:
        # Try direct path construction
        if hasattr(file_obj, 'relPath') and hasattr(file_obj, 'baseName'):
            rel_path_obj = file_obj.relPath
            base_name_obj = file_obj.baseName

            if (hasattr(rel_path_obj, 'isSet') and rel_path_obj.isSet() and
                hasattr(base_name_obj, 'isSet') and base_name_obj.isSet()):

                rel_path = Path(str(rel_path_obj))
                base_name = str(base_name_obj)

                # If relPath is absolute, use it directly
                if rel_path.is_absolute():
                    return rel_path / base_name

                # Otherwise, need project directory
                if project_directory:
                    return project_directory / rel_path / base_name

        # Fallback: check if file object has __str__ method that returns path
        file_str = str(file_obj)
        if file_str and file_str != file_obj.__class__.__name__:
            return Path(file_str)

    except Exception as e:
        logger.debug(f"Error getting full path for {file_obj.objectName()}: {e}")

    return None


def validate_file_metadata_completeness(file_obj: CDataFile) -> Dict[str, Any]:
    """
    Validate that a file object has all required metadata for database registration.

    Args:
        file_obj: CDataFile object to validate

    Returns:
        Dictionary with 'valid' boolean and 'missing' list of required fields

    Example:
        >>> validation = validate_file_metadata_completeness(file_obj)
        >>> if not validation['valid']:
        ...     print(f"Missing: {validation['missing']}")
    """
    required_fields = ['mimeTypeName']  # At minimum, need file type
    recommended_fields = ['guiLabel', 'baseName']

    missing_required = []
    missing_recommended = []

    for field in required_fields:
        value = file_obj.get_qualifier(field)
        if not value:
            missing_required.append(field)

    for field in recommended_fields:
        # For baseName, check attribute instead of qualifier
        if field == 'baseName':
            if not hasattr(file_obj, 'baseName') or not file_obj.baseName.isSet():
                missing_recommended.append(field)
        else:
            value = file_obj.get_qualifier(field)
            if not value:
                missing_recommended.append(field)

    return {
        'valid': len(missing_required) == 0,
        'missing_required': missing_required,
        'missing_recommended': missing_recommended,
        'has_base_name': hasattr(file_obj, 'baseName') and file_obj.baseName.isSet(),
        'has_rel_path': hasattr(file_obj, 'relPath') and file_obj.relPath.isSet(),
        'file_exists': hasattr(file_obj, 'exists') and file_obj.exists(),
    }


def debug_print_container_structure(container, max_depth: int = 5, current_depth: int = 0):
    """
    Print the hierarchical structure of a container for debugging.

    Args:
        container: CData object to print
        max_depth: Maximum depth to traverse
        current_depth: Current depth (used internally)

    Example:
        >>> debug_print_container_structure(plugin.outputData)
        outputData (CContainer)
          ├─ HKLOUT (CProgramHklDataFile) [SET]
          │  ├─ baseName: "output.mtz" [SET]
          │  ├─ contentFlag: 1 [SET]
          ├─ XYZOUT (CPdbDataFile) [NOT_SET]
    """
    if current_depth >= max_depth:
        return

    indent = "  " * current_depth
    # Get name - prefer 'name' attribute, fall back to objectName() method
    obj_name = "unnamed"
    if hasattr(container, 'name') and container.name:
        obj_name = container.name
    elif hasattr(container, 'objectName'):
        obj_name = container.objectName()
    obj_type = container.__class__.__name__

    # Print this object
    is_set = ""
    if hasattr(container, 'isSet'):
        is_set = " [SET]" if container.isSet() else " [NOT_SET]"

    logger.debug(f"{indent}{obj_name} ({obj_type}){is_set}")

    # Print children
    if hasattr(container, 'childNames'):
        try:
            child_names = container.childNames()
            for i, child_name in enumerate(child_names):
                child = getattr(container, child_name, None)
                if child is not None:
                    prefix = "├─" if i < len(child_names) - 1 else "└─"
                    logger.debug(f"{indent}{prefix} {child_name}")
                    debug_print_container_structure(child, max_depth, current_depth + 1)
        except Exception as e:
            logger.debug(f"{indent}  [Error: {e}]")
