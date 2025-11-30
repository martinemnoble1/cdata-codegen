import { Grid2, LinearProgress, Paper, Stack, Typography } from "@mui/material";
import { CCP4i2TaskInterfaceProps } from "./task-container";
import { CCP4i2TaskElement } from "../task-elements/task-element";
import { CCP4i2Tab, CCP4i2Tabs } from "../task-elements/tabs";
import { useJob } from "../../../utils";
import { CCP4i2ContainerElement } from "../task-elements/ccontainer";
import { useEffect, useRef } from "react";

const TaskInterface: React.FC<CCP4i2TaskInterfaceProps> = (props) => {
  const { job } = props;
  const { useTaskItem, useFileDigest, mutateContainer } = useJob(job.id);

  const { value: SEQUENCETEXT, update: setSEQUENCETEXT } =
    useTaskItem("SEQUENCETEXT");

  const { item: SEQINItem } = useTaskItem("SEQIN");

  // Use the file digest hook to get sequence data
  const { data: SEQINDigest } = useFileDigest(SEQINItem?._objectPath);

  // Track last set sequence to avoid re-setting the same value
  const lastSetSequenceRef = useRef<string | null>(null);

  // Extract sequence from SEQIN digest when it changes
  useEffect(() => {
    // API returns {success: true, data: {...}} - extract the data
    const digestData = SEQINDigest?.data;
    if (!digestData || !setSEQUENCETEXT || job?.status !== 1) return;

    const newSequence = digestData.sequence || "";
    if (!newSequence) return;

    // Build the formatted sequence text
    const formattedSequence = `>${digestData.identifier || ""}\n${newSequence}`.replace(
      "*",
      ""
    );

    // Don't re-set if we already set this value
    if (lastSetSequenceRef.current === formattedSequence) return;

    console.log("Updating sequence from SEQIN digest");
    lastSetSequenceRef.current = formattedSequence;
    setSEQUENCETEXT(formattedSequence);
  }, [SEQINDigest, setSEQUENCETEXT, job?.status]);

  return (
    <CCP4i2Tabs {...props}>
      <CCP4i2Tab label="Main inputs">
        <CCP4i2ContainerElement
          {...props}
          itemName=""
          qualifiers={{ guiLabel: "Key files" }}
          containerHint="FolderLevel"
          initiallyOpen={true}
          size={{ xs: 12 }}
        >
          <CCP4i2TaskElement
            {...props}
            itemName="SEQUENCETEXT"
            qualifiers={{ guiLabel: "Sequence", guiMode: "multiLine" }}
            sx={{ minWidth: "100%", minHeight: "10rem" }}
          />

          <CCP4i2TaskElement
            {...props}
            itemName="SEQIN"
            qualifiers={{ guiLabel: "File from which to extract sequence" }}
          />

          <CCP4i2TaskElement
            {...props}
            itemName="XYZIN"
            qualifiers={{ guiLabel: "MTZFile (for Matthews volumne calc)" }}
          />
        </CCP4i2ContainerElement>
      </CCP4i2Tab>
    </CCP4i2Tabs>
  );
};
export default TaskInterface;
