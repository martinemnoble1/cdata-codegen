#!/bin/bash
# Test dispatcher for i2run tests
# Usage: ./run_test.sh <test_file_or_dir> [pytest_args...]
# Example: ./run_test.sh server/ccp4x/tests/i2run/test_i2run.py
# Example: ./run_test.sh server/ccp4x/tests/i2run/test_i2run.py::test_prosmart_refmac
# Example: ./run_test.sh i2run/ --ignore=test_mrbump.py -n auto
# Example: ./run_test.sh i2run/ -n 4 -v

source /Applications/ccp4-9/bin/ccp4.setup-sh

set -e  # Exit on error

# Set up environment
export CCP4I2_ROOT=$(pwd)
export PYTHONPATH=$(pwd):$(pwd)/server:$PYTHONPATH
export DJANGO_SETTINGS_MODULE=ccp4x.config.settings

# Optional: Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Get test path from first argument
TEST_PATH="${1:-server/ccp4x/tests/i2run/test_i2run.py}"
shift  # Remove first argument, leaving remaining args for pytest

# Run pytest with all remaining arguments passed through
echo "Running pytest $TEST_PATH $@"
python -m pytest "$TEST_PATH" "$@"
