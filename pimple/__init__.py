"""
Pimple - CCP4 log file parsing for reports

This package provides Qt-free parsing functionality for CCP4 log files.
The full MGQTmatplotlib module contains GUI components that require Qt,
but the core parsing functions (CCP4Table, CCP4LogToEtree) work without Qt.

This init file creates a mock MGQTmatplotlib module that can be imported
even when Qt is not available, with just the parsing functions.
"""

# Try to import the full module with Qt support
try:
    from . import MGQTmatplotlib
    QT_GUI_AVAILABLE = True
    # Extract what we need
    CCP4LogToEtree = MGQTmatplotlib.CCP4LogToEtree
    CCP4Table = MGQTmatplotlib.CCP4Table
except (ImportError, AttributeError) as e:
    # Qt not available - create a minimal MGQTmatplotlib module with just what we need
    QT_GUI_AVAILABLE = False

    # Create a minimal module namespace
    import sys
    import os
    import math
    from types import ModuleType
    from lxml import etree

    # Create namespace for execution
    namespace = {
        '__name__': 'pimple.MGQTmatplotlib',
        '__file__': os.path.join(os.path.dirname(__file__), 'MGQTmatplotlib.py'),
        'sys': sys,
        'os': os,
        'math': math,
        'etree': etree,
    }

    # Define scaling_functions (needed by CCP4Table)
    exec("""
scaling_functions = { 'oneoversqrt' : lambda x,pos,format='%.1f': (format)%(math.pow(x,-0.5)) if x > 1e-8  else ' ' }
""", namespace)

    # Read the source file
    from pathlib import Path
    module_path = Path(__file__).parent / "MGQTmatplotlib.py"
    with open(module_path) as f:
        source = f.read()

    # Extract CCP4Table class definition
    ccp4table_start = source.find('class CCP4Table:')
    if ccp4table_start == -1:
        raise ImportError("Could not find CCP4Table class in MGQTmatplotlib.py")

    lines = source[ccp4table_start:].split('\n')
    class_lines = [lines[0]]
    for i in range(1, len(lines)):
        line = lines[i]
        if line and not line[0].isspace() and (line.startswith('class ') or line.startswith('def ')):
            break
        class_lines.append(line)

    ccp4table_code = '\n'.join(class_lines)
    exec(ccp4table_code, namespace)

    # Extract CCP4LogToEtree and related functions
    functions_to_extract = ['CCP4LogToEtree', 'CCP4LogToXML', 'CCP4LogFileNameToEtree', 'CCP4LogFileNameToXML']
    for func_name in functions_to_extract:
        pattern = f'def {func_name}('
        func_start = source.find(pattern)
        if func_start == -1:
            continue

        lines = source[func_start:].split('\n')
        func_lines = [lines[0]]
        for i in range(1, len(lines)):
            line = lines[i]
            if line and not line[0].isspace() and (line.startswith('class ') or line.startswith('def ') or line.startswith('if __name__')):
                break
            func_lines.append(line)

        func_code = '\n'.join(func_lines)
        exec(func_code, namespace)

    # Create a fake module object
    MGQTmatplotlib = ModuleType('pimple.MGQTmatplotlib')
    for key, value in namespace.items():
        setattr(MGQTmatplotlib, key, value)

    # Register it in sys.modules so future imports work
    sys.modules['pimple.MGQTmatplotlib'] = MGQTmatplotlib

    # Export what we need
    CCP4LogToEtree = namespace['CCP4LogToEtree']
    CCP4Table = namespace['CCP4Table']

__all__ = ['CCP4LogToEtree', 'CCP4Table', 'MGQTmatplotlib', 'QT_GUI_AVAILABLE']
