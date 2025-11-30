import { Grid2, LinearProgress, Paper, Stack, Typography } from "@mui/material";
import { CCP4i2TaskInterfaceProps } from "./task-container";
import { CCP4i2TaskElement } from "../task-elements/task-element";
import { CCP4i2Tab, CCP4i2Tabs } from "../task-elements/tabs";
import { useJob, useDigestEffect } from "../../../utils";
import { CCP4i2ContainerElement } from "../task-elements/ccontainer";

const TaskInterface: React.FC<CCP4i2TaskInterfaceProps> = (props) => {
  const { job } = props;
  const { useTaskItem, useFileDigest, mutateContainer } = useJob(job.id);

  const { value: SEQUENCETEXT, update: setSEQUENCETEXT } =
    useTaskItem("SEQUENCETEXT");

  const { item: SEQINItem } = useTaskItem("SEQIN");

  // Use the file digest hook to get sequence data
  const SEQINDigest = useFileDigest(SEQINItem?._objectPath);

  // Auto-update sequence text when SEQIN file changes
  useDigestEffect(
    SEQINDigest,
    (digestData) => {
      const newSequence = digestData.sequence || "";
      if (!newSequence) return undefined;

      // Build the formatted sequence text
      return `>${digestData.identifier || ""}\n${newSequence}`.replace("*", "");
    },
    setSEQUENCETEXT,
    job?.status
  );

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
