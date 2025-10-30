"""
Async file gleaning operations using modern CData introspection.

This module replaces the legacy glean_job_files.py with async/await operations
and uses the new CData metadata system for robust file extraction.
"""

import logging
import uuid
from pathlib import Path
from typing import List, Dict, Any

from asgiref.sync import sync_to_async

# Import CData utilities for modern introspection
from .cdata_utils import (
    find_all_files,
    find_objects_by_type,
    extract_file_metadata,
    extract_kpi_values,
)

logger = logging.getLogger(f"ccp4x:{__name__}")


async def glean_output_files_async(job, container, db_handler, unset_missing=True) -> List:
    """
    Glean output files from a container using modern async operations.

    This function:
    1. Finds all CDataFile objects in container using hierarchical traversal
    2. Extracts metadata using CData's metadata system
    3. Registers files in database
    4. Links files back to container objects
    5. Optionally unsets missing files

    Args:
        job: Django Job model instance
        container: CData container (typically plugin.outputData)
        db_handler: AsyncDatabaseHandler instance
        unset_missing: If True, unset file objects that don't exist on disk

    Returns:
        List of created File model instances

    Example:
        >>> files = await glean_output_files_async(job, plugin.outputData, handler)
        >>> print(f"Gleaned {len(files)} output files")
    """
    files_created = []

    # Find all output files using modern hierarchical traversal
    output_files = find_all_files(container)
    logger.info(f"Found {len(output_files)} output file objects")

    for file_obj in output_files:
        try:
            # Check if file exists on disk
            file_exists = hasattr(file_obj, 'exists') and file_obj.exists()

            if not file_exists:
                if unset_missing and hasattr(file_obj, 'unSet'):
                    file_obj.unSet()
                    logger.debug(f"Unset missing file: {file_obj.name}")
                else:
                    logger.debug(f"Skipping non-existent file: {file_obj.name}")
                continue

            # Extract metadata using modern CData system
            metadata = extract_file_metadata(file_obj)

            # Validate file has required metadata
            if metadata['file_type'] == 'unknown':
                logger.warning(
                    f"File {file_obj.name} has unknown type - "
                    f"class {file_obj.__class__.__name__} needs mimeTypeName qualifier"
                )
                # Try to continue with 'unknown' type
                # continue

            # Get full file path
            file_path = Path(str(file_obj))

            # Register file in database
            file_record = await db_handler.register_output_file(
                job_uuid=job.uuid,
                file_path=file_path,
                file_type=metadata['file_type'],
                param_name=metadata['name'],
                content_flag=metadata.get('content_flag'),
                sub_type=metadata.get('sub_type'),
                annotation=metadata.get('annotation', metadata.get('gui_label', '')),
            )

            # Link back to container
            if hasattr(file_obj, 'dbFileId'):
                file_obj.dbFileId.set(str(file_record.uuid))

            files_created.append(file_record)
            logger.info(f"Gleaned output file: {metadata['name']} -> {file_path.name}")

        except Exception as e:
            logger.exception(f"Error gleaning file {file_obj.name}: {e}")

    logger.info(f"Successfully gleaned {len(files_created)} output files")
    return files_created


async def glean_input_file_uses_async(job, container, db_handler) -> int:
    """
    Create FileUse records for input files.

    This tracks which input files were actually used by the job.

    Args:
        job: Django Job model instance
        container: CData container (typically plugin.inputData)
        db_handler: AsyncDatabaseHandler instance

    Returns:
        Number of FileUse records created
    """
    uses_created = 0

    # Find all input files
    input_files = find_all_files(container)
    logger.info(f"Found {len(input_files)} input file objects")

    for file_obj in input_files:
        try:
            # Check if file has database ID and is set
            if not hasattr(file_obj, 'dbFileId'):
                continue

            db_file_id_obj = file_obj.dbFileId
            if not hasattr(db_file_id_obj, 'isSet') or not db_file_id_obj.isSet():
                continue

            file_uuid_str = str(db_file_id_obj).strip()
            if len(file_uuid_str) == 0:
                continue

            # Check if file actually exists and is set
            if not hasattr(file_obj, 'isSet') or not file_obj.isSet():
                logger.debug(f"Skipping unset file: {file_obj.name}")
                continue

            file_exists = hasattr(file_obj, 'exists') and file_obj.exists()
            if not file_exists:
                logger.debug(f"Skipping non-existent input file: {file_obj.name}")
                continue

            # Register FileUse
            await db_handler.register_input_file(
                job_uuid=job.uuid,
                file_uuid=uuid.UUID(file_uuid_str),
                param_name=file_obj.name,
            )
            uses_created += 1
            logger.info(f"Registered input file use: {file_obj.name}")

        except Exception as e:
            logger.exception(f"Error registering input file use {file_obj.name}: {e}")

    logger.info(f"Created {uses_created} input file use records")
    return uses_created


