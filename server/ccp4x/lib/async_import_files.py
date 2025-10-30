"""
Async file import operations using modern CData introspection.

This module replaces the legacy import_files.py with async/await operations
and uses the new CData metadata system instead of fragile string-based access.
"""

import asyncio
import logging
import shutil
import uuid
from pathlib import Path
from typing import Optional

from asgiref.sync import sync_to_async

# Import CData utilities for modern introspection
from .cdata_utils import find_all_files, extract_file_metadata

logger = logging.getLogger(f"ccp4x:{__name__}")


async def import_input_files_async(job, plugin, db_handler):
    """
    Import input files for a job using modern async operations.

    This function:
    1. Finds all CDataFile objects in inputData using hierarchical traversal
    2. For files already in database, creates FileUse records
    3. For external files, copies to CCP4_IMPORTED_FILES and registers
    4. Updates container objects with new file locations

    Args:
        job: Django Job model instance
        plugin: CPluginScript instance
        db_handler: AsyncDatabaseHandler instance

    Returns:
        Number of files imported

    Example:
        >>> await import_input_files_async(job, plugin, db_handler)
        3  # Imported 3 files
    """
    files_imported = 0

    # Find all input files using modern hierarchical traversal
    input_files = find_all_files(plugin.inputData)
    logger.info(f"Found {len(input_files)} input file objects")

    for file_obj in input_files:
        try:
            # Check if file already has database ID (previously registered)
            if hasattr(file_obj, 'dbFileId'):
                db_file_id_obj = file_obj.dbFileId
                if hasattr(db_file_id_obj, 'isSet') and db_file_id_obj.isSet():
                    file_uuid_str = str(db_file_id_obj)
                    if len(file_uuid_str.strip()) > 0:
                        # File already in database, just create FileUse
                        await db_handler.register_input_file(
                            job_uuid=job.uuid,
                            file_uuid=uuid.UUID(file_uuid_str),
                            param_name=file_obj.name,
                        )
                        logger.info(f"Registered existing file for {file_obj.name}")
                        files_imported += 1
                        continue

            # Check if file has a baseName set (external file to import)
            if hasattr(file_obj, 'baseName'):
                base_name_obj = file_obj.baseName
                if hasattr(base_name_obj, 'isSet') and base_name_obj.isSet():
                    base_name = str(base_name_obj).strip()
                    if len(base_name) > 0:
                        # Import external file
                        await import_external_file_async(job, file_obj, db_handler)
                        files_imported += 1

        except Exception as e:
            logger.exception(f"Error importing file {file_obj.name}: {e}")

    logger.info(f"Imported {files_imported} input files")
    return files_imported


async def import_external_file_async(job, file_obj, db_handler):
    """
    Import an external file to CCP4_IMPORTED_FILES using modern CData introspection.

    Args:
        job: Django Job model instance
        file_obj: CDataFile object
        db_handler: AsyncDatabaseHandler instance
    """
    # Extract metadata using modern CData system
    metadata = extract_file_metadata(file_obj)

    # Get source file path
    source_path = await get_source_file_path(job, file_obj)
    if source_path is None or not source_path.exists():
        logger.warning(f"Source file does not exist: {source_path}")
        return

    # Determine destination path in CCP4_IMPORTED_FILES
    import_dir = Path(job.project.directory) / "CCP4_IMPORTED_FILES"
    dest_path = import_dir / source_path.name

    # Ensure unique filename
    dest_path = await ensure_unique_path(dest_path)

    # Ensure import directory exists
    await sync_to_async(import_dir.mkdir)(parents=True, exist_ok=True)

    # Copy file asynchronously
    await async_copy_file(source_path, dest_path)
    logger.info(f"Copied {source_path} to {dest_path}")

    # Load file to set content flag
    if hasattr(file_obj, 'loadFile'):
        await sync_to_async(file_obj.loadFile)()

    if hasattr(file_obj, 'setContentFlag'):
        await sync_to_async(file_obj.setContentFlag)(reset=True)

    # Calculate checksum if available
    checksum = None
    if hasattr(file_obj, 'checksum'):
        try:
            checksum = await sync_to_async(file_obj.checksum)()
        except Exception as e:
            logger.debug(f"Could not calculate checksum: {e}")

    # Register in database
    file_record = await db_handler.register_imported_file(
        job_uuid=job.uuid,
        file_path=dest_path,
        file_type=metadata['file_type'],
        param_name=metadata['name'],
        source_path=source_path,
        annotation=metadata.get('annotation', f"Imported from {source_path.name}"),
        checksum=checksum,
    )

    # Update container to reflect new location
    if hasattr(file_obj, 'dbFileId'):
        file_obj.dbFileId.set(str(file_record.uuid))

    if hasattr(file_obj, 'relPath'):
        file_obj.relPath.set("CCP4_IMPORTED_FILES")

    if hasattr(file_obj, 'baseName'):
        file_obj.baseName.set(dest_path.name)

    if hasattr(file_obj, 'project'):
        file_obj.project.set(str(job.project.uuid))

    # Reload file with new location
    if hasattr(file_obj, 'loadFile'):
        await sync_to_async(file_obj.loadFile)()

    if hasattr(file_obj, 'setContentFlag'):
        await sync_to_async(file_obj.setContentFlag)(reset=True)

    logger.info(f"Successfully imported {file_obj.name}")


