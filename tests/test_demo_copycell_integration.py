"""
Integration test for demo_copycell pattern with AsyncProcessManager.

This test demonstrates the exact pattern from demo_copycell but using
simple shell commands instead of real crystallography programs.

The pattern:
1. Run first subprocess (mtzdump) to extract cell parameters
2. On completion, run second subprocess (pdbset) to apply them
3. Report final status

This validates that the async signal chain works correctly.
"""

import pytest
import time
import tempfile
from pathlib import Path
from core.base_object.signal_system import Signal, Slot
from core.async_process_manager import AsyncProcessManager


class SimpleMockPlugin:
    """
    Simplified mock plugin that mimics CPluginScript behavior.

    This represents plugins like 'mtzdump' or 'pdbset' but uses
    simple shell commands for testing.
    """

    SUCCEEDED = 0
    FAILED = 1

    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.finished = Signal[dict](name=f'{name}_finished')
        self._process_manager = AsyncProcessManager()
        self._pid = None

        # Mock container with input/output data
        self.container = type('Container', (), {
            'inputData': type('InputData', (), {})(),
            'outputData': type('OutputData', (), {})(),
        })()

    def process(self):
        """Start the plugin's subprocess."""
        # Simulate command execution
        # In real plugin this would be mtzdump, pdbset, etc.
        if self.name == 'mock_mtzdump':
            command = 'echo'
            args = ['CELL: 78.0 78.0 38.0 90.0 90.0 90.0']
        elif self.name == 'mock_pdbset':
            command = 'echo'
            args = ['PDB file updated with cell']
        else:
            command = 'echo'
            args = [f'{self.name} output']

        # Create handler
        handler = [self._on_finished, {}]

        # Start process
        self._pid = self._process_manager.startProcess(
            command=command,
            args=args,
            handler=handler,
            ifAsync=True
        )

        return SimpleMockPlugin.SUCCEEDED

    def _on_finished(self, pid):
        """Called when subprocess completes."""
        exit_code = self._process_manager.getJobData(pid, 'exitCode')

        # Simulate reading output (in real plugin would parse log file)
        if self.name == 'mock_mtzdump':
            # Simulate extracting cell parameters
            self.container.outputData.CELL = "78.0 78.0 38.0 90.0 90.0 90.0"

        # Emit finished signal
        finish_status = SimpleMockPlugin.SUCCEEDED if exit_code == 0 else SimpleMockPlugin.FAILED
        status_dict = {
            'pid': pid,
            'finishStatus': finish_status
        }

        self.finished.emit(status_dict)


