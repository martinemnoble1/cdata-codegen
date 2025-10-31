"""
CCP4Modules.py - Modern module accessor for CCP4 components

This module provides access to CCP4 system components in a modern,
Django-based architecture. It replaces the legacy CCP4Modules class
with simple function accessors.

This module maintains backward compatibility with legacy code that
imports from core.CCP4Modules.
"""

from .CCP4TaskManager import TASKMANAGER
from .CCP4ProjectsManager import PROJECTSMANAGER

__all__ = ['TASKMANAGER', 'PROJECTSMANAGER']
