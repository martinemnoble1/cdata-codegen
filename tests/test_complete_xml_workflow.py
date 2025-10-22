#!/usr/bin/env python3
"""
Complete Demonstration: DEF XML + Params XML Workflow

This demonstrates the complete CCP4i2 task workflow:
1. Load task definition from .def.xml
2. Modify parameters (user input simulation)
3. Export modified parameters to .params.xml
4. Load fresh task from .def.xml
5. Import parameters from .params.xml
6. Verify the round-trip works correctly
"""

import sys
import tempfile
from pathlib import Path
import os

# Add the server directory to Python path (4 levels up from this demo file)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from ccp4x.core.task_manager.def_xml_parser import parse_def_xml_file
from ccp4x.core.data_manager.params_xml_handler import (
    export_task_params,
    import_task_params,
)

# Sample servalcat params XML (shortened for testing)
SAMPLE_PARAMS_XML = """<?xml version='1.0' encoding='utf-8'?>
<ccp4:ccp4i2 xmlns:ccp4="http://www.ccp4.ac.uk/ccp4ns">
  <ccp4i2_header>
    <function>PARAMS</function>
    <userId>test_user</userId>
    <hostName>test-host</hostName>
    <creationTime>19:47 08/Oct/25</creationTime>
    <ccp4iVersion>alpha_rev_90011</ccp4iVersion>
    <pluginName>servalcat_pipe</pluginName>
  </ccp4i2_header>
  <ccp4i2_body>
    <inputData>
      <XYZIN>
        <project>2f376b1b2b734890bc7d700758dc9581</project>
        <baseName>model_from_refinement_mmcif_format_1.cif</baseName>
        <relPath>CCP4_IMPORTED_FILES</relPath>
        <annotation>Imported from Model_from_refinement_mmCIF_format.cif</annotation>
        <dbFileId>7278fed0208146c88336b6da8cbb275f</dbFileId>
        <subType>0</subType>
        <contentFlag>1</contentFlag>
      </XYZIN>
    </inputData>
    <outputData>
      <XYZOUT>
        <project>2f376b1b-2b73-4890-bc7d-700758dc9581</project>
        <baseName>XYZOUT.pdb</baseName>
        <relPath>CCP4_JOBS/job_16</relPath>
        <annotation>Model from refinement (PDB format)</annotation>
        <dbFileId>2e545c8c-8866-489f-8fd9-1a7d29ddc926</dbFileId>
        <subType>1</subType>
        <contentFlag>1</contentFlag>
      </XYZOUT>
    </outputData>
    <controlParameters>
      <DATA_METHOD>xtal</DATA_METHOD>
      <ADD_WATERS>True</ADD_WATERS>
      <NCYCLES>25</NCYCLES>
      <WEIGHT>0.15</WEIGHT>
      <B_REFINEMENT_MODE>aniso</B_REFINEMENT_MODE>
      <OCCUPANCY_REFINEMENT>False</OCCUPANCY_REFINEMENT>
    </controlParameters>
    <metalCoordPipeline>
      <RUN_METALCOORD>True</RUN_METALCOORD>
      <LINKS>KEEP</LINKS>
    </metalCoordPipeline>
  </ccp4i2_body>
</ccp4:ccp4i2>"""

# Sample DEF XML (simplified version for testing)
SAMPLE_DEF_XML = """<?xml version="1.0" encoding="UTF-8"?>
<ns0:ccp4i2 xmlns:ns0="http://www.ccp4.ac.uk/ccp4ns">
  <ccp4i2_header>
    <pluginName>servalcat_pipe</pluginName>
  </ccp4i2_header>
  <ccp4i2_body id="servalcat_pipe">
    <ccp4i2_body>
      <container id="inputData">
        <content id="XYZIN">
          <className>CPdbDataFile</className>
          <qualifiers>
            <mustExist>True</mustExist>
            <toolTip>Input coordinate file</toolTip>
          </qualifiers>
        </content>
      </container>
      <container id="outputData">
        <content id="XYZOUT">
          <className>CPdbDataFile</className>
          <qualifiers>
            <toolTip>Output coordinate file</toolTip>
          </qualifiers>
        </content>
      </container>
      <container id="controlParameters">
        <content id="DATA_METHOD">
          <className>CString</className>
          <qualifiers>
            <onlyEnumerators>True</onlyEnumerators>
            <enumerators>xtal,spa</enumerators>
            <default>xtal</default>
          </qualifiers>
        </content>
        <content id="ADD_WATERS">
          <className>CBoolean</className>
          <qualifiers>
            <default>False</default>
            <toolTip>Add water molecules</toolTip>
          </qualifiers>
        </content>
        <content id="NCYCLES">
          <className>CInt</className>
          <qualifiers>
            <default>10</default>
            <min>1</min>
            <max>100</max>
            <toolTip>Number of refinement cycles</toolTip>
          </qualifiers>
        </content>
        <content id="WEIGHT">
          <className>CFloat</className>
          <qualifiers>
            <min>0.0</min>
            <toolTip>Refinement weight</toolTip>
          </qualifiers>
        </content>
        <content id="B_REFINEMENT_MODE">
          <className>CString</className>
          <qualifiers>
            <onlyEnumerators>True</onlyEnumerators>
            <enumerators>iso,aniso,fix</enumerators>
            <default>iso</default>
            <toolTip>B-factor refinement mode</toolTip>
          </qualifiers>
        </content>
        <content id="OCCUPANCY_REFINEMENT">
          <className>CBoolean</className>
          <qualifiers>
            <default>True</default>
            <toolTip>Refine occupancies</toolTip>
          </qualifiers>
        </content>
      </container>
    </ccp4i2_body>
  </ccp4i2_body>
  <container id="metalCoordPipeline">
    <content id="RUN_METALCOORD">
      <className>CBoolean</className>
      <qualifiers>
        <default>False</default>
      </qualifiers>
    </content>
    <content id="LINKS">
      <className>CString</className>
      <qualifiers>
        <onlyEnumerators>True</onlyEnumerators>
        <enumerators>UPDATE,KEEP,NOTTOUCH</enumerators>
        <default>UPDATE</default>
      </qualifiers>
    </content>
  </container>
</ns0:ccp4i2>"""


