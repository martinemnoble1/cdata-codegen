#!/usr/bin/env pwsh
# ccp4i2.ps1 - Modern CLI for cdata-codegen (CCP4i2 replacement) - PowerShell version
#
# This wrapper sets up the environment and runs the modern CLI interface.
# The CLI provides a clean, resource-oriented command structure.
#
# Usage:
#   ccp4i2 projects list
#   ccp4i2 jobs create <project> <task>
#   ccp4i2 jobs run <project> <job> --detach

# Get the directory where this script lives (project root)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Export project root as CCP4I2_ROOT
$env:CCP4I2_ROOT = $ScriptDir

# Add project root and server to PYTHONPATH
$env:PYTHONPATH = "$ScriptDir;$ScriptDir\server;$env:PYTHONPATH"

# Activate virtual environment
$VenvActivate = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"
if (Test-Path $VenvActivate) {
    & $VenvActivate
} else {
    Write-Warning "Virtual environment not found at $ScriptDir\.venv"
}

# Source CCP4 environment setup (Windows version)
# Note: You may need to adjust the path for your CCP4 installation
$CCP4Setup = "C:\CCP4\ccp4-9\bin\ccp4.setup.ps1"
if (Test-Path $CCP4Setup) {
    & $CCP4Setup
} else {
    # Try alternative location
    $CCP4SetupAlt = Join-Path $env:USERPROFILE "CCP4\ccp4-9\bin\ccp4.setup.ps1"
    if (Test-Path $CCP4SetupAlt) {
        & $CCP4SetupAlt
    } else {
        Write-Warning "CCP4 setup script not found"
    }
}

# Execute the modern CLI with all forwarded arguments
$ManageCLI = Join-Path $ScriptDir "server\manage_cli.py"
& python $ManageCLI $args
exit $LASTEXITCODE
