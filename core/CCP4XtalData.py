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

        Args:
            work_directory: Ignored for this class

        Returns:
            Full path to this file (no conversion needed)
        """
        # No conversion needed - already in FPHI format
        return self.getFullPath()


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

    # Add your methods here
    pass


class CMmcifReflDataFile(CMmcifReflDataFileStub):
    """
    A reflection file in mmCIF format
    
    Extends CMmcifReflDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


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

    # Add your methods here
    pass


class CMtzDataFile(CMtzDataFileStub):
    """
    An MTZ experimental data file
    
    Extends CMtzDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


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

    def as_FPAIR(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to FPAIR format (Anomalous Structure Factors).

        FPAIR format: Fplus, SIGFplus, Fminus, SIGFminus

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            NotImplementedError: Conversion logic not yet implemented
        """
        output_path = self._get_conversion_output_path('FPAIR', work_directory=work_directory)

        # TODO: Implement conversion logic
        raise NotImplementedError(
            f"Conversion to FPAIR format not yet implemented. "
            f"Would output to: {output_path}"
        )

    def as_IMEAN(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to IMEAN format (Mean Intensities).

        IMEAN format: I, SIGI

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            NotImplementedError: Conversion logic not yet implemented
        """
        output_path = self._get_conversion_output_path('IMEAN', work_directory=work_directory)

        # TODO: Implement conversion logic
        raise NotImplementedError(
            f"Conversion to IMEAN format not yet implemented. "
            f"Would output to: {output_path}"
        )

    def _ensure_container_child(self, container, name, child_class):
        """Helper to get or create a child in a container.

        Args:
            container: Parent container
            name: Child name
            child_class: Class to instantiate if child doesn't exist

        Returns:
            The child object
        """
        # First check if it already exists
        try:
            return getattr(container, name)
        except AttributeError:
            pass

        # Doesn't exist - create WITHOUT parent, then add to container
        # (add_item will set the parent, and by then signals are initialized)
        child = child_class(name=name)
        container.add_item(child)
        return child

    def as_FMEAN(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to FMEAN format (Mean Structure Factors).

        FMEAN format: F, SIGF

        Uses the ctruncate plugin to perform French-Wilson conversion
        from intensities to structure factor amplitudes.

        Args:
            work_directory: Directory for ctruncate working files

        Returns:
            Full path to converted file

        Raises:
            RuntimeError: If ctruncate plugin is not available
            RuntimeError: If conversion fails
        """
        import os
        from core.CCP4PluginScript import CPluginScript
        from core.base_object.fundamental_types import CInt, CBoolean

        # Auto-detect content flag from file
        self.setContentFlag()
        current_flag = int(self.contentFlag)

        if current_flag == 0:
            raise ValueError("Cannot convert: contentFlag could not be determined from file")

        # If already FMEAN, just copy the file
        if current_flag == self.CONTENT_FLAG_FMEAN:
            import shutil
            from pathlib import Path
            output_path = self._get_conversion_output_path('FMEAN', work_directory=work_directory)
            input_path = Path(self.getFullPath())
            shutil.copy2(input_path, output_path)
            return str(output_path)

        # Get ctruncate plugin
        wrapper_class = TASKMANAGER().get_plugin_class('ctruncate')
        if wrapper_class is None:
            raise RuntimeError("ctruncate plugin not available")

        # Create ctruncate instance with working directory
        ctruncate_work = os.path.join(work_directory, "ctruncate") if work_directory else "ctruncate"
        wrapper = wrapper_class(parent=self, workDirectory=ctruncate_work)

        # Populate container manually (in production, this would come from def.xml loading)
        # NOTE: The ccp4i2 wrapper expects these items but since we're using our new CContainer
        # without def.xml loading, we need to create them explicitly
        inp = wrapper.container.inputData
        self._ensure_container_child(inp, 'HKLIN', CMtzDataFile)
        inp.HKLIN.setFullPath(self.getFullPath())

        # Configure to output mini-MTZ with FMEAN format (create params if needed)
        par = wrapper.container.controlParameters
        self._ensure_container_child(par, 'OUTPUTMINIMTZ', CBoolean)
        self._ensure_container_child(par, 'OUTPUTMINIMTZCONTENTFLAG', CInt)
        par.OUTPUTMINIMTZ.set(True)
        par.OUTPUTMINIMTZCONTENTFLAG.set(self.CONTENT_FLAG_FMEAN)

        # Get expected column names from CONTENT_SIGNATURE_LIST
        # contentFlag is 1-indexed, so subtract 1 for list index
        column_names = self.CONTENT_SIGNATURE_LIST[current_flag - 1]

        # Set column names based on current content flag
        # IMPORTANT: Use .set() to mark the container as set (needed for isSet() check)
        if current_flag == self.CONTENT_FLAG_IPAIR:
            # Anomalous intensities: ['Iplus', 'SIGIplus', 'Iminus', 'SIGIminus']
            self._ensure_container_child(inp, 'ISIGIanom', CProgramColumnGroup)
            inp.ISIGIanom.set({
                'Ip': column_names[0],
                'SIGIp': column_names[1],
                'Im': column_names[2],
                'SIGIm': column_names[3]
            })
        elif current_flag == self.CONTENT_FLAG_IMEAN:
            # Mean intensities: ['I', 'SIGI']
            self._ensure_container_child(inp, 'ISIGI', CProgramColumnGroup)
            inp.ISIGI.set({
                'I': column_names[0],
                'SIGI': column_names[1]
            })
        elif current_flag == self.CONTENT_FLAG_FPAIR:
            # Anomalous structure factors: ['Fplus', 'SIGFplus', 'Fminus', 'SIGFminus']
            self._ensure_container_child(par, 'AMPLITUDES', CBoolean)
            par.AMPLITUDES.set(True)
            self._ensure_container_child(inp, 'FSIGFanom', CProgramColumnGroup)
            inp.FSIGFanom.set({
                'Fp': column_names[0],
                'SIGFp': column_names[1],
                'Fm': column_names[2],
                'SIGFm': column_names[3]
            })

        # Set output file paths
        # Important: Output must go to work_directory (not input directory) to ensure writability
        if work_directory:
            from pathlib import Path
            input_path = Path(self.getFullPath())
            # HKLOUT: full ctruncate output (all columns)
            hklout_name = f"{input_path.stem}_full{input_path.suffix}"
            hklout_path = str(Path(work_directory) / hklout_name)
            # OBSOUT: mini-MTZ with only requested columns (F, SIGF)
            obsout_name = f"{input_path.stem}_as_FMEAN{input_path.suffix}"
            obsout_path = str(Path(work_directory) / obsout_name)
        else:
            hklout_path = self._get_conversion_output_path('FMEAN_full', work_directory=work_directory)
            obsout_path = self._get_conversion_output_path('FMEAN', work_directory=work_directory)

        wrapper.container.outputData.HKLOUT.setFullPath(hklout_path)
        wrapper.container.outputData.OBSOUT.setFullPath(obsout_path)

        # Run ctruncate
        status = wrapper.process()

        if status != CPluginScript.SUCCEEDED:
            error_msg = f"ctruncate conversion failed with status {status}."
            if wrapper.errorReport.count() > 0:
                error_msg += f"\nErrors:\n{wrapper.errorReport.report()}"
            error_msg += f"\nCheck logs in {ctruncate_work}"
            raise RuntimeError(error_msg)

        # Manually call processOutputFiles to create the mini-MTZ
        # (normally called by postProcess, but we skip that for synchronous execution)
        if hasattr(wrapper, 'processOutputFiles'):
            try:
                wrapper.processOutputFiles()
            except AttributeError as e:
                # Handle missing methods like datasetName() that are not critical
                # The essential work (creating mini-MTZ) is done by splitMtz
                print(f"[DEBUG as_FMEAN] processOutputFiles partial failure (non-critical): {e}")

        # Return path to mini-MTZ output (OBSOUT), not the full HKLOUT
        # OBSOUT contains only the requested columns (F, SIGF for FMEAN)
        # while HKLOUT contains all columns including intensities
        obsout_path = wrapper.container.outputData.OBSOUT.getFullPath()

        # Debug: List files created by ctruncate
        print(f"[DEBUG as_FMEAN] Expected OBSOUT: {obsout_path}")
        print(f"[DEBUG as_FMEAN] Expected HKLOUT: {wrapper.container.outputData.HKLOUT.getFullPath()}")
        print(f"[DEBUG as_FMEAN] ctruncate work directory: {ctruncate_work}")
        from pathlib import Path
        if work_directory and Path(work_directory).exists():
            print(f"[DEBUG as_FMEAN] Files in work_directory:")
            for f in Path(work_directory).rglob("*.mtz"):
                print(f"  {f} (size: {f.stat().st_size} bytes)")

        # Also check the ctruncate subdirectory
        if Path(ctruncate_work).exists():
            print(f"[DEBUG as_FMEAN] Files in ctruncate work directory:")
            for f in Path(ctruncate_work).rglob("*.mtz"):
                print(f"  {f} (size: {f.stat().st_size} bytes)")

        if not obsout_path or not os.path.exists(obsout_path):
            raise RuntimeError(f"ctruncate mini-MTZ output not found. Expected at: {obsout_path}")

        return str(obsout_path)


class CPhaserRFileDataFile(CPhaserRFileDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CPhaserRFileDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPhaserSolDataFile(CPhaserSolDataFileStub):
    """
    QObject(self, parent: typing.Optional[PySide2.QtCore.QObject] = None) -> None
    
    Extends CPhaserSolDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPhiFomColumnGroup(CPhiFomColumnGroupStub):
    """
    A group of MTZ columns required for program input
    
    Extends CPhiFomColumnGroupStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


class CPhsDataFile(CPhsDataFileStub, CMiniMtzDataFile):
    """
    An MTZ experimental data file

    Inherits from:
    - CPhsDataFileStub: Metadata and structure
    - CMiniMtzDataFile: Shared full-fat methods

    Extends CPhsDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    def as_HL(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to HL format (Hendrickson-Lattman coefficients).

        HL format: HLA, HLB, HLC, HLD

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            NotImplementedError: Conversion logic not yet implemented
        """
        output_path = self._get_conversion_output_path('HL', work_directory=work_directory)

        # TODO: Implement conversion logic
        raise NotImplementedError(
            f"Conversion to HL format not yet implemented. "
            f"Would output to: {output_path}"
        )

    def as_PHIFOM(self, work_directory: Optional[Any] = None) -> str:
        """
        Convert this file to PHIFOM format (Phase + Figure of Merit).

        PHIFOM format: PHI, FOM

        Args:
            work_directory: Directory for output if input dir not writable

        Returns:
            Full path to converted file

        Raises:
            NotImplementedError: Conversion logic not yet implemented
        """
        output_path = self._get_conversion_output_path('PHIFOM', work_directory=work_directory)

        # TODO: Implement conversion logic
        raise NotImplementedError(
            f"Conversion to PHIFOM format not yet implemented. "
            f"Would output to: {output_path}"
        )


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
            bool: True if set() has been called with mappings
        """
        return self._is_set

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

    # Add your methods here
    pass


class CUnmergedDataFile(CUnmergedDataFileStub):
    """
    Handle MTZ, XDS and scalepack files. Allow wildcard filename
    
    Extends CUnmergedDataFileStub with implementation-specific methods.
    Add file I/O, validation, and business logic here.
    """

    # Add your methods here
    pass


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

