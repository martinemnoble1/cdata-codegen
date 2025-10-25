"""
Tests for lazy-loading plugin registry.
"""

import pytest
import os
from core.CCP4TaskManager import TASKMANAGER


@pytest.mark.skipif(
    'CCP4I2_ROOT' not in os.environ,
    reason="CCP4I2_ROOT environment variable not set"
)
class TestPluginRegistry:
    """Tests for the lazy-loading plugin registry."""

    def test_list_plugins(self):
        """Test listing all available plugins without importing."""
        tm = TASKMANAGER()

        plugins = tm.list_plugins()

        assert len(plugins) > 100, "Should find many plugins"
        assert 'pointless' in plugins
        assert 'refmac' in plugins
        assert 'aimless' in plugins

    def test_get_metadata_without_import(self):
        """Test getting plugin metadata without importing the plugin."""
        tm = TASKMANAGER()

        meta = tm.get_plugin_metadata('pointless')

        assert meta is not None
        assert meta['TASKNAME'] == 'pointless'
        assert meta['TASKVERSION'] == 0.0
        assert 'TASKTITLE' in meta
        assert 'ERROR_CODES' in meta
        # Should have import info
        assert '_import_module' in meta
        assert '_import_class' in meta

    def test_get_metadata_nonexistent(self):
        """Test getting metadata for non-existent plugin."""
        tm = TASKMANAGER()

        meta = tm.get_plugin_metadata('nonexistent_plugin_xyz')

        assert meta is None

    def test_lazy_load_plugin(self):
        """Test lazy loading a plugin class."""
        tm = TASKMANAGER()

        # This should trigger lazy import
        PointlessClass = tm.get_plugin_class('pointless')

        assert PointlessClass is not None, "Should load pointless plugin"
        assert PointlessClass.__name__ == 'pointless'
        assert hasattr(PointlessClass, 'TASKNAME')
        assert PointlessClass.TASKNAME == 'pointless'
        assert PointlessClass.TASKVERSION == 0.0

    def test_lazy_load_caching(self):
        """Test that loaded plugins are cached."""
        tm = TASKMANAGER()

        # Load once
        PointlessClass1 = tm.get_plugin_class('pointless')

        # Load again
        PointlessClass2 = tm.get_plugin_class('pointless')

        # Should be the same object (cached)
        assert PointlessClass1 is PointlessClass2

    def test_load_multiple_plugins(self):
        """Test loading multiple different plugins."""
        tm = TASKMANAGER()

        # These plugins have minimal dependencies and should load
        test_plugins = ['pointless', 'unique', 'mtzheader']

        loaded_count = 0
        for plugin_name in test_plugins:
            plugin_class = tm.get_plugin_class(plugin_name)
            if plugin_class:
                loaded_count += 1
                assert plugin_class.TASKNAME == plugin_name

        # At least some should load successfully
        assert loaded_count > 0, "At least one plugin should load"

    def test_get_nonexistent_plugin(self):
        """Test trying to load a plugin that doesn't exist."""
        tm = TASKMANAGER()

        result = tm.get_plugin_class('nonexistent_plugin_xyz')

        assert result is None

    def test_metadata_has_error_codes(self):
        """Test that plugin metadata includes error codes."""
        tm = TASKMANAGER()

        meta = tm.get_plugin_metadata('pointless')

        assert 'ERROR_CODES' in meta
        error_codes = meta['ERROR_CODES']
        assert isinstance(error_codes, dict)
        assert len(error_codes) > 0

    def test_plugin_class_is_subclass_of_cpluginscript(self):
        """Test that loaded plugins are CPluginScript subclasses."""
        tm = TASKMANAGER()

        PointlessClass = tm.get_plugin_class('pointless')

        if PointlessClass:
            # Should have CPluginScript in its MRO
            class_names = [cls.__name__ for cls in PointlessClass.__mro__]
            assert any('PluginScript' in name for name in class_names)
