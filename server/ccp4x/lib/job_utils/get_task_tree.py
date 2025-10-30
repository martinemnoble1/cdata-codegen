from core.CCP4TaskManager import CTaskManager


def get_task_tree():
    taskManager = CTaskManager()
    result = {
        "tree": taskManager.taskTree(),
        "lookup": taskManager.taskLookup,
        "iconLookup": taskManager.taskIconLookup,
    }
    return result
