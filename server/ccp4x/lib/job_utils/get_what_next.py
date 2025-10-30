from ...db import models
from django.http import JsonResponse
from core import CCP4Modules
from .get_job_plugin import get_job_plugin


def get_what_next(job: models.Job):
    the_job_plugin = get_job_plugin(job)
    if the_job_plugin is None:
        return {"Status": "Failed", "result": []}

    taskManager = CCP4Modules.TASKMANAGER()
    if hasattr(the_job_plugin, "WHATNEXT"):
        result = {
            "Status": "Success",
            "result": [
                {
                    "taskName": taskName,
                    "shortTitle": taskManager.getShortTitle(taskName),
                    "title": taskManager.getTitle(taskName),
                }
                for taskName in the_job_plugin.WHATNEXT
            ],
        }
    else:
        result = {"Status": "Failed", "result": []}
    return result
