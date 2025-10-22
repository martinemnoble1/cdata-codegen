"""Auto-generated from CCP4i2 metadata. DO NOT EDIT.

To extend these classes, create subclasses in core/extensions/
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Any

# Metadata system
from core.base_object.class_metadata import cdata_class, attribute, AttributeType

# Base classes
from core.base_object.base_classes import CData

# Fundamental types
from core.base_object.fundamental_types import CFloat, CInt, CString

# Cross-file class references
from core.generated.CCP4XtalData import CSpaceGroup


@cdata_class(
    attributes={
        "value": attribute(AttributeType.FLOAT, tooltip="value attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
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
class CPerformanceIndicator(CData):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    value: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPerformanceIndicator.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RFactor": attribute(AttributeType.FLOAT, tooltip="RFactor attribute"),
        "completeness": attribute(AttributeType.FLOAT, tooltip="completeness attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
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
class CModelBuildPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    RFactor: Optional[CFloat] = None
    completeness: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CModelBuildPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "cutoff": attribute(AttributeType.FLOAT, tooltip="cutoff attribute"),
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
class CPairefPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    cutoff: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPairefPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroup", tooltip="spaceGroup attribute"),
        "highResLimit": attribute(AttributeType.FLOAT, tooltip="highResLimit attribute"),
        "rMeas": attribute(AttributeType.FLOAT, tooltip="rMeas attribute"),
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
class CDataReductionPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    spaceGroup: Optional[CSpaceGroup] = None
    highResLimit: Optional[CFloat] = None
    rMeas: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDataReductionPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "phaseError": attribute(AttributeType.FLOAT, tooltip="phaseError attribute"),
        "weightedPhaseError": attribute(AttributeType.FLOAT, tooltip="weightedPhaseError attribute"),
        "reflectionCorrelation": attribute(AttributeType.FLOAT, tooltip="reflectionCorrelation attribute"),
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
class CPhaseErrorPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    phaseError: Optional[CFloat] = None
    weightedPhaseError: Optional[CFloat] = None
    reflectionCorrelation: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CPhaseErrorPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "spaceGroup": attribute(AttributeType.CUSTOM, custom_class="CSpaceGroup", tooltip="spaceGroup attribute"),
        "highResLimit": attribute(AttributeType.FLOAT, tooltip="highResLimit attribute"),
        "ccHalf": attribute(AttributeType.FLOAT, tooltip="ccHalf attribute"),
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
class CDataReductionCCPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    spaceGroup: Optional[CSpaceGroup] = None
    highResLimit: Optional[CFloat] = None
    ccHalf: Optional[CFloat] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CDataReductionCCPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "columnLabelsString": attribute(AttributeType.STRING, tooltip="columnLabelsString attribute"),
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
class CTestObsConversionsPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    columnLabelsString: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CTestObsConversionsPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RMSxyz": attribute(AttributeType.FLOAT, tooltip="RMSxyz attribute"),
        "nResidues": attribute(AttributeType.INT, tooltip="nResidues attribute"),
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
class CSuperposePerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    RMSxyz: Optional[CFloat] = None
    nResidues: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CSuperposePerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RFactor": attribute(AttributeType.FLOAT, tooltip="RFactor attribute"),
        "RFree": attribute(AttributeType.FLOAT, tooltip="RFree attribute"),
        "RMSBond": attribute(AttributeType.FLOAT, tooltip="RMSBond attribute"),
        "RMSAngle": attribute(AttributeType.FLOAT, tooltip="RMSAngle attribute"),
        "weightUsed": attribute(AttributeType.FLOAT, tooltip="weightUsed attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
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
class CRefinementPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    RFactor: Optional[CFloat] = None
    RFree: Optional[CFloat] = None
    RMSBond: Optional[CFloat] = None
    RMSAngle: Optional[CFloat] = None
    weightUsed: Optional[CFloat] = None
    annotation: Optional[CString] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CRefinementPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "nAtoms": attribute(AttributeType.INT, tooltip="nAtoms attribute"),
        "nResidues": attribute(AttributeType.INT, tooltip="nResidues attribute"),
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
class CAtomCountPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

    nAtoms: Optional[CInt] = None
    nResidues: Optional[CInt] = None

    def __init__(self, parent=None, name=None, **kwargs):
        """
        Initialize CAtomCountPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "FOM": attribute(AttributeType.FLOAT, tooltip="FOM attribute"),
        "CFOM": attribute(AttributeType.FLOAT, tooltip="CFOM attribute"),
        "Hand1Score": attribute(AttributeType.FLOAT, tooltip="Hand1Score attribute"),
        "Hand2Score": attribute(AttributeType.FLOAT, tooltip="Hand2Score attribute"),
        "CC": attribute(AttributeType.FLOAT, tooltip="CC attribute"),
        "RFactor": attribute(AttributeType.FLOAT, tooltip="RFactor attribute"),
        "RFree": attribute(AttributeType.FLOAT, tooltip="RFree attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
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
class CExpPhasPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

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
        Initialize CExpPhasPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)


@cdata_class(
    attributes={
        "RFactor": attribute(AttributeType.FLOAT, tooltip="RFactor attribute"),
        "RFree": attribute(AttributeType.FLOAT, tooltip="RFree attribute"),
        "R": attribute(AttributeType.FLOAT, tooltip="R attribute"),
        "R1Factor": attribute(AttributeType.FLOAT, tooltip="R1Factor attribute"),
        "R1Free": attribute(AttributeType.FLOAT, tooltip="R1Free attribute"),
        "R1": attribute(AttributeType.FLOAT, tooltip="R1 attribute"),
        "CCFwork_avg": attribute(AttributeType.FLOAT, tooltip="CCFwork_avg attribute"),
        "CCFfree_avg": attribute(AttributeType.FLOAT, tooltip="CCFfree_avg attribute"),
        "CCF_avg": attribute(AttributeType.FLOAT, tooltip="CCF_avg attribute"),
        "CCIwork_avg": attribute(AttributeType.FLOAT, tooltip="CCIwork_avg attribute"),
        "CCIfree_avg": attribute(AttributeType.FLOAT, tooltip="CCIfree_avg attribute"),
        "CCI_avg": attribute(AttributeType.FLOAT, tooltip="CCI_avg attribute"),
        "FSCaverage": attribute(AttributeType.FLOAT, tooltip="FSCaverage attribute"),
        "annotation": attribute(AttributeType.STRING, tooltip="annotation attribute"),
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
class CServalcatPerformance(CPerformanceIndicator):
    """QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None"""

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
        Initialize CServalcatPerformance.

        Args:
            parent: Parent object in hierarchy
            name: Object name
            **kwargs: Additional keyword arguments
        """
        super().__init__(parent=parent, name=name, **kwargs)
