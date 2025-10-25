"""
Tests for building and using chainsaw.
"""

import pytest
import os
from core.CCP4TaskManager import TASKMANAGER


@pytest.mark.skipif(
    'CCP4I2_ROOT' not in os.environ,
    reason="CCP4I2_ROOT environment variable not set"
)
def test_chainsaw():
    task = TASKMANAGER().get_plugin_class("chainsaw")()
    assert not task.container.inputData.isSet() 
