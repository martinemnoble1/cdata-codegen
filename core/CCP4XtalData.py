"""
Implementation classes for CCP4XtalData.py

Extends stub classes from core.cdata_stubs with methods and business logic.
This file is safe to edit - add your implementation code here.
"""

from __future__ import annotations
from typing import Optional, Any

from core.base_object.error_reporting import CErrorReport
from core.cdata_stubs.CCP4XtalData import CAltSpaceGroupStub, CAltSpaceGroupListStub, CAnomalousColumnGroupStub, CAnomalousIntensityColumnGroupStub, CAnomalousScatteringElementStub, CAsuComponentStub, CAsuComponentListStub, CCellStub, CCellAngleStub, CCellLengthStub, CColumnGroupStub, CColumnGroupItemStub, CColumnGroupListStub, CColumnTypeStub, CColumnTypeListStub, CCrystalNameStub, CDatasetStub, CDatasetListStub, CDatasetNameStub, CDialsJsonFileStub, CDialsPickleFileStub, CExperimentalDataTypeStub, CFPairColumnGroupStub, CFSigFColumnGroupStub, CFormFactorStub, CFreeRColumnGroupStub, CFreeRDataFileStub, CGenericReflDataFileStub, CHLColumnGroupStub, CIPairColumnGroupStub, CISigIColumnGroupStub, CImageFileStub, CImageFileListStub, CImosflmXmlDataFileStub, CImportUnmergedStub, CImportUnmergedListStub, CMapCoeffsDataFileStub, CMapColumnGroupStub, CMapDataFileStub, CMergeMiniMtzStub, CMergeMiniMtzListStub, CMiniMtzDataFileStub, CMiniMtzDataFileListStub, CMmcifReflDataStub, CMmcifReflDataFileStub, CMtzColumnStub, CMtzColumnGroupStub, CMtzColumnGroupTypeStub, CMtzDataStub, CMtzDataFileStub, CMtzDatasetStub, CObsDataFileStub, CPhaserRFileDataFileStub, CPhaserSolDataFileStub, CPhiFomColumnGroupStub, CPhsDataFileStub, CProgramColumnGroupStub, CProgramColumnGroup0Stub, CRefmacKeywordFileStub, CReindexOperatorStub, CResolutionRangeStub, CRunBatchRangeStub, CRunBatchRangeListStub, CShelxFADataFileStub, CShelxLabelStub, CSpaceGroupStub, CSpaceGroupCellStub, CUnmergedDataContentStub, CUnmergedDataFileStub, CUnmergedDataFileListStub, CUnmergedMtzDataFileStub, CWavelengthStub, CXia2ImageSelectionStub, CXia2ImageSelectionListStub
from core.CCP4TaskManager import TASKMANAGER

class CAltSpaceGroup(CAltSpaceGroupStub):
    """
    A string holding the space group
    
    Extends CAltSpaceGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAltSpaceGroupList(CAltSpaceGroupListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CAltSpaceGroupListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAnomalousColumnGroup(CAnomalousColumnGroupStub):
    """
    Selection of F/I and AnomF/I columns from MTZ.
