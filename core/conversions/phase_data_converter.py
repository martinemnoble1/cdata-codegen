"""
Converter for phase data format transformations using gemmi.

This module handles conversions between different phase data formats in MTZ files:

Phase Data Files (CPhsDataFile):
- HL (1): Hendrickson-Lattman coefficients (HLA, HLB, HLC, HLD)
- PHIFOM (2): Phase + Figure of Merit (PHI, FOM)

Map Coefficients Files (CMapCoeffsDataFile):
- FPHI (1): Structure factors + Phase (F, PHI)

Conversion Matrix (CPhsDataFile):
                TO
          HL   PHIFOM
FROM HL    ✓      ✓
     PHIFOM ✓      ✓

Gemmi Support:
- gemmi handles HL coefficients natively (column type 'A')
- gemmi.Mtz.get_f_phi() returns ComplexAsuData from F+PHI columns
- ComplexAsuData stores F*exp(i*PHI) as complex numbers
- gemmi.ensure_asu() properly handles HL coefficient transformations during reindexing

Implementation Approach:
1. HL → PHIFOM: Extract best phase and FOM from HL coefficients
   - Use gemmi's built-in HL handling
   - Calculate phase probability distribution maximum
   - Compute figure of merit from probability distribution

2. PHIFOM → HL: Convert phase+FOM to HL representation
   - Approximate HL coefficients from PHI and FOM
   - May use simple approximation: HLA=FOM*cos(PHI), HLB=FOM*sin(PHI), HLC=HLD=0

3. FPHI conversions:
   - FPHI data naturally represented as complex: F*exp(i*PHI)
   - Use gemmi.Mtz.get_f_phi() for reading
   - Extract amplitude and phase with abs() and angle()

Note: See gemmi/docs/hkl.rst lines 734-738 for HL coefficient handling
"""

from typing import Optional, Any