async def glean_performance_indicators_async(job, container, db_handler) -> int:
    """
    Extract performance indicators (KPIs) from container using modern CData introspection.

    Args:
        job: Django Job model instance
        container: CData container (typically plugin.outputData)
        db_handler: AsyncDatabaseHandler instance

    Returns:
        Number of KPI values registered
    """
    # Import CPerformanceIndicator type
    try:
        from core.CCP4PerformanceData import CPerformanceIndicator
    except ImportError:
        try:
            from core.CCP4PerformanceData import CPerformanceIndicator
        except ImportError:
            logger.warning("Could not import CPerformanceIndicator - skipping KPI gleaning")
            return 0

    kpi_count = 0

    # Find all performance indicator objects
    kpis = find_objects_by_type(container, CPerformanceIndicator)
    logger.info(f"Found {len(kpis)} performance indicator objects")

    for kpi in kpis:
        try:
            # Extract all KPI values using modern utility
            values = extract_kpi_values(kpi)

            # Register each value in database
            for key, value in values.items():
                try:
                    if isinstance(value, (int, float)):
                        await db_handler.register_job_float_value(
                            job_uuid=job.uuid,
                            key=key,
                            value=float(value),
                        )
                        kpi_count += 1
                        logger.debug(f"Registered float KPI: {key} = {value}")

                    elif isinstance(value, str) and len(value) > 0:
                        await db_handler.register_job_char_value(
                            job_uuid=job.uuid,
                            key=key,
                            value=value,
                        )
                        kpi_count += 1
                        logger.debug(f"Registered string KPI: {key} = {value}")

                except Exception as e:
                    logger.exception(f"Error registering KPI {key}: {e}")

        except Exception as e:
            kpi_path = kpi.object_path() if hasattr(kpi, 'object_path') else str(kpi)
            logger.exception(f"Error gleaning KPIs from {kpi_path}: {e}")

    logger.info(f"Successfully gleaned {kpi_count} performance indicators")
    return kpi_count


async def glean_all_async(
    job,
    container,
    db_handler,
    glean_outputs: bool = True,
    glean_inputs: bool = True,
    glean_kpis: bool = True,
) -> Dict[str, Any]:
    """
    Glean all information from a container (files, file uses, KPIs).

    This is a convenience function that runs all gleaning operations.

    Args:
        job: Django Job model instance
        container: CPluginScript instance (has inputData and outputData)
        db_handler: AsyncDatabaseHandler instance
        glean_outputs: Whether to glean output files
        glean_inputs: Whether to glean input file uses
        glean_kpis: Whether to glean performance indicators

    Returns:
        Dictionary with counts of gleaned items

    Example:
        >>> results = await glean_all_async(job, plugin, handler)
        >>> print(f"Gleaned {results['output_files']} files, {results['kpis']} KPIs")
    """
    results = {
        'output_files': 0,
        'input_uses': 0,
        'kpis': 0,
    }

    # Glean output files
    if glean_outputs and hasattr(container, 'outputData'):
        files = await glean_output_files_async(
            job, container.outputData, db_handler
        )
        results['output_files'] = len(files)

    # Glean input file uses
    if glean_inputs and hasattr(container, 'inputData'):
        uses = await glean_input_file_uses_async(
            job, container.inputData, db_handler
        )
        results['input_uses'] = uses

    # Glean performance indicators
    if glean_kpis and hasattr(container, 'outputData'):
        kpis = await glean_performance_indicators_async(
            job, container.outputData, db_handler
        )
        results['kpis'] = kpis

    logger.info(
        f"Gleaning complete: {results['output_files']} files, "
        f"{results['input_uses']} input uses, {results['kpis']} KPIs"
    )

    return results


async def save_params_after_gleaning(plugin, job):
    """
    Save plugin parameters after gleaning files.

    This updates the job's parameter file to reflect the database file IDs.

    Args:
        plugin: CPluginScript instance
        job: Django Job model instance
    """
    # Import save_params_for_job from legacy utilities
    from .job_utils.save_params_for_job import save_params_for_job

    # Run synchronously (it's a quick operation)
    await sync_to_async(save_params_for_job)(plugin, job, mode="PARAMS")
    logger.info(f"Saved parameters for job {job.number}")


# Legacy compatibility wrapper
async def glean_job_files_async_compat(job_id: str, container, role_list=[0, 1]) -> None:
    """
    Legacy compatibility wrapper that matches old glean_job_files signature.

    This is for gradual migration from the old glean_job_files.py.

    Args:
        job_id: Job UUID as string
        container: CPluginScript instance or container
        role_list: List of roles to glean (0=OUT, 1=IN)
    """
    from ..db.async_db_handler import AsyncDatabaseHandler
    from ..db import models

    # Get job from database
    job = await sync_to_async(models.Job.objects.get)(uuid=uuid.UUID(job_id))

    # Create temporary handler
    handler = AsyncDatabaseHandler(project_uuid=job.project.uuid)

    # Glean based on role list
    if 0 in role_list:  # FILE_ROLE_OUT
        await glean_output_files_async(job, container.outputData, handler)

    if 1 in role_list:  # FILE_ROLE_IN
        await glean_input_file_uses_async(job, container.inputData, handler)

    # Always glean KPIs if we're gleaning outputs
    if 0 in role_list:
        await glean_performance_indicators_async(job, container.outputData, handler)
