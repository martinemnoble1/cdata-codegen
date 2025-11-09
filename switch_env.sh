#!/bin/bash
# Switch between Python 3.9 and Python 3.11 environments
# Usage: ./switch_env.sh [py39|py311]

switch_to_env() {
    local env_file=$1
    local env_name=$2

    echo "Switching to $env_name environment..."

    # Load the environment config to get VENV_TARGET
    source "$env_file"

    # Remove existing .venv symlink if it exists
    if [ -L .venv ]; then
        rm .venv
    elif [ -d .venv ] && [ ! -L .venv ]; then
        echo "ERROR: .venv exists but is not a symlink!"
        echo "Please manually rename .venv to .venv.py311 or .venv.old-py39"
        exit 1
    fi

    # Create new symlink
    ln -s "$VENV_TARGET" .venv

    # Copy the env file to .env
    cp "$env_file" .env

    echo "✓ Switched to $env_name"
    echo "✓ .venv -> $VENV_TARGET"
    echo ""
    cat .env | grep -v "^#" | grep -v "^$"
}

if [ "$1" == "py39" ]; then
    switch_to_env .env.py39 "Python 3.9 (CCP4-9)"
elif [ "$1" == "py311" ]; then
    switch_to_env .env.py311 "Python 3.11 (CCP4-20251105)"
elif [ "$1" == "status" ] || [ "$1" == "" ]; then
    echo "Current environment configuration:"
    echo "=========================================="
    if [ -f .env ]; then
        cat .env | grep -v "^#" | grep -v "^$"
        echo ""
        if [ -L .venv ]; then
            echo "Symlink: .venv -> $(readlink .venv)"
        elif [ -d .venv ]; then
            echo "⚠️  .venv is a directory, not a symlink!"
        else
            echo "⚠️  .venv does not exist!"
        fi
    else
        echo "ERROR: .env file not found"
        echo ""
        echo "Run: ./switch_env.sh py39   (for Python 3.9)"
        echo "  or: ./switch_env.sh py311  (for Python 3.11)"
    fi
else
    echo "Usage: ./switch_env.sh [py39|py311|status]"
    echo ""
    echo "  py39   - Switch to Python 3.9 (CCP4-9)"
    echo "  py311  - Switch to Python 3.11 (CCP4-20251105)"
    echo "  status - Show current configuration (default)"
    exit 1
fi