Expected to be part of ab initio phasing dataset ( CDataset)
    
    Extends CAnomalousColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAnomalousIntensityColumnGroup(CAnomalousIntensityColumnGroupStub):
    """
    Selection of I and AnomI columns from MTZ.
Expected to be part of ab initio phasing dataset ( CDataset)
    
    Extends CAnomalousIntensityColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAnomalousScatteringElement(CAnomalousScatteringElementStub):
    """
    Definition of a anomalous scattering element
    
    Extends CAnomalousScatteringElementStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAsuComponent(CAsuComponentStub):
    """
    A component of the asymmetric unit. This is for use in MR, defining
what we are searching for. 
    
    Extends CAsuComponentStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CAsuComponentList(CAsuComponentListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CAsuComponentListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CCell(CCellStub):
    """
    A unit cell
    
    Extends CCellStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CCellAngle(CCellAngleStub):
    """
    A cell angle
    
    Extends CCellAngleStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CCellLength(CCellLengthStub):
    """
    A cell length
    
    Extends CCellLengthStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CColumnGroup(CColumnGroupStub):
    """
    Groups of columns in MTZ - probably from analysis by hklfile
    
    Extends CColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CColumnGroupItem(CColumnGroupItemStub):
    """
    Definition of set of columns that form a 'group'
    
    Extends CColumnGroupItemStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CColumnGroupList(CColumnGroupListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CColumnGroupListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CColumnType(CColumnTypeStub):
    """
    A list of recognised MTZ column types
    
    Extends CColumnTypeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CColumnTypeList(CColumnTypeListStub):
    """
    A list of acceptable MTZ column types
    
    Extends CColumnTypeListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CCrystalName(CCrystalNameStub):
    """
    A string
    
    Extends CCrystalNameStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDataset(CDatasetStub):
    """
    The experimental data model for ab initio phasing
    
    Extends CDatasetStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDatasetList(CDatasetListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CDatasetListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDatasetName(CDatasetNameStub):
    """
    A string
    
    Extends CDatasetNameStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDialsJsonFile(CDialsJsonFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CDialsJsonFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CDialsPickleFile(CDialsPickleFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CDialsPickleFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CExperimentalDataType(CExperimentalDataTypeStub):
    """
    Experimental data type e.g. native or peak
    
    Extends CExperimentalDataTypeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFPairColumnGroup(CFPairColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CFPairColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFSigFColumnGroup(CFSigFColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CFSigFColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFormFactor(CFormFactorStub):
    """
    The for factor (Fp and Fpp) for a giving element and wavelength
    
    Extends CFormFactorStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFreeRColumnGroup(CFreeRColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CFreeRColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CFreeRDataFile(CFreeRDataFileStub):
    """
    An MTZ experimental data file

    NOTE: Cannot inherit from CMiniMtzDataFile due to definition order.
    CMiniMtzDataFile is defined later in the file.

    Extends CFreeRDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def _introspect_content_flag(self) -> Optional[int]:
        """
        Auto-detect content flag by reading MTZ columns and matching against
        CONTENT_SIGNATURE_LIST.

        This method uses gemmi to read the MTZ file and extract column labels,
        then compares them against the class's CONTENT_SIGNATURE_LIST to
        determine the appropriate contentFlag value.

        Returns:
            Detected content flag (1-indexed), or None if file cannot be read
            or no signature matches.
        """
        from pathlib import Path

        # Check if file exists
        file_path = self.getFullPath()
        if not file_path or not Path(file_path).exists():
            return None

        # Check if class has CONTENT_SIGNATURE_LIST
        if not hasattr(self.__class__, 'CONTENT_SIGNATURE_LIST'):
            return None

        signature_list = self.__class__.CONTENT_SIGNATURE_LIST

        try:
            import gemmi

            # Read MTZ file
            mtz = gemmi.read_mtz_file(file_path)

            # Extract column labels (just the names, not types)
            column_labels = [col.label for col in mtz.columns]
            column_set = set(column_labels)

            # Match against signatures
            for idx, required_columns in enumerate(signature_list):
                required_set = set(required_columns)

                # Check if all required columns are present
                if required_set.issubset(column_set):
                    # Match found: return contentFlag (1-indexed)
                    return idx + 1

            # No match found
            return None

        except Exception:
            # File reading error or gemmi not available
            return None


class CGenericReflDataFile(CGenericReflDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CGenericReflDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CHLColumnGroup(CHLColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CHLColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CIPairColumnGroup(CIPairColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CIPairColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CISigIColumnGroup(CISigIColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CISigIColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CImageFile(CImageFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CImageFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CImageFileList(CImageFileListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CImageFileListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CImosflmXmlDataFile(CImosflmXmlDataFileStub):
    """
    An iMosflm data file
    
    Extends CImosflmXmlDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CImportUnmerged(CImportUnmergedStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CImportUnmergedStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CImportUnmergedList(CImportUnmergedListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CImportUnmergedListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMapCoeffsDataFile(CMapCoeffsDataFileStub):
    """
    An MTZ experimental data file

    NOTE: Cannot inherit from CMiniMtzDataFile due to definition order.
    CMiniMtzDataFile is defined later in the file.

    Extends CMapCoeffsDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def as_FPHI(self, work_directory: Optional[Any] = None) -> str:
        """
        Return path to this file as FPHI format.

        Since CMapCoeffsDataFile only has one content type (FPHI),
        this method simply returns the current file path without conversion.

        FPHI format: F, PHI

        This is a thin wrapper around PhaseDataConverter.to_fphi().
        See core.conversions.phase_data_converter for implementation details.

        Args:
            work_directory: Ignored for this class

        Returns:
            Full path to this file (no conversion needed)
        """
        from core.conversions import PhaseDataConverter
        return PhaseDataConverter.to_fphi(self, work_directory=work_directory)


class CPhsDataFile(CPhsDataFileStub):
    """
    An MTZ phase data file.

    Handles phase data in different formats:
    - HL (1): Hendrickson-Lattman coefficients (HLA, HLB, HLC, HLD)
    - PHIFOM (2): Phase + Figure of Merit (PHI, FOM)

    NOTE: Cannot inherit from CMiniMtzDataFile due to definition order.
    CMiniMtzDataFile is defined later in the file.

    Extends CPhsDataFileStub with conversion methods for transforming
    between different phase data representations.
    """

    def setContentFlag(self):
        """
        Introspect the MTZ file to determine the phase data content type.

        Sets self.contentFlag to:
        - 1 (CONTENT_FLAG_HL): Hendrickson-Lattman coefficients (HLA, HLB, HLC, HLD)
        - 2 (CONTENT_FLAG_PHIFOM): Phase + Figure of Merit (PHI, FOM)
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
            mtz = gemmi.read_mtz_file(input_path)
            column_labels = {col.label.upper() for col in mtz.columns}

            # Check for HL coefficients
            hl_cols = {'HLA', 'HLB', 'HLC', 'HLD'}
            if hl_cols.issubset(column_labels):
                self.contentFlag.set(self.CONTENT_FLAG_HL)
                return self.CONTENT_FLAG_HL

            # Check for PHI/FOM
            phifom_cols = {'PHI', 'FOM'}
            if phifom_cols.issubset(column_labels):
                self.contentFlag.set(self.CONTENT_FLAG_PHIFOM)
                return self.CONTENT_FLAG_PHIFOM

            # Cannot determine
            self.contentFlag.set(0)
            return 0

        except Exception:
            self.contentFlag.set(0)
            return 0

    def as_HL(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to HL format (Hendrickson-Lattman coefficients).

        HL format: HLA, HLB, HLC, HLD

        This is a thin wrapper around PhaseDataConverter.to_hl().
        See core.conversions.phase_data_converter for implementation details.

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            ValueError: If conversion not possible from current format
        """
        from core.conversions import PhaseDataConverter
        return PhaseDataConverter.to_hl(self, work_directory=work_directory)

    def as_PHIFOM(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to PHIFOM format (Phase + Figure of Merit).

        PHIFOM format: PHI, FOM

        This is a thin wrapper around PhaseDataConverter.to_phifom().
        See core.conversions.phase_data_converter for implementation details.

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            ValueError: If conversion not possible from current format
        """
        from core.conversions import PhaseDataConverter
        return PhaseDataConverter.to_phifom(self, work_directory=work_directory)


class CMapColumnGroup(CMapColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CMapColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMapDataFile(CMapDataFileStub):
    """
    A CCP4 Map file
    
    Extends CMapDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMergeMiniMtz(CMergeMiniMtzStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CMergeMiniMtzStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMergeMiniMtzList(CMergeMiniMtzListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CMergeMiniMtzListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMiniMtzDataFile(CMiniMtzDataFileStub):
    """
    An MTZ experimental data file

    Extends CMiniMtzDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Note: _get_conversion_output_path() is now in CDataFile base class

    def _introspect_content_flag(self) -> Optional[int]:
        """
        Auto-detect content flag by reading MTZ columns and matching against
        CONTENT_SIGNATURE_LIST.

        This method uses gemmi to read the MTZ file and extract column labels,
        then compares them against the class's CONTENT_SIGNATURE_LIST to
        determine the appropriate contentFlag value.

        Returns:
            Detected content flag (1-indexed), or None if:
            - File doesn't exist
            - File cannot be read
            - No signature matches the columns
            - Class has no CONTENT_SIGNATURE_LIST

        Example:
            >>> obs_file = CObsDataFile('/path/to/file.mtz')
            >>> obs_file.setContentFlag()  # Auto-detects from file
            >>> print(obs_file.contentFlag)  # 4 (if columns are F, SIGF)
        """
        from pathlib import Path

        # Check if file exists
        file_path = self.getFullPath()
        if not file_path or not Path(file_path).exists():
            return None

        # Check if class has CONTENT_SIGNATURE_LIST
        if not hasattr(self.__class__, 'CONTENT_SIGNATURE_LIST'):
            return None

        signature_list = self.__class__.CONTENT_SIGNATURE_LIST

        try:
            import gemmi

            # Read MTZ file
            mtz = gemmi.read_mtz_file(file_path)

            # Extract column labels (just the names, not types)
            column_labels = [col.label for col in mtz.columns]
            column_set = set(column_labels)

            # Match against signatures
            for idx, required_columns in enumerate(signature_list):
                required_set = set(required_columns)

                # Check if all required columns are present
                if required_set.issubset(column_set):
                    # Match found: return contentFlag (1-indexed)
                    return idx + 1

            # No match found
            return None

        except Exception as e:
            # File reading error or gemmi not available
            # Could log this in the future
            return None


class CMiniMtzDataFileList(CMiniMtzDataFileListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CMiniMtzDataFileListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMmcifReflData(CMmcifReflDataStub):
    """
    Generic mmCIF data.
This is intended to be a base class for other classes
specific to coordinates, reflections or geometry data.

    Extends CMmcifReflDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def loadFile(self, file_path: str):
        """
        Load mmCIF reflection file using gemmi library.

        This method:
        1. Reads mmCIF file using gemmi.cif.read()
        2. Extracts cell, space group, wavelength
        3. Detects which column types are present
        4. Uses proper CData setters (NO __dict__ manipulation)

        Args:
            file_path: Full path to mmCIF file

        Returns:
            CErrorReport with any errors encountered

        Example:
            >>> cif_data = CMmcifReflData()
            >>> error = cif_data.loadFile('/path/to/reflections.cif')
            >>> if error.count() == 0:
            ...     print(f"Has F columns: {cif_data.haveFobsColumn.value}")
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
                details=f"mmCIF file does not exist or is not a file: '{file_path}'",
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
            # Read mmCIF file using gemmi
            cif_doc = gemmi.cif.read(str(file_path))

            # Get the first data block
            if len(cif_doc) == 0:
                error.append(
                    klass=self.__class__.__name__,
                    code=104,
                    details=f"mmCIF file contains no data blocks: '{file_path}'",
                    name=self.object_name() if hasattr(self, 'object_name') else ''
                )
                return error

            block = cif_doc[0]

            # Extract cell parameters using smart assignment
            if hasattr(self, 'cell') and self.cell is not None:
                try:
                    self.cell.a = float(block.find_value('_cell.length_a'))
                    self.cell.b = float(block.find_value('_cell.length_b'))
                    self.cell.c = float(block.find_value('_cell.length_c'))
                    self.cell.alpha = float(block.find_value('_cell.angle_alpha'))
                    self.cell.beta = float(block.find_value('_cell.angle_beta'))
                    self.cell.gamma = float(block.find_value('_cell.angle_gamma'))
                except (ValueError, RuntimeError):
                    pass  # Cell parameters not available

            # Extract space group using smart assignment
            if hasattr(self, 'spaceGroup') and self.spaceGroup is not None:
                try:
                    sg_name = block.find_value('_symmetry.space_group_name_H-M')
                    if sg_name:
                        self.spaceGroup = sg_name.strip('"').strip("'").strip()
                except RuntimeError:
                    # Try alternative tag
                    try:
                        sg_num = block.find_value('_symmetry.Int_Tables_number')
                        if sg_num:
                            self.spaceGroup = f"Space group {sg_num}"
                    except RuntimeError:
                        pass  # Space group not available

            # Extract wavelength using smart assignment
            if hasattr(self, 'wavelength') and self.wavelength is not None:
                try:
                    wavelength_val = block.find_value('_diffrn_radiation_wavelength.wavelength')
                    if wavelength_val:
                        self.wavelength = float(wavelength_val)
                except (ValueError, RuntimeError):
                    pass  # Wavelength not available

            # Detect which column types are present
            # Check for FreeR column
            if hasattr(self, 'haveFreeRColumn') and self.haveFreeRColumn is not None:
                self.haveFreeRColumn = block.find_loop('_refln.status') is not None

            # Check for F_meas columns
            if hasattr(self, 'haveFobsColumn') and self.haveFobsColumn is not None:
                self.haveFobsColumn = (
                    block.find_loop('_refln.F_meas') is not None or
                    block.find_loop('_refln.F_meas_au') is not None
                )

            # Check for F+/F- columns
            if hasattr(self, 'haveFpmObsColumn') and self.haveFpmObsColumn is not None:
                self.haveFpmObsColumn = block.find_loop('_refln.pdbx_F_plus') is not None

            # Check for intensity columns
            if hasattr(self, 'haveIobsColumn') and self.haveIobsColumn is not None:
                self.haveIobsColumn = (
                    block.find_loop('_refln.intensity_meas') is not None or
                    block.find_loop('_refln.F_squared_meas') is not None
                )

            # Check for I+/I- columns
            if hasattr(self, 'haveIpmObsColumn') and self.haveIpmObsColumn is not None:
                self.haveIpmObsColumn = block.find_loop('_refln.pdbx_I_plus') is not None

            # Store gemmi CIF document for advanced queries
            # Use object.__setattr__ to bypass smart assignment
            object.__setattr__(self, '_gemmi_cif_doc', cif_doc)

            # Emit signal if available
            if hasattr(self, 'dataLoaded'):
                try:
                    self.dataLoaded.emit()
                except:
                    pass  # Signal system may not be available

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=103,
                details=f"Error reading mmCIF file '{file_path}': {e}",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )

        return error


class CMmcifReflDataFile(CMmcifReflDataFileStub):
    """
    A reflection file in mmCIF format

    Extends CMmcifReflDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def __init__(self, file_path: str = None, parent=None, name=None, **kwargs):
        super().__init__(file_path=file_path, parent=parent, name=name, **kwargs)
        # Set the content class name qualifier
        self.set_qualifier('fileContentClassName', 'CMmcifReflData')


class CMtzColumn(CMtzColumnStub):
    """
    An MTZ column with column label and column type
    
    Extends CMtzColumnStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMtzColumnGroup(CMtzColumnGroupStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CMtzColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMtzColumnGroupType(CMtzColumnGroupTypeStub, CColumnType):
    """
    
    Inherits from:
    - CMtzColumnGroupTypeStub: Metadata and structure
    - CColumnType: Shared full-fat methods
    A list of recognised MTZ column types
    
    Extends CMtzColumnGroupTypeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CMtzData(CMtzDataStub):
    """
    Base class for classes holding file contents

    Extends CMtzDataStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def loadFile(self, file_path: str):
        """
        Load MTZ file using gemmi library.

        This method:
        1. Reads MTZ file using gemmi.read_mtz_file()
        2. Extracts metadata (cell, spacegroup, resolution, datasets)
        3. Populates CData attributes using proper setters (NO __dict__ manipulation)
        4. Stores gemmi Mtz object for advanced queries

        Args:
            file_path: Full path to MTZ file

        Returns:
            CErrorReport with any errors encountered

        Example:
            >>> mtz_data = CMtzData()
            >>> error = mtz_data.loadFile('/path/to/data.mtz')
            >>> if error.count() == 0:
            ...     print(f"Space group: {mtz_data.spaceGroup}")
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
                details=f"MTZ file does not exist or is not a file: '{file_path}'",
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
            # Read MTZ file using gemmi
            mtz = gemmi.read_mtz_file(str(file_path))

            # Extract cell parameters using smart assignment (NO __dict__)
            if hasattr(self, 'cell') and self.cell is not None:
                self.cell.a = mtz.cell.a
                self.cell.b = mtz.cell.b
                self.cell.c = mtz.cell.c
                self.cell.alpha = mtz.cell.alpha
                self.cell.beta = mtz.cell.beta
                self.cell.gamma = mtz.cell.gamma

            # Extract space group using smart assignment
            if hasattr(self, 'spaceGroup') and self.spaceGroup is not None:
                self.spaceGroup = mtz.spacegroup.hm

            # Extract resolution range using smart assignment
            if hasattr(self, 'resolutionRange') and self.resolutionRange is not None:
                mtz.update_reso()
                self.resolutionRange.low = mtz.resolution_low()
                self.resolutionRange.high = mtz.resolution_high()

            # Extract column names
            if hasattr(self, 'listOfColumns') and self.listOfColumns is not None:
                column_names = [col.label for col in mtz.columns]
                self.listOfColumns = column_names

            # Extract dataset information
            if hasattr(self, 'datasets') and self.datasets is not None:
                dataset_names = [ds.dataset_name for ds in mtz.datasets]
                self.datasets = dataset_names

            # Extract crystal names
            if hasattr(self, 'crystalNames') and self.crystalNames is not None:
                crystal_names = [ds.crystal_name for ds in mtz.datasets]
                self.crystalNames = crystal_names

            # Extract wavelengths
            if hasattr(self, 'wavelengths') and self.wavelengths is not None:
                wavelength_list = [ds.wavelength for ds in mtz.datasets]
                self.wavelengths = wavelength_list

            # Extract dataset cells
            if hasattr(self, 'datasetCells') and self.datasetCells is not None:
                cells = []
                for ds in mtz.datasets:
                    cells.append({
                        'a': ds.cell.a,
                        'b': ds.cell.b,
                        'c': ds.cell.c,
                        'alpha': ds.cell.alpha,
                        'beta': ds.cell.beta,
                        'gamma': ds.cell.gamma
                    })
                self.datasetCells = cells

            # Determine if merged (MTZ files are typically merged)
            if hasattr(self, 'merged') and self.merged is not None:
                self.merged = True

            # Store gemmi Mtz object for advanced queries
            # Use object.__setattr__ to bypass smart assignment
            object.__setattr__(self, '_gemmi_mtz', mtz)

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=103,
                details=f"Error reading MTZ file '{file_path}': {e}",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )

        return error


class CMtzDataFile(CMtzDataFileStub):
    """
    An MTZ experimental data file

    Extends CMtzDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def __init__(self, file_path: str = None, parent=None, name=None, **kwargs):
        super().__init__(file_path=file_path, parent=parent, name=name, **kwargs)
        # Set the content class name qualifier
        self.set_qualifier('fileContentClassName', 'CMtzData')


class CMtzDataset(CMtzDatasetStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CMtzDatasetStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CObsDataFile(CObsDataFileStub, CMiniMtzDataFile):
    """
    An MTZ experimental data file

    Inherits from:
    - CObsDataFileStub: Metadata and structure
    - CMiniMtzDataFile: Shared full-fat methods

    Extends CObsDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def as_IPAIR(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to IPAIR format (Anomalous Intensities).

        IPAIR format: Iplus, SIGIplus, Iminus, SIGIminus

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            NotImplementedError: Conversion logic not yet implemented
        """
        output_path = self._get_conversion_output_path('IPAIR', work_directory=work_directory)

        # TODO: Implement actual conversion logic using gemmi
        # This will involve:
        # 1. Reading current MTZ file
        # 2. Converting data to IPAIR format
        # 3. Writing to output_path

        raise NotImplementedError(
            f"Conversion to IPAIR format not yet implemented. "
            f"Would output to: {output_path}"
        )

    def _ensure_container_child(self, container, name: str, child_class):
        """
        Ensure a container has a child of specified type.

        Helper method for conversion routines that need to initialize container children.

        Args:
            container: CContainer instance
            name: Name of the child attribute
            child_class: Class to instantiate if child doesn't exist

        Returns:
            The child instance (existing or newly created)
        """
        if not hasattr(container, name) or getattr(container, name) is None:
            child = child_class(name=name)
            container.add_item(child)
        return getattr(container, name)

    def as_FPAIR(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to FPAIR format (Anomalous Structure Factors).

        FPAIR format: Fplus, SIGFplus, Fminus, SIGFminus

        Uses ctruncate to convert IPAIR (anomalous intensities) to FPAIR
        (anomalous structure factor amplitudes) via French-Wilson conversion.

        This is a thin wrapper around ObsDataConverter.to_fpair().
        See core.conversions.obs_data_converter for implementation details.

        Args:
            work_directory: Directory for ctruncate working files

        Returns:
            Full path to converted file

        Raises:
            ValueError: If contentFlag cannot be determined or conversion not possible
            RuntimeError: If ctruncate plugin is not available or conversion fails
        """
        from core.conversions import ObsDataConverter
        return ObsDataConverter.to_fpair(self, work_directory=work_directory)


    def as_IMEAN(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to IMEAN format (Mean Intensities).

        IMEAN format: I, SIGI

        Uses ctruncate to convert IPAIR (anomalous intensities) to IMEAN
        (mean intensities) by averaging I+ and I-.

        This is a thin wrapper around ObsDataConverter.to_imean().
        See core.conversions.obs_data_converter for implementation details.

        Args:
            work_directory: Directory for ctruncate working files

        Returns:
            Full path to converted file

        Raises:
            ValueError: If contentFlag cannot be determined or conversion not possible
            RuntimeError: If ctruncate plugin is not available or conversion fails
        """
        from core.conversions import ObsDataConverter
        return ObsDataConverter.to_imean(self, work_directory=work_directory)

    def as_FMEAN(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to FMEAN format (Mean Structure Factors).

        FMEAN format: F, SIGF

        Handles multiple input formats:
        - IPAIR → FMEAN: French-Wilson via ctruncate
        - IMEAN → FMEAN: French-Wilson via ctruncate
        - FPAIR → FMEAN: Inverse-variance weighted mean via gemmi

        This is a thin wrapper around ObsDataConverter.to_fmean().
        See core.conversions.obs_data_converter for implementation details.

        Args:
            work_directory: Directory for working files

        Returns:
            Full path to converted file

        Raises:
            ValueError: If contentFlag cannot be determined
            RuntimeError: If conversion fails
        """
        from core.conversions import ObsDataConverter
        return ObsDataConverter.to_fmean(self, work_directory=work_directory)


class CProgramColumnGroup(CProgramColumnGroupStub):
    """
    A group of MTZ columns required for program input.

    This class maps between generic column names (e.g., 'Ip', 'SIGIp') and
    actual MTZ column labels (e.g., 'Iplus', 'SIGIplus'). It behaves like
    a dictionary that can be accessed via attributes.

    Example:
        >>> colgroup = CProgramColumnGroup()
        >>> colgroup.set({'Ip': 'Iplus', 'SIGIp': 'SIGIplus'})
        >>> print(colgroup.Ip)  # Returns 'Iplus'
        >>> print(colgroup.isSet())  # Returns True

    This provides compatibility with ccp4i2 wrapper code that expects
    attribute access to column mappings.
    """

    def __init__(self, parent=None, name=None, **kwargs):
        """Initialize with an internal column mapping dict."""
        super().__init__(parent=parent, name=name, **kwargs)
        # Internal storage for column name mappings
        self._column_mapping = {}
        self._is_set = False

    def set(self, mapping: dict):
        """
        Set the column name mappings.

        Args:
            mapping: Dict mapping generic column names to actual MTZ column labels
                    e.g., {'Ip': 'Iplus', 'SIGIp': 'SIGIplus', 'Im': 'Iminus', 'SIGIm': 'SIGIminus'}
        """
        if isinstance(mapping, dict):
            self._column_mapping = mapping.copy()
            self._is_set = True
        else:
            # If it's a CData object, try to extract its value
            if hasattr(mapping, '__dict__') and '_column_mapping' in mapping.__dict__:
                self._column_mapping = mapping._column_mapping.copy()
                self._is_set = mapping._is_set
            else:
                raise TypeError(f"Expected dict, got {type(mapping)}")

    def isSet(self):
        """
        Check if column mappings have been set.

        Returns:
            bool: True if set() has been called with mappings AND mappings contain data
        """
        # Check both the flag AND that we have actual column mappings
        # This prevents reporting True for empty/uninitialized column groups
        return self._is_set and len(self._column_mapping) > 0

    def __getattr__(self, name):
        """
        Allow attribute access to column mappings.

        Args:
            name: Generic column name (e.g., 'Ip', 'SIGIp')

        Returns:
            The mapped MTZ column label, or None if not found
        """
        # Avoid recursion for internal attributes
        if name.startswith('_'):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Check if we have this column mapping
        if '_column_mapping' in self.__dict__ and name in self._column_mapping:
            return self._column_mapping[name]

        # For missing column names, return None (matches ccp4i2 behavior)
        # This allows wrapper code to check `if inp.ISIGI.I:` without errors
        return None

    def __setattr__(self, name, value):
        """
        Allow attribute assignment to update column mappings.

        Args:
            name: Generic column name
            value: Actual MTZ column label
        """
        # Internal attributes go through normal path
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            # For column names, store in mapping
            if '_column_mapping' not in self.__dict__:
                self.__dict__['_column_mapping'] = {}
            if '_is_set' not in self.__dict__:
                self.__dict__['_is_set'] = False

            self._column_mapping[name] = value
            self._is_set = True

    def get(self, name, default=None):
        """
        Get a mapped column name with optional default.

        Args:
            name: Generic column name
            default: Value to return if name not found

        Returns:
            Mapped column label or default
        """
        return self._column_mapping.get(name, default)

    def keys(self):
        """Return all generic column names."""
        return self._column_mapping.keys()

    def values(self):
        """Return all mapped column labels."""
        return self._column_mapping.values()

    def items(self):
        """Return all (generic_name, mapped_label) pairs."""
        return self._column_mapping.items()


class CProgramColumnGroup0(CProgramColumnGroup0Stub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CProgramColumnGroup0Stub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CRefmacKeywordFile(CRefmacKeywordFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CRefmacKeywordFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CReindexOperator(CReindexOperatorStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CReindexOperatorStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CResolutionRange(CResolutionRangeStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CResolutionRangeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CRunBatchRange(CRunBatchRangeStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CRunBatchRangeStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CRunBatchRangeList(CRunBatchRangeListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CRunBatchRangeListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CShelxFADataFile(CShelxFADataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CShelxFADataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CShelxLabel(CShelxLabelStub):
    """
    A string
    
    Extends CShelxLabelStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSpaceGroup(CSpaceGroupStub):
    """
    A string holding the space group
    
    Extends CSpaceGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CSpaceGroupCell(CSpaceGroupCellStub):
    """
    Cell space group and parameters
    
    Extends CSpaceGroupCellStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CUnmergedDataContent(CUnmergedDataContentStub):
    """
    Base class for classes holding file contents

    Extends CUnmergedDataContentStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def loadFile(self, file_path: str):
        """
        Load unmerged reflection file using gemmi library.

        Supports multiple formats:
        - MTZ (using gemmi.read_mtz_file)
        - mmCIF (using gemmi.cif.read)
        - Other formats detected by extension

        Args:
            file_path: Full path to reflection file

        Returns:
            CErrorReport with any errors encountered

        Example:
            >>> unmerged = CUnmergedDataContent()
            >>> error = unmerged.loadFile('/path/to/unmerged.mtz')
            >>> if error.count() == 0:
            ...     print(f"Format: {unmerged.format.value}")
            ...     print(f"Merged: {unmerged.merged.value}")
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
                details=f"File does not exist or is not a file: '{file_path}'",
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

        # Determine format from extension
        suffix = path_obj.suffix.lower()

        try:
            # Handle MTZ files
            if suffix == '.mtz':
                self._load_mtz_file(file_path, gemmi, error)

            # Handle mmCIF files
            elif suffix in ['.cif', '.mmcif', '.ent']:
                self._load_mmcif_file(file_path, gemmi, error)

            # Handle Scalepack format (.sca, .hkl)
            elif suffix in ['.sca', '.hkl']:
                self._load_scalepack_file(file_path, error)

            # Handle XDS files (INTEGRATE.HKL, XDS_ASCII.HKL)
            elif 'INTEGRATE' in path_obj.name or 'XDS_ASCII' in path_obj.name or suffix == '.hkl':
                # Try XDS format first
                try:
                    self._load_xds_file(file_path, gemmi, error)
                except:
                    # Fall back to Scalepack
                    self._load_scalepack_file(file_path, error)

            elif suffix == '.shelx':
                self.format = 'shelx'
                self.merged = 'unk'
                self.knowncell = False
                self.knownwavelength = False
                object.__setattr__(self, '_file_path', file_path)

            else:
                # Try MTZ as default for unknown extensions
                try:
                    self._load_mtz_file(file_path, gemmi, error)
                except:
                    self.format = 'unk'
                    error.append(
                        klass=self.__class__.__name__,
                        code=103,
                        details=f"Unknown file format for: '{file_path}'",
                        name=self.object_name() if hasattr(self, 'object_name') else ''
                    )

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=104,
                details=f"Error reading file '{file_path}': {e}",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )

        return error

    def _load_mtz_file(self, file_path: str, gemmi, error):
        """Load MTZ file and extract metadata."""
        mtz = gemmi.read_mtz_file(str(file_path))

        # Set format
        self.format = 'mtz'

        # Determine if merged (unmerged MTZ have batch columns)
        has_batch = any(col.label == 'BATCH' for col in mtz.columns)
        self.merged = 'unmerged' if has_batch else 'merged'

        # Extract cell using smart assignment
        if hasattr(self, 'cell') and self.cell is not None:
            self.cell.a = mtz.cell.a
            self.cell.b = mtz.cell.b
            self.cell.c = mtz.cell.c
            self.cell.alpha = mtz.cell.alpha
            self.cell.beta = mtz.cell.beta
            self.cell.gamma = mtz.cell.gamma

        # Extract space group
        if hasattr(self, 'spaceGroup') and self.spaceGroup is not None:
            self.spaceGroup = mtz.spacegroup.hm

        # Extract resolution range
        mtz.update_reso()
        if hasattr(self, 'lowRes') and self.lowRes is not None:
            self.lowRes = mtz.resolution_low()
        if hasattr(self, 'highRes') and self.highRes is not None:
            self.highRes = mtz.resolution_high()

        # Extract dataset information
        if len(mtz.datasets) > 0:
            # Use first non-HKL_base dataset
            for ds in mtz.datasets:
                if ds.dataset_name != 'HKL_base':
                    if hasattr(self, 'datasetName') and self.datasetName is not None:
                        self.datasetName = ds.dataset_name
                    if hasattr(self, 'crystalName') and self.crystalName is not None:
                        self.crystalName = ds.crystal_name
                    if hasattr(self, 'wavelength') and self.wavelength is not None:
                        self.wavelength = ds.wavelength
                    break

        # Number of datasets
        if hasattr(self, 'numberofdatasets') and self.numberofdatasets is not None:
            self.numberofdatasets = len(mtz.datasets)

        # Number of lattices (count of batches)
        if has_batch:
            if hasattr(self, 'numberLattices') and self.numberLattices is not None:
                self.numberLattices = len(mtz.batches)

        # Cell and wavelength are known for MTZ
        self.knowncell = True
        self.knownwavelength = True

        # Store gemmi Mtz object
        object.__setattr__(self, '_gemmi_mtz', mtz)

    def _load_mmcif_file(self, file_path: str, gemmi, error):
        """Load mmCIF file and extract metadata."""
        cif_doc = gemmi.cif.read(str(file_path))

        if len(cif_doc) == 0:
            error.append(
                klass=self.__class__.__name__,
                code=105,
                details=f"mmCIF file contains no data blocks: '{file_path}'",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )
            return

        block = cif_doc[0]

        # Set format
        self.format = 'mmcif'

        # mmCIF reflection files are typically merged
        self.merged = 'merged'

        # Extract cell
        if hasattr(self, 'cell') and self.cell is not None:
            try:
                self.cell.a = float(block.find_value('_cell.length_a'))
                self.cell.b = float(block.find_value('_cell.length_b'))
                self.cell.c = float(block.find_value('_cell.length_c'))
                self.cell.alpha = float(block.find_value('_cell.angle_alpha'))
                self.cell.beta = float(block.find_value('_cell.angle_beta'))
                self.cell.gamma = float(block.find_value('_cell.angle_gamma'))
                self.knowncell = True
            except (ValueError, RuntimeError):
                self.knowncell = False

        # Extract space group
        if hasattr(self, 'spaceGroup') and self.spaceGroup is not None:
            try:
                sg_name = block.find_value('_symmetry.space_group_name_H-M')
                if sg_name:
                    self.spaceGroup = sg_name.strip('"').strip("'").strip()
            except RuntimeError:
                pass

        # Extract wavelength
        if hasattr(self, 'wavelength') and self.wavelength is not None:
            try:
                wavelength_val = block.find_value('_diffrn_radiation_wavelength.wavelength')
                if wavelength_val:
                    self.wavelength = float(wavelength_val)
                    self.knownwavelength = True
                else:
                    self.knownwavelength = False
            except (ValueError, RuntimeError):
                self.knownwavelength = False

        # Store gemmi CIF document
        object.__setattr__(self, '_gemmi_cif_doc', cif_doc)

    def _load_xds_file(self, file_path: str, gemmi, error):
        """Load XDS file (INTEGRATE.HKL or XDS_ASCII.HKL) using gemmi."""
        xds = gemmi.read_xds_ascii(str(file_path))

        # Set format
        if 'INTEGRATE' in Path(file_path).name:
            self.format = 'xds'
        else:
            self.format = 'xds'

        # XDS files are always unmerged
        self.merged = 'unmerged'

        # Extract cell using smart assignment
        if hasattr(self, 'cell') and self.cell is not None:
            cell_params = xds.cell_constants
            self.cell.a = cell_params[0]
            self.cell.b = cell_params[1]
            self.cell.c = cell_params[2]
            self.cell.alpha = cell_params[3]
            self.cell.beta = cell_params[4]
            self.cell.gamma = cell_params[5]
            self.knowncell = True
        else:
            self.knowncell = False

        # Extract space group from number
        if hasattr(self, 'spaceGroup') and self.spaceGroup is not None:
            sg_num = xds.spacegroup_number
            # Convert to Hermann-Mauguin symbol if possible
            try:
                from gemmi import SpaceGroup
                sg = SpaceGroup(sg_num)
                self.spaceGroup = sg.hm
            except:
                self.spaceGroup = f"Space group {sg_num}"

        # Extract wavelength
        if hasattr(self, 'wavelength') and self.wavelength is not None:
            self.wavelength = xds.wavelength
            self.knownwavelength = True
        else:
            self.knownwavelength = False

        # Number of reflections
        data_size = xds.data_size
        if data_size > 0:
            # Store data size info
            object.__setattr__(self, '_xds_data_size', data_size)

        # Store gemmi XDS object
        object.__setattr__(self, '_gemmi_xds', xds)

    def _load_scalepack_file(self, file_path: str, error):
        """Load Scalepack (.sca) file header to extract metadata.

        Scalepack has two formats:

        Merged format:
          Line 1: Version (1 = merged)
          Line 2: -987 (magic number)
          Line 3: a b c alpha beta gamma space_group

        Unmerged format:
          Line 1: nsyms space_group (e.g., "8 C2221")
          Line 2+: Symmetry matrices (nsyms * 3 lines)
          No cell parameters in file
        """
        try:
            with open(file_path, 'r') as f:
                line1 = f.readline().strip()
                line2 = f.readline().strip()
                line3 = f.readline().strip()

            # Set format
            self.format = 'sca'

            # Detect file format by checking line 2
            if line2 == '-987':
                # MERGED FORMAT: line1 = version, line2 = -987, line3 = cell
                try:
                    version = int(line1)
                    if version == 1:
                        self.merged = 'merged'
                    elif version in [2, 3]:
                        self.merged = 'unmerged'
                    else:
                        self.merged = 'unk'
                except ValueError:
                    self.merged = 'unk'

                # Parse cell parameters from line 3
                parts = line3.split()
                if len(parts) >= 6:
                    try:
                        self.cell.a = float(parts[0])
                        self.cell.b = float(parts[1])
                        self.cell.c = float(parts[2])
                        self.cell.alpha = float(parts[3])
                        self.cell.beta = float(parts[4])
                        self.cell.gamma = float(parts[5])
                        self.knowncell = True

                        # Space group is after cell parameters
                        if len(parts) > 6:
                            sg_text = ' '.join(parts[6:])
                            self.spaceGroup = sg_text.strip()
                    except (ValueError, IndexError):
                        self.knowncell = False
                else:
                    self.knowncell = False

                # Merged format doesn't have wavelength
                self.knownwavelength = False

            else:
                # UNMERGED FORMAT: line1 = "nsyms spacegroup"
                self.merged = 'unmerged'

                # Parse space group from line 1
                parts = line1.split(None, 1)  # Split on first whitespace
                if len(parts) >= 2:
                    try:
                        nsyms = int(parts[0])
                        spacegroup = parts[1]
                        self.spaceGroup = spacegroup
                    except (ValueError, IndexError):
                        pass

                # Unmerged Scalepack files do not contain cell or wavelength
                self.knowncell = False
                self.knownwavelength = False

            # Store file path for potential future full parsing
            object.__setattr__(self, '_file_path', file_path)

        except Exception as e:
            error.append(
                klass=self.__class__.__name__,
                code=107,
                details=f"Error parsing Scalepack file '{file_path}': {e}",
                name=self.object_name() if hasattr(self, 'object_name') else ''
            )


class CUnmergedDataFile(CUnmergedDataFileStub):
    """
    Handle MTZ, XDS and scalepack files. Allow wildcard filename

    Extends CUnmergedDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def __init__(self, file_path: str = None, parent=None, name=None, **kwargs):
        super().__init__(file_path=file_path, parent=parent, name=name, **kwargs)
        # Set the content class name qualifier
        self.set_qualifier('fileContentClassName', 'CUnmergedDataContent')


class CUnmergedDataFileList(CUnmergedDataFileListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CUnmergedDataFileListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CUnmergedMtzDataFile(CUnmergedMtzDataFileStub, CMtzDataFile):
    """
    
    Inherits from:
    - CUnmergedMtzDataFileStub: Metadata and structure
    - CMtzDataFile: Shared full-fat methods
    An MTZ experimental data file
    
    Extends CUnmergedMtzDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CWavelength(CWavelengthStub):
    """
    Wavelength in Angstrom
    
    Extends CWavelengthStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CXia2ImageSelection(CXia2ImageSelectionStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CXia2ImageSelectionStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CXia2ImageSelectionList(CXia2ImageSelectionListStub):
    """
    A list with all items of one CData sub-class
    
    Extends CXia2ImageSelectionListStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass

