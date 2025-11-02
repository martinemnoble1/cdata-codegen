from typing import List
from ccp4x.db import models
from ..plugins.get_plugin import get_job_plugin
from ..containers.find_objects import find_object_by_path


def object_method(
    the_job: models.Job,
    object_path: str,
    method_name: str,
    args: List[str] = None,
    kwargs: dict = None,
):

    if args is None:
        args = []
    if kwargs is None:
        kwargs = {}

    the_job_plugin = get_job_plugin(the_job)
    base_element = find_object_by_path(the_job_plugin.container, object_path)
    if method_name == "validity":
        result = base_element.validity(base_element.get())
    else:
        result = getattr(base_element, method_name)(*args, **kwargs)
    return result
