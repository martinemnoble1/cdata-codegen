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

    def loadFile(self):
        """
        Load the XML file and populate fileContent with CAsuContent.

        This method reads the XML file at the path specified by getFullPath()
        and parses it into the fileContent attribute.
        """
        # Check if already loaded
        if hasattr(self, 'fileContent') and self.fileContent is not None:
            return

        # Get the file path
        file_path = self.getFullPath()
        if not file_path:
            print(f"Debug: getFullPath() returned empty for CAsuDataFile")
            return

        print(f"Debug: Loading ASU file from {file_path}")

        # Parse the XML file
        import xml.etree.ElementTree as ET
        from pathlib import Path

        if not Path(file_path).exists():
            return

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Create CAsuContent object
            # Import here to avoid circular imports
            from core.cdata_stubs.CCP4ModelData import CAsuContentStub, CAsuContentSeqStub

            # Find the class - it might be in stubs or in this file
            try:
                from core.CCP4ModelData import CAsuContent
            except ImportError:
                CAsuContent = CAsuContentStub

            try:
                from core.CCP4ModelData import CAsuContentSeq
            except ImportError:
                CAsuContentSeq = CAsuContentSeqStub

            # Create fileContent
            self.fileContent = CAsuContent(parent=self, name='fileContent')

            # Parse sequences from XML
            # Handle namespace
            ns = {'ccp4': 'http://www.ccp4.ac.uk/ccp4ns'}
            body = root.find('.//ccp4i2_body', ns) or root.find('.//ccp4i2_body')

            if body is not None:
                seqList_elem = body.find('seqList')
                if seqList_elem is not None:
                    for seq_elem in seqList_elem.findall('CAsuContentSeq'):
                        seq_obj = CAsuContentSeq(parent=self.fileContent.seqList, name=None)

                        # Parse sequence fields
                        if seq_elem.find('sequence') is not None:
                            seq_obj.sequence = seq_elem.find('sequence').text or ''
                        if seq_elem.find('nCopies') is not None:
                            seq_obj.nCopies = int(seq_elem.find('nCopies').text or '1')
                        if seq_elem.find('polymerType') is not None:
                            seq_obj.polymerType = seq_elem.find('polymerType').text or ''
                        if seq_elem.find('name') is not None:
                            seq_obj.name = seq_elem.find('name').text or ''
                        if seq_elem.find('description') is not None:
                            seq_obj.description = seq_elem.find('description').text or ''

                        # Add to seqList
                        self.fileContent.seqList.append(seq_obj)

        except ET.ParseError as e:
            print(f"Error parsing XML file {file_path}: {e}")
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")

    def writeFasta(
        self,
        fileName: str,
        indx: int = -1,
        format: str = 'fasta',
        writeMulti: bool = False,
        polymerTypes: list = None
    ):
        """
        Write sequences to a FASTA or PIR format file.

        Args:
            fileName: Output file path
            indx: Index of specific sequence to write (-1 for all)
            format: Output format ('fasta' or 'pir')
            writeMulti: Write multiple copies based on nCopies
            polymerTypes: List of polymer types to include (default: PROTEIN, RNA, DNA)
        """
        if polymerTypes is None:
            polymerTypes = ["PROTEIN", "RNA", "DNA"]

        # Load the file to populate fileContent
        self.loadFile()

        # Check if fileContent was populated
        if not hasattr(self, 'fileContent') or self.fileContent is None:
            print(f"Warning: No fileContent loaded from {self.getFullPath()}")
            return

        # Get selection mode from qualifiers if available
        selectionMode = self.get_qualifier('selectionMode', default=0)

        text = ''

        if indx < 0:
            # Write all sequences
            if not hasattr(self.fileContent, 'seqList'):
                return  # No sequences to write

            for seqObj in self.fileContent.seqList:
                # Filter by polymer type
                if str(seqObj.polymerType) not in polymerTypes:
                    continue

                # Determine number of copies to write
                if writeMulti:
                    nCopies = int(seqObj.nCopies)
                else:
                    nCopies = min(1, int(seqObj.nCopies))

                # Write each copy
                for nC in range(nCopies):
                    name = str(seqObj.name)

                    # Check selection if available
                    if selectionMode == 0 or (not hasattr(self, 'selection')) or \
                       (not self.selection.isSet()) or self.selection.get(name, True):

                        # Write FASTA/PIR header
                        text += '>' + name + '\n'
                        if format == 'pir':
                            text += '\n'

                        # Write sequence in 60-character lines
                        seq = str(seqObj.sequence)
                        while len(seq) > 0:
                            text += seq[0:60] + '\n'
                            seq = seq[60:]
        else:
            # Write single sequence by index
            if not hasattr(self.fileContent, 'seqList') or \
               indx >= len(self.fileContent.seqList):
                return

            seqObj = self.fileContent.seqList[indx]

            # Write FASTA/PIR header
            text += '>' + str(seqObj.name) + '\n'
            if format == 'pir':
                text += '\n'

            # Write sequence in 60-character lines
            seq = str(seqObj.sequence)
            while len(seq) > 0:
                text += seq[0:60] + '\n'
                seq = seq[60:]

        # Save to file
        with open(fileName, 'w') as f:
            f.write(text)


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

    def loadFile(self, file_path: str):
        """
        Load PDB or mmCIF coordinate file using gemmi library.

        This method:
        1. Reads coordinate file using gemmi.read_structure()
        2. Stores gemmi Structure object for queries
        3. Handles both PDB and mmCIF formats automatically

        Args:
            file_path: Full path to coordinate file (.pdb, .cif, .ent)

        Returns:
            CErrorReport with any errors encountered

        Example:
            >>> pdb_data = CPdbData()
            >>> error = pdb_data.loadFile('/path/to/model.pdb')
            >>> if error.count() == 0:
            ...     print(f"Loaded structure with {len(pdb_data._gemmi_structure)} models")
        """
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path

        error = CErrorReport()

        # Validate file path
        if not file_path:
            return error

        path_obj = Path(file_path)
        if not path_obj.exists() or not path_obj.is_file():
            error.append(
                klass=self.__class__.__name__,
                code=101,
                details=f"Coordinate file does not exist or is not a file: '{file_path}'",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )
            return error

        try:
            import gemmi
        except ImportError as e:
            error.append(
                klass=self.__class__.__name__,
                code=102,
                details=f"Failed to import gemmi library: {e}",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )
            return error

        try:
            # Read structure using gemmi (handles PDB and mmCIF automatically)
            structure = gemmi.read_structure(str(file_path))

            # Store gemmi Structure object for advanced queries
            # Use object.__setattr__ to bypass smart assignment
            object.__setattr__(self, '_gemmi_structure', structure)

            # Emit signal if available
            if hasattr(self, 'dataChanged'):
                try:
                    self.dataChanged.emit()
                except:
                    pass  # Signal system may not be available

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=103,
                details=f"Error reading coordinate file '{file_path}': {e}",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )

        return error