class MockDemoCopycell:
    """
    Mock version of demo_copycell pipeline.

    This exactly mimics the demo_copycell pattern:
    1. Run mtzdump to get cell parameters
    2. When it finishes, run pdbset to apply them to PDB
    3. Report final status
    """

    SUCCEEDED = 0
    FAILED = 1

    def __init__(self, name: str = 'demo_copycell'):
        self.name = name
        self.finished = Signal[dict](name=f'{name}_finished')
        self.mtzdump = None
        self.pdbset = None
        self.final_status = None

        # Mock container
        self.container = type('Container', (), {
            'inputData': type('InputData', (), {
                'HKLIN': 'input.mtz',
                'XYZIN': 'input.pdb'
            })(),
            'outputData': type('OutputData', (), {
                'XYZOUT': 'output.pdb'
            })(),
        })()

    def connectSignal(self, origin, signal_name: str, handler):
        """Connect signal to handler (mimics CPluginScript.connectSignal)."""
        if signal_name == 'finished' and hasattr(origin, 'finished'):
            origin.finished.connect(handler, weak=False)
        else:
            raise ValueError(f"Unknown signal '{signal_name}'")

    def makePluginObject(self, plugin_name: str):
        """Create a plugin instance (mimics CPluginScript.makePluginObject)."""
        if plugin_name == 'mtzdump':
            return SimpleMockPlugin(name='mock_mtzdump', parent=self)
        elif plugin_name == 'pdbset':
            return SimpleMockPlugin(name='mock_pdbset', parent=self)
        else:
            raise ValueError(f"Unknown plugin: {plugin_name}")

    def process(self):
        """
        Main entry point - mimics demo_copycell.process().

        Step 1: Run mtzdump to get cell parameters from MTZ file.
        """
        # Create mtzdump instance
        self.mtzdump = self.makePluginObject('mtzdump')

        # Set input file (in real code: self.mtzdump.container.inputData.HKLIN.set(...))
        self.mtzdump.container.inputData.HKLIN = self.container.inputData.HKLIN

        # Connect finished signal to handler
        self.connectSignal(self.mtzdump, 'finished', self.process_1)

        # Start mtzdump (async)
        self.mtzdump.process()

        return MockDemoCopycell.SUCCEEDED

    @Slot(dict)
    def process_1(self, status_dict):
        """
        Called when mtzdump finishes - mimics demo_copycell.process_1().

        Step 2: Run pdbset to copy cell parameters to PDB file.
        """
        status = status_dict['finishStatus']

        if status == SimpleMockPlugin.FAILED:
            self.final_status = MockDemoCopycell.FAILED
            self.finished.emit({'finishStatus': self.final_status})
            return

        # Create pdbset instance
        self.pdbset = self.makePluginObject('pdbset')

        # Set input file
        self.pdbset.container.inputData.XYZIN = self.container.inputData.XYZIN

        # Copy cell from mtzdump output
        self.pdbset.container.inputData.CELL = self.mtzdump.container.outputData.CELL

        # Set output file
        self.pdbset.container.outputData.XYZOUT = self.container.outputData.XYZOUT

        # Connect to final handler
        self.connectSignal(self.pdbset, 'finished', self.postProcessWrapper)

        # Start pdbset (async)
        self.pdbset.process()

    @Slot(dict)
    def postProcessWrapper(self, status_dict):
        """
        Called when pdbset finishes - final handler.

        This would normally do post-processing, here just records status.
        """
        status = status_dict['finishStatus']
        self.final_status = status
        self.finished.emit({'finishStatus': self.final_status})


