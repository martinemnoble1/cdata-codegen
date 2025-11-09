"""
Simple test to debug signal-driven pipeline execution.

This mimics aimless_pipe but with minimal complexity.
"""
from pathlib import Path
from .utils import i2run, demoData
import asyncio


def test_simple_signal_chain():
    """Test a simple two-step signal-driven pipeline."""

    # Use pointless (a simple, fast wrapper) twice in sequence
    args = ["test_pipeline_wrapper"]

    # Note: This will fail because test_pipeline_wrapper doesn't exist yet
    # But it will help us understand where the signal chain breaks

    # For now, let's just test pointless alone to see if it works
    mtz = demoData("gamma", "gamma_native.mtz")
    args = ["pointless", "--HKLIN", f"file={mtz}"]

    with i2run(args, project_name="test_signal_chain") as job:
        # Check that pointless completed
        assert (job / "HKLOUT.mtz").exists(), "Pointless did not create output file"
        print(f"✓ Pointless completed successfully")
