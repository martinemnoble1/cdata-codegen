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


class _ProcessManagerStub:
    """Stub for legacy PROCESSMANAGER - returns sensible defaults.

    This is a simplified process manager that works with our synchronous
    execution model. It returns exit codes from the plugin instances that
    stored them during execution.
    """
    def __init__(self):
        # Registry to store plugin instances by PID
        # In synchronous execution, PID is just the plugin's id()
        self._registry = {}

    def register(self, plugin):
        """Register a plugin instance."""
        pid = id(plugin)
        self._registry[pid] = plugin
        return pid

    def unregister(self, pid):
        """Unregister a plugin instance."""
        if pid in self._registry:
            del self._registry[pid]

    def getJobData(self, pid=None, attribute=None):
        """Return job data for the given PID.

        Args:
            pid: Process ID (typically id(plugin))
            attribute: Attribute to query ('exitStatus' or 'exitCode')

        Returns:
            Requested attribute value, or 0 if not found
        """
        if pid in self._registry:
            plugin = self._registry[pid]
            if attribute == 'exitStatus':
                return getattr(plugin, '_exitStatus', 0)
            if attribute == 'exitCode':
                return getattr(plugin, '_exitCode', 0)

        # Default to success if not found
        if attribute == 'exitStatus':
            return 0  # Success
        if attribute == 'exitCode':
            return 0  # Success
        return None


# Global singleton instance
_process_manager_instance = _ProcessManagerStub()


def PROCESSMANAGER():
    """Return global process manager instance for legacy compatibility."""
    return _process_manager_instance


__all__ = ['TASKMANAGER', 'PROJECTSMANAGER', 'PROCESSMANAGER', 'QTAPPLICATION']


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