class TestDemoCopycellIntegration:
    """Test the demo_copycell async pattern."""

    def test_demo_copycell_two_step_pipeline(self):
        """
        Test complete demo_copycell pipeline with two async steps.

        This validates:
        1. First plugin (mtzdump) runs and finishes
        2. Handler creates and starts second plugin (pdbset)
        3. Second plugin finishes
        4. Final status is reported
        """
        result = {'status': None, 'completed': False}

        @Slot(dict)
        def on_pipeline_finished(status_dict):
            result['status'] = status_dict['finishStatus']
            result['completed'] = True

        # Create and run pipeline
        pipeline = MockDemoCopycell(name='test_demo_copycell')
        pipeline.finished.connect(on_pipeline_finished, weak=False)

        # Start pipeline
        status = pipeline.process()
        assert status == MockDemoCopycell.SUCCEEDED, "Pipeline failed to start"

        # Wait for completion (both plugins need to finish)
        for _ in range(100):  # Max 10 seconds
            if result['completed']:
                break
            time.sleep(0.1)

        # Verify pipeline completed
        assert result['completed'], "Pipeline did not complete"
        assert result['status'] == MockDemoCopycell.SUCCEEDED, "Pipeline failed"

        # Verify both plugins ran
        assert pipeline.mtzdump is not None, "mtzdump was not created"
        assert pipeline.pdbset is not None, "pdbset was not created"

        # Verify data flow
        assert hasattr(pipeline.mtzdump.container.outputData, 'CELL'), \
            "mtzdump did not produce CELL output"
        assert pipeline.pdbset.container.inputData.CELL is not None, \
            "pdbset did not receive CELL input"

    def test_demo_copycell_mtzdump_failure(self):
        """Test that pipeline stops if mtzdump fails."""
        result = {'status': None, 'completed': False}

        @Slot(dict)
        def on_pipeline_finished(status_dict):
            result['status'] = status_dict['finishStatus']
            result['completed'] = True

        # Create pipeline with failing mtzdump
        class FailingDemoCopycell(MockDemoCopycell):
            def makePluginObject(self, plugin_name: str):
                if plugin_name == 'mtzdump':
                    # Create plugin that will fail
                    class FailingPlugin(SimpleMockPlugin):
                        def process(self):
                            handler = [self._on_finished, {}]
                            self._pid = self._process_manager.startProcess(
                                command='false',  # Always fails
                                handler=handler,
                                ifAsync=True
                            )
                            return SimpleMockPlugin.SUCCEEDED
                    return FailingPlugin(name='failing_mtzdump', parent=self)
                else:
                    return super().makePluginObject(plugin_name)

        pipeline = FailingDemoCopycell(name='failing_pipeline')
        pipeline.finished.connect(on_pipeline_finished, weak=False)
        pipeline.process()

        # Wait for completion
        for _ in range(100):
            if result['completed']:
                break
            time.sleep(0.1)

        # Verify
        assert result['completed'], "Pipeline did not complete"
        assert result['status'] == MockDemoCopycell.FAILED, "Pipeline should have failed"
        assert pipeline.mtzdump is not None, "mtzdump was created"
        assert pipeline.pdbset is None, "pdbset should not have been created"

    def test_demo_copycell_pdbset_failure(self):
        """Test that pipeline reports failure if pdbset fails."""
        result = {'status': None, 'completed': False}

        @Slot(dict)
        def on_pipeline_finished(status_dict):
            result['status'] = status_dict['finishStatus']
            result['completed'] = True

        # Create pipeline with failing pdbset
        class FailingPdbsetPipeline(MockDemoCopycell):
            def makePluginObject(self, plugin_name: str):
                if plugin_name == 'pdbset':
                    # Create plugin that will fail
                    class FailingPlugin(SimpleMockPlugin):
                        def process(self):
                            handler = [self._on_finished, {}]
                            self._pid = self._process_manager.startProcess(
                                command='false',  # Always fails
                                handler=handler,
                                ifAsync=True
                            )
                            return SimpleMockPlugin.SUCCEEDED
                    return FailingPlugin(name='failing_pdbset', parent=self)
                else:
                    return super().makePluginObject(plugin_name)

        pipeline = FailingPdbsetPipeline(name='pdbset_failing_pipeline')
        pipeline.finished.connect(on_pipeline_finished, weak=False)
        pipeline.process()

        # Wait for completion
        for _ in range(100):
            if result['completed']:
                break
            time.sleep(0.1)

        # Verify
        assert result['completed'], "Pipeline did not complete"
        assert result['status'] == MockDemoCopycell.FAILED, "Pipeline should have failed"
        assert pipeline.mtzdump is not None, "mtzdump was created"
        assert pipeline.pdbset is not None, "pdbset was created"

    def test_signal_chain_timing(self):
        """
        Test that signals fire in correct order.

        Verifies:
        1. mtzdump finishes before pdbset starts
        2. pdbset finishes before final handler
        3. All handlers execute in sequence
        """
        events = []

        class TimingPipeline(MockDemoCopycell):
            def process(self):
                events.append(('pipeline_start', time.time()))
                return super().process()

            @Slot(dict)
            def process_1(self, status_dict):
                events.append(('mtzdump_finished', time.time()))
                events.append(('pdbset_start', time.time()))
                super().process_1(status_dict)

            @Slot(dict)
            def postProcessWrapper(self, status_dict):
                events.append(('pdbset_finished', time.time()))
                super().postProcessWrapper(status_dict)

        result = {'completed': False}

        @Slot(dict)
        def on_finished(status_dict):
            events.append(('pipeline_finished', time.time()))
            result['completed'] = True

        pipeline = TimingPipeline(name='timing_test')
        pipeline.finished.connect(on_finished, weak=False)
        pipeline.process()

        # Wait for completion
        for _ in range(100):
            if result['completed']:
                break
            time.sleep(0.1)

        assert result['completed'], "Pipeline did not complete"

        # Verify event order
        event_names = [e[0] for e in events]
        assert event_names == [
            'pipeline_start',
            'mtzdump_finished',
            'pdbset_start',
            'pdbset_finished',
            'pipeline_finished'
        ], f"Events out of order: {event_names}"

        # Verify timing (each step happens after previous)
        times = [e[1] for e in events]
        for i in range(len(times) - 1):
            assert times[i] <= times[i + 1], \
                f"Event {i} happened after event {i+1}"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
