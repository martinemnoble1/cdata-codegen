#!/bin/bash
# Test runner for async database integration tests

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Async Database Integration Test Runner${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Source CCP4 environment to get executables on PATH
if [ -f /Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh ]; then
    echo -e "${YELLOW}Sourcing CCP4 environment...${NC}"
    source /Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh
    echo -e "${GREEN}✓ CCP4 environment loaded${NC}"
    echo "  CCP4: $CCP4"
    echo "  CBIN: $CBIN"
else
    echo -e "${YELLOW}Warning: CCP4 environment not found at /Users/nmemn/Developer/ccp4-20251105${NC}"
    echo "  Some tests requiring CCP4 executables may fail"
fi
echo ""

# Set up environment
export CCP4I2_ROOT=$(pwd)
# Python path: server directory for Django imports, project root for core imports
export PYTHONPATH=$(pwd)/server:$(pwd):$PYTHONPATH
export DJANGO_SETTINGS_MODULE=ccp4x.config.test_settings

# Create temporary database
TMP_DB=$(mktemp -t test_db_XXXXXX).sqlite3
export CCP4I2_DB_FILE=$TMP_DB

# Create temporary projects directory
TMP_PROJECTS=$(mktemp -d -t test_projects_XXXXXX)
export CCP4I2_PROJECTS_DIR=$TMP_PROJECTS

echo -e "${YELLOW}Test Configuration:${NC}"
echo "  CCP4I2_ROOT: $CCP4I2_ROOT"
echo "  Test Database: $TMP_DB"
echo "  Projects Directory: $TMP_PROJECTS"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Cleaning up...${NC}"
    if [ -f "$TMP_DB" ]; then
        rm -f "$TMP_DB"
        echo "  Removed test database: $TMP_DB"
    fi
    if [ -d "$TMP_PROJECTS" ]; then
        rm -rf "$TMP_PROJECTS"
        echo "  Removed test projects directory: $TMP_PROJECTS"
    fi
}
trap cleanup EXIT

# Change to server directory for Django
cd server

echo -e "${YELLOW}Step 1: Running Django migrations...${NC}"
python manage.py migrate --run-syncdb 2>&1 | grep -E "(Applying|Operations|OK)" || true
echo -e "${GREEN}✓ Migrations complete${NC}"
echo ""

# Return to root directory
cd ..

echo -e "${YELLOW}Step 2: Running database integration tests...${NC}"
echo ""

# Run basic database integration tests
echo -e "${YELLOW}2a. Basic database operations...${NC}"
python -m pytest tests/test_async_db_integration.py -v -s

echo ""
echo -e "${YELLOW}2b. End-to-end plugin execution with database...${NC}"
# Run end-to-end tests with real plugin execution
python -m pytest tests/test_async_plugin_with_database.py -v -s

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "${GREEN}========================================${NC}"
