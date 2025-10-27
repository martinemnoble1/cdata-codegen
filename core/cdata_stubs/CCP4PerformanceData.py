"""Auto-generated from CCP4i2 metadata. DO NOT EDIT.

This is a stub file - extend classes in core/ to add methods.
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

# Metadata system
from core.base_object.class_metadata import cdata_class, attribute, AttributeType

# Base classes
from core.base_object.base_classes import CData

# Fundamental types
from core.base_object.fundamental_types import CFloat, CInt, CString

# Cross-file stub class references
from core.cdata_stubs.CCP4XtalData import CSpaceGroupStub


@cdata_class(
    attributes={
        "value": attribute(AttributeType.FLOAT),
        "annotation": attribute(AttributeType.STRING),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['value', 'annotation'],
)
class CPerformanceIndicatorStub(CData):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CPerformanceIndicator.py
    to add methods and implementation-specific functionality.
    """

    value: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPerformanceIndicatorStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "nAtoms": attribute(AttributeType.INT),
        "nResidues": attribute(AttributeType.INT),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['nAtoms', 'nResidues'],
)
class CAtomCountPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CAtomCountPerformance.py
    to add methods and implementation-specific functionality.
    """

    nAtoms: Optional[CInt] = None
    nResidues: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAtomCountPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "FOM": attribute(AttributeType.FLOAT),
        "CFOM": attribute(AttributeType.FLOAT),
        "Hand1Score": attribute(AttributeType.FLOAT),
        "Hand2Score": attribute(AttributeType.FLOAT),
        "CC": attribute(AttributeType.FLOAT),
        "RFactor": attribute(AttributeType.FLOAT),
        "RFree": attribute(AttributeType.FLOAT),
        "annotation": attribute(AttributeType.STRING),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=[
        'FOM',
        'CFOM',
        'Hand1Score',
        'Hand2Score',
        'CC',
        'RFactor',
        'RFree',
        'annotation'],
)
class CExpPhasPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CExpPhasPerformance.py
    to add methods and implementation-specific functionality.
    """

    FOM: Optional[CFloat] = None
    CFOM: Optional[CFloat] = None
    Hand1Score: Optional[CFloat] = None
    Hand2Score: Optional[CFloat] = None
    CC: Optional[CFloat] = None
    RFactor: Optional[CFloat] = None
    RFree: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CExpPhasPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "cutoff": attribute(AttributeType.FLOAT),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['cutoff'],
)
class CPairefPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CPairefPerformance.py
    to add methods and implementation-specific functionality.
    """

    cutoff: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPairefPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroupStub"),
        "highResLimit": attribute(AttributeType.FLOAT),
        "ccHalf": attribute(AttributeType.FLOAT),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['spaceGroup', 'highResLimit', 'ccHalf'],
)
class CDataReductionCCPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CDataReductionCCPerformance.py
    to add methods and implementation-specific functionality.
    """

    spaceGroup: Optional[CSpaceGroupStub] = None
    highResLimit: Optional[CFloat] = None
    ccHalf: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDataReductionCCPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RMSxyz": attribute(AttributeType.FLOAT),
        "nResidues": attribute(AttributeType.INT),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['RMSxyz', 'nResidues'],
)
class CSuperposePerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CSuperposePerformance.py
    to add methods and implementation-specific functionality.
    """

    RMSxyz: Optional[CFloat] = None
    nResidues: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CSuperposePerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RFactor": attribute(AttributeType.FLOAT),
        "completeness": attribute(AttributeType.FLOAT),
        "annotation": attribute(AttributeType.STRING),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['RFactor', 'completeness', 'annotation'],
)
class CModelBuildPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CModelBuildPerformance.py
    to add methods and implementation-specific functionality.
    """

    RFactor: Optional[CFloat] = None
    completeness: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CModelBuildPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "columnLabelsString": attribute(AttributeType.STRING),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['columnLabelsString'],
)
class CTestObsConversionsPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CTestObsConversionsPerformance.py
    to add methods and implementation-specific functionality.
    """

    columnLabelsString: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CTestObsConversionsPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RFactor": attribute(AttributeType.FLOAT),
        "RFree": attribute(AttributeType.FLOAT),
        "RMSBond": attribute(AttributeType.FLOAT),
        "RMSAngle": attribute(AttributeType.FLOAT),
        "weightUsed": attribute(AttributeType.FLOAT),
        "annotation": attribute(AttributeType.STRING),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=[
        'RFactor',
        'RFree',
        'RMSBond',
        'RMSAngle',
        'weightUsed',
        'annotation'],
)
class CRefinementPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CRefinementPerformance.py
    to add methods and implementation-specific functionality.
    """

    RFactor: Optional[CFloat] = None
    RFree: Optional[CFloat] = None
    RMSBond: Optional[CFloat] = None
    RMSAngle: Optional[CFloat] = None
    weightUsed: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRefinementPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RFactor": attribute(AttributeType.FLOAT),
        "RFree": attribute(AttributeType.FLOAT),
        "R": attribute(AttributeType.FLOAT),
        "R1Factor": attribute(AttributeType.FLOAT),
        "R1Free": attribute(AttributeType.FLOAT),
        "R1": attribute(AttributeType.FLOAT),
        "CCFwork_avg": attribute(AttributeType.FLOAT),
        "CCFfree_avg": attribute(AttributeType.FLOAT),
        "CCF_avg": attribute(AttributeType.FLOAT),
        "CCIwork_avg": attribute(AttributeType.FLOAT),
        "CCIfree_avg": attribute(AttributeType.FLOAT),
        "CCI_avg": attribute(AttributeType.FLOAT),
        "FSCaverage": attribute(AttributeType.FLOAT),
        "annotation": attribute(AttributeType.STRING),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=[
        'RFactor',
        'RFree',
        'R',
        'R1Factor',
        'R1Free',
        'R1',
        'FSCaverage',
        'annotation'],
)
class CServalcatPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CServalcatPerformance.py
    to add methods and implementation-specific functionality.
    """

    RFactor: Optional[CFloat] = None
    RFree: Optional[CFloat] = None
    R: Optional[CFloat] = None
    R1Factor: Optional[CFloat] = None
    R1Free: Optional[CFloat] = None
    R1: Optional[CFloat] = None
    CCFwork_avg: Optional[CFloat] = None
    CCFfree_avg: Optional[CFloat] = None
    CCF_avg: Optional[CFloat] = None
    CCIwork_avg: Optional[CFloat] = None
    CCIfree_avg: Optional[CFloat] = None
    CCI_avg: Optional[CFloat] = None
    FSCaverage: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CServalcatPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroupStub"),
        "highResLimit": attribute(AttributeType.FLOAT),
        "rMeas": attribute(AttributeType.FLOAT),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=['spaceGroup', 'highResLimit', 'rMeas'],
)
class CDataReductionPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CDataReductionPerformance.py
    to add methods and implementation-specific functionality.
    """

    spaceGroup: Optional[CSpaceGroupStub] = None
    highResLimit: Optional[CFloat] = None
    rMeas: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDataReductionPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "phaseError": attribute(AttributeType.FLOAT),
        "weightedPhaseError": attribute(AttributeType.FLOAT),
        "reflectionCorrelation": attribute(AttributeType.FLOAT),
    },
    error_codes={
        "300": {
            "description": "Passed",
            "severity": 0
        },
        "301": {
            "description": "Data value not set"
        },
        "302": {
            "description": "Performance indicator value difference greater than tolereance"
        },
        "303": {
            "description": "Performance indicator value different"
        },
        "304": {
            "description": "Performance indicator value difference greater than tolereance - but improved",
            "severity": 2
        },
        "305": {
            "description": "Performance indicator not used",
            "severity": 0
        }
    },
    qualifiers={
        "allowUndefined": True,
        "guiDefinition": {},
        "saveToDb": False,
    },
    qualifiers_order=[
        'allowUndefined',
        'default',
        'toolTip',
        'guiLabel',
        'guiDefinition',
        'helpFile',
        'saveToDb'],
    qualifiers_definition={
        "allowUndefined": {'type': 'bool'},
        "default": {'type': 'dict'},
        "toolTip": {'type': 'str'},
        "guiLabel": {'type': 'str'},
        "guiDefinition": {'type': 'dict'},
        "helpFile": {'type': 'str'},
        "saveToDb": {'type': 'bool', 'description': 'Save this data in the database'},
    },
    contents_order=[
        'phaseError',
        'weightedPhaseError',
        'reflectionCorrelation'],
)
class CPhaseErrorPerformanceStub(CPerformanceIndicatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    This is a pure data class stub. Extend it in core/CPhaseErrorPerformance.py
    to add methods and implementation-specific functionality.
    """

    phaseError: Optional[CFloat] = None
    weightedPhaseError: Optional[CFloat] = None
    reflectionCorrelation: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPhaseErrorPerformanceStub.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)
