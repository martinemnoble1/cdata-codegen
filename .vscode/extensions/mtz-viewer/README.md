# MTZ File Viewer Extension

VS Code extension for previewing MTZ crystallographic data files.

## Features

- **Custom Editor**: Opens `.mtz` files in a formatted preview
- **Metadata Display**: Shows comprehensive MTZ file information:
  - File path, title, reflection count, resolution range
  - Space group (number, Hermann-Mauguin symbol, point group)
  - Unit cell parameters (a, b, c, α, β, γ, volume)
  - Datasets with wavelength information
  - All columns with type, dataset, and value ranges
  - Column type reference legend

## Installation

This extension is installed locally in the workspace.

### Manual Installation

1. The extension is already in `.vscode/extensions/mtz-viewer/`
2. Open VS Code in this workspace
3. The extension should activate automatically when you open an `.mtz` file

### Development Mode

To develop or debug the extension:

1. Open the workspace in VS Code
2. Press `F5` to launch Extension Development Host
3. Open any `.mtz` file in the new window
4. The custom MTZ viewer should open

## Usage

1. Open any `.mtz` file in the workspace (e.g., `demo_data/gamma/freeR.mtz`)
2. The file will automatically open in the MTZ Preview editor
3. View comprehensive metadata in a formatted table layout

## Requirements

- Python 3 (uses `.venv/bin/python` if available, otherwise `python3`)
- `gemmi` Python package (already installed in project venv)
- The `tools/mtz_preview.py` script in the workspace

## Extension Settings

This extension has no configurable settings.

## Technical Details

The extension:
1. Registers a custom editor for `*.mtz` files
2. Runs `tools/mtz_preview.py` to extract MTZ metadata
3. Converts the markdown output to HTML
4. Displays in a VS Code webview with theme-aware styling

## Known Issues

- Tables may not wrap well on very narrow windows
- Very large MTZ files may take a moment to load

## Release Notes

### 0.1.0

Initial release:
- Custom editor for MTZ files
- Comprehensive metadata display
- Theme-aware styling
