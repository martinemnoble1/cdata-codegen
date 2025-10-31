"""
CCP4Modules.py - Modern module accessor for CCP4 components

This module provides access to CCP4 system components in a modern,
Django-based architecture. It replaces the legacy CCP4Modules class
with simple function accessors.

This module maintains backward compatibility with legacy code that
imports from core.CCP4Modules.
"""

import sys
from .CCP4TaskManager import TASKMANAGER
from .CCP4ProjectsManager import PROJECTSMANAGER

__all__ = ['TASKMANAGER', 'PROJECTSMANAGER', 'QTAPPLICATION']


def QTAPPLICATION():
    """
    Get or create the singleton QApplication instance.

    This replaces the legacy CCP4Modules.QTAPPLICATION() function from classic ccp4i2.
    In the old system, this ensured a single Qt application instance.
    In our Qt-free architecture, it returns the QCoreApplication singleton.

    Returns:
        QCoreApplication: The singleton application instance

    Example:
        >>> from core import CCP4Modules
        >>> app = CCP4Modules.QTAPPLICATION()
        >>> event_loop = QEventLoop(parent=app)
        >>> event_loop.exec_()
    """
    from PySide2.QtCore import QCoreApplication

    # Get existing instance or create new one
    app = QCoreApplication.instance()
    if app is None:
        # No instance exists - create one
        # Pass sys.argv for Qt compatibility
        app = QCoreApplication(sys.argv)
    return app
