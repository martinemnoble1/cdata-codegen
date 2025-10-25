"""
Implementation classes for CCP4ModelData.py

Extends stub classes from core.cdata_stubs with methods and business logic.
This file is safe to edit - add your implementation code here.
"""

from __future__ import annotations
from typing import Optional, Any

from core.cdata_stubs.CCP4ModelData import CAsuContentStub, CAsuContentSeqStub, CAsuContentSeqListStub, CAsuDataFileStub, CAtomRefmacSelectionStub, CAtomRefmacSelectionGroupsStub, CAtomRefmacSelectionListStub, CAtomRefmacSelectionOccupancyStub, CAtomSelectionStub, CBlastDataStub, CBlastDataFileStub, CBlastItemStub, CChemCompStub, CDictDataStub, CDictDataFileStub, CElementStub, CEnsembleStub, CEnsembleListStub, CEnsemblePdbDataFileStub, CHhpredDataStub, CHhpredDataFileStub, CHhpredItemStub, CMDLMolDataFileStub, CMol2DataFileStub, CMonomerStub, COccRefmacSelectionListStub, COccRelationRefmacListStub, CPdbDataStub, CPdbDataFileStub, CPdbDataFileListStub, CPdbEnsembleItemStub, CResidueRangeStub, CResidueRangeListStub, CSeqAlignDataFileStub, CSeqDataFileStub, CSeqDataFileListStub, CSequenceStub, CSequenceAlignmentStub, CSequenceMetaStub, CSequenceStringStub, CTLSDataFileStub


class CAsuContent(CAsuContentStub):
    """
    Base class for classes holding file contents
    
    Extends CAsuContentStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAsuContentSeq(CAsuContentSeqStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CAsuContentSeqStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAsuContentSeqList(CAsuContentSeqListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CAsuContentSeqListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAsuDataFile(CAsuDataFileStub):
    """
    A reference to an XML file with CCP4i2 Header
    
    Extends CAsuDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAtomRefmacSelection(CAtomRefmacSelectionStub):
    """
    A residue range selection for rigid body groups
    
    Extends CAtomRefmacSelectionStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAtomRefmacSelectionGroups(CAtomRefmacSelectionGroupsStub):
    """
    A group selection for occupancy groups
    
    Extends CAtomRefmacSelectionGroupsStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAtomRefmacSelectionList(CAtomRefmacSelectionListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CAtomRefmacSelectionListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAtomRefmacSelectionOccupancy(CAtomRefmacSelectionOccupancyStub):
    """
    A residue range selection for occupancy groups
    
    Extends CAtomRefmacSelectionOccupancyStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAtomSelection(CAtomSelectionStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CAtomSelectionStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CBlastData(CBlastDataStub):
    """
    Base class for classes holding file contents
    
    Extends CBlastDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CBlastDataFile(CBlastDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CBlastDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CBlastItem(CBlastItemStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CBlastItemStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CChemComp(CChemCompStub):
    """
    Component of CDictDataFile contents
    
    Extends CChemCompStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDictData(CDictDataStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CDictDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDictDataFile(CDictDataFileStub):
    """
    A refmac dictionary file
    
    Extends CDictDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CElement(CElementStub):
    """
    Chemical element 
    
    Extends CElementStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CEnsemble(CEnsembleStub):
    """
    An ensemble of models. Typically, this would be a set of related
PDB files, but models could also be xtal or EM maps. This should
be indicated by the types entry.
A single ensemble is a CList of structures.
    
    Extends CEnsembleStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CEnsembleList(CEnsembleListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CEnsembleListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CEnsemblePdbDataFile(CEnsemblePdbDataFileStub):
    """
    A PDB coordinate file containing ensemble of structures as 'NMR' models
    
    Extends CEnsemblePdbDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CHhpredData(CHhpredDataStub):
    """
    Base class for classes holding file contents
    
    Extends CHhpredDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CHhpredDataFile(CHhpredDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CHhpredDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CHhpredItem(CHhpredItemStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CHhpredItemStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMDLMolDataFile(CMDLMolDataFileStub):
    """
    A molecule definition file (MDL)
    
    Extends CMDLMolDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMol2DataFile(CMol2DataFileStub):
    """
    A molecule definition file (MOL2)
    
    Extends CMol2DataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMonomer(CMonomerStub):
    """
    A monomer compound. ?smiles
    
    Extends CMonomerStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class COccRefmacSelectionList(COccRefmacSelectionListStub):
    """
    A list with all items of one CData sub-class
    
    Extends COccRefmacSelectionListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class COccRelationRefmacList(COccRelationRefmacListStub):
    """
    A list with all items of one CData sub-class
    
    Extends COccRelationRefmacListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPdbData(CPdbDataStub):
    """
    Contents of a PDB file - a subset with functionality for GUI
    
    Extends CPdbDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPdbDataFile(CPdbDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CPdbDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPdbDataFileList(CPdbDataFileListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CPdbDataFileListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPdbEnsembleItem(CPdbEnsembleItemStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CPdbEnsembleItemStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CResidueRange(CResidueRangeStub):
    """
    A residue range selection
    
    Extends CResidueRangeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CResidueRangeList(CResidueRangeListStub):
    """
    A list of residue range selections
    
    Extends CResidueRangeListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSeqAlignDataFile(CSeqAlignDataFileStub):
    """
    A (multiple) sequence alignment file
    
    Extends CSeqAlignDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSeqDataFile(CSeqDataFileStub):
    """
    A sequence file
    
    Extends CSeqDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSeqDataFileList(CSeqDataFileListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CSeqDataFileListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSequence(CSequenceStub):
    """
    A string of sequence one-letter codes
Need to be able to parse common seq file formats
Do we need to support alternative residues
What about nucleic/polysach?
    
    Extends CSequenceStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSequenceAlignment(CSequenceAlignmentStub):
    """
    An alignment of two or more sequences.
Each sequence is obviously related to class CSequence, but
will also contain gaps relevant to the alignment. We could
implement the contents as a list of CSequence objects?
The alignment is typically formatted in a file as consecutive 
or interleaved sequences.
    
    Extends CSequenceAlignmentStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSequenceMeta(CSequenceMetaStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CSequenceMetaStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSequenceString(CSequenceStringStub):
    """
    A string
    
    Extends CSequenceStringStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CTLSDataFile(CTLSDataFileStub):
    """
    A refmac TLS file
    
    Extends CTLSDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass

