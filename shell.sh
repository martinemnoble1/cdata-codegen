#!/bin/bash
# Django shell with full CCP4 environment
# Usage: ./shell.sh

# Get the directory where this script lives (project root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Export project root as CCP4I2_ROOT
export CCP4I2_ROOT="$SCRIPT_DIR"

# Add project root and server to PYTHONPATH
export PYTHONPATH="$CCP4I2_ROOT:$CCP4I2_ROOT/server:$PYTHONPATH"

# Activate virtual environment
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
else
    echo "Warning: Virtual environment not found at $SCRIPT_DIR/.venv" >&2
fi

# Source CCP4 environment setup
if [ -f "/Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh" ]; then
    source /Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh
else
    echo "Warning: CCP4 setup script not found at /Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh" >&2
fi

# Set Django settings
export DJANGO_SETTINGS_MODULE=ccp4x.config.settings

# Launch Django shell
cd "$SCRIPT_DIR/server"
python manage.py shell
