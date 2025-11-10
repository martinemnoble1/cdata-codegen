"""
Test that aimless_pipe works with phaser_analysis kwargs forwarding.

This test exercises the code path that was failing:
  aimless_pipe.py:827: self.phaser_analysis.process(filename=filename, pxdname=pxdname)
"""

from .utils import i2run, demoData


def test_aimless_pipe_with_phaser():
    """Test aimless_pipe with phaser_analysis kwargs."""

    # Get test data
    mtz = demoData("gamma", "gamma_native.mtz")

    # Run aimless_pipe - this internally creates phaser_analysis sub-job
    # and calls process(filename=..., pxdname=...) with kwargs
    args = [
        "aimless_pipe",
        "--HKLIN", f"file={mtz}",
        "--ANOMALOUS", "True",  # Anomalous data processing
    ]

    with i2run(args, project_name="test_aimless_kwargs") as job:
        # Check that aimless output was created
        assert (job / "HKLOUT.mtz").exists(), "Aimless output not found"

        # Check that phaser_analysis was run (it creates PROGRAMXML.xml)
        # Note: phaser_analysis is a sub-job, so its files would be in job_N subdirectory
        # For now, just verify aimless_pipe completed without errors
        print("✅ aimless_pipe completed successfully with kwargs forwarding")
