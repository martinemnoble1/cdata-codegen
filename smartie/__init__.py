"""
smartie - CCP4 logfile parsing library

This is the real smartie library from CCP4i2, which parses CCP4 program
log files to extract tables and graph data for reports.

Main API:
    parselog(filename) - Parse a CCP4 logfile and return a logfile object

Example:
    import smartie
    logfile = smartie.parselog('/path/to/program.log')
    tables = logfile.tables()
    for table in tables:
        print(f"Table: {table.title()}")
        print(f"Rows: {table.nrows()}, Columns: {table.ncolumns()}")
"""

# Import main API from smartie module
from .smartie import parselog

# Export main API
__all__ = ['parselog']
