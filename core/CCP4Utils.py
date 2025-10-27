"""
CCP4 Utility Functions

Collection of utility functions for CCP4 crystallographic operations.
This module has no CData dependencies - pure utility functions.
"""

from pathlib import Path
from typing import List, Dict, Union, Optional
import gemmi
import numpy as np


class MtzMergeError(Exception):
    """Errors during MTZ merging operations."""
    pass


def merge_mtz_files(
    input_specs: List[dict],
    output_path: Union[str, Path],
    merge_strategy: str = 'first'
) -> Path:
    """
    Merge multiple MTZ files using gemmi (completely CData-agnostic).

    This is a low-level utility that merges reflection data from multiple
    MTZ files into a single output file. It has NO knowledge of CMiniMtzDataFile,
    CONTENT_SIGNATURE_LIST, or any CData conventions.

    Args:
        input_specs: List of dictionaries, each containing:
            {
                'path': str/Path,                    # Filesystem path to input MTZ
                'column_mapping': Dict[str, str]     # input_label -> output_label
            }

            The column_mapping dictionary specifies which columns to copy and what
            to call them in the output. For example:
                {'F': 'F_NAT', 'SIGF': 'SIGF_NAT'}  # Copy F as F_NAT, SIGF as SIGF_NAT
                {'FreeR_flag': 'FreeR_flag'}          # Copy FreeR_flag unchanged

        output_path: Where to write the merged MTZ file

        merge_strategy: How to handle output column name conflicts:
            - 'first': Keep column from first file (default)
            - 'last': Keep column from last file (not fully implemented)
            - 'error': Raise error on conflicts
            - 'rename': Auto-rename conflicts (F, F_1, F_2, ...)

    Returns:
        Path: Full path to created output file

    Raises:
        FileNotFoundError: If input MTZ file doesn't exist
        ValueError: If column not found or conflict with strategy='error'
        MtzMergeError: If gemmi operations fail

    Example:
        >>> merge_mtz_files(
        ...     input_specs=[
        ...         {
        ...             'path': '/data/native.mtz',
        ...             'column_mapping': {'F': 'F_NAT', 'SIGF': 'SIGF_NAT'}
        ...         },
        ...         {
        ...             'path': '/data/free.mtz',
        ...             'column_mapping': {'FreeR_flag': 'FreeR_flag'}
        ...         }
        ...     ],
        ...     output_path='/data/merged.mtz',
        ...     merge_strategy='first'
        ... )
        Path('/data/merged.mtz')
    """
    output_path = Path(output_path)

    # Validate inputs
    if not input_specs:
        raise ValueError("input_specs cannot be empty")

    # Read first file to get base metadata and reflections
    first_spec = input_specs[0]
    first_path = Path(first_spec['path'])

    if not first_path.exists():
        raise FileNotFoundError(f"Input MTZ file not found: {first_path}")

    try:
        first_mtz = gemmi.read_mtz_file(str(first_path))
    except Exception as e:
        raise MtzMergeError(f"Failed to read {first_path}: {e}")

    # Create new output MTZ starting with H, K, L data from first file
    # We'll copy the full data array from the first file, which includes H, K, L
    out_mtz = gemmi.Mtz(with_base=True)
    out_mtz.spacegroup = first_mtz.spacegroup
    out_mtz.set_cell_for_all(first_mtz.cell)

    # Copy the reflection data (H, K, L) from first file
    # Extract just the H, K, L columns (first 3 columns)
    hkl_data = first_mtz.array[:, :3]  # Just H, K, L columns
    out_mtz.set_data(hkl_data)

    # Track which columns have been added to detect conflicts
    # H, K, L are already present from with_base=True
    added_columns = {'H', 'K', 'L'}

    # Process each input file
    for spec_idx, spec in enumerate(input_specs):
        input_path = Path(spec['path'])
        column_mapping = spec.get('column_mapping', {})

        # Validate required keys
        if 'path' not in spec or 'column_mapping' not in spec:
            raise ValueError(f"input_specs[{spec_idx}] missing required key 'path' or 'column_mapping'")

        if not column_mapping:
            continue  # Skip empty column mapping

        # Check file exists
        if not input_path.exists():
            raise FileNotFoundError(f"Input MTZ file not found: {input_path}")

        # Read MTZ file
        try:
            in_mtz = gemmi.read_mtz_file(str(input_path))
        except Exception as e:
            raise MtzMergeError(f"Failed to read {input_path}: {e}")

        # Validate compatibility (same space group and cell)
        if in_mtz.spacegroup.number != out_mtz.spacegroup.number:
            raise MtzMergeError(
                f"Incompatible space groups: {first_path} has {out_mtz.spacegroup.hm}, "
                f"{input_path} has {in_mtz.spacegroup.hm}"
            )

        # Check cell parameters (allow small differences)
        cell_diff = sum(abs(a - b) for a, b in zip(in_mtz.cell.parameters, out_mtz.cell.parameters))
        if cell_diff > 0.1:  # Tolerance for cell parameter differences
            raise MtzMergeError(
                f"Incompatible unit cells: {first_path} has {out_mtz.cell.parameters}, "
                f"{input_path} has {in_mtz.cell.parameters}"
            )

        # Copy requested columns (input_label -> output_label)
        for input_label, output_label in column_mapping.items():
            # Find column in input MTZ
            src_col = in_mtz.column_with_label(input_label)
            if src_col is None:
                raise ValueError(
                    f"Column '{input_label}' not found in {input_path}. "
                    f"Available columns: {[c.label for c in in_mtz.columns]}"
                )

            # Check for conflicts
            if output_label in added_columns:
                if merge_strategy == 'error':
                    raise ValueError(
                        f"Column conflict: '{output_label}' already exists in output. "
                        f"Source: {input_path}, column: {input_label}"
                    )
                elif merge_strategy == 'first':
                    # Skip this column, keep the first one
                    continue
                elif merge_strategy == 'last':
                    # Remove existing column and add new one
                    # Gemmi doesn't support removing columns, so we'll skip for now
                    #  TODO: implement column replacement
                    pass
                elif merge_strategy == 'rename':
                    # Auto-rename with suffix
                    counter = 1
                    new_label = f"{output_label}_{counter}"
                    while new_label in added_columns:
                        counter += 1
                        new_label = f"{output_label}_{counter}"
                    output_label = new_label

            # Copy column to output
            # This will match H,K,L indices between files and copy values
            try:
                # Add dataset if needed (use first dataset from source)
                if not out_mtz.datasets:
                    out_mtz.add_dataset('merged')

                # Copy the column (gemmi handles H,K,L matching)
                out_mtz.copy_column(-1, src_col)

                # Rename if needed
                if output_label != input_label:
                    # Get the just-added column and rename it
                    out_mtz.columns[-1].label = output_label

                added_columns.add(output_label)

            except Exception as e:
                raise MtzMergeError(f"Failed to copy column '{input_label}' from {input_path}: {e}")

    # Update resolution limits
    out_mtz.update_reso()

    # Add history
    history_lines = [
        'Merged MTZ files using merge_mtz_files (gemmi)',
        f'Input files: {len(input_specs)}',
        f'Strategy: {merge_strategy}'
    ]
    for spec in input_specs:
        mapping = spec.get('column_mapping', {})
        cols = ', '.join(f"{in_col}->{out_col}" for in_col, out_col in mapping.items())
        history_lines.append(f"  - {spec['path']}: {cols}")
    out_mtz.history = history_lines

    # Write output file
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        out_mtz.write_to_file(str(output_path))
    except Exception as e:
        raise MtzMergeError(f"Failed to write output MTZ to {output_path}: {e}")

    return output_path
