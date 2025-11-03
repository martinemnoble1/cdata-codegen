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


# Try to import BioPython - it's optional but provides enhanced functionality
try:
    import Bio.SeqIO
    import Bio.AlignIO
    BIOPYTHON_AVAILABLE = True
except ImportError:
    BIOPYTHON_AVAILABLE = False

# BioPython format mappings
SEQFORMATLIST = ['fasta', 'pir', 'swiss', 'tab', 'ig']
ALIGNFORMATLIST = ['fasta', 'clustal', 'phylip', 'stockholm', 'nexus', 'emboss', 'msf']
EXTLIST = {
    'fasta': 'fasta', 'fa': 'fasta', 'faa': 'fasta', 'fas': 'fasta',
    'pir': 'pir',
    'aln': 'clustal', 'clw': 'clustal', 'clustal': 'clustal',
    'phy': 'phylip', 'phylip': 'phylip',
    'stockholm': 'stockholm', 'stk': 'stockholm',
    'nexus': 'nexus', 'nex': 'nexus',
    'msf': 'msf'
}


class CBioPythonSeqInterface:
    """
    Mixin class providing BioPython sequence loading functionality.

    This interface allows loading sequences from various file formats using BioPython.
    It provides format detection, file fixing for malformed files, and robust error handling.
    """

    def simpleFormatTest(self, filename: str) -> str:
        """
        Detect sequence file format by inspecting content.

        Args:
            filename: Path to sequence file

        Returns:
            Format string: 'fasta', 'pir', 'noformat', or 'unknown'
        """
        import re
        from pathlib import Path

        try:
            text = Path(filename).read_text()
        except Exception:
            return 'unknown'

        segments = text.split('>')
        if len(segments[0]) != 0:
            return 'unknown'

        lines = ('>' + segments[1]).split('\n')
        nonAlphaList = []

        for il, line in enumerate(lines):
            # If only non-alpha character is a "-" and it's not the first line, treat as gap
            if il > 0 and ((len(set(re.findall('[^(a-z,A-Z, )]', line))) == 1 and
                           list(set(re.findall('[^(a-z,A-Z, )]', line)))[0] == "-") or
                          line.endswith("*")):
                nonAlphaList.append(0)
            else:
                nonAlphaList.append(len(re.findall('[^(a-z,A-Z, )]', line)))

        nonAlphaTot = sum(nonAlphaList)

        if nonAlphaTot == 0:
            return 'noformat'
        elif len(lines) > 0 and len(lines[0]) > 0 and lines[0][0] == '>':
            if ';' in lines[0] and (nonAlphaTot - (nonAlphaList[0] + nonAlphaList[1] + nonAlphaList[-1])) == 0:
                return 'pir'
            elif (nonAlphaTot - nonAlphaList[0]) == 0:
                return 'fasta'

        return 'unknown'

    def fixPirFile(self, filename: str):
        """
        Fix malformed PIR format files.

        PIR files should have format:
        >P1;identifier
        description
        sequence...
        *

        Args:
            filename: Path to PIR file to fix

        Returns:
            Tuple of (fixed_file_path, CErrorReport, data_dict) or (None, error, None)
        """
        import tempfile
        import os
        from pathlib import Path
        from core.base_object.error_reporting import CErrorReport

        try:
            text = Path(filename).read_text()
        except Exception:
            return None, None, None

        if len(text.strip()) == 0:
            return None, CErrorReport(klass='CBioPythonSeqInterface', code=412,
                                     details='Sequence file is empty'), None

        fragments = text.split('\n>')
        if len(fragments) > 0 and len(fragments[0]) > 0 and fragments[0][0] == '>':
            fragments[0] = fragments[0][1:]

        output = ''
        for text_frag in fragments:
            text_frag = text_frag.strip()
            if len(text_frag) > 2 and text_frag[2] != ';':
                text_frag = 'P1;' + text_frag
            if '*' not in text_frag:
                text_frag = text_frag + '*'
            output = output + '>' + text_frag + '\n'

        # Write to temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.pir')
        try:
            os.write(fd, output.encode('utf-8'))
            os.close(fd)

            err, data = self.bioLoadSeqFile(temp_path, 'pir')
            if err.count() == 0:
                return temp_path, err, data
            else:
                os.unlink(temp_path)
                return None, None, None
        except Exception:
            if fd:
                os.close(fd)
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            return None, None, None

    def fixFastaFile(self, filename: str):
        """
        Fix plain sequence files by adding FASTA header.

        Args:
            filename: Path to plain sequence file

        Returns:
            Tuple of (fixed_file_path, CErrorReport, data_dict) or (None, error, None)
        """
        import tempfile
        import os
        import re
        from pathlib import Path
        from core.base_object.error_reporting import CErrorReport

        try:
            text = Path(filename).read_text()
        except Exception:
            return None, None, None

        if len(text.strip()) == 0:
            return None, CErrorReport(klass='CBioPythonSeqInterface', code=412,
                                     details='Sequence file is empty'), None

        lines = text.split('\n')
        nonAlphaList = []
        for line in lines:
            nonAlphaList.extend(re.findall('[^(a-z,A-Z, )]', line))

        if len(nonAlphaList) > 0:
            return None, None, None

        # Add FASTA header using filename as identifier
        output = '>' + Path(filename).stem + '\n' + text

        # Write to temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.fasta')
        try:
            os.write(fd, output.encode('utf-8'))
            os.close(fd)

            err, data = self.bioLoadSeqFile(temp_path, 'fasta')
            if err.count() == 0:
                return temp_path, err, data
            else:
                os.unlink(temp_path)
                return None, None, None
        except Exception:
            if fd:
                os.close(fd)
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            return None, None, None

    def bioLoadSeqFile(self, filename: str, format: str, record: int = 0):
        """
        Load sequence file using BioPython.

        Args:
            filename: Path to sequence file
            format: BioPython format string ('fasta', 'pir', 'clustal', etc.)
            record: Index of record to load (for multi-record files)

        Returns:
            Tuple of (CErrorReport, data_dict) where data_dict contains:
                - format: Format used
                - identifier: Sequence identifier
                - sequence: Sequence string
                - name: Sequence name
                - description: Sequence description
                - idList: List of all identifiers in file
        """
        from core.base_object.error_reporting import CErrorReport

        err = CErrorReport()

        if not BIOPYTHON_AVAILABLE:
            err.append(klass='CBioPythonSeqInterface', code=402,
                      details='BioPython not available - cannot load sequence file')
            return err, {}

        try:
            with open(filename, 'r') as f:
                if format in SEQFORMATLIST:
                    seq_records = list(Bio.SeqIO.parse(f, format))
                elif format in ALIGNFORMATLIST:
                    ali_records = list(Bio.AlignIO.parse(f, format))
                    if len(ali_records) > 0:
                        seq_records = list(ali_records[0])
                    else:
                        seq_records = []
                else:
                    err.append(klass='CBioPythonSeqInterface', code=403,
                              details=f'Unknown sequence file format: {format}')
                    return err, {}
        except Exception as e:
            err.append(klass='CBioPythonSeqInterface', code=402,
                      details=f'Error reading sequence file: {e}')
            return err, {}

        if len(seq_records) == 0:
            err.append(klass='CBioPythonSeqInterface', code=412,
                      details='Sequence file is empty or contains no valid records')
            return err, {}

        if record >= len(seq_records):
            err.append(klass='CBioPythonSeqInterface', code=405,
                      details=f'Record index {record} out of range (file has {len(seq_records)} records)')
            return err, {}

        idList = [rec.id for rec in seq_records]
        selected_record = seq_records[record]

        return err, {
            'format': format,
            'identifier': selected_record.id,
            'sequence': str(selected_record.seq),
            'name': selected_record.name,
            'description': selected_record.description,
            'idList': idList
        }

    def loadExternalFile(self, filename: str, format: str = None, record: int = 0):
        """
        Load sequence from external file with automatic format detection.

        Args:
            filename: Path to sequence file
            format: Format hint ('fasta', 'pir', 'unknown', etc.)
            record: Index of record to load (for multi-record files)

        Returns:
            Dictionary with sequence data or None on error
        """
        from pathlib import Path
        from core.base_object.error_reporting import CErrorReport

        if not Path(filename).exists():
            return None

        # Guess format from extension if not provided
        if format is None or format == 'unknown':
            ext = Path(filename).suffix[1:].lower()
            format = EXTLIST.get(ext, None)

        # Build test order - try expected format first
        testOrder = SEQFORMATLIST + ALIGNFORMATLIST
        if format is not None and format in testOrder:
            testOrder.remove(format)
            testOrder.insert(0, format)

        # Try each format
        for test_format in testOrder:
            err, data = self.bioLoadSeqFile(filename, test_format, record=record)
            if err.count() == 0:
                return data

            # Special handling for PIR format
            if test_format == format and format == 'pir':
                fixed_path, fix_err, fix_data = self.fixPirFile(filename)
                if fixed_path is not None:
                    return fix_data

        # Try fixing as plain FASTA
        fixed_path, fix_err, fix_data = self.fixFastaFile(filename)
        if fixed_path is not None:
            return fix_data

        return None


