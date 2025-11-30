import React, {
  useCallback,
  useEffect,
  useMemo,
  useRef,
} from "react";
import { Paper } from "@mui/material";
import { CCP4i2TaskInterfaceProps } from "./task-container";
import { CCP4i2TaskElement } from "../task-elements/task-element";
import { CCP4i2Tab, CCP4i2Tabs } from "../task-elements/tabs";
import { CCP4i2ContainerElement } from "../task-elements/ccontainer";
import { useJob } from "../../../utils";
import { useRunCheck } from "../../../providers/run-check-provider";

/**
 * Task interface component for Phaser Experimental Phasing LLG (Log-Likelihood Gain) calculation.
 *
 * Provides functionality for:
 * - Calculating log-likelihood gains for experimental phasing solutions
 * - Partial model input as coordinates or map coefficients
 * - Scattering content specification for accurate phasing
 * - Basic crystallographic parameter control
 * - Automatic wavelength detection from reflection files
 */
const TaskInterface: React.FC<CCP4i2TaskInterfaceProps> = (props) => {
  const { job } = props;
  const { useTaskItem, useFileDigest, mutateContainer, validation } = useJob(
    job.id
  );

  // Get task items for file handling and parameter updates
  const { item: F_SIGFItem } = useTaskItem("F_SIGF");
  const { value: XYZIN_PARTIALValue } = useTaskItem("XYZIN_PARTIAL");
  const { update: updateWAVELENGTH } = useTaskItem("WAVELENGTH");

  // File digest for wavelength extraction
  const { data: F_SIGFDigest } = useFileDigest(F_SIGFItem?._objectPath);

  // Track last set wavelength to avoid re-setting the same value
  const lastSetWavelengthRef = useRef<number | null>(null);

  // Task values for visibility conditions (memoized to prevent re-creation)
  const taskValues = useMemo(
    () => ({
      partialModelOrMap: useTaskItem("PARTIALMODELORMAP").value,
      compBy: useTaskItem("COMP_BY").value,
    }),
    [useTaskItem]
  );

  const { processedErrors, setProcessedErrors } = useRunCheck();

  // Visibility conditions (stable references)
  const visibility = useMemo(
    () => ({
      isPartialModel: () => taskValues.partialModelOrMap === "MODEL",
      isPartialMap: () => taskValues.partialModelOrMap === "MAP",
      isAsuFile: () => taskValues.compBy === "ASU",
      isMolecularWeight: () => taskValues.compBy === "MW",
    }),
    [taskValues]
  );

  // Effect for error processing when XYZIN_PARTIAL changes
  useEffect(() => {
    if (!setProcessedErrors) return;

    const errorKey = "phaser_EP_LLG.inputData.XYZIN_PARTIAL";
    const hasError =
      processedErrors && Object.keys(processedErrors).includes(errorKey);

    if (XYZIN_PARTIALValue?.contentFlag === 2) {
      // Add error if not already present
      if (!hasError) {
        setProcessedErrors({
          ...validation,
          [errorKey]: {
            messages: ["Phaser apps can only work with PDB format"],
            maxSeverity: 2,
          },
        });
      }
    } else if (hasError) {
      // Remove error if it exists but shouldn't
      const newErrors = { ...processedErrors };
      delete newErrors[errorKey];
      setProcessedErrors(newErrors);
    }
  }, [XYZIN_PARTIALValue?.contentFlag, validation, setProcessedErrors]);

  // Extract wavelength from F_SIGF digest when it changes
  useEffect(() => {
    // API returns {success: true, data: {...}} - extract the data
    const digestData = F_SIGFDigest?.data;
    if (!digestData || !updateWAVELENGTH || job?.status !== 1) return;

    // Extract wavelength from the last dataset
    const wavelengths = digestData.wavelengths;
    if (!wavelengths || wavelengths.length === 0) return;

    const wavelength = wavelengths[wavelengths.length - 1];

    // Sanity check: wavelength should be positive and reasonable (< 9 Angstrom)
    if (!wavelength || wavelength <= 0 || wavelength >= 9) return;

    // Don't re-set if we already set this value
    if (lastSetWavelengthRef.current === wavelength) return;

    console.log("Updating wavelength from F_SIGF digest:", wavelength);
    lastSetWavelengthRef.current = wavelength;
    updateWAVELENGTH(wavelength);
  }, [F_SIGFDigest, updateWAVELENGTH, job?.status]);

  // Element configurations (stable reference)
  const elementConfigs = useMemo(
    () => ({
      inputData: [
        { key: "F_SIGF", label: "Reflections" },
        {
          key: "PARTIALMODELORMAP",
          label: "Partial model as",
          toolTip:
            "Partial model can be provided as coordinates or a set of map coefficients",
        },
        {
          key: "XYZIN_PARTIAL",
          label: "Partial model coordinates",
          visible: visibility.isPartialModel,
        },
        {
          key: "MAPCOEFF_PARTIAL",
          label: "Partial model map coefficients",
          visible: visibility.isPartialMap,
        },
      ],
      scatteringContent: [
        { key: "COMP_BY", label: "How to specify scattering content" },
        {
          key: "ASUFILE",
          label: "CCP4i2 ASU file",
          visible: visibility.isAsuFile,
        },
        {
          key: "ASU_NUCLEICACID_MW",
          label: "Nucleic acid (Da)",
          visible: visibility.isMolecularWeight,
        },
        {
          key: "ASU_PROTEIN_MW",
          label: "Protein (Da)",
          visible: visibility.isMolecularWeight,
        },
      ],
      basicControls: [
        { key: "WAVELENGTH", label: "Wavelength" },
        { key: "RESOLUTION_LOW", label: "Low resolution limit" },
        { key: "RESOLUTION_HIGH", label: "High resolution limit" },
      ],
      modelSimilarity: [
        {
          key: "PART_VARI",
          label: "How to specify similarity (i.e. sequence or coords)",
        },
        {
          key: "PART_DEVI",
          label: "Sequence identity (0.0-1.0) or RMSD (Angstroms)",
        },
      ],
      keywords: [{ key: "keywords", label: "Additional keywords" }],
    }),
    [visibility]
  );

  // Stable render helper function
  const renderElements = useCallback(
    (elements: any[]) =>
      elements.map(({ key, label, visible = () => true, ...extraProps }) => (
        <CCP4i2TaskElement
          {...props}
          key={key}
          itemName={key}
          qualifiers={{ guiLabel: label, ...extraProps }}
          visibility={visible}
        />
      )),
    [props]
  );

  return (
    <Paper>
      <CCP4i2Tabs>
        <CCP4i2Tab label="Main inputs" key="main">
          <CCP4i2ContainerElement
            {...props}
            itemName=""
            qualifiers={{
              guiLabel: "Input data",
              initiallyOpen: true,
            }}
            containerHint="BlockLevel"
            key="Input data"
          >
            {renderElements(elementConfigs.inputData)}
          </CCP4i2ContainerElement>

          <CCP4i2ContainerElement
            {...props}
            itemName=""
            qualifiers={{
              guiLabel: "Scattering in the crystal",
              initiallyOpen: true,
            }}
            containerHint="FolderLevel"
            key="Scattering"
          >
            {renderElements(elementConfigs.scatteringContent)}
          </CCP4i2ContainerElement>

          <CCP4i2ContainerElement
            {...props}
            itemName=""
            qualifiers={{
              guiLabel: "Basic controls",
              initiallyOpen: true,
            }}
            containerHint="FolderLevel"
            key="Basic controls"
          >
            {renderElements(elementConfigs.basicControls)}
          </CCP4i2ContainerElement>

          <CCP4i2ContainerElement
            {...props}
            itemName=""
            qualifiers={{
              guiLabel: "Similarity of search model",
              initiallyOpen: true,
            }}
            containerHint="FolderLevel"
            key="Similarity"
            visibility={visibility.isPartialModel}
          >
            {renderElements(elementConfigs.modelSimilarity)}
          </CCP4i2ContainerElement>
        </CCP4i2Tab>

        <CCP4i2Tab label="Keywords" key="keywords">
          {renderElements(elementConfigs.keywords)}
        </CCP4i2Tab>
      </CCP4i2Tabs>
    </Paper>
  );
};

export default TaskInterface;
