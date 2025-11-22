#!/bin/bash
# Install MTZ Viewer extension to VS Code

EXTENSION_DIR="$HOME/.vscode/extensions/mtz-viewer"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing MTZ Viewer extension..."
echo "Source: $SOURCE_DIR"
echo "Target: $EXTENSION_DIR"

# Remove existing installation
if [ -L "$EXTENSION_DIR" ] || [ -d "$EXTENSION_DIR" ]; then
    echo "Removing existing installation..."
    rm -rf "$EXTENSION_DIR"
fi

# Create symlink
ln -s "$SOURCE_DIR" "$EXTENSION_DIR"

echo "✅ Extension installed!"
echo ""
echo "Next steps:"
echo "1. Reload VS Code window (Cmd+Shift+P -> 'Reload Window')"
echo "2. Open any .mtz file"
echo "3. The MTZ Preview should open automatically"
