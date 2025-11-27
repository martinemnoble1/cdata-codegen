#!/bin/bash
#
# Run a prosmart_refmac job via the HTTP API using gamma demo data.
#
# Usage:
#   ./scripts/run_refmac_via_api.sh <project_id_or_name>
#
# Examples:
#   ./scripts/run_refmac_via_api.sh 1                    # by project ID
#   ./scripts/run_refmac_via_api.sh "My Project"         # by project name (requires lookup)
#
# Prerequisites:
#   - Django server running (./manage.py runserver or similar)
#   - Demo data available in demo_data/gamma/
#
# Environment variables:
#   API_BASE_URL  - Base URL of the API (default: http://localhost:8000)
#

set -e

# Configuration
API_BASE_URL="${API_BASE_URL:-http://localhost:8000}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DEMO_DATA_DIR="$PROJECT_ROOT/demo_data/gamma"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "\n${YELLOW}=== Step $1: $2 ===${NC}"
}

# Check arguments
if [ $# -lt 1 ]; then
    echo "Usage: $0 <project_id>"
    echo ""
    echo "Arguments:"
    echo "  project_id  - The numeric ID of the project to create the job in"
    echo ""
    echo "Environment variables:"
    echo "  API_BASE_URL  - Base URL of the API (default: http://localhost:8000)"
    echo ""
    echo "Example:"
    echo "  $0 1"
    echo "  API_BASE_URL=http://localhost:8080 $0 1"
    exit 1
fi

PROJECT_ID="$1"

# Verify demo data exists
PDB_FILE="$DEMO_DATA_DIR/gamma_model.pdb"
MTZ_FILE="$DEMO_DATA_DIR/merged_intensities_Xe.mtz"

if [ ! -f "$PDB_FILE" ]; then
    log_error "Demo PDB file not found: $PDB_FILE"
    exit 1
fi

if [ ! -f "$MTZ_FILE" ]; then
    log_error "Demo MTZ file not found: $MTZ_FILE"
    exit 1
fi

log_info "Using API at: $API_BASE_URL"
log_info "Project ID: $PROJECT_ID"
log_info "Demo data directory: $DEMO_DATA_DIR"

# Step 1: Create the job
log_step 1 "Creating prosmart_refmac job"

CREATE_RESPONSE=$(curl -s -X POST \
    "$API_BASE_URL/projects/$PROJECT_ID/create_task/" \
    -H "Content-Type: application/json" \
    -d '{
        "task_name": "prosmart_refmac",
        "title": "API Test - Gamma Refmac"
    }')

echo "Response: $CREATE_RESPONSE"

# Extract job ID from response
JOB_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('new_job', {}).get('id', ''))" 2>/dev/null)
JOB_UUID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('new_job', {}).get('uuid', ''))" 2>/dev/null)

if [ -z "$JOB_ID" ]; then
    log_error "Failed to create job. Response: $CREATE_RESPONSE"
    exit 1
fi

log_success "Created job ID: $JOB_ID (UUID: $JOB_UUID)"

# Step 2: Upload PDB file
log_step 2 "Uploading PDB file (XYZIN)"