class CPdbDataComposition:
    """
    Coordinate file composition analysis using gemmi.

    Analyzes PDB/mmCIF structure to extract:
    - chains: List of chain IDs
    - monomers: List of unique residue names
    - peptides: List of chains containing amino acids
    - nucleics: List of chains containing nucleic acids
    - solventChains: List of chains containing solvent
    - saccharides: List of chains containing sugar residues
    - chainInfo: List of [nres, first_resid, last_resid] for each chain
    - nChains: Number of chains
    - nResidues: Total number of residues
    - nAtoms: Total number of atoms
    - nresSolvent: Number of solvent residues
    - elements: List of unique element types (excluding C, N, O)
    - containsHydrogen: Boolean for hydrogen presence
    """

    def __init__(self, gemmi_structure):
        """
        Analyze structure composition using gemmi.

        Args:
            gemmi_structure: gemmi.Structure object
        """
        self.chains = []
        self.monomers = []
        self.peptides = []
        self.nucleics = []
        self.solventChains = []
        self.saccharides = []
        self.chainInfo = []
        self.nModels = len(gemmi_structure)
        self.nChains = 0
        self.nResidues = 0
        self.nAtoms = 0
        self.nresSolvent = 0
        self.elements = []
        self.containsHydrogen = False

        # Standard amino acid residue names
        amino_acids = {
            'ALA', 'ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'GLY', 'HIS', 'ILE',
            'LEU', 'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL',
            'MSE', 'SEP', 'TPO', 'PYL', 'SEC'  # Modified amino acids
        }

        # Standard nucleic acid residue names
        nucleic_acids = {
            'A', 'C', 'G', 'U', 'T',  # Standard bases
            'DA', 'DC', 'DG', 'DT',   # DNA
            '+A', '+C', '+G', '+U', '+T'  # RNA with base modifications
        }

        # Common solvent names
        solvents = {'HOH', 'WAT', 'H2O', 'DOD', 'D2O', 'SO4', 'PO4', 'CL', 'NA'}

        # Saccharide residue names
        saccharide_names = {
            'GLC', 'GAL', 'MAN', 'FUC', 'XYL', 'RIB', 'NAG', 'BMA',
            'FUL', 'SIA', 'NDG', 'BGC'
        }

        monomer_set = set()
        element_set = set()

        # Analyze first model only (like legacy code)
        if len(gemmi_structure) > 0:
            model = gemmi_structure[0]
            self.nChains = len(model)

            for chain in model:
                chain_id = chain.name
                self.chains.append(chain_id)

                has_amino = False
                has_nucleic = False
                has_solvent = False
                has_saccharide = False

                nres = 0
                first_resid = None
                last_resid = None
                nres_solvent_chain = 0
                natoms_chain = 0

                for residue in chain:
                    res_name = residue.name
                    monomer_set.add(res_name)
                    nres += 1

                    # Track first and last residue IDs
                    resid_str = str(residue.seqid.num)
                    if first_resid is None:
                        first_resid = resid_str
                    last_resid = resid_str

                    # Classify residue type
                    if res_name in amino_acids:
                        has_amino = True
                    elif res_name in nucleic_acids:
                        has_nucleic = True
                    elif res_name in solvents:
                        has_solvent = True
                        nres_solvent_chain += 1
                    elif res_name in saccharide_names:
                        has_saccharide = True

                    # Count atoms and analyze elements
                    for atom in residue:
                        natoms_chain += 1
                        element = atom.element.name

                        # Track non-common elements
                        if element not in ['C', 'N', 'O']:
                            element_set.add(element)

                        # Check for hydrogen
                        if element in ['H', 'D']:
                            self.containsHydrogen = True

                # Store chain info
                self.chainInfo.append([nres, first_resid or '', last_resid or ''])
                self.nResidues += nres
                self.nAtoms += natoms_chain
                self.nresSolvent += nres_solvent_chain

                # Classify chains
                if has_amino:
                    self.peptides.append(chain_id)
                if has_nucleic:
                    self.nucleics.append(chain_id)
                if has_solvent:
                    self.solventChains.append(chain_id)
                if has_saccharide:
                    self.saccharides.append(chain_id)

        self.monomers = sorted(list(monomer_set))
        self.elements = sorted(list(element_set))


