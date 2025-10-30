import logging
import datetime
import json
import pathlib
import os
import subprocess
from pytz import timezone
from django.http import Http404
from django.http import FileResponse
from django.core.management import call_command
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, JSONParser
from ..lib.job_utils.list_project import list_project
from ..lib.job_utils.get_task_tree import get_task_tree
from ..lib.job_utils.create_task import create_task
from ..lib.job_utils.preview_file import preview_file

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from . import serializers
from ..db import models
from ..lib.job_utils.find_dependent_jobs import delete_job_and_dependents
from django.http import JsonResponse
from django.conf import settings
from django.utils.text import slugify

logger = logging.getLogger(f"ccp4x:{__name__}")


class ProjectViewSet(ModelViewSet):
    """
    ProjectViewSet

    This viewset provides various actions to interact with the `Project` model and its related entities.
    It includes endpoints for importing projects, retrieving associated files, jobs, and metadata, as well
    as handling project-specific operations like directory listing, file retrieval, and task creation.

    Actions:
        - import_project: Handles the upload and import of project files (ZIP format).
        - files: Retrieves a list of files associated with a specific project.
        - jobs: Retrieves a list of jobs associated with a specific project.
        - job_float_values: Retrieves all `JobFloatValue` instances associated with a specific project.
        - job_char_values: Retrieves job characteristic values for a specific project.
        - tags: Retrieves tags associated with a specific project.
        - directory: Retrieves the directory listing of a specific project.
        - project_file: Retrieves a specific file from the project's directory.
        - preview_file: Previews a specific file from the project's directory using a specified viewer.
        - task_tree: Retrieves the task tree structure (not directly tied to a specific project).
        - create_task: Creates a new task (job) within a specific project.

    Attributes:
        - queryset: The queryset used to retrieve `Project` objects.
        - serializer_class: The default serializer class for the viewset.
        - parser_classes: The parsers allowed for handling incoming data.

    Notes:
        - The `import_project` action ensures secure file handling and validates file types.
        - Several actions update the `last_access` timestamp of the project to track usage.
        - Directory traversal attacks are mitigated in file-related actions by validating file paths.
        - Logging is used extensively to capture errors and important events.
    """

    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            logger.warning("Deleting project %s", instance)
            while (
                models.Job.objects.filter(project=instance, parent__isnull=True).count()
                > 0
            ):
                last_job = models.Job.objects.filter(
                    project=instance, parent__isnull=True
                ).last()
                logger.warning("Deleting job %s", last_job)
                delete_job_and_dependents(last_job)

            # Attempt some security by using a defined list of subdirectories for deletion
            for subdir in [
                "CCP4_COOT",
                "CCP4_IMPORTED_FILES",
                "CCP4_JOBS",
                "CCP4_PROJECT_FILES",
                "CCP4_TMP",
            ]:
                subdir_path = os.path.join(instance.directory, subdir)
                if os.path.exists(subdir_path):
                    logger.warning("Deleting subdirectory %s", subdir_path)
                    # Definitely need to
                    for root, dirs, files in os.walk(
                        subdir_path, topdown=False, followlinks=False
                    ):
                        for file in files:
                            file_path = os.path.join(root, file)
                        for directory in dirs:
                            dir_path = os.path.join(root, directory)
                            try:
                                os.rmdir(dir_path)
                            except Exception as e:
                                logger.warning(
                                    "Failed to delete directory %s: %s", dir_path, e
                                )
                            except Exception as e:
                                logger.warning(
                                    "Failed to delete file %s: %s", file_path, e
                                )
                    try:
                        os.rmdir(subdir_path)
                    except Exception as e:
                        logger.warning(
                            "Failed to delete directory %s: %s", subdir_path, e
                        )
            # Attempt to delete any special files in the project directory
            for special_file in [".DS_Store"]:
                special_file_path = os.path.join(instance.directory, special_file)
                if os.path.exists(special_file_path):
                    logger.warning("Deleting special file %s", special_file_path)
                    try:
                        os.remove(special_file_path)
                    except Exception as e:
                        logger.warning(
                            "Failed to delete file %s: %s", special_file_path, e
                        )
            # Attempt to delete the main project directory
            try:
                os.rmdir(instance.directory)
            except Exception as e:
                logger.warning(
                    "Failed to delete project directory %s: %s", instance.directory, e
                )
            instance.delete()
            logger.warning("Deleted project %s", instance)

            # Note I am adding a bit of body to the response because of an odd
            # javascript feature which presents as network error if no body in response.
            return Response({"status": "Success"})
        except Http404:
            return Http404("Job not found")

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[],
        parser_classes=[
            JSONParser,
            FormParser,
            MultiPartParser,
        ],  # Allow JSON and form data
    )
    def import_project(self, request):
        uploaded_files = request.FILES.getlist("files")
        if not uploaded_files:
            return Response(
                {"status": "Failed", "reason": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Define a secure, platform-independent storage path
        secure_storage_dir = pathlib.Path(settings.MEDIA_ROOT) / "uploaded_files"
        secure_storage_dir.mkdir(parents=True, exist_ok=True)

        # Save the file to the secure storage directory
        for uploaded_file in uploaded_files:
            if not uploaded_file.name.endswith(".zip"):
                return Response(
                    {"status": "Failed", "reason": "Invalid file type"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Ensure the filename is safe
            # if not uploaded_file.name.isalnum():
            #    return Response(
            #        {"status": "Failed", "reason": "Invalid file name"},
            #        status=status.HTTP_400_BAD_REQUEST,
            #    )
            file_path = secure_storage_dir / slugify(uploaded_file.name)
            with open(file_path, "wb") as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            try:
                call_command("import_ccp4_project_zip", str(file_path), "--detach")
            except Exception as e:
                logger.exception(
                    "Failed to import project from %s", file_path, exc_info=e
                )
                return Response(
                    {"status": "Failed", "reason": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            logger.warning("File uploaded and saved to %s", file_path)

        return Response({"status": "Success"})

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.FileSerializer,
    )
    def files(self, request, pk=None):
        """
        Retrieve a list of files associated with a specific project.

        Parameters:

            request (Request): The HTTP request object.
            pk (int, optional): The primary key of the project.

        Returns:
            Response: A Response object containing serialized file data.
        """

        project = models.Project.objects.get(pk=pk)
        serializer = serializers.FileSerializer(
            models.File.objects.filter(job__project=project), many=True
        )
        project.last_access = datetime.datetime.now(tz=timezone("UTC"))
        project.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.FileSerializer,
    )
    def file_uses(self, request, pk=None):
        """
        Retrieve a list of file_uses associated with a specific project.

        Parameters:

            request (Request): The HTTP request object.
            pk (int, optional): The primary key of the project.

        Returns:
            Response: A Response object containing serialized file_use data.
        """

        project = models.Project.objects.get(pk=pk)
        serializer = serializers.FileUseSerializer(
            models.FileUse.objects.filter(job__project=project), many=True
        )
        project.last_access = datetime.datetime.now(tz=timezone("UTC"))
        project.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.JobSerializer,
        parser_classes=[
            JSONParser,
            FormParser,
            MultiPartParser,
        ],  # Allow JSON and form data
    )
    def jobs(self, request, pk=None):
        """
        Retrieve a list of jobs associated with a specific project.
        Args:
            request (Request): The HTTP request object.
            pk (int, optional): The primary key of the project.
        Returns:
            Response: A Response object containing serialized job data.
        """

        project = models.Project.objects.get(pk=pk)
        serializer = serializers.JobSerializer(
            models.Job.objects.filter(project=project), many=True
        )
        project.last_access = datetime.datetime.now(tz=timezone("UTC"))
        project.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.JobFloatValueSerializer,
    )
    def job_float_values(self, request, pk=None):
        """
        Retrieve all JobFloatValue instances associated with a specific project.
        Args:
            request (Request): The HTTP request object.
            pk (int, optional): The primary key of the project.
        Returns:
            Response: A Response object containing serialized data of JobFloatValue instances.
        """

        project = models.Project.objects.get(pk=pk)
        serializer = serializers.JobFloatValueSerializer(
            models.JobFloatValue.objects.filter(job__project=project), many=True
        )
        project.last_access = datetime.datetime.now(tz=timezone("UTC"))
        project.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.JobCharValueSerializer,
    )
    def job_char_values(self, request, pk=None):
        """
        Retrieve job characteristic values for a specific project.
        Args:
            request (Request): The HTTP request object.
            pk (int, optional): The primary key of the project.
        Returns:
            Response: A Response object containing serialized job characteristic values.
        """

        project = models.Project.objects.get(pk=pk)
        serializer = serializers.JobCharValueSerializer(
            models.JobCharValue.objects.filter(job__project=project), many=True
        )
        project.last_access = datetime.datetime.now(tz=timezone("UTC"))
        project.save()
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get", "post"],
        permission_classes=[],
        serializer_class=serializers.ProjectTagSerializer,
    )
    def tags(self, request, pk=None):
        """
        Retrieve tags for a specific project (GET) or add a tag to a project (POST).

        GET: Returns list of tags for the project
        POST: Expects 'tag_id' in request data to add tag to project
        """
        project = models.Project.objects.get(pk=pk)

        if request.method == "GET":
            # Return project tags
            project_tag_serializer = serializers.ProjectTagSerializer(
                project.tags, many=True
            )
            project.last_access = datetime.datetime.now(tz=timezone("UTC"))
            project.save()
            return Response(project_tag_serializer.data)

        elif request.method == "POST":
            # Add tag to project
            try:
                tag_id = request.data.get("tag_id")

                if not tag_id:
                    return Response(
                        {"error": "tag_id is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                tag = models.ProjectTag.objects.get(pk=tag_id)
                project.tags.add(tag)
                project.last_access = datetime.datetime.now(tz=timezone("UTC"))
                project.save()

                return Response(
                    {
                        "status": "success",
                        "message": f"Tag '{tag.text}' added to project",
                    },
                    status=status.HTTP_200_OK,
                )

            except models.ProjectTag.DoesNotExist:
                return Response(
                    {"error": "Tag not found"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            except Exception as e:
                logger.exception("Failed to add tag to project", exc_info=e)
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.ProjectSerializer,
    )
    def directory(self, request, pk=None):
        """
        Handles the request to retrieve the directory listing of a project.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int, optional): The primary key of the project to retrieve the directory listing for.

        Returns:
            JsonResponse: A JSON response containing the status and the directory listing of the project.
                          If successful, the response contains the directory listing in the "container" field.
                          If a TypeError occurs during JSON encoding, the response contains an error message.

        Raises:
            Project.DoesNotExist: If no project with the given primary key exists.
        """

        the_project = models.Project.objects.get(pk=pk)
        result = list_project(str(the_project.uuid))
        try:
            result_str = json.dumps(result, indent=2)
            return JsonResponse(
                json.loads(f'{{"status": "Success", "container": {result_str}}}')
            )
        except TypeError as err:
            logger.exception("Failed encoding listing of %s", exc_info=err)
            return JsonResponse(
                {status: "Failed", "container": {"Reason": "TypeError"}}
            )

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.ProjectSerializer,
    )
    def project_file(self, request, pk=None):
        """
        Retrieve a file from the specified project directory.
        This view handles GET requests to retrieve a file from a project's directory.
        It ensures that the requested file path is within the project's directory to
        prevent directory traversal attacks.

        Args:
            request (HttpRequest): The HTTP request object containing query parameters.
            pk (int, optional): The primary key of the project.

        Raises:
            Http404: If the requested file path is not within the project's directory.

        Returns:
            FileResponse: A response object containing the requested file.
        """
        the_project = models.Project.objects.get(pk=pk)
        file_path = request.GET.get("path")
        logger.info("File path %s", file_path)
        composite_path: pathlib.Path = pathlib.Path(the_project.directory) / file_path
        if pathlib.Path(the_project.directory) not in composite_path.resolve().parents:
            raise Http404("Unacceptable file")

        return FileResponse(open(composite_path, "rb"), filename=composite_path.name)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[],
        serializer_class=serializers.ProjectSerializer,
    )
    def preview_file(self, request, pk=None):
        """
        Preview a file from the specified project directory, using the specified viewer.
        This view handles POST requests to preview a file from a project's directory.
        It ensures that the requested file path is within the project's directory to
        prevent directory traversal attacks.

        Args:
            request (HttpRequest): The HTTP request object containing query parameters.
            pk (int, optional): The primary key of the project.

        Raises:
            Http404: If the requested file path is not within the project's directory.

        Returns:
            JsonResponse: A JSON response indicating success or failure of the viewer launch.
        """
        the_project = models.Project.objects.get(pk=pk)
        file_path = request.data.get("path")
        viewer = request.data.get("viewer")
        composite_path = pathlib.Path(the_project.directory) / (
            file_path if not file_path.startswith("/") else file_path[1:]
        )
        if not composite_path.resolve().is_relative_to(
            pathlib.Path(the_project.directory)
        ):
            raise Http404("Unacceptable file - outside project directory")

        logger.info("Previewing file %s with viewer %s", composite_path, viewer)
        try:
            # call_command("preview_file", "-d", "-e", viewer, "-p", str(composite_path))
            preview_file(viewer, str(composite_path))
            return JsonResponse({"status": "Success"})
        except Exception as err:
            logger.exception(
                "Failed to preview file %s with viewer %s",
                composite_path,
                viewer,
                exc_info=err,
            )
            return JsonResponse({"status": "Failed", "reason": str(err)})

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[],
        serializer_class=serializers.ProjectSerializer,
    )
    def create_task(self, request, pk=None):
        the_project = models.Project.objects.get(pk=pk)
        new_job = create_task(the_project, json.loads(request.body.decode("utf-8")))
        serializer = serializers.JobSerializer(new_job)
        return JsonResponse({"status": "Success", "new_job": serializer.data})

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[],
        serializer_class=serializers.ProjectSerializer,
    )
    def export(self, request, pk=None):
        the_project = models.Project.objects.get(pk=pk)

        # Generate unique filepath based on project name, rooted in project.directory
        project_name = slugify(the_project.name or f"project_{the_project.id}")
        project_export = models.ProjectExport.objects.create(
            project=the_project, time=datetime.datetime.now(tz=timezone("UTC"))
        )
        project_export.save()
        timestamp = project_export.time.strftime("%Y%m%d_%H%M%S")
        export_file_name = f"{project_name}_export_{timestamp}.ccp4_project.zip"
        export_file_path = os.path.join(
            the_project.directory, "CCP4_PROJECT_FILES", export_file_name
        )

        # Ensure the export file path doesn't already exist (add counter if needed)
        counter = 1
        base_name = export_file_name
        while os.path.exists(export_file_path):
            name_without_ext = base_name.rsplit(".", 1)[0]
            export_file_name = f"{name_without_ext}_{counter}.ccp4_project.zip"
            export_file_path = os.path.join(
                the_project.directory, "CCP4_PROJECT_FILES", export_file_name
            )
            counter += 1

        # Create log file path with same base name but .export.log extension
        log_file_name = export_file_name.replace(".ccp4_project.zip", ".export.log")
        log_file_path = os.path.join(
            the_project.directory, "CCP4_PROJECT_FILES", log_file_name
        )

        # Start subprocess to run export_project management command in background
        try:
            with open(log_file_path, "w") as log_file:
                process = subprocess.Popen(
                    [
                        "ccp4-python",
                        "manage.py",
                        "export_project",
                        "-pi",
                        str(the_project.id),
                        "-o",
                        export_file_path,
                    ],
                    stdout=log_file,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )

            return JsonResponse(
                {
                    "status": "Success",
                    "export_file_name": export_file_name,
                    "log_file_name": log_file_name,
                    "process_id": process.pid,
                }
            )
        except Exception as e:
            logger.exception(
                "Failed to start export process for project %s",
                the_project.id,
                exc_info=e,
            )
            return JsonResponse({"status": "Failed", "reason": str(e)})

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[],
        serializer_class=serializers.ProjectExportSerializer,
    )
    def exports(self, request, pk=None):
        """
        Retrieve a list of project exports for a specific project.

        This action returns all ProjectExport instances associated with the given project,
        ordered by creation time (most recent first). This allows users to see the history
        of exports and their status.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int, optional): The primary key of the project.

        Returns:
            Response: A Response object containing serialized ProjectExport data,
                     including export file names, creation times, and status information.
        """
        try:
            project = models.Project.objects.get(pk=pk)

            # Get all exports for this project, ordered by most recent first
            project_exports = models.ProjectExport.objects.filter(
                project=project
            ).order_by("-time")

            # Update project last access time
            project.last_access = datetime.datetime.now(tz=timezone("UTC"))
            project.save()

            # Serialize the export data
            serializer = serializers.ProjectExportSerializer(project_exports, many=True)

            return Response(
                serializer.data,
            )

        except models.Project.DoesNotExist:
            return Response(
                {"status": "Failed", "reason": "Project not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception(
                "Failed to retrieve exports for project %s", pk, exc_info=e
            )
            return Response(
                {"status": "Failed", "reason": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(
        detail=True,
        methods=["delete"],
        permission_classes=[],
        url_path=r"tags/(?P<tag_id>\d+)",
    )
    def remove_tag(self, request, pk=None, tag_id=None):
        """
        Remove a tag from a specific project.
        """
        try:
            project = models.Project.objects.get(pk=pk)
            tag = models.ProjectTag.objects.get(pk=tag_id)
            project.tags.remove(tag)
            project.last_access = datetime.datetime.now(tz=timezone("UTC"))
            project.save()

            return Response(
                {
                    "status": "success",
                    "message": f"Tag '{tag.text}' removed from project",
                },
                status=status.HTTP_200_OK,
            )

        except models.Project.DoesNotExist:
            return Response(
                {"error": "Project not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except models.ProjectTag.DoesNotExist:
            return Response(
                {"error": "Tag not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            logger.exception("Failed to remove tag from project", exc_info=e)
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
