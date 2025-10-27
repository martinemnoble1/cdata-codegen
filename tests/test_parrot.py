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
def test_parrot():
    task = TASKMANAGER().get_plugin_class("parrot")()
    task.container.inputData.XYZIN = os.path.join(os.environ["CCP4I2_ROOT"], "demo_data", "gamma", "merged_intensities_native.mtz")
    assert task.container.inputData.XYZIN.__str__().endswith("merged_intensities_native.mtz")
    task.container.inputData.ABCD = os.path.join(os.environ["CCP4I2_ROOT"], "demo_data", "gamma", "initial_phases.mtz")
    assert task.container.inputData.ABCD.__str__().endswith("initial_phases.mtz")
    task.container.inputData.ASUIN = os.path.join(os.environ["CCP4I2_ROOT"], "demo_data", "gamma", "gamma.asu.xml")
    assert task.container.inputData.ASUIN.__str__().endswith("gamma.asu.xml")