UPLOAD_PDB_RESPONSE=$(curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/upload_file_param/" \
    -F "objectPath=prosmart_refmac.inputData.XYZIN" \
    -F "file=@$PDB_FILE")

echo "Response: $UPLOAD_PDB_RESPONSE"

STATUS=$(echo "$UPLOAD_PDB_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'Unknown'))" 2>/dev/null)
if [ "$STATUS" != "Success" ]; then
    log_error "Failed to upload PDB file"
    exit 1
fi

log_success "PDB file uploaded successfully"

# Step 3: Upload MTZ file with column selector
log_step 3 "Uploading MTZ file (F_SIGF) with anomalous column selector"

UPLOAD_MTZ_RESPONSE=$(curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/upload_file_param/" \
    -F "objectPath=prosmart_refmac.inputData.F_SIGF" \
    -F "file=@$MTZ_FILE" \
    -F "column_selector=/*/*/[Iplus,SIGIplus,Iminus,SIGIminus]")

echo "Response: $UPLOAD_MTZ_RESPONSE"

STATUS=$(echo "$UPLOAD_MTZ_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'Unknown'))" 2>/dev/null)
if [ "$STATUS" != "Success" ]; then
    log_error "Failed to upload MTZ file"
    exit 1
fi

log_success "MTZ file uploaded successfully"

# Step 4: Set control parameters
log_step 4 "Setting control parameters"

# Set NCYCLES
log_info "Setting NCYCLES=2"
curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/set_parameter/" \
    -H "Content-Type: application/json" \
    -d '{
        "object_path": "prosmart_refmac.controlParameters.NCYCLES",
        "value": 2
    }' | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"  Status: {d.get('status')}\")"

# Set ADD_WATERS=false
log_info "Setting ADD_WATERS=false"
curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/set_parameter/" \
    -H "Content-Type: application/json" \
    -d '{
        "object_path": "prosmart_refmac.controlParameters.ADD_WATERS",
        "value": false
    }' | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"  Status: {d.get('status')}\")"

# Set VALIDATE_MOLPROBITY=false
log_info "Setting VALIDATE_MOLPROBITY=false"
curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/set_parameter/" \
    -H "Content-Type: application/json" \
    -d '{
        "object_path": "prosmart_refmac.controlParameters.VALIDATE_MOLPROBITY",
        "value": false
    }' | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"  Status: {d.get('status')}\")"

# Set USEANOMALOUS=true
log_info "Setting USEANOMALOUS=true"
curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/set_parameter/" \
    -H "Content-Type: application/json" \
    -d '{
        "object_path": "prosmart_refmac.controlParameters.USEANOMALOUS",
        "value": true
    }' | python3 -c "import sys, json; d=json.load(sys.stdin); print(f\"  Status: {d.get('status')}\")"

log_success "Control parameters set"

# Step 5: Run the job
log_step 5 "Running the job"

RUN_RESPONSE=$(curl -s -X POST \
    "$API_BASE_URL/jobs/$JOB_ID/run/" \
    -H "Content-Type: application/json")

echo "Response: $RUN_RESPONSE"

log_success "Job execution initiated"

# Step 6: Poll for completion (optional)
log_step 6 "Polling for job status"

log_info "Polling every 10 seconds (Ctrl+C to stop)..."

POLL_COUNT=0
MAX_POLLS=60  # 10 minutes max

while [ $POLL_COUNT -lt $MAX_POLLS ]; do
    STATUS_RESPONSE=$(curl -s "$API_BASE_URL/jobs/$JOB_ID/")

    JOB_STATUS=$(echo "$STATUS_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status', 'Unknown'))" 2>/dev/null)
    JOB_STATUS_DISPLAY=$(echo "$STATUS_RESPONSE" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('status_display', 'Unknown'))" 2>/dev/null)

    echo -ne "\r[$(date +%H:%M:%S)] Job status: $JOB_STATUS_DISPLAY ($JOB_STATUS)    "

    # Status codes: 1=PENDING, 3=RUNNING, 5=FAILED, 6=FINISHED
    if [ "$JOB_STATUS" = "6" ]; then
        echo ""
        log_success "Job completed successfully!"
        break
    elif [ "$JOB_STATUS" = "5" ]; then
        echo ""
        log_error "Job failed!"
        break
    fi

    sleep 10
    POLL_COUNT=$((POLL_COUNT + 1))
done

if [ $POLL_COUNT -ge $MAX_POLLS ]; then
    echo ""
    log_error "Timeout waiting for job to complete"
fi

# Summary
echo ""
echo "=========================================="
echo "Job Summary"
echo "=========================================="
echo "Job ID:     $JOB_ID"
echo "Job UUID:   $JOB_UUID"
echo "API URL:    $API_BASE_URL/jobs/$JOB_ID/"
echo ""
echo "To check job status manually:"
echo "  curl $API_BASE_URL/jobs/$JOB_ID/"
echo ""
echo "To view job details in browser:"
echo "  open $API_BASE_URL/jobs/$JOB_ID/"
echo "=========================================="
