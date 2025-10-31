"""
Parameter setting utilities using CPluginScript + dbHandler architecture.

Provides functions to set job parameters with proper type handling and persistence.
Uses CPluginScript to ensure proper file handling, database synchronization,
and validation.
"""

import logging
import json
from typing import Union, Any, Dict
from pathlib import Path

from ccp4x.db import models
from ccp4x.lib.response import Result
from ccp4x.lib.utils.plugins.plugin_context import get_plugin_with_context
from ccp4x.lib.job_utils.set_parameter import set_parameter_container

logger = logging.getLogger(__name__)


def set_parameter(
    job: models.Job,
    object_path: str,
    value: Union[str, int, float, bool, dict, None]
) -> Result[Dict[str, Any]]:
    """
    Set a parameter value using CPluginScript + dbHandler architecture.

    This function uses CPluginScript to ensure:
    - Proper file handling (CDataFile.setFullPath() with DB awareness)
    - Database synchronization (dbHandler.updateJobStatus())
    - Correct object hierarchy
    - Validation support

    Args:
        job: Job model instance
        object_path: Path to the parameter
                    Examples:
                    - "inputData.XYZIN" - Sets entire file object
                    - "inputData.XYZIN.baseName" - Sets just filename
                    - "container.NCYCLES" - Sets control parameter
        value: New value for the parameter

    Returns:
        Result[Dict] with parameter info or error

    Example:
        >>> # Set file parameter (creates/updates Django File record)
        >>> result = set_parameter(job, "inputData.XYZIN", "/path/to/file.pdb")
        >>> if result.success:
        ...     print(f"File path: {result.data['file_path']}")
        ...     print(f"DB File ID: {result.data.get('db_file_id')}")
        >>>
        >>> # Set annotation
        >>> result = set_parameter(job, "inputData.XYZIN.annotation", "My structure")
        >>>
        >>> # Set control parameter
        >>> result = set_parameter(job, "container.NCYCLES", 10)
    """
    # Get plugin with database context
    plugin_result = get_plugin_with_context(job)
    if not plugin_result.success:
        return Result.fail(
            f"Failed to load plugin: {plugin_result.error}",
            details=plugin_result.error_details
        )

    plugin = plugin_result.data

    try:
        # Set parameter through plugin's container
        # This ensures proper file handling, validation, and hierarchy
        logger.debug(
            "Setting parameter %s = %s on job %s (task: %s)",
            object_path, value, job.uuid, job.task_name
        )

        set_parameter_container(plugin.container, object_path, value)

        # Save parameters to XML
        params_file = job.directory / "params.xml"
        logger.debug("Saving parameters to %s", params_file)
        plugin.container.saveDataToXml(str(params_file))

        # Update database via dbHandler (if available)
        if plugin._dbHandler:
            logger.debug("Updating database via dbHandler for job %s", job.uuid)
            plugin._dbHandler.updateJobStatus(
                jobId=str(job.uuid),
                container=plugin.container
            )

        # Get the actual object for return info
        obj = plugin.container
        parts = object_path.split('.')
        for part in parts:
            if hasattr(obj, part):
                obj = getattr(obj, part)
            else:
                obj = None
                break

        # Build result data
        result_data = {
            "path": object_path,
            "value": value,
            "object_type": type(obj).__name__ if obj else "Unknown",
        }

        # Add file-specific info if it's a CDataFile
        if obj and hasattr(obj, 'getFullPath'):
            full_path = obj.getFullPath()
            if full_path:
                result_data["file_path"] = full_path

            # Get dbFileId if available
            if hasattr(obj, 'dbFileId'):
                db_file_attr = getattr(obj, 'dbFileId')
                if hasattr(db_file_attr, 'value') and db_file_attr.value:
                    result_data["db_file_id"] = str(db_file_attr.value)

            # Get baseName if available
            if hasattr(obj, 'baseName'):
                base_name_attr = getattr(obj, 'baseName')
                if hasattr(base_name_attr, 'value'):
                    result_data["base_name"] = str(base_name_attr.value)
                else:
                    result_data["base_name"] = str(base_name_attr)

        logger.info(
            "Successfully set parameter %s on job %s: %s",
            object_path, job.uuid, result_data.get('file_path', value)
        )
        return Result.ok(result_data)

    except AttributeError as e:
        logger.error(
            "Parameter path '%s' not found on job %s: %s",
            object_path, job.uuid, str(e)
        )
        return Result.fail(
            f"Parameter path '{object_path}' not found",
            details={
                "job_id": str(job.uuid),
                "task_name": job.task_name,
                "object_path": object_path,
                "error": str(e)
            }
        )

    except Exception as e:
        logger.exception(
            "Failed to set parameter %s on job %s",
            object_path, job.uuid
        )
        return Result.fail(
            f"Error setting parameter: {str(e)}",
            details={
                "job_id": str(job.uuid),
                "task_name": job.task_name,
                "object_path": object_path,
                "value": value,
                "error_type": type(e).__name__
            }
        )
