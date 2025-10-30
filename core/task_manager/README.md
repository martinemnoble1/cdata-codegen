# Task Manager and Plugin Registry

This directory contains the plugin registry system for cdata-codegen.

## Directory Structure

- **plugin_registry.py** - Auto-generated lazy-loading plugin registry (LOCKED)
- **plugin_lookup.json** - Plugin metadata index (LOCKED)
- **plugin_lookup.py** - Script to regenerate plugin registry (DO NOT RUN)
- **defxml_lookup.json** - Index of .def.xml files for plugin definitions
- **defxml_lookup.py** - Script to regenerate defxml index
- **def_xml_handler.py** - Parser for .def.xml plugin definition files
- **params_xml_handler.py** - Parser for .params.xml parameter files
- **task_lookup.json** - Legacy task lookup file

## IMPORTANT: Locked Files

The following files are **LOCKED** and should **NOT** be regenerated:

- `plugin_registry.py` (344KB, 148 plugins)
- `plugin_lookup.json` (449KB, 148 plugins)

These files were pre-generated from the legacy ccp4i2 codebase and contain metadata for all plugins in the `wrappers/`, `wrappers2/`, and `pipelines/` directories.

**Why they are locked:**
1. The legacy plugin code requires dependencies (qtgui, report, etc.) not available in this environment
2. The plugin code itself is stable legacy code that should not be modified
3. Regeneration would require a full ccp4i2 environment with all dependencies

## Plugin Registry Usage

The plugin registry provides lazy-loading access to plugin classes:

```python
from core.CCP4TaskManager import TASKMANAGER

# Get task manager instance
task_mgr = TASKMANAGER()

# Get plugin class (lazy loaded)
plugin_class = task_mgr.get_plugin_class('ctruncate')

# Get plugin metadata (no import required)
metadata = task_mgr.get_plugin_metadata('ctruncate')

# List all available plugins
plugins = task_mgr.list_plugins()  # Returns 148 plugin names
```

## Available Plugins

The registry contains 148 plugins including:

- **Data Processing**: ctruncate, aimless, pointless, dials_*, xia2_*
- **Phasing**: phaser_*, shelx_*, crank2_*
- **Refinement**: refmac, buster, prosmart
- **Model Building**: buccaneer, parrot, coot_*
- **Analysis**: molprobity, edstats, moorhen_*
- **Utilities**: pdbset, rwcontents, superpose

## Regenerating DEF.XML Lookup

The defxml lookup can be safely regenerated to pick up new .def.xml files:

```bash
export CCP4I2_ROOT=/Users/nmemn/Developer/cdata-codegen
python core/task_manager/defxml_lookup.py
```

This will scan for .def.xml files and update `defxml_lookup.json`.

## CCP4I2_ROOT Environment Variable

All tests and the plugin system expect `CCP4I2_ROOT` to point to the project root:

```bash
export CCP4I2_ROOT=/Users/nmemn/Developer/cdata-codegen
```

The project root now contains:
- `wrappers/` - Legacy ccp4i2 plugin wrappers
- `wrappers2/` - Additional legacy plugins
- `pipelines/` - Multi-step pipeline plugins
- `demo_data/` - Test data files
- `core/` - New Python implementation
- `server/` - Django backend

## Plugin Import Paths

Plugins are imported using their module paths relative to CCP4I2_ROOT:

- Wrappers: `wrappers.{plugin_name}.script.{module}`
- Wrappers2: `wrappers2.{plugin_name}.script.{module}`
- Pipelines: `pipelines.{plugin_name}.script.{module}`

The registry handles all import logic automatically.
