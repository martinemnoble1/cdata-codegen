#!/bin/bash
# Test dispatcher for i2run tests
# Usage: ./run_test.sh <test_file> [<test_name>]
# Example: ./run_test.sh server/ccp4x/tests/i2run/test_i2run.py
# Example: ./run_test.sh server/ccp4x/tests/i2run/test_i2run.py::test_prosmart_refmac

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

# Get test path from argument
TEST_PATH="${1:-server/ccp4x/tests/i2run/test_i2run.py}"

# Run pytest with verbose output
if [ -z "$2" ]; then
    # Run all tests in file
    echo "Running all tests in $TEST_PATH"
    python -m pytest "$TEST_PATH"
else
    # Run specific test
    echo "Running test $TEST_PATH::$2"
    python -m pytest "$TEST_PATH::$2"
fi
