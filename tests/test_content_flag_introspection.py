"""
Tests for automatic content flag introspection in CDataFile descendants.

Tests the setContentFlag() method's ability to auto-detect contentFlag
values by inspecting MTZ file columns and matching against CONTENT_SIGNATURE_LIST.
"""

import pytest
from pathlib import Path

# Import the classes we're testing
from core.CCP4XtalData import CObsDataFile, CFreeRDataFile


class TestContentFlagIntrospection:
    """Test automatic content flag detection from MTZ files."""

    @staticmethod
    def get_content_flag_value(file_obj):
        """Helper to get contentFlag value (handles CData wrapper or plain int)."""
        if hasattr(file_obj.contentFlag, 'value'):
            return file_obj.contentFlag.value
        else:
            return file_obj.contentFlag

    @pytest.fixture
    def gamma_demo_data_dir(self):
        """Path to gamma demo data directory in CCP4i2."""
        return Path("/Users/nmemn/Developer/ccp4i2/demo_data/gamma")

    def test_obs_ipair_introspection(self, gamma_demo_data_dir):
        """Test CObsDataFile detects IPAIR content flag from merged_intensities_native.mtz."""
        # File has columns: Iplus, SIGIplus, Iminus, SIGIminus
        # Should match IPAIR signature (index 0 → contentFlag=1)

        mtz_file = gamma_demo_data_dir / "merged_intensities_native.mtz"
        assert mtz_file.exists(), f"Test file not found: {mtz_file}"

        # Create CObsDataFile with the file path
        obs_file = CObsDataFile(file_path=str(mtz_file))

        # Trigger introspection
        obs_file.setContentFlag()

        # Get contentFlag value
        flag_value = self.get_content_flag_value(obs_file)

        # Verify it detected IPAIR (contentFlag=1)
        assert flag_value == 1, \
            f"Expected IPAIR (1), got {flag_value}"

        # Verify it matches the constant
        assert flag_value == CObsDataFile.CONTENT_FLAG_IPAIR

    def test_freer_introspection(self, gamma_demo_data_dir):
        """Test CFreeRDataFile detects FREER content flag from freeR.mtz."""
        # File has column: FREER
        # Should match FREER signature (index 0 → contentFlag=1)

        mtz_file = gamma_demo_data_dir / "freeR.mtz"
        assert mtz_file.exists(), f"Test file not found: {mtz_file}"

        # Create CFreeRDataFile with the file path
        freer_file = CFreeRDataFile(file_path=str(mtz_file))

        # Trigger introspection
        freer_file.setContentFlag()

        # Get contentFlag value
        flag_value = self.get_content_flag_value(freer_file)

        # Verify it detected FREER (contentFlag=1)
        assert flag_value == 1, \
            f"Expected FREER (1), got {flag_value}"

        # Verify it matches the constant
        assert flag_value == CFreeRDataFile.CONTENT_FLAG_FREER

    def test_explicit_content_flag_setting(self, gamma_demo_data_dir):
        """Test explicit content flag setting still works."""
        mtz_file = gamma_demo_data_dir / "merged_intensities_native.mtz"
        obs_file = CObsDataFile(file_path=str(mtz_file))

        # Explicitly set to FMEAN (contentFlag=4)
        obs_file.setContentFlag(4)

        # Get contentFlag value
        flag_value = self.get_content_flag_value(obs_file)

        # Should be 4, not auto-detected 1
        assert flag_value == 4
        assert flag_value == CObsDataFile.CONTENT_FLAG_FMEAN

    def test_introspection_nonexistent_file(self):
        """Test introspection gracefully handles non-existent files."""
        obs_file = CObsDataFile(file_path="/nonexistent/file.mtz")

        # Should not raise exception
        obs_file.setContentFlag()

        # contentFlag should be None or unset
        # (behavior depends on whether attribute was initialized)
        if hasattr(obs_file, 'contentFlag') and obs_file.contentFlag is not None:
            # If it exists, check it's not explicitly set
            assert not obs_file.isSet('contentFlag'), \
                "contentFlag should not be set for non-existent file"

    def test_introspection_no_match(self, gamma_demo_data_dir):
        """Test introspection when file columns don't match any signature."""
        # Use a file that's not likely to match any specific signature
        # (This is a bit tricky - freeR actually has a match, but we can
        # test this properly once we have more conversion methods)

        # For now, just verify the method doesn't crash
        mtz_file = gamma_demo_data_dir / "freeR.mtz"
        obs_file = CObsDataFile(file_path=str(mtz_file))  # Wrong class for this file

        # Should not raise exception
        obs_file.setContentFlag()

        # contentFlag might be None or might have detected something
        # The important thing is it didn't crash

    def test_content_annotation_matches_flag(self, gamma_demo_data_dir):
        """Test that detected contentFlag corresponds to correct annotation."""
        mtz_file = gamma_demo_data_dir / "merged_intensities_native.mtz"
        obs_file = CObsDataFile(file_path=str(mtz_file))

        # Trigger introspection
        obs_file.setContentFlag()

        # Get the annotation for the detected flag
        flag_value = self.get_content_flag_value(obs_file)
        annotation = CObsDataFile.CONTENT_ANNOTATION[flag_value - 1]

        # IPAIR should have annotation "Anomalous Is"
        assert annotation == "Anomalous Is", \
            f"Expected 'Anomalous Is', got '{annotation}'"

    def test_signature_list_exists(self):
        """Verify that test classes have CONTENT_SIGNATURE_LIST."""
        assert hasattr(CObsDataFile, 'CONTENT_SIGNATURE_LIST')
        assert hasattr(CFreeRDataFile, 'CONTENT_SIGNATURE_LIST')

        # CObsDataFile should have 4 signatures (IPAIR, FPAIR, IMEAN, FMEAN)
        assert len(CObsDataFile.CONTENT_SIGNATURE_LIST) == 4

        # CFreeRDataFile should have 1 signature (FREER)
        assert len(CFreeRDataFile.CONTENT_SIGNATURE_LIST) == 1

    def test_ipair_signature_content(self):
        """Verify IPAIR signature matches expected columns."""
        ipair_signature = CObsDataFile.CONTENT_SIGNATURE_LIST[0]
        expected_columns = ['Iplus', 'SIGIplus', 'Iminus', 'SIGIminus']

        assert ipair_signature == expected_columns, \
            f"IPAIR signature mismatch: {ipair_signature} != {expected_columns}"

    def test_freer_signature_content(self):
        """Verify FREER signature matches expected columns."""
        freer_signature = CFreeRDataFile.CONTENT_SIGNATURE_LIST[0]
        expected_columns = ['FREER']

        assert freer_signature == expected_columns, \
            f"FREER signature mismatch: {freer_signature} != {expected_columns}"


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