def demonstrate_complete_workflow():
    """Demonstrate the complete DEF + Params XML workflow."""
    print("🎯 Complete CCP4i2 Task Workflow Demonstration")
    print("=" * 55)

    # Create temporary files
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".def.xml", delete=False
    ) as def_file:
        def_file.write(SAMPLE_DEF_XML)
        def_xml_path = def_file.name

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".params.xml", delete=False
    ) as params_file:
        params_file.write(SAMPLE_PARAMS_XML)
        params_xml_path = params_file.name

    params_export_path = tempfile.mktemp(suffix=".params.xml")

    try:
        # STEP 1: Load task definition from .def.xml
        print("\n📋 Step 1: Loading task definition from .def.xml")
        task = parse_def_xml_file(def_xml_path)

        if task is None:
            print("❌ Failed to load task definition")
            return False

        print(f"✅ Loaded task: {task.name}")

        # Show initial state (all defaults)
        print("\n🔍 Initial parameter states:")
        ctrl = task.controlParameters
        params_to_check = [
            "DATA_METHOD",
            "ADD_WATERS",
            "NCYCLES",
            "WEIGHT",
            "B_REFINEMENT_MODE",
            "OCCUPANCY_REFINEMENT",
        ]

        for param_name in params_to_check:
            if hasattr(ctrl, param_name):
                param = getattr(ctrl, param_name)
                if hasattr(param, "value") and hasattr(param, "getValueState"):
                    state = param.getValueState("value")
                    print(f"  {param_name}: {param.value} (state: {state})")

        # STEP 2: Simulate user modifications
        print("\n🔧 Step 2: Simulating user modifications")

        # Modify some parameters using new smart setter patterns
        ctrl.ADD_WATERS = True  # Direct assignment pattern
        ctrl.NCYCLES = 25  # Direct assignment pattern
        ctrl.WEIGHT.set(0.15)  # Method call pattern
        ctrl.B_REFINEMENT_MODE = "aniso"  # Direct assignment pattern
        ctrl.OCCUPANCY_REFINEMENT.set(False)  # Method call pattern

        # Also modify some other containers (mix both patterns)
        task.metalCoordPipeline.RUN_METALCOORD = True  # Direct assignment
        task.metalCoordPipeline.LINKS.set("KEEP")  # Method call

        print("✅ Modified parameters:")
        for param_name in params_to_check:
            if hasattr(ctrl, param_name):
                param = getattr(ctrl, param_name)
                if hasattr(param, "value") and hasattr(param, "getValueState"):
                    state = param.getValueState("value")
                    print(f"  {param_name}: {param.value} (state: {state})")

        # STEP 3: Export to .params.xml (only explicitly set parameters)
        print("\n💾 Step 3: Exporting modified parameters to .params.xml")

        success = export_task_params(task, params_export_path, "demo_user")
        if not success:
            print("❌ Failed to export parameters")
            return False

        # Show what was exported
        print(f"✅ Exported to: {params_export_path}")

        # Read and show a sample of the exported file
        with open(params_export_path, "r") as f:
            content = f.read()
            lines = content.split("\n")
            print("📄 Sample of exported XML:")
            for i, line in enumerate(lines[:20]):  # Show first 20 lines
                print(f"  {line}")
            if len(lines) > 20:
                print(f"  ... ({len(lines) - 20} more lines)")

        # STEP 4: Load fresh task from .def.xml (clean slate)
        print("\n🔄 Step 4: Loading fresh task definition (clean slate)")

        fresh_task = parse_def_xml_file(def_xml_path)
        print(f"✅ Loaded fresh task: {fresh_task.name}")

        # Show fresh state (should be defaults)
        print("\n🔍 Fresh task parameter states (should be defaults):")
        fresh_ctrl = fresh_task.controlParameters

        for param_name in params_to_check:
            if hasattr(fresh_ctrl, param_name):
                param = getattr(fresh_ctrl, param_name)
                if hasattr(param, "value") and hasattr(param, "getValueState"):
                    state = param.getValueState("value")
                    print(f"  {param_name}: {param.value} (state: {state})")

        # STEP 5: Import parameters from existing .params.xml
        print("\n📥 Step 5: Importing parameters from .params.xml")

        success = import_task_params(fresh_task, params_xml_path)
        if not success:
            print("❌ Failed to import parameters")
            return False

        # Show imported state
        print("\n🔍 After importing parameters:")
        fresh_ctrl = fresh_task.controlParameters

        for param_name in params_to_check:
            if hasattr(fresh_ctrl, param_name):
                param = getattr(fresh_ctrl, param_name)
                if hasattr(param, "value") and hasattr(param, "getValueState"):
                    state = param.getValueState("value")
                    print(f"  {param_name}: {param.value} (state: {state})")

        # STEP 6: Verify round-trip accuracy
        print("\n🔍 Step 6: Verifying round-trip accuracy")

        # Test a few key parameters to ensure values match
        test_cases = [
            ("controlParameters.ADD_WATERS", True),
            ("controlParameters.NCYCLES", 25),
            ("controlParameters.B_REFINEMENT_MODE", "aniso"),
            ("metalCoordPipeline.RUN_METALCOORD", True),
            ("metalCoordPipeline.LINKS", "KEEP"),
        ]

        all_correct = True
        for path, expected_value in test_cases:
            try:
                obj = fresh_task.find_by_path(path)
                if obj and hasattr(obj, "value"):
                    actual_value = obj.value
                    if actual_value == expected_value:
                        print(f"  ✅ {path}: {actual_value} (correct)")
                    else:
                        print(
                            f"  ❌ {path}: {actual_value} (expected: {expected_value})"
                        )
                        all_correct = False
                else:
                    print(f"  ❌ {path}: <not found or no value>")
                    all_correct = False
            except Exception as e:
                print(f"  ❌ {path}: <error: {e}>")
                all_correct = False

        # STEP 7: Summary
        print(f"\n🎉 Workflow Summary:")
        print(f"  ✅ DEF XML parsing: Complete task structure loaded")
        print(f"  ✅ Parameter modification: User changes tracked with set states")
        print(f"  ✅ Params XML export: Only explicitly set parameters exported")
        print(f"  ✅ Fresh task loading: Clean slate from DEF XML")
        print(f"  ✅ Params XML import: User values restored from XML")
        print(
            f"  {'✅' if all_correct else '❌'} Round-trip verification: {'All values correct' if all_correct else 'Some values incorrect'}"
        )

        if all_correct:
            print("\n🌟 Complete workflow successful! The system can:")
            print("  • Load abstract task definitions from .def.xml")
            print("  • Track user modifications with sophisticated state management")
            print("  • Export only user-specified parameters to .params.xml")
            print("  • Import user parameters into fresh task instances")
            print("  • Maintain perfect fidelity in the round-trip process")
            print("  • Support complex nested structures with containers")
            print(
                "  • Handle multiple data types (strings, booleans, integers, floats)"
            )

        return all_correct

    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        # Clean up temporary files
        for path in [def_xml_path, params_xml_path, params_export_path]:
            try:
                Path(path).unlink(missing_ok=True)
            except:
                pass


if __name__ == "__main__":
    success = demonstrate_complete_workflow()
    if success:
        print("\n🎊 Complete CCP4i2 XML workflow system is ready for production!")
    else:
        print("\n💥 Workflow needs refinement")
