"""
Implementation classes for CCP4Data.py

Extends stub classes from core.cdata_stubs with methods and business logic.
This file is safe to edit - add your implementation code here.
"""

from __future__ import annotations
from typing import Optional, Any

from core.cdata_stubs.CCP4Data import CBaseDataStub, CCollectionStub, CDictStub, CFloatRangeStub, CFollowFromJobStub, CI2DataTypeStub, CIntRangeStub, CJobStatusStub, CJobTitleStub, COneWordStub, COutputFileListStub, CPatchSelectionStub, CRangeStub, CRangeSelectionStub, CUUIDStub

# Re-export fundamental types for legacy code compatibility
# Many legacy files use "CCP4Data.CList", "CCP4Data.CString", etc.
# which are actually in base_object.fundamental_types
from core.base_object.fundamental_types import CList, CString, CInt, CFloat, CBoolean


class CBaseData(CBaseDataStub):
    """
    Base class for simple classes
    
    Extends CBaseDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CCollection(CCollectionStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CCollectionStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDict(CDictStub, CCollection):
    """
    
    Inherits from:
    - CDictStub: Metadata and structure
    - CCollection: Shared full-fat methods
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CDictStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFloatRange(CFloatRangeStub):
    """
    Two floats defining start and end of range

    Extends CFloatRangeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFollowFromJob(CFollowFromJobStub):
    """
    A string
    
    Extends CFollowFromJobStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CI2DataType(CI2DataTypeStub):
    """
    A string
    
    Extends CI2DataTypeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CIntRange(CIntRangeStub):
    """
    Two integers defining start and end of range
    
    Extends CIntRangeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CJobStatus(CJobStatusStub):
    """
    An integer
    
    Extends CJobStatusStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CJobTitle(CJobTitleStub):
    """
    A string
    
    Extends CJobTitleStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class COneWord(COneWordStub):
    """
    A single word string - no white space
    
    Extends COneWordStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class COutputFileList(COutputFileListStub):
    """
    A list with all items of one CData sub-class
    
    Extends COutputFileListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPatchSelection(CPatchSelectionStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CPatchSelectionStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CRange(CRangeStub):
    """
    Base class for CIntRange and CFloatRange
    
    Extends CRangeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CRangeSelection(CRangeSelectionStub):
    """
    Range selection string (e.g., "1-10,15,20-25").

    Extends CRangeSelectionStub with validation for range selection syntax.
    Validates format like "1-10,15,20-25" where ranges are specified as
    comma-separated numbers or hyphen-separated ranges.
    """

    ERROR_CODES = {
        201: {'description': 'Range selection contains invalid character'},
        202: {'description': 'Range selection contains bad syntax'}
    }

    def validity(self, arg):
        """
        Validate range selection string syntax.

        Legacy API compatibility method for validating range selection format.
        Checks for:
        - Only digits, commas, and hyphens
        - Valid range syntax (start-end where start < end)
        - No empty ranges

        Args:
            arg: String to validate (e.g., "1-10,15,20-25")

        Returns:
            CErrorReport: Error report with validation issues
        """
        from core.base_object.error_reporting import CErrorReport
        from core.base_object.base_classes import CData

        err = CErrorReport()

        # Check for undefined value
        if arg is None:
            if not self.get_qualifier('allowUndefined'):
                err.append(
                    "CData", 2,
                    details="Value is not set",
                    name=self.object_path()
                )
            return err

        # Remove whitespace
        arg = self.removeWhiteSpace(arg)

        # Check for invalid characters (only allow digits, comma, hyphen)
        import re
        s = re.search(r'[^0-9,\-]', arg)
        if s is not None:
            err.append(
                "CRangeSelection", 201,
                details=self.ERROR_CODES[201]['description'],
                name=self.object_path()
            )
        else:
            # Check each range component
            rList = arg.split(',')
            for r in rList:
                if len(r) < 1:
                    # Empty range (e.g., "1,,2")
                    err.append(
                        "CRangeSelection", 202,
                        details=self.ERROR_CODES[202]['description'],
                        name=self.object_path()
                    )
                elif r.count('-') > 1:
                    # Too many hyphens (e.g., "1-2-3")
                    err.append(
                        "CRangeSelection", 202,
                        details=self.ERROR_CODES[202]['description'],
                        name=self.object_path()
                    )
                elif r.count('-') == 1:
                    # Range format "start-end"
                    rr = r.split('-')
                    try:
                        if int(rr[0]) > int(rr[1]):
                            # Start is greater than end (e.g., "10-5")
                            err.append(
                                "CRangeSelection", 202,
                                details=self.ERROR_CODES[202]['description'],
                                name=self.object_path()
                            )
                    except:
                        # Invalid integers
                        err.append(
                            "CRangeSelection", 202,
                            details=self.ERROR_CODES[202]['description'],
                            name=self.object_path()
                        )

        return err


class CUUID(CUUIDStub):
    """
    A string
    
    Extends CUUIDStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass

