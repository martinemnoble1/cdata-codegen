"""
Modern async database handler for CCP4i2 plugin execution tracking.

This handler provides a clean API for integrating CPluginScript with the Django database,
using modern Python patterns like async/await, context managers, and type hints.
"""

import datetime
import logging
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager

from asgiref.sync import sync_to_async
from django.db import transaction

from core.CCP4PluginScript import CPluginScript
# DISABLED: Old ccp4i2 import
# from ccp4i2.dbapi import CCP4DbApi

from . import models


logger = logging.getLogger(f"ccp4x:{__name__}")


class AsyncDatabaseHandler:
    """
    Modern async database handler for CCP4i2 plugin execution.

    This handler provides:
    - Async/await interface for non-blocking database operations
    - Automatic job lifecycle tracking
    - Signal integration for status updates
    - Context manager support for transactions
    - Type-safe API with modern Python patterns

    Example Usage:
        db_handler = AsyncDatabaseHandler(project_uuid)

        # Create job in database
        job = await db_handler.create_job(
            task_name="ctruncate",
            title="Convert intensities to amplitudes",
            parent_job_uuid=parent_uuid
        )

        # Track job lifecycle automatically
        async with db_handler.track_job(plugin_instance):
            await plugin_instance.execute()

        # Job status, files, and metadata are automatically updated
    """

    def __init__(self, project_uuid: uuid.UUID):
        """
        Initialize database handler for a specific project.

        Args:
            project_uuid: UUID of the project to track jobs for
        """
        self.project_uuid = project_uuid
        self._project: Optional[models.Project] = None

    async def get_project(self) -> models.Project:
        """Get the project instance, cached after first retrieval."""
        if self._project is None:
            self._project = await sync_to_async(
                models.Project.objects.get
            )(uuid=self.project_uuid)
        return self._project

    async def create_job(
        self,
        task_name: str,
        title: Optional[str] = None,
        parent_job_uuid: Optional[uuid.UUID] = None,
        job_number: Optional[str] = None,
    ) -> models.Job:
        """
        Create a new job in the database.

        Args:
            task_name: Name of the plugin/task (e.g., "ctruncate")
            title: Human-readable job title
            parent_job_uuid: UUID of parent job for nested execution
            job_number: Optional explicit job number (e.g., "1" or "1.2")

        Returns:
            Created Job instance

        Example:
            job = await handler.create_job(
                task_name="refmac",
                title="Refinement round 1",
                parent_job_uuid=parent.uuid
            )
        """
        project = await self.get_project()

        @sync_to_async
        def _create_job():
            with transaction.atomic():
                # Determine parent job if specified
                parent_job = None
                if parent_job_uuid:
                    parent_job = models.Job.objects.get(uuid=parent_job_uuid)

                # Auto-generate job number if not provided
                if job_number is None:
                    if parent_job:
                        # Get highest child number for this parent
                        siblings = models.Job.objects.filter(parent=parent_job)
                        if siblings.exists():
                            max_num = max(
                                int(s.number.split('.')[-1])
                                for s in siblings
                            )
                            child_num = max_num + 1
                        else:
                            child_num = 1
                        computed_number = f"{parent_job.number}.{child_num}"
                    else:
                        # Top-level job
                        project.last_job_number += 1
                        project.save()
                        computed_number = str(project.last_job_number)
                else:
                    computed_number = job_number

                # Create the job
                job = models.Job.objects.create(
                    project=project,
                    parent=parent_job,
                    number=computed_number,
                    title=title or task_name,
                    task_name=task_name,
                    status=models.Job.Status.PENDING,
                )

                return job

        return await _create_job()

    async def update_job_status(
        self,
        job_uuid: uuid.UUID,
        status: int,
        finish_time: Optional[datetime.datetime] = None,
    ) -> None:
        """
        Update job status in the database.

        Args:
            job_uuid: UUID of job to update
            status: New status (models.Job.Status enum value)
            finish_time: Optional finish time (auto-set for FINISHED status)
        """
        @sync_to_async
        def _update():
            with transaction.atomic():
                job = models.Job.objects.get(uuid=job_uuid)
                job.status = status

                if status == models.Job.Status.FINISHED:
                    job.finish_time = finish_time or datetime.datetime.now()

                job.save()

        await _update()

    async def register_output_file(
        self,
        job_uuid: uuid.UUID,
        file_path: Path,
        file_type: str,
        param_name: str,
        content_flag: Optional[int] = None,
        sub_type: Optional[int] = None,
        annotation: str = "",
    ) -> models.File:
        """
        Register an output file for a job.

        Args:
            job_uuid: UUID of the job that created this file
            file_path: Path to the file (relative to job directory)
            file_type: File type name (e.g., "hklin", "xyzout")
            param_name: Parameter name in plugin (e.g., "HKLOUT")
            content_flag: Content flag from CCP4 data objects
            sub_type: Sub-type from CCP4 data objects
            annotation: Human-readable description

        Returns:
            Created File instance
        """
        @sync_to_async
        def _register():
            with transaction.atomic():
                job = models.Job.objects.get(uuid=job_uuid)

                # Get or create file type
                file_type_obj, _ = models.FileType.objects.get_or_create(
                    name=file_type,
                    defaults={"description": f"File type: {file_type}"}
                )

                # Create file record
                file_obj = models.File.objects.create(
                    name=file_path.name,
                    directory=models.File.Directory.JOB_DIR,
                    type=file_type_obj,
                    sub_type=sub_type,
                    content=content_flag,
                    annotation=annotation,
                    job=job,
                    job_param_name=param_name,
                )

                # Create FileUse record
                models.FileUse.objects.create(
                    file=file_obj,
                    job=job,
                    role=models.FileUse.Role.OUT,
                    job_param_name=param_name,
                )

                return file_obj

        return await _register()

    async def register_input_file(
        self,
        job_uuid: uuid.UUID,
        file_uuid: uuid.UUID,
        param_name: str,
    ) -> None:
        """
        Register that a job uses an existing file as input.

        Args:
            job_uuid: UUID of the job using this file
            file_uuid: UUID of the file being used
            param_name: Parameter name in plugin (e.g., "HKLIN")
        """
        @sync_to_async
        def _register():
            with transaction.atomic():
                job = models.Job.objects.get(uuid=job_uuid)
                file_obj = models.File.objects.get(uuid=file_uuid)

                # Check if FileUse already exists
                if not models.FileUse.objects.filter(
                    file=file_obj,
                    job=job,
                    role=models.FileUse.Role.IN,
                    job_param_name=param_name,
                ).exists():
                    models.FileUse.objects.create(
                        file=file_obj,
                        job=job,
                        role=models.FileUse.Role.IN,
                        job_param_name=param_name,
                    )

        await _register()

    async def register_imported_file(
        self,
        job_uuid: uuid.UUID,
        file_path: Path,
        file_type: str,
        param_name: str,
        source_path: Path,
        annotation: str = "",
        checksum: Optional[str] = None,
    ) -> models.File:
        """
        Register an imported file that was copied to CCP4_IMPORTED_FILES.

        Args:
            job_uuid: UUID of the job that imported this file
            file_path: Path to the imported file in CCP4_IMPORTED_FILES
            file_type: File type name (e.g., "application/CCP4-mtz")
            param_name: Parameter name in plugin
            source_path: Original source path before import
            annotation: Human-readable description
            checksum: Optional file checksum

        Returns:
            Created File instance
        """
        @sync_to_async
        def _register():
            with transaction.atomic():
                job = models.Job.objects.get(uuid=job_uuid)

                # Get or create file type
                file_type_obj, _ = models.FileType.objects.get_or_create(
                    name=file_type,
                    defaults={"description": f"File type: {file_type}"}
                )

                # Create file record
                file_obj = models.File.objects.create(
                    name=file_path.name,
                    directory=models.File.Directory.IMPORT_DIR,
                    type=file_type_obj,
                    annotation=annotation,
                    job=job,
                    job_param_name=param_name,
                )

                # Create FileImport record
                models.FileImport.objects.create(
                    file=file_obj,
                    name=str(source_path),
                    checksum=checksum or "",
                    last_modified=datetime.datetime.now(),
                )

                # Create FileUse record
                models.FileUse.objects.create(
                    file=file_obj,
                    job=job,
                    role=models.FileUse.Role.IN,
                    job_param_name=param_name,
                )

                return file_obj

        return await _register()

    async def register_job_float_value(
        self,
        job_uuid: uuid.UUID,
        key: str,
        value: float,
        description: Optional[str] = None,
    ) -> None:
        """
        Register a float KPI value for a job.

        Args:
            job_uuid: UUID of the job
            key: KPI key name
            value: Float value
            description: Optional description of the KPI
        """
        @sync_to_async
        def _register():
            with transaction.atomic():
                job = models.Job.objects.get(uuid=job_uuid)

                # Get or create key
                job_value_key, _ = models.JobValueKey.objects.get_or_create(
                    name=key,
                    defaults={"description": description or key}
                )

                # Create or update value
                models.JobFloatValue.objects.update_or_create(
                    job=job,
                    key=job_value_key,
                    defaults={"value": value}
                )

        await _register()

    async def register_job_char_value(
        self,
        job_uuid: uuid.UUID,
        key: str,
        value: str,
        description: Optional[str] = None,
    ) -> None:
        """
        Register a string KPI value for a job.

        Args:
            job_uuid: UUID of the job
            key: KPI key name
            value: String value
            description: Optional description of the KPI
        """
        @sync_to_async
        def _register():
            with transaction.atomic():
                job = models.Job.objects.get(uuid=job_uuid)

                # Get or create key
                job_value_key, _ = models.JobValueKey.objects.get_or_create(
                    name=key,
                    defaults={"description": description or key}
                )

                # Create or update value
                models.JobCharValue.objects.update_or_create(
                    job=job,
                    key=job_value_key,
                    defaults={"value": value}
                )

        await _register()

    async def glean_job_files(
        self,
        job_uuid: uuid.UUID,
        container,
    ) -> List[models.File]:
        """
        Extract file information from a job's output container using modern CData utilities.

        This method inspects the job's output container and registers all
        output files in the database.

        Args:
            job_uuid: UUID of the job
            container: CDataContainer with output data

        Returns:
            List of created File instances
        """
        # Import here to avoid circular dependency
        from ..lib.cdata_utils import find_all_files, extract_file_metadata

        files_created = []

        # Use modern hierarchical traversal to find all files
        output_files = find_all_files(container)
        logger.info(f"Found {len(output_files)} files in output container")
        print(f"[DEBUG glean_job_files] Found {len(output_files)} files in output container")

        for file_obj in output_files:
            print(f"[DEBUG glean_job_files] Processing {file_obj.name}:")
            print(f"  isSet(): {file_obj.isSet() if hasattr(file_obj, 'isSet') else 'N/A'}")
            print(f"  exists(): {file_obj.exists() if hasattr(file_obj, 'exists') else 'N/A'}")
            print(f"  getFullPath(): {file_obj.getFullPath() if hasattr(file_obj, 'getFullPath') else 'N/A'}")

            # Check if file is set (baseName has been assigned)
            if not hasattr(file_obj, 'isSet') or not file_obj.isSet():
                logger.debug(f"Skipping unset file: {file_obj.name}")
                print(f"  -> Skipping: not set")
                continue

            # Check if file exists on disk
            if not hasattr(file_obj, 'exists') or not file_obj.exists():
                logger.debug(f"Skipping non-existent file: {file_obj.name} (path: {file_obj.getFullPath() if hasattr(file_obj, 'getFullPath') else 'N/A'})")
                print(f"  -> Skipping: doesn't exist")
                continue

            print(f"  -> Will glean this file")

            # Extract metadata using modern CData system
            try:
                metadata = extract_file_metadata(file_obj)

                print(f"[DEBUG glean_job_files] Extracted metadata for {file_obj.name}:")
                print(f"  file_type (mimeTypeName): {metadata['file_type']}")
                print(f"  content_flag: {metadata.get('content_flag', 'NOT SET')}")
                print(f"  sub_type: {metadata.get('sub_type', 'NOT SET')}")
                print(f"  gui_label: {metadata.get('gui_label', 'NOT SET')}")

                # Get full file path
                file_path = Path(str(file_obj))

                # Register the file in database
                file_record = await self.register_output_file(
                    job_uuid=job_uuid,
                    file_path=file_path,
                    file_type=metadata['file_type'],
                    param_name=metadata['name'],
                    content_flag=metadata.get('content_flag'),
                    sub_type=metadata.get('sub_type'),
                    annotation=metadata.get('annotation', metadata.get('gui_label', '')),
                )

                print(f"  -> Registered as: {file_record.type.name if file_record.type else 'NO TYPE'}")

                # Link back to container
                if hasattr(file_obj, 'dbFileId'):
                    file_obj.dbFileId.set(str(file_record.uuid))

                files_created.append(file_record)

            except Exception as e:
                logger.exception(f"Error gleaning file {file_obj.name}: {e}")

        return files_created

    async def glean_performance_indicators(
        self,
        job_uuid: uuid.UUID,
        container,
    ) -> int:
        """
        Extract performance indicators (KPIs) from output container.

        Args:
            job_uuid: UUID of the job
            container: CDataContainer with output data

        Returns:
            Number of KPIs extracted
        """
        # Import here to avoid circular dependency
        from ..lib.cdata_utils import extract_kpi_values
        # Will need to import CPerformanceIndicator type
        try:
            from core.CCP4PerformanceData import CPerformanceIndicator
        except ImportError:
            try:
                from core.CCP4PerformanceData import CPerformanceIndicator
            except ImportError:
                logger.warning("Could not import CPerformanceIndicator")
                return 0

        count = 0

        # Find all performance indicator objects
        from ..lib.cdata_utils import find_objects_by_type
        kpis = find_objects_by_type(container, CPerformanceIndicator)

        for kpi in kpis:
            try:
                # Extract all KPI values
                values = extract_kpi_values(kpi)

                # Register each value in database
                for key, value in values.items():
                    if isinstance(value, float):
                        await self.register_job_float_value(
                            job_uuid=job_uuid,
                            key=key,
                            value=value,
                        )
                        count += 1
                    elif isinstance(value, str) and len(value) > 0:
                        await self.register_job_char_value(
                            job_uuid=job_uuid,
                            key=key,
                            value=value,
                        )
                        count += 1

            except Exception as e:
                logger.exception(f"Error gleaning KPIs from {kpi.object_path()}: {e}")

        return count

    @asynccontextmanager
    async def track_job(self, plugin: CPluginScript):
        """
        Context manager for automatic job lifecycle tracking.

        This context manager:
        1. Creates job record in database (if not exists)
        2. Connects to plugin signals to track status changes
        3. Updates database on status transitions
        4. Registers output files on completion

        Usage:
            async with db_handler.track_job(plugin_instance):
                await plugin_instance.execute()
            # Job is automatically tracked and files registered

        Args:
            plugin: CPluginScript instance to track
        """
        # Create job if doesn't exist in database
        if plugin.get_db_job_id() is None:
            parent_uuid = None
            if plugin.parent and hasattr(plugin.parent, 'get_db_job_id'):
                parent_uuid = plugin.parent.get_db_job_id()

            job = await self.create_job(
                task_name=plugin.TASKNAME or "unknown",
                title=plugin.name,
                parent_job_uuid=parent_uuid,
            )
            plugin.set_db_job_id(job.uuid)
            plugin.set_db_job_number(job.number)

            # Set project ID for database-aware file handling
            plugin._dbProjectId = self.project_uuid

            # Attach this handler to the plugin so CDataFile can find it
            plugin._db_handler = self

            # Set work directory to job directory for proper file paths
            # This ensures output files are created in the correct job directory
            from pathlib import Path
            job_dir_sync = await sync_to_async(lambda: job.directory)()
            plugin.workDirectory = Path(job_dir_sync)

        job_uuid = plugin.get_db_job_id()

        try:
            # Mark as running
            await self.update_job_status(job_uuid, models.Job.Status.RUNNING)

            # Execute the plugin
            yield plugin

            # After execution, update job status based on plugin status
            plugin_status = plugin.get_status()
            status_map = {
                CPluginScript.SUCCEEDED: models.Job.Status.FINISHED,
                CPluginScript.FAILED: models.Job.Status.FAILED,
            }

            if plugin_status in status_map:
                db_status = status_map[plugin_status]
                await self.update_job_status(job_uuid, db_status)
                logger.info(f"Job {job_uuid} status updated to {db_status}")

            # After execution, glean output files and KPIs if finished successfully
            print(f"[DEBUG track_job] plugin_status = {plugin_status}, SUCCEEDED = {CPluginScript.SUCCEEDED}")
            if plugin_status == CPluginScript.SUCCEEDED:
                print(f"[DEBUG track_job] Status is SUCCEEDED, gleaning files...")
                output_container = plugin.container.outputData if hasattr(plugin.container, 'outputData') else None
                print(f"[DEBUG track_job] output_container = {output_container}")
                print(f"[DEBUG track_job] output_container is not None = {output_container is not None}")
                if output_container is not None:
                    files_gleaned = await self.glean_job_files(job_uuid, output_container)
                    logger.info(f"Gleaned {len(files_gleaned)} output files")
                    print(f"[DEBUG track_job] Gleaned {len(files_gleaned)} output files")

                    kpis_gleaned = await self.glean_performance_indicators(job_uuid, output_container)
                    logger.info(f"Gleaned {kpis_gleaned} performance indicators")
                    print(f"[DEBUG track_job] Gleaned {kpis_gleaned} performance indicators")
                else:
                    print(f"[DEBUG track_job] No output container found!")
            else:
                print(f"[DEBUG track_job] Status is NOT SUCCEEDED, skipping gleaning")

        finally:
            # Cleanup if needed
            pass


    async def find_file_by_path(
        self,
        file_path: str,
        job_number: str,
        filename: str
    ) -> Optional[models.File]:
        """
        Find an existing file record in the database by job and filename.

        This method is called by CDataFile.setFullPath() to update file attributes
        from the database when a file path is set in a database-aware context.

        Args:
            file_path: Full absolute path to the file
            job_number: Job number (e.g., "1.2")
            filename: Base filename

        Returns:
            File instance if found, None otherwise
        """
        try:
            return await sync_to_async(models.File.objects.get)(
                job__project__uuid=self.project_uuid,
                job__number=job_number,
                name=filename
            )
        except models.File.DoesNotExist:
            return None
        except Exception as e:
            logger.debug(f"Error finding file by path: {e}")
            return None

    async def get_file_path(self, file_uuid: uuid.UUID) -> Optional[str]:
        """
        Get the full file path from a database file UUID.

        This method is called by CDataFile.getFullPath() when dbFileId is set,
        allowing the file path to be retrieved from the database.

        Args:
            file_uuid: UUID of the file record

        Returns:
            Full path to the file, or None if not found
        """
        try:
            file_record = await sync_to_async(models.File.objects.get)(uuid=file_uuid)
            return str(file_record.path) if file_record.path else None
        except models.File.DoesNotExist:
            return None
        except Exception as e:
            logger.debug(f"Error getting file path: {e}")
            return None

    def find_file_by_path_sync(
        self,
        file_path: str,
        job_number: str,
        filename: str
    ) -> Optional[Dict[str, Any]]:
        """
        Synchronous version of find_file_by_path for use by CDataFile.

        Returns a dict with file attributes instead of a model instance
        to avoid exposing Django models to core code.

        Returns:
            Dict with keys: uuid, name, path, relative_path, or None if not found
        """
        try:
            file_record = models.File.objects.get(
                job__project__uuid=self.project_uuid,
                job__number=job_number,
                name=filename
            )
            return {
                'uuid': str(file_record.uuid),
                'name': file_record.name,
                'path': str(file_record.path) if file_record.path else None,
                'relative_path': file_record.relative_path,
            }
        except models.File.DoesNotExist:
            return None
        except Exception as e:
            logger.debug(f"Error finding file by path: {e}")
            return None

    def get_file_path_sync(self, file_uuid: uuid.UUID) -> Optional[str]:
        """
        Synchronous version of get_file_path for use by CDataFile.

        Args:
            file_uuid: UUID of the file record

        Returns:
            Full path to the file, or None if not found
        """
        try:
            file_record = models.File.objects.get(uuid=file_uuid)
            return str(file_record.path) if file_record.path else None
        except models.File.DoesNotExist:
            return None
        except Exception as e:
            logger.debug(f"Error getting file path: {e}")
            return None

    def getProjectDirectory(self, project_id: str) -> Optional[str]:
        """
        Get the directory path for a project by its UUID.

        Used by CDataFile.getFullPath() to construct full file paths from
        project/relPath/baseName components.

        Args:
            project_id: UUID of the project (as string)

        Returns:
            Full path to the project directory, or None if not found
        """
        try:
            import uuid as uuid_module
            project_uuid = uuid_module.UUID(str(project_id))
            project = models.Project.objects.get(uuid=project_uuid)
            return str(project.directory) if project.directory else None
        except models.Project.DoesNotExist:
            logger.debug(f"Project not found: {project_id}")
            return None
        except Exception as e:
            logger.debug(f"Error getting project directory: {e}")
            return None


def plugin_status_to_job_status(finish_status: int) -> int:
    """
    Convert CPluginScript finish status to Job.Status enum value.

    Args:
        finish_status: CPluginScript status code

    Returns:
        models.Job.Status enum value
    """
    status_map = {
        CPluginScript.SUCCEEDED: models.Job.Status.FINISHED,
        CPluginScript.FAILED: models.Job.Status.FAILED,
        CPluginScript.INTERRUPTED: models.Job.Status.INTERRUPTED,
        CPluginScript.MARK_TO_DELETE: models.Job.Status.TO_DELETE,
        CPluginScript.UNSATISFACTORY: models.Job.Status.UNSATISFACTORY,
    }
    return status_map.get(finish_status, models.Job.Status.FAILED)
