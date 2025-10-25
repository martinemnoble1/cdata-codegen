"""
Stub QtCore module for plugin discovery.

Provides minimal Qt-compatible decorators and classes to allow plugin files
to be imported without requiring PySide2. This is only used for introspection
during plugin discovery - not for actual Qt functionality.
"""

from typing import Any, Callable, TypeVar

FuncT = TypeVar('FuncT', bound=Callable[..., Any])


def Slot(*arg_types, **kwargs) -> Callable[[FuncT], FuncT]:
    """
    Stub for Qt's Slot decorator.

    This is a no-op decorator that allows code using @Slot to be imported.
    It's compatible with our signal_system.Slot if needed, but for plugin
    discovery we just pass through the original function unchanged.

    Usage (from CCP4i2 plugins):
        @Slot()
        def my_slot(self):
            pass

        @Slot(str, int)
        def handle_data(self, text, value):
            pass
    """
    def decorator(func: FuncT) -> FuncT:
        # Just return the function unchanged - we only need imports to work
        return func
    return decorator


# Stub Signal class - many plugins import this
class Signal:
    """Stub Signal class."""
    def __init__(self, *args):
        pass

    def connect(self, slot):
        pass

    def emit(self, *args):
        pass


# Stub QObject - base class for Qt objects
class QObject:
    """Stub QObject class."""
    def __init__(self, parent=None):
        self.parent = parent


# Other common QtCore items that might be imported
class QThread:
    """Stub QThread class."""
    pass


class QTimer:
    """Stub QTimer class."""
    pass


class Qt:
    """Stub Qt namespace class."""
    # Common Qt enum values
    AlignLeft = 0x0001
    AlignRight = 0x0002
    AlignCenter = 0x0004
    AlignTop = 0x0020
    AlignBottom = 0x0040


# Common property decorator
def Property(type, *args, **kwargs):
    """Stub Property decorator."""
    def decorator(func):
        return func
    return decorator
