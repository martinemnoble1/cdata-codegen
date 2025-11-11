#!/usr/bin/env python3
"""
Test container serialization with file attributes to debug input_params.xml issue.

This test mimics the modelASUCheck workflow:
1. Create a container with file parameters (like XYZIN, ASUIN)
2. Set file paths via string assignment
3. Serialize to XML
4. Check that files appear in serialized output
"""

import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET

from core.CCP4Container import CContainer
from core.CCP4File import CDataFile


def test_container_with_file_attributes():
    """Test that file attributes serialize correctly when assigned via string paths."""

    # Create a test container structure like task.container.inputData
    container = CContainer(name="container")
    input_data = CContainer(name="inputData")
    container.inputData = input_data

    # Create file attributes (like XYZIN, ASUIN)
    xyzin = CDataFile(name="XYZIN")
    asuin = CDataFile(name="ASUIN")

    input_data.XYZIN = xyzin
    input_data.ASUIN = asuin

    print(f"[DEBUG] Created container structure")
    print(f"[DEBUG]   container.inputData = {container.inputData}")
    print(f"[DEBUG]   container.inputData.XYZIN = {container.inputData.XYZIN}")
    print(f"[DEBUG]   container.inputData.ASUIN = {container.inputData.ASUIN}")

    # Set file paths via string assignment (simulating i2run command parsing)
    with tempfile.NamedTemporaryFile(suffix=".cif", delete=False) as f:
        cif_path = f.name
    with tempfile.NamedTemporaryFile(suffix=".xml", delete=False) as f:
        asu_path = f.name

    print(f"\n[DEBUG] Assigning file paths:")
    print(f"[DEBUG]   XYZIN = {cif_path}")
    print(f"[DEBUG]   ASUIN = {asu_path}")

    # This is how i2run sets file paths
    container.inputData.XYZIN = cif_path
    container.inputData.ASUIN = asu_path

    print(f"\n[DEBUG] After assignment:")
    print(f"[DEBUG]   XYZIN.baseName.value = {container.inputData.XYZIN.baseName.value}")
    print(f"[DEBUG]   ASUIN.baseName.value = {container.inputData.ASUIN.baseName.value}")

    # Check isSet() status
    print(f"\n[DEBUG] Checking isSet() status:")
    print(f"[DEBUG]   container.isSet('inputData') = {container.isSet('inputData')}")
    print(f"[DEBUG]   container.inputData.isSet('XYZIN') = {container.inputData.isSet('XYZIN')}")
    print(f"[DEBUG]   container.inputData.isSet('ASUIN') = {container.inputData.isSet('ASUIN')}")

    # Check value states
    print(f"\n[DEBUG] Checking _value_states:")
    if hasattr(container, '_value_states'):
        print(f"[DEBUG]   container._value_states = {container._value_states}")
    if hasattr(container.inputData, '_value_states'):
        print(f"[DEBUG]   container.inputData._value_states = {container.inputData._value_states}")

    # Serialize with excludeUnset=False (should include files)
    print(f"\n[DEBUG] Serializing with excludeUnset=False...")
    body_etree = container.getEtree(excludeUnset=False)

    # Pretty print the XML
    xml_string = ET.tostring(body_etree, encoding='unicode')
    print(f"\n[DEBUG] Serialized XML:\n{xml_string}")

    # Parse and check structure
    assert body_etree.tag == "container"

    # Find inputData
    input_data_elem = body_etree.find("inputData")
    assert input_data_elem is not None, "inputData element not found in XML"

    # Find XYZIN
    xyzin_elem = input_data_elem.find("XYZIN")
    assert xyzin_elem is not None, "XYZIN element not found in XML - isSet() may be broken"

    # Find baseName
    basename_elem = xyzin_elem.find("baseName")
    assert basename_elem is not None, "baseName element not found in XYZIN"
    assert basename_elem.text == cif_path, f"Expected baseName={cif_path}, got {basename_elem.text}"

    # Find ASUIN
    asuin_elem = input_data_elem.find("ASUIN")
    assert asuin_elem is not None, "ASUIN element not found in XML - isSet() may be broken"

    print(f"\n✅ Test passed! Files are correctly serialized.")

    # Cleanup
    Path(cif_path).unlink(missing_ok=True)
    Path(asu_path).unlink(missing_ok=True)


def test_container_with_excludeUnset_true():
    """Test that files are excluded when excludeUnset=True and not explicitly set."""

    container = CContainer(name="container")
    input_data = CContainer(name="inputData")
    container.inputData = input_data

    # Create file but DON'T set its path
    xyzin = CDataFile(name="XYZIN")
    input_data.XYZIN = xyzin

    print(f"\n[DEBUG] Container with unset file:")
    print(f"[DEBUG]   XYZIN.baseName.value = '{xyzin.baseName.value}'")
    print(f"[DEBUG]   XYZIN.isSet() = {xyzin.isSet()}")
    print(f"[DEBUG]   container.inputData.isSet('XYZIN') = {container.inputData.isSet('XYZIN')}")

    # Serialize with excludeUnset=True (should NOT include XYZIN or inputData)
    body_etree = container.getEtree(excludeUnset=True)
    xml_string = ET.tostring(body_etree, encoding='unicode')
    print(f"\n[DEBUG] Serialized XML with excludeUnset=True:\n{xml_string}")

    # The entire container should be empty because inputData has no set children
    assert body_etree.tag == "container"
    assert len(list(body_etree)) == 0, "Container should be empty when all children are unset"

    print(f"\n✅ Test passed! Unset files are correctly excluded.")


if __name__ == "__main__":
    print("=" * 80)
    print("TEST 1: Container with file attributes (excludeUnset=False)")
    print("=" * 80)
    test_container_with_file_attributes()

    print("\n" + "=" * 80)
    print("TEST 2: Container with unset file (excludeUnset=True)")
    print("=" * 80)
    test_container_with_excludeUnset_true()

    print("\n" + "=" * 80)
    print("ALL TESTS PASSED")
    print("=" * 80)