class CPdbDataFile(CPdbDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None

    Extends CPdbDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def __init__(self, file_path: str = None, parent=None, name=None, **kwargs):
        super().__init__(file_path=file_path, parent=parent, name=name, **kwargs)
        # Set the content class name qualifier
        self.set_qualifier('fileContentClassName', 'CPdbData')

    def _introspect_content_flag(self) -> Optional[int]:
        """Auto-detect contentFlag by determining if file is PDB or mmCIF format.

        Returns:
            1 (CONTENT_FLAG_PDB) if PDB format
            2 (CONTENT_FLAG_MMCIF) if mmCIF format
            None if file cannot be read or format cannot be determined
        """
        from pathlib import Path

        file_path = self.getFullPath()
        if not file_path or not Path(file_path).exists():
            return None

        try:
            # Check the file extension first
            path = Path(file_path)
            suffix = path.suffix.lower()

            # mmCIF files typically have .cif or .mmcif extensions
            if suffix in ['.cif', '.mmcif']:
                return self.__class__.CONTENT_FLAG_MMCIF

            # PDB files typically have .pdb or .ent extensions
            elif suffix in ['.pdb', '.ent']:
                return self.__class__.CONTENT_FLAG_PDB

            # If extension is ambiguous, check file content
            # mmCIF files start with "data_" or have loop structures
            with open(file_path, 'r') as f:
                first_line = f.readline().strip()
                if first_line.startswith('data_') or first_line.startswith('loop_'):
                    return self.__class__.CONTENT_FLAG_MMCIF
                # PDB files typically start with record types like HEADER, CRYST1, ATOM, etc.
                elif first_line.startswith(('HEADER', 'CRYST1', 'ATOM', 'HETATM', 'MODEL')):
                    return self.__class__.CONTENT_FLAG_PDB

            # Default to PDB if we can't determine
            return self.__class__.CONTENT_FLAG_PDB

        except Exception:
            return None

    def setContentFlag(self):
        """
        Introspect the PDB/mmCIF file using gemmi to determine the format type.

        Sets self.contentFlag to:
        - 1 (CONTENT_FLAG_PDB): PDB format
        - 2 (CONTENT_FLAG_MMCIF): mmCIF format
        - 0: If content type cannot be determined

        Returns:
            int: The detected content flag value
        """
        import gemmi
        from pathlib import Path

        input_path = self.getFullPath()
        if not input_path or not Path(input_path).exists():
            self.contentFlag.set(0)
            return 0

        try:
            # Use gemmi to read the structure - it auto-detects format
            structure = gemmi.read_structure(input_path)

            # Check the file extension to determine format
            path = Path(input_path)
            suffix = path.suffix.lower()

            # mmCIF files
            if suffix in ['.cif', '.mmcif']:
                self.contentFlag.set(self.CONTENT_FLAG_MMCIF)
                return self.CONTENT_FLAG_MMCIF
            # PDB files
            elif suffix in ['.pdb', '.ent']:
                self.contentFlag.set(self.CONTENT_FLAG_PDB)
                return self.CONTENT_FLAG_PDB
            else:
                # Default to PDB if ambiguous
                self.contentFlag.set(self.CONTENT_FLAG_PDB)
                return self.CONTENT_FLAG_PDB

        except Exception as e:
            # If gemmi fails, fall back to simple text introspection
            try:
                with open(input_path, 'r') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith('data_') or first_line.startswith('loop_'):
                        self.contentFlag.set(self.CONTENT_FLAG_MMCIF)
                        return self.CONTENT_FLAG_MMCIF
                    else:
                        self.contentFlag.set(self.CONTENT_FLAG_PDB)
                        return self.CONTENT_FLAG_PDB
            except Exception:
                self.contentFlag.set(0)
                return 0

    def fileExtensions(self):
        """
        Return appropriate file extension(s) for CPdbDataFile.

        CPdbDataFile can be either PDB or mmCIF format. We determine which by:
        1. If file exists: introspect using gemmi
        2. If contentFlag is set: use that (2 = mmCIF, other = PDB)
        3. Default: PDB

        Returns:
            list: [primary_extension] - either ['pdb'] or ['mmcif']
        """
        from pathlib import Path

        # Check if file exists and introspect it
        full_path = self.getFullPath()
        if full_path and Path(full_path).exists():
            try:
                # Use gemmi to determine format from actual file
                import gemmi
                structure = gemmi.read_structure(full_path)

                # Check file extension to determine format
                suffix = Path(full_path).suffix.lower()
                if suffix in ['.cif', '.mmcif']:
                    return ['mmcif']
                else:
                    return ['pdb']
            except Exception:
                # If gemmi fails, default to pdb
                return ['pdb']

        # For new files (not yet created), check contentFlag if set
        content_flag = 0
        if hasattr(self, 'contentFlag') and self.contentFlag is not None:
            if hasattr(self.contentFlag, 'value'):
                content_flag = self.contentFlag.value if self.contentFlag.value is not None else 0
            else:
                content_flag = int(self.contentFlag) if self.contentFlag else 0

        # contentFlag: 2 = mmCIF, anything else = PDB (default)
        if content_flag == self.CONTENT_FLAG_MMCIF:
            return ['mmcif']
        else:
            return ['pdb']


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

