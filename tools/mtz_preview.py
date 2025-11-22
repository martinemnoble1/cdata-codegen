#!/usr/bin/env python3
"""
MTZ file preview script for VS Code custom editor.

Usage: python mtz_preview.py <mtz_file>

Outputs JSON with MTZ header information for display in VS Code.
"""

import sys
import json
from pathlib import Path


def preview_mtz(mtz_path: str) -> dict:
    """
    Extract header information from an MTZ file.

    Returns:
        dict: MTZ metadata including crystals, datasets, columns, cell, spacegroup
    """
    try:
        import gemmi
    except ImportError:
        return {
            "error": "gemmi not installed",
            "message": "Install gemmi: pip install gemmi"
        }

    try:
        mtz = gemmi.read_mtz_file(mtz_path)
    except Exception as e:
        return {
            "error": "Failed to read MTZ file",
            "message": str(e)
        }

    # Extract basic information
    result = {
        "file_path": str(Path(mtz_path).absolute()),
        "title": mtz.title if hasattr(mtz, 'title') else "N/A",
        "spacegroup": {
            "number": mtz.spacegroup.number if mtz.spacegroup else None,
            "name": mtz.spacegroup.hm if mtz.spacegroup else "Unknown",
            "point_group": mtz.spacegroup.point_group_hm() if mtz.spacegroup else "Unknown"
        },
        "cell": {
            "a": round(mtz.cell.a, 3),
            "b": round(mtz.cell.b, 3),
            "c": round(mtz.cell.c, 3),
            "alpha": round(mtz.cell.alpha, 2),
            "beta": round(mtz.cell.beta, 2),
            "gamma": round(mtz.cell.gamma, 2),
            "volume": round(mtz.cell.volume, 1)
        },
        "nreflections": mtz.nreflections,
        "resolution": {
            "min": round(mtz.resolution_high(), 3),
            "max": round(mtz.resolution_low(), 2)
        },
        "datasets": [],
        "columns": []
    }

    # Extract dataset information
    for dataset in mtz.datasets:
        dataset_info = {
            "id": dataset.id,
            "name": dataset.dataset_name,
            "crystal_name": (dataset.crystal.name
                             if hasattr(dataset, 'crystal') and dataset.crystal
                             else None),
            "wavelength": (round(dataset.wavelength, 4)
                          if dataset.wavelength > 0 else None),
        }
        result["datasets"].append(dataset_info)

    # Extract column information
    for col in mtz.columns:
        col_info = {
            "label": col.label,
            "type": col.type,
            "dataset_id": col.dataset.id if col.dataset else None,
            "dataset_name": col.dataset.dataset_name if col.dataset else None,
            "min_value": round(col.min_value, 3) if col.min_value != float('inf') else None,
            "max_value": round(col.max_value, 3) if col.max_value != float('-inf') else None,
            "source": col.source if hasattr(col, 'source') and col.source else None
        }
        result["columns"].append(col_info)

    # Add column type legend
    result["column_types"] = {
        "H": "index h,k,l",
        "J": "intensity",
        "K": "intensity (anomalous)",
        "G": "amplitude",
        "L": "amplitude (anomalous)",
        "F": "structure factor amplitude",
        "D": "anomalous difference",
        "Q": "standard deviation (sigma)",
        "M": "standard deviation (sigma, anomalous)",
        "E": "normalized structure factor",
        "P": "phase angle (degrees)",
        "W": "weight",
        "A": "Hendrickson-Lattman coefficient",
        "B": "batch number",
        "Y": "M/ISYM",
        "I": "integer (e.g., FreeR flag)"
    }

    return result


def format_as_markdown(data: dict) -> str:
    """Format MTZ metadata as Markdown for display."""
    if "error" in data:
        return f"# Error\n\n**{data['error']}**\n\n{data['message']}"

    md = []

    # Header
    md.append(f"# MTZ File: {Path(data['file_path']).name}")
    md.append("")

    # Basic info
    md.append("## Overview")
    md.append(f"- **File**: `{data['file_path']}`")
    md.append(f"- **Title**: {data['title']}")
    md.append(f"- **Reflections**: {data['nreflections']:,}")
    md.append(f"- **Resolution**: {data['resolution']['min']} Å - {data['resolution']['max']} Å")
    md.append("")

    # Spacegroup
    md.append("## Space Group")
    md.append(f"- **Number**: {data['spacegroup']['number']}")
    md.append(f"- **Hermann-Mauguin**: {data['spacegroup']['name']}")
    md.append(f"- **Point Group**: {data['spacegroup']['point_group']}")
    md.append("")

    # Unit cell
    md.append("## Unit Cell")
    cell = data['cell']
    md.append(f"- **a, b, c**: {cell['a']} Å, {cell['b']} Å, {cell['c']} Å")
    md.append(f"- **α, β, γ**: {cell['alpha']}°, {cell['beta']}°, {cell['gamma']}°")
    md.append(f"- **Volume**: {cell['volume']} ų")
    md.append("")

    # Datasets
    if data['datasets']:
        md.append("## Datasets")
        md.append("")
        md.append("| ID | Name | Crystal | Wavelength (Å) |")
        md.append("|---|---|---|---|")
        for ds in data['datasets']:
            wavelength = (f"{ds['wavelength']:.4f}"
                         if ds['wavelength'] else "N/A")
            crystal = ds.get('crystal_name', 'N/A') or 'N/A'
            md.append(f"| {ds['id']} | {ds['name']} | {crystal} | "
                     f"{wavelength} |")
        md.append("")

    # Columns
    if data['columns']:
        md.append("## Columns")
        md.append("")
        md.append("| Label | Type | Dataset | Min | Max |")
        md.append("|---|---|---|---|---|")
        for col in data['columns']:
            min_val = (f"{col['min_value']:.3f}"
                      if col['min_value'] is not None else "N/A")
            max_val = (f"{col['max_value']:.3f}"
                      if col['max_value'] is not None else "N/A")
            dataset = (col['dataset_name'] or
                      f"ID:{col['dataset_id']}" or "N/A")
            md.append(f"| {col['label']} | {col['type']} | {dataset} | "
                     f"{min_val} | {max_val} |")
        md.append("")

    # Column type legend
    md.append("## Column Type Reference")
    md.append("")
    for code, description in sorted(data['column_types'].items()):
        md.append(f"- **{code}**: {description}")
    md.append("")

    return "\n".join(md)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "error": "No file specified",
            "message": "Usage: python mtz_preview.py <mtz_file>"
        }))
        sys.exit(1)

    mtz_file = sys.argv[1]

    if not Path(mtz_file).exists():
        print(json.dumps({
            "error": "File not found",
            "message": f"MTZ file not found: {mtz_file}"
        }))
        sys.exit(1)

    # Extract metadata
    data = preview_mtz(mtz_file)

    # Output format: --json for JSON, default is Markdown
    if "--json" in sys.argv:
        print(json.dumps(data, indent=2))
    else:
        print(format_as_markdown(data))


if __name__ == "__main__":
    main()
