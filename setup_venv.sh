#!/bin/bash
# Post-installation cleanup script for cdata-codegen virtual environment
# Removes broken MolProbity executables installed by cctbx-base package

set -e

echo "=== cdata-codegen Virtual Environment Setup ==="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Error: .venv directory not found"
    echo "Please create virtual environment first:"
    echo "  python3.11 -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "✓ Virtual environment found at .venv/"
source .venv/bin/activate

# Check for broken MolProbity executables
MOLPROBITY_COUNT=$(ls .venv/bin/molprobity.* 2>/dev/null | wc -l)

if [ "$MOLPROBITY_COUNT" -gt 0 ]; then
    echo ""
    echo "⚠️  Found $MOLPROBITY_COUNT broken MolProbity executables from cctbx-base"
    echo ""
    echo "These executables have hardcoded conda build paths and will shadow"
    echo "the working CCP4 MolProbity tools, causing validation tests to fail."
    echo ""
    echo "Listing broken executables:"
    ls .venv/bin/molprobity.* 2>/dev/null | sed 's/^/  - /'
    echo ""
    read -p "Remove these broken executables? [Y/n] " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
        rm .venv/bin/molprobity.*
        echo "✅ Removed broken MolProbity executables"
    else
        echo "⚠️  Skipped removal - validation tests with MolProbity will fail"
    fi
else
    echo "✓ No broken MolProbity executables found"
fi

echo ""
echo "=== Virtual Environment Status ==="
echo ""

# Check Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if CCP4 modules are symlinked
SYMLINK_COUNT=$(ls -la .venv/lib/python3.11/site-packages/ 2>/dev/null | grep "^l" | wc -l)
echo "CCP4 symlinked modules: $SYMLINK_COUNT"

if [ "$SYMLINK_COUNT" -lt 10 ]; then
    echo ""
    echo "⚠️  Expected 10 symlinked CCP4 modules, found $SYMLINK_COUNT"
    echo "Run symlink setup commands from DEVELOPMENT_SETUP_SUMMARY.md"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Source CCP4 environment: source /path/to/ccp4/bin/ccp4.setup-sh"
echo "2. Verify MolProbity: which molprobity.ramalyze"
echo "   (should point to CCP4 bin, not .venv/bin)"
echo "3. Run tests: ./run_test.sh tests/i2run"
echo ""