class PhaseDataConverter:
    """
    Static converter class for phase data format transformations.

    Handles conversions between HL coefficients, PHI/FOM, and F/PHI formats.
    All methods are static and take the file instance as first parameter.
    """

    @staticmethod
    def to_hl(phase_file, work_directory: Optional[Any] = None) -> str:
        """
        Convert phase data to HL format (Hendrickson-Lattman coefficients).

        HL format: HLA, HLB, HLC, HLD

        Possible conversions:
        - PHIFOM → HL: Convert phase+FOM to HL coefficients using approximation
        - FPHI → HL: Not supported (requires structure factor information)

        The PHIFOM → HL conversion uses a centrosymmetric approximation:
        - HLA = FOM * cos(PHI)
        - HLB = FOM * sin(PHI)
        - HLC = 0
        - HLD = 0

        This approximation is reasonable when only PHI and FOM are known,
        but does not capture the full phase probability distribution.

        Args:
            phase_file: CPhsDataFile or CMapCoeffsDataFile instance
            work_directory: Directory for output files

        Returns:
            Full path to converted HL file

        Raises:
            ValueError: If conversion not possible from current format
        """
        import gemmi

        output_path = phase_file._get_conversion_output_path('HL', work_directory=work_directory)
        input_path = phase_file.getFullPath()

        # Read input MTZ
        mtz = gemmi.read_mtz_file(input_path)

        # Detect current content flag and route to appropriate conversion
        content_flag = phase_file.contentFlag

        if content_flag == 1:  # HL format
            # Already in HL format, just return current path
            return input_path
        elif content_flag == 2:  # PHIFOM format
            return PhaseDataConverter._phifom_to_hl_gemmi(
                input_path, output_path, mtz)
        else:
            raise ValueError(
                f"Cannot convert from contentFlag={content_flag} to HL. "
                f"Only PHIFOM (2) → HL conversion is supported."
            )

    @staticmethod
    def to_phifom(phase_file, work_directory: Optional[Any] = None) -> str:
        """
        Convert phase data to PHIFOM format (Phase + Figure of Merit).

        PHIFOM format: PHI, FOM

        Possible conversions:
        - HL → PHIFOM: Convert HL coefficients to best phase estimate + FOM
        - FPHI → PHIFOM: Extract phase, estimate FOM (may assume FOM=1.0)

        Args:
            phase_file: CPhsDataFile or CMapCoeffsDataFile instance
            work_directory: Directory for output files

        Returns:
            Full path to converted PHIFOM file

        Raises:
            ValueError: If conversion not possible from current format
        """
        import gemmi

        output_path = phase_file._get_conversion_output_path('PHIFOM', work_directory=work_directory)
        input_path = phase_file.getFullPath()

        # Read input MTZ
        mtz = gemmi.read_mtz_file(input_path)

        # Detect current content flag and route to appropriate conversion
        content_flag = phase_file.contentFlag

        if content_flag == 1:  # HL format
            return PhaseDataConverter._hl_to_phifom_gemmi(
                input_path, output_path, mtz)
        elif content_flag == 2:  # PHIFOM format
            # Already in PHIFOM format, just return current path
            return input_path
        else:
            raise ValueError(
                f"Cannot convert from contentFlag={content_flag} to PHIFOM. "
                f"Only HL (1) → PHIFOM conversion is supported."
            )

    @staticmethod
    def to_fphi(map_coeffs_file, work_directory: Optional[Any] = None) -> str:
        """
        Return path to FPHI format file.

        Since CMapCoeffsDataFile only has one content type (FPHI),
        this method simply returns the current file path without conversion.

        FPHI format: F, PHI

        Args:
            map_coeffs_file: CMapCoeffsDataFile instance
            work_directory: Ignored for this conversion

        Returns:
            Full path to current file (no conversion needed)
        """
        # No conversion needed - CMapCoeffsDataFile is always FPHI
        return map_coeffs_file.getFullPath()

    @staticmethod
    def _phifom_to_hl_gemmi(input_path: str, output_path: str, mtz) -> str:
        """
        Convert PHIFOM format to HL coefficients using gemmi.

        Uses centrosymmetric approximation:
        - HLA = FOM * cos(PHI)
        - HLB = FOM * sin(PHI)
        - HLC = 0
        - HLD = 0

        Args:
            input_path: Path to input MTZ with PHI/FOM
            output_path: Path for output MTZ with HL coefficients
            mtz: gemmi.Mtz object (already loaded)

        Returns:
            Path to output MTZ file
        """
        import gemmi
        import numpy as np

        # Find PHI and FOM columns
        phi_col = None
        fom_col = None

        for col in mtz.columns:
            label = col.label.upper()
            if col.type == 'P' or 'PHI' in label:  # Phase column
                phi_col = col
            elif col.type == 'W' or 'FOM' in label:  # Weight/FOM column
                fom_col = col

        if phi_col is None:
            raise ValueError(f"Could not find PHI column in input MTZ")
        if fom_col is None:
            raise ValueError(f"Could not find FOM column in input MTZ")

        # Extract PHI and FOM as numpy arrays
        phi = np.array(phi_col)  # Degrees
        fom = np.array(fom_col)

        # Convert PHI to radians for calculation
        phi_rad = np.radians(phi)

        # Calculate HL coefficients using centrosymmetric approximation
        hla = fom * np.cos(phi_rad)
        hlb = fom * np.sin(phi_rad)
        hlc = np.zeros_like(fom)
        hld = np.zeros_like(fom)

        # Create output MTZ with same structure
        out_mtz = gemmi.Mtz(with_base=False)
        out_mtz.spacegroup = mtz.spacegroup
        out_mtz.set_cell_for_all(mtz.cell)

        # Add a single dataset for all columns
        out_mtz.add_dataset('hl_data')

        # Add H, K, L columns
        out_mtz.add_column('H', 'H')
        out_mtz.add_column('K', 'H')
        out_mtz.add_column('L', 'H')

        # Add HL coefficient columns
        out_mtz.add_column('HLA', 'A')  # HL coefficient type
        out_mtz.add_column('HLB', 'A')
        out_mtz.add_column('HLC', 'A')
        out_mtz.add_column('HLD', 'A')

        # Set data
        out_mtz.set_data(np.column_stack([
            np.array(mtz.column_with_label('H')),
            np.array(mtz.column_with_label('K')),
            np.array(mtz.column_with_label('L')),
            hla,
            hlb,
            hlc,
            hld
        ]))

        # Write output
        out_mtz.write_to_file(output_path)
        return output_path

    @staticmethod
    def _hl_to_phifom_gemmi(input_path: str, output_path: str, mtz) -> str:
        """
        Convert HL coefficients to PHIFOM format using gemmi.

        Reads HLA, HLB, HLC, HLD columns and calculates best phase (PHI) and
        figure of merit (FOM) using numerical optimization of the phase
        probability distribution.

        Args:
            input_path: Path to input MTZ with HL coefficients
            output_path: Path for output MTZ with PHI/FOM
            mtz: gemmi.Mtz object (already loaded)

        Returns:
            Path to output MTZ file

        References:
            - Read, R.J. (1986). Acta Cryst. A42, 140-149.
            - Hendrickson & Lattman (1970). Acta Cryst. B26, 136-143.
        """
        import gemmi
        import numpy as np

        # Find HL coefficient columns (column type 'A')
        hl_cols = {}
        for col in mtz.columns:
            if col.type == 'A':  # HL coefficient type
                label = col.label
                if 'HLA' in label:
                    hl_cols['HLA'] = col
                elif 'HLB' in label:
                    hl_cols['HLB'] = col
                elif 'HLC' in label:
                    hl_cols['HLC'] = col
                elif 'HLD' in label:
                    hl_cols['HLD'] = col

        if len(hl_cols) != 4:
            raise ValueError(
                f"Expected 4 HL coefficient columns (HLA, HLB, HLC, HLD), "
                f"found {len(hl_cols)}: {list(hl_cols.keys())}"
            )

        # Extract HL coefficients as numpy arrays
        hla = np.array(hl_cols['HLA'])
        hlb = np.array(hl_cols['HLB'])
        hlc = np.array(hl_cols['HLC'])
        hld = np.array(hl_cols['HLD'])

        # Calculate PHI and FOM from HL coefficients
        phi, fom = PhaseDataConverter._hl_to_phifom_calculation(hla, hlb, hlc, hld)

        # Create output MTZ with same structure
        out_mtz = gemmi.Mtz(with_base=False)
        out_mtz.spacegroup = mtz.spacegroup
        out_mtz.set_cell_for_all(mtz.cell)

        # Add a single dataset for all columns
        out_mtz.add_dataset('phase_data')

        # Add H, K, L columns
        out_mtz.add_column('H', 'H')
        out_mtz.add_column('K', 'H')
        out_mtz.add_column('L', 'H')

        # Add PHI and FOM columns
        out_mtz.add_column('PHI', 'P')  # Phase column type
        out_mtz.add_column('FOM', 'W')  # Weight/FOM column type

        # Set data
        out_mtz.set_data(np.column_stack([
            np.array(mtz.column_with_label('H')),
            np.array(mtz.column_with_label('K')),
            np.array(mtz.column_with_label('L')),
            phi,
            fom
        ]))

        # Write output
        out_mtz.write_to_file(output_path)
        return output_path

    @staticmethod
    def _hl_to_phifom_calculation(hla, hlb, hlc, hld):
        """
        Calculate best phase and FOM from Hendrickson-Lattman coefficients.

        The phase probability distribution P(phi) is proportional to:
        exp(A*cos(phi) + B*sin(phi) + C*cos(2*phi) + D*sin(2*phi))

        where A=HLA, B=HLB, C=HLC, D=HLD

        Best phase (phi_best) is found by maximizing P(phi) numerically.
        FOM = <cos(phi - phi_best)> is calculated by numerical integration.

        Args:
            hla, hlb, hlc, hld: Hendrickson-Lattman coefficient arrays (numpy)

        Returns:
            tuple: (phi_best, fom) - Best phase estimate and figure of merit
                   Both in degrees for phi_best, FOM in [0, 1]

        References:
            - Read, R.J. (1986). Acta Cryst. A42, 140-149.
            - Hendrickson & Lattman (1970). Acta Cryst. B26, 136-143.
        """
        import numpy as np

        n_reflections = len(hla)
        phi_best = np.zeros(n_reflections)
        fom = np.zeros(n_reflections)

        # Sample phases from 0 to 360 degrees
        # Use fine grid for accurate maximum finding
        phi_samples = np.linspace(0, 2 * np.pi, 360)

        for i in range(n_reflections):
            # Calculate phase probability distribution
            # P(phi) ∝ exp(A*cos(phi) + B*sin(phi) + C*cos(2*phi) + D*sin(2*phi))
            exponent = (hla[i] * np.cos(phi_samples) +
                        hlb[i] * np.sin(phi_samples) +
                        hlc[i] * np.cos(2 * phi_samples) +
                        hld[i] * np.sin(2 * phi_samples))

            # Prevent overflow by subtracting maximum
            exponent_max = np.max(exponent)
            prob = np.exp(exponent - exponent_max)

            # Find best phase (maximum probability)
            max_idx = np.argmax(prob)
            phi_best[i] = phi_samples[max_idx]

            # Calculate FOM = <cos(phi - phi_best)> by numerical integration
            # FOM = ∫ cos(phi - phi_best) * P(phi) dphi / ∫ P(phi) dphi
            cos_term = np.cos(phi_samples - phi_best[i])
            numerator = np.trapezoid(cos_term * prob, phi_samples)
            denominator = np.trapezoid(prob, phi_samples)

            fom[i] = numerator / denominator if denominator > 0 else 0.0

            # Ensure FOM is in valid range [0, 1]
            fom[i] = np.clip(fom[i], 0.0, 1.0)

        # Convert phi_best from radians to degrees
        phi_best_deg = np.degrees(phi_best)

        return phi_best_deg, fom