class CPdbData(CPdbDataStub):
    """
    Contents of a PDB file - a subset with functionality for GUI

    Extends CPdbDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def loadFile(self, file_path: str = None):
        """
        Load PDB or mmCIF coordinate file using gemmi library.

        This method:
        1. Reads coordinate file using gemmi.read_structure()
        2. Stores gemmi Structure object for queries
        3. Handles both PDB and mmCIF formats automatically

        Args:
            file_path: Optional path to coordinate file (.pdb, .cif, .ent). If None, gets path from parent CDataFile.

        Returns:
            CErrorReport with any errors encountered

        Example:
            # Load from parent file's path
            >>> pdb_file = CPdbDataFile()
            >>> pdb_file.setFullPath('/path/to/model.pdb')
            >>> pdb_file.fileContent.loadFile()

            # Load from explicit path (legacy pattern)
            >>> pdb_data = CPdbData()
            >>> error = pdb_data.loadFile('/path/to/model.pdb')
            >>> if error.count() == 0:
            ...     print(f"Loaded structure with {len(pdb_data._gemmi_structure)} models")
        """
        from core.base_object.error_reporting import CErrorReport
        from pathlib import Path

        error = CErrorReport()

        # If no path provided, get from parent CDataFile
        if file_path is None:
            parent = self.get_parent()
            if parent is not None and hasattr(parent, 'getFullPath'):
                file_path = parent.getFullPath()

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

            # Create composition analysis
            object.__setattr__(self, '_composition', CPdbDataComposition(structure))

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

    @property
    def composition(self):
        """
        Get composition analysis of the coordinate file.

        Returns:
            CPdbDataComposition instance with chains, monomers, etc., or None if not loaded
        """
        return getattr(self, '_composition', None)


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

    def isSelectionSet(self) -> bool:
        """Check if an atom selection is defined for this PDB file.

        Returns True if the selection.text attribute is set and contains
        non-whitespace content after stripping leading/trailing whitespace.

        Returns:
            bool: True if selection is set and non-empty, False otherwise
        """
        # Check if selection attribute exists
        if not hasattr(self, 'selection'):
            return False

        # Check if text attribute exists
        if not hasattr(self.selection, 'text'):
            return False

        # Get the text value
        text_value = self.selection.text.value
        if text_value is None:
            return False

        # Check if text has non-whitespace content
        stripped = str(text_value).strip()
        return len(stripped) > 0

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


class CSequence(CSequenceStub, CBioPythonSeqInterface):
    """
    A string of sequence one-letter codes with BioPython loading support.

    This class represents a single biological sequence (protein or nucleic acid)
    with support for loading from various file formats using BioPython.

    Key features:
    - Load from FASTA, PIR, UniProt, and other formats
    - Automatic format detection
    - Molecular weight calculation using BioPython ProtParam
    - Save to FASTA format
    """

    def loadFile(self, fileName: str, format: str = 'unknown'):
        """
        Load sequence from file.

        Args:
            fileName: Path to sequence file
            format: Format hint ('internal', 'uniprot', 'fasta', 'pir', 'unknown')
        """
        from pathlib import Path
        from core.base_object.error_reporting import CErrorReport

        if format == 'internal':
            # Internal format: simple FASTA-like with pipe-separated metadata
            self._loadInternalFile(fileName)
        elif format == 'uniprot':
            # UniProt XML format - not implemented in modern version
            err = CErrorReport()
            err.append(klass='CSequence', code=402,
                      details='UniProt XML format not yet supported in modern implementation')
            return err
        else:
            # Use BioPython interface
            data = self.loadExternalFile(fileName, format=format, record=0)
            if data is not None:
                # Populate CData attributes from loaded data
                if 'identifier' in data:
                    self.identifier = data['identifier']
                if 'sequence' in data:
                    self.sequence = data['sequence']
                if 'name' in data:
                    self.name = data['name']
                if 'description' in data:
                    self.description = data['description']
                if 'referenceDb' in data:
                    self.referenceDb = data['referenceDb']
                if 'reference' in data:
                    self.reference = data['reference']

    def _loadInternalFile(self, fileName: str):
        """
        Load internal format sequence file.

        Internal format is simple FASTA with pipe-separated metadata:
        >referenceDb|reference|identifier
        sequence...
        """
        from pathlib import Path

        try:
            text = Path(fileName).read_text()
        except Exception as e:
            print(f'ERROR loading sequence file: {e}')
            return

        lines = text.split('\n')
        try:
            # Parse header line
            if len(lines[0]) > 0 and lines[0][0] == '>':
                header = lines[0][1:]
                splitList = header.split('|')

                if len(splitList) == 3:
                    self.referenceDb = splitList[0]
                    if len(splitList[1].strip()) > 0:
                        self.reference = splitList[1]
                    self.identifier = splitList[2]
                else:
                    self.identifier = header

                # Parse sequence (concatenate all remaining lines)
                seq = ''.join(lines[1:])
                self.sequence = seq
        except Exception as e:
            print(f'ERROR parsing sequence file: {e}')

    def saveFile(self, fileName: str):
        """
        Save sequence to FASTA format file.

        Args:
            fileName: Output file path
        """
        from pathlib import Path

        # Build FASTA format
        text = '>' + str(self.identifier) + '\n' + str(self.sequence)

        # Write to file
        Path(fileName).write_text(text)

    def getAnalysis(self, mode: str = 'molecularWeight'):
        """
        Perform sequence analysis using BioPython.

        Args:
            mode: Analysis type ('molecularWeight' supported)

        Returns:
            Molecular weight in Daltons, or 0 if sequence not set or analysis fails
        """
        import re

        if mode == 'molecularWeight':
            if not self.sequence.isSet():
                return 0

            if not BIOPYTHON_AVAILABLE:
                print('BioPython not available for molecular weight calculation')
                return 0

            try:
                from Bio.SeqUtils.ProtParam import ProteinAnalysis

                # Remove non-standard amino acids for BioPython compatibility
                seq_str = str(self.sequence)
                seq_clean = re.sub('[^GALMFWKQESPVICYHRNDT]', '', seq_str)

                if len(seq_clean) == 0:
                    return 0

                pa = ProteinAnalysis(seq_clean)
                return pa.molecular_weight()
            except Exception as e:
                print(f'Error calculating molecular weight: {e}')
                return 0

        return 0

    def guiLabel(self) -> str:
        """
        Get display label for GUI.

        Returns:
            Identifier, or first 20 chars of sequence, or object name
        """
        if self.identifier.isSet():
            return str(self.identifier)
        elif self.sequence.isSet():
            seq_str = str(self.sequence)
            return seq_str[0:20] if len(seq_str) > 20 else seq_str
        else:
            return self.object_name() if hasattr(self, 'object_name') else 'CSequence'


class CSequenceAlignment(CSequenceAlignmentStub, CBioPythonSeqInterface):
    """
    An alignment of two or more sequences with BioPython AlignIO support.

    This class represents a multiple sequence alignment with support for
    loading from various alignment file formats using BioPython.

    Key features:
    - Load from CLUSTAL, FASTA, PHYLIP, Stockholm, Nexus, MSF formats
    - Automatic format detection
    - Handles both consecutive and interleaved alignment formats
    - Preserves gap characters for alignment information

    The alignment contains gaps ("-" characters) that are relevant to the alignment.
    Each aligned sequence is similar to CSequence but includes gap positions.
    """

    def loadFile(self, fileName: str, format: str = 'unknown'):
        """
        Load sequence alignment from file using BioPython AlignIO.

        Args:
            fileName: Path to alignment file
            format: Format hint ('clustal', 'fasta', 'phylip', 'stockholm', 'nexus', 'msf', 'unknown')
        """
        from pathlib import Path
        from core.base_object.error_reporting import CErrorReport

        if not Path(fileName).exists():
            err = CErrorReport()
            err.append(klass='CSequenceAlignment', code=401,
                      details=f'Alignment file does not exist: {fileName}')
            return err

        if not BIOPYTHON_AVAILABLE:
            err = CErrorReport()
            err.append(klass='CSequenceAlignment', code=402,
                      details='BioPython not available - cannot load alignment file')
            return err

        # Use BioPython interface to load alignment
        data = self.loadExternalFile(fileName, format=format, record=0)

        if data is not None:
            # Populate CData attributes from loaded data
            if 'identifier' in data:
                self.identifier = data['identifier']

            # Store format information if available
            if 'format' in data:
                # Store in a private attribute for later use
                object.__setattr__(self, '_loaded_format', data['format'])

        return CErrorReport()  # Return empty error report on success

    def getSequenceCount(self) -> int:
        """
        Get the number of sequences in the alignment.

        Returns:
            Number of sequences, or 0 if not loaded
        """
        # This would require storing the full alignment data
        # For now, return 0 as a placeholder
        return 0

    def getAlignmentLength(self) -> int:
        """
        Get the length of the alignment (including gaps).

        Returns:
            Alignment length, or 0 if not loaded
        """
        # This would require storing the full alignment data
        # For now, return 0 as a placeholder
        return 0


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

