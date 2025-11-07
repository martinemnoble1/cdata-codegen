#!/bin/bash
# Regenerate plugin registry with CCP4-10 environment

source /Users/nmemn/Developer/ccp4-20251105/bin/ccp4.setup-sh

export CCP4I2_ROOT=$(pwd)
export PYTHONPATH=$(pwd):$(pwd)/server:$PYTHONPATH

.venv/bin/python core/task_manager/plugin_lookup.py