async def get_source_file_path(job, file_obj) -> Optional[Path]:
    """
    Get the source file path from a CDataFile object.

    Args:
        job: Django Job model instance
        file_obj: CDataFile object

    Returns:
        Path to source file, or None if cannot be determined
    """
    base_name = None
    rel_path = None

    # Extract baseName
    if hasattr(file_obj, 'baseName'):
        base_name_obj = file_obj.baseName
        if hasattr(base_name_obj, 'isSet') and base_name_obj.isSet():
            base_name = str(base_name_obj).strip()

    # Extract relPath
    if hasattr(file_obj, 'relPath'):
        rel_path_obj = file_obj.relPath
        if hasattr(rel_path_obj, 'isSet') and rel_path_obj.isSet():
            rel_path = str(rel_path_obj).strip()

    if not base_name:
        return None

    # Try different path constructions
    if rel_path:
        # Try relPath / baseName
        source_path = Path(rel_path) / base_name
        if source_path.exists():
            return source_path

        # Try project_dir / relPath / baseName
        source_path = Path(job.project.directory) / rel_path / base_name
        if source_path.exists():
            return source_path

    # Try just baseName (current directory or absolute)
    source_path = Path(base_name)
    if source_path.exists():
        return source_path

    return None


async def ensure_unique_path(dest_path: Path) -> Path:
    """
    Ensure destination path is unique by appending _1, _2, etc if needed.

    Args:
        dest_path: Desired destination path

    Returns:
        Unique path that doesn't exist
    """
    def path_exists(p):
        return p.exists()

    if not await sync_to_async(path_exists)(dest_path):
        return dest_path

    # Path exists, find unique name
    counter = 1
    while True:
        stem = dest_path.stem
        suffix = dest_path.suffix
        parent = dest_path.parent

        new_path = parent / f"{stem}_{counter}{suffix}"
        if not await sync_to_async(path_exists)(new_path):
            return new_path

        counter += 1

        # Safety check
        if counter > 1000:
            raise RuntimeError(f"Could not find unique path for {dest_path}")


async def async_copy_file(source: Path, dest: Path):
    """
    Copy a file asynchronously using asyncio.

    Args:
        source: Source file path
        dest: Destination file path
    """
    # Use sync_to_async to avoid blocking
    await sync_to_async(shutil.copyfile)(str(source), str(dest))


async def save_params_after_import(plugin, job):
    """
    Save plugin parameters after importing files.

    This updates the job's parameter file to reflect the new file locations.

    Args:
        plugin: CPluginScript instance
        job: Django Job model instance
    """
    # Import save_params_for_job from legacy utilities
    from .job_utils.save_params_for_job import save_params_for_job

    # Run synchronously (it's a quick operation)
    await sync_to_async(save_params_for_job)(plugin, job, mode="JOB_INPUT")
    logger.info(f"Saved parameters for job {job.number}")


# Legacy compatibility wrapper
async def import_files_async_compat(job, plugin):
    """
    Legacy compatibility wrapper that doesn't require db_handler.

    This is for gradual migration from the old import_files.py.

    Args:
        job: Django Job model instance
        plugin: CPluginScript instance

    Returns:
        Updated plugin instance
    """
    from ..db.async_db_handler import AsyncDatabaseHandler

    # Create temporary handler
    handler = AsyncDatabaseHandler(project_uuid=job.project.uuid)

    # Import files
    await import_input_files_async(job, plugin, handler)

    # Save parameters
    await save_params_after_import(plugin, job)

    return plugin
