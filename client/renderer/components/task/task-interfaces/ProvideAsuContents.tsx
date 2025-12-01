import {
  Alert,
  Grid2,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { CCP4i2TaskInterfaceProps } from "./task-container";
import { CCP4i2TaskElement } from "../task-elements/task-element";
import { CCP4i2Tab, CCP4i2Tabs } from "../task-elements/tabs";
import { useApi } from "../../../api";
import { useJob } from "../../../utils";
import { CCP4i2ContainerElement } from "../task-elements/ccontainer";
import { useCallback, useState } from "react";
import useSWR from "swr";
import { apiPost } from "../../../api-fetch";
import { BaseSpacegroupCellElement } from "../task-elements/base-spacegroup-cell-element";

const TaskInterface: React.FC<CCP4i2TaskInterfaceProps> = (props) => {
  const api = useApi();
  const { job } = props;
  const { useTaskItem, useFileDigest, fetchDigest } = useJob(job.id);
  const { update: setAsuContent } = useTaskItem("ASU_CONTENT");
  const { item: asuContentInItem } = useTaskItem("ASUCONTENTIN");
  const { item: hklinItem } = useTaskItem("HKLIN");

  // State to hold HKLIN digest (fetched imperatively on file change)
  const [hklinDigest, setHklinDigest] = useState<any>(null);

  // File digest for HKLIN (used for Matthews calculation) - also use SWR for initial load
  const { data: HKLINDigestSWR } = useFileDigest(
    `ProvideAsuContents.inputData.HKLIN`
  );

  // Use imperatively fetched digest if available, otherwise fall back to SWR data
  const HKLINDigest = hklinDigest || HKLINDigestSWR;

  /**
   * Handle HKLIN file change - fetch digest for Matthews calculation.
   */
  const handleHKLINChange = useCallback(async () => {
    console.log("handleHKLINChange called, hklinItem:", hklinItem?._objectPath);
    if (!hklinItem?._objectPath) {
      console.log("handleHKLINChange: no objectPath, returning early");
      return;
    }

    console.log("handleHKLINChange: fetching digest for", hklinItem._objectPath);
    const digestData = await fetchDigest(hklinItem._objectPath);
    console.log("handleHKLINChange: got digest data:", digestData);
    setHklinDigest(digestData ? { data: digestData } : null);
  }, [hklinItem?._objectPath, fetchDigest]);

  /**
   * Handle ASUCONTENTIN file change - explicitly fetch digest and populate ASU_CONTENT.
   * Uses imperative fetchDigest for deterministic, race-condition-free behavior.
   */
  const handleAsuContentInChange = useCallback(async () => {
    if (!asuContentInItem?._objectPath) return;

    // Fetch the digest for the newly uploaded/selected file
    const digestData = await fetchDigest(asuContentInItem._objectPath);

    // Extract seqList and populate ASU_CONTENT
    if (digestData?.seqList && Array.isArray(digestData.seqList)) {
      const seqList = digestData.seqList.map((seq: any) => ({
        name: seq.name,
        sequence: seq.sequence,
        polymerType: seq.polymerType,
        description: seq.description,
        nCopies: seq.nCopies,
      }));
      await setAsuContent(seqList);
    }
  }, [asuContentInItem?._objectPath, fetchDigest, setAsuContent]);

  /**
   * Fetch ASU content validity from the backend.
   * This calls the validity() method on CAsuContentSeqList which checks:
   * - At least one sequence entry
   * - Each entry has valid polymerType, name, nCopies > 0, sequence length > 1
   */
  const { data: asuValidity, mutate: mutateAsuValidity } = useSWR(
    [`jobs/${job.id}/object_method`, "validity", "ASU_CONTENT"],
    ([url]) =>
      apiPost(url, {
        object_path: "ProvideAsuContents.inputData.ASU_CONTENT",
        method_name: "validity",
      })
  );

  // ASU content is valid when the backend validity check passes
  // API response format: {success: true, data: {result: {...}}}
  const isAsuContentValid = asuValidity?.data?.result?.valid === true;

  /**
   * Fetches the molecular weight for the current job's ASU content using SWR.
   * Only fetches when ASU_CONTENT is valid (passes all validation checks).
   */
  const { data: molWeight, mutate: mutateMolWeight } = useSWR(
    isAsuContentValid ? [`jobs/${job.id}/object_method`, "molecularWeight"] : null,
    ([url]) =>
      apiPost(url, {
        object_path: "ProvideAsuContents.inputData.ASU_CONTENT",
        method_name: "molecularWeight",
      })
  );

  /**
   * Fetches and caches the Matthews coefficient analysis for the current job using SWR.
   * Only fetches when we have both a valid molecular weight result AND an HKLIN file.
   */
  const { data: matthewsAnalysis } = useSWR(
    // Only fetch when we have molecular weight AND HKLIN digest
    // API response format: {success: true, data: {result: <value>}}
    molWeight?.data?.result && HKLINDigest?.data
      ? [
          `jobs/${job.id}/object_method`,
          "matthewsCoeff",
          molWeight.data.result,
          HKLINDigest.data,
        ]
      : null,
    ([url, , molWeightResult]) =>
      apiPost(url, {
        object_path: "ProvideAsuContents.inputData.HKLIN.fileContent",
        method_name: "matthewsCoeff",
        kwargs: { molWt: molWeightResult },
      }),
    { keepPreviousData: true }
  );

  return (
    <CCP4i2Tabs {...props}>
      <CCP4i2Tab label="Main inputs">
        <CCP4i2ContainerElement
          {...props}
          itemName=""
          qualifiers={{
            guiLabel: "Optionally load existing AU content file to edit",
          }}
          containerHint="BlockLevel"
          initiallyOpen={true}
          size={{ xs: 12 }}
        >
          <CCP4i2TaskElement
            {...props}
            itemName="ASUCONTENTIN"
            qualifiers={{ guiLabel: "ASU contents" }}
            onChange={handleAsuContentInChange}
          />
        </CCP4i2ContainerElement>
        <CCP4i2ContainerElement
          {...props}
          itemName=""
          qualifiers={{
            guiLabel:
              "Specify the protein/nucleic acid sequences in the crystal",
          }}
          containerHint="FolderLevel"
          initiallyOpen={true}
          size={{ xs: 12 }}
        >
          <CCP4i2TaskElement
            {...props}
            itemName="ASU_CONTENT"
            qualifiers={{ guiLabel: "ASU contents" }}
            onChange={() => {
              // Re-check validity and molecular weight when ASU content changes
              mutateAsuValidity();
              mutateMolWeight();
            }}
          />
        </CCP4i2ContainerElement>
        <Typography>
          Molecular weight:{" "}
          {molWeight?.data?.result
            ? molWeight.data.result?.toFixed(2)
            : isAsuContentValid
              ? "(calculating...)"
              : asuValidity?.data?.result?.message || "(no valid sequences)"}
        </Typography>
        <CCP4i2ContainerElement
          {...props}
          itemName=""
          qualifiers={{ guiLabel: "Solvent analysis" }}
          containerHint="BlockLevel"
          initiallyOpen={true}
          size={{ xs: 12 }}
        >
          <Grid2 container spacing={2}>
            <Grid2 size={{ xs: 12, sm: 8 }}>
              <CCP4i2TaskElement
                {...props}
                itemName="HKLIN"
                qualifiers={{ guiLabel: "MTZFile (for Matthews volume calc)" }}
                onChange={handleHKLINChange}
              />
              {/* Show MTZ file info when digest is available */}
              {HKLINDigest?.data && (
                <Stack spacing={1} sx={{ mt: 1 }}>
                  <BaseSpacegroupCellElement data={HKLINDigest.data} />
                  {/* Warning if no wavelengths (e.g., FreeR-only file) */}
                  {HKLINDigest.data.cell && (!HKLINDigest.data.wavelengths || HKLINDigest.data.wavelengths.length === 0) && (
                    <Alert severity="info" sx={{ py: 0 }}>
                      No wavelength information in this MTZ file
                    </Alert>
                  )}
                </Stack>
              )}
            </Grid2>
            <Grid2 size={{ xs: 12, sm: 4 }}>
              {matthewsAnalysis?.success && matthewsAnalysis?.data?.result ? (
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Multiplier</TableCell>
                      <TableCell>%Solvent</TableCell>
                      <TableCell>Probability</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {matthewsAnalysis?.data?.result?.results.map((result) => (
                      <TableRow key={result.nmol_in_asu}>
                        <TableCell>{result.nmol_in_asu}</TableCell>
                        <TableCell>
                          {result.percent_solvent.toFixed(2)}
                        </TableCell>
                        <TableCell>{result.prob_matth.toFixed(2)}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                "Provide MTZ file to calculate Matthews coefficient"
              )}
            </Grid2>
          </Grid2>
        </CCP4i2ContainerElement>
      </CCP4i2Tab>
    </CCP4i2Tabs>
  );
};
export default TaskInterface;
