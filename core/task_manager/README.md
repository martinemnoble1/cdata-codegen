# Task Manager and Plugin Registry

This directory contains the plugin registry system for cdata-codegen.

## Directory Structure

- **plugin_registry.py** - Auto-generated lazy-loading plugin registry
- **plugin_lookup.json** - Plugin metadata index
- **plugin_lookup.py** - Script to regenerate plugin registry
- **defxml_lookup.json** - Index of .def.xml files for plugin definitions
- **defxml_lookup.py** - Script to regenerate defxml index
- **def_xml_handler.py** - Parser for .def.xml plugin definition files
- **params_xml_handler.py** - Parser for .params.xml parameter files
- **task_lookup.json** - Legacy task lookup file

## Regenerating Plugin Registry

The plugin registry can be regenerated from the local plugins in `wrappers/`, `wrappers2/`, and `pipelines/`:

```bash
export CCP4I2_ROOT=/Users/nmemn/Developer/cdata-codegen
.venv/bin/python core/task_manager/plugin_lookup.py
```

**Important Notes:**
1. Use the virtual environment's Python (`.venv/bin/python`) to ensure all dependencies are available
2. The script will scan all three plugin directories and extract metadata from CPluginScript subclasses
3. Plugins that fail to import (due to missing dependencies like qtgui, mmut, etc.) will be skipped with warnings
4. The generated files contain metadata for plugins that can be successfully imported (~144 plugins)
5. Module paths are automatically corrected to be relative to CCP4I2_ROOT (e.g., `pipelines.servalcat_pipe.script.servalcat_pipe`)

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
plugins = task_mgr.list_plugins()  # Returns 144 plugin names
```

## Available Plugins

The registry contains 144 plugins including:

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
