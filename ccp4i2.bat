@echo off
REM ccp4i2.bat - Modern CLI for cdata-codegen (CCP4i2 replacement) - Windows version
REM
REM This wrapper sets up the environment and runs the modern CLI interface.
REM The CLI provides a clean, resource-oriented command structure.
REM
REM Usage:
REM   ccp4i2 projects list
REM   ccp4i2 jobs create <project> <task>
REM   ccp4i2 jobs run <project> <job> --detach

setlocal enabledelayedexpansion

REM Get the directory where this script lives (project root)
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

REM Export project root as CCP4I2_ROOT
set "CCP4I2_ROOT=%SCRIPT_DIR%"

REM Add project root and server to PYTHONPATH
set "PYTHONPATH=%CCP4I2_ROOT%;%CCP4I2_ROOT%\server;%PYTHONPATH%"

REM Activate virtual environment
if exist "%SCRIPT_DIR%\.venv\Scripts\activate.bat" (
    call "%SCRIPT_DIR%\.venv\Scripts\activate.bat"
) else (
    echo Warning: Virtual environment not found at %SCRIPT_DIR%\.venv 1>&2
)

REM Source CCP4 environment setup (Windows version)
REM Adjust path as needed for Windows CCP4 installation
if exist "C:\CCP4\ccp4-9\bin\ccp4.setup.bat" (
    call "C:\CCP4\ccp4-9\bin\ccp4.setup.bat"
) else (
    REM Try alternative location
    if exist "%USERPROFILE%\CCP4\ccp4-9\bin\ccp4.setup.bat" (
        call "%USERPROFILE%\CCP4\ccp4-9\bin\ccp4.setup.bat"
    ) else (
        echo Warning: CCP4 setup script not found 1>&2
    )
)

REM Execute the modern CLI with all forwarded arguments
python "%SCRIPT_DIR%\server\manage_cli.py" %*
