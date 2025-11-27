from typing import List
from ccp4x.db import models
from ..plugins.get_plugin import get_job_plugin


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
    base_element = the_job_plugin.container.find_by_path(object_path, skip_first=True)
    if method_name == "validity":
        result = base_element.validity(base_element.get())
    else:
        result = getattr(base_element, method_name)(*args, **kwargs)
    return result
