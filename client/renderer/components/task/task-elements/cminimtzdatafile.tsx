import { Stack } from "@mui/material";
import { CDataFileElement } from "./cdatafile";
import { CCP4i2TaskElementProps } from "./task-element";
import { useCallback, useMemo } from "react";
import { BaseSpacegroupCellElement } from "./base-spacegroup-cell-element";
import { readFilePromise, useJob, useProject } from "../../../utils";
import { useCCP4i2Window } from "../../../app-context";
import { selectMtzColumns } from "./mtz-column-dialog";

export const CMiniMtzDataFileElement: React.FC<CCP4i2TaskElementProps> = (
  props
) => {
  const { job, itemName, onChange, visibility } = props;
  const { useTaskItem, useFileDigest, uploadFileParam } = useJob(job.id);
  const { mutateJobs, mutateFiles } = useProject(job.project);
  const { item } = useTaskItem(itemName);
  const { cootModule } = useCCP4i2Window();

  const { data: fileDigest, mutate: mutateDigest } = useFileDigest(
    item?._objectPath || ""
  );

  const infoContent = useMemo(
    () => <BaseSpacegroupCellElement data={fileDigest} />,
    [fileDigest]
  );

  /**
   * Handle file selection from the file picker.
   * This is the single entry point for file uploads - it handles:
   * 1. Showing the column selection dialog (for MTZ files)
   * 2. Uploading the file with the selected columns (with intent tracking)
   * 3. Updating the UI state
   */
  const handleFileSelection = useCallback(
    async (files: FileList | null) => {
      if (!files || files.length === 0 || !item || !cootModule) {
        return;
      }

      const file = files[0];

      try {
        // Show column selection dialog if needed (Promise-based, no component state)
        const columnSelector = await selectMtzColumns({
          file,
          item,
          cootModule,
        });

        // User cancelled the dialog
        if (columnSelector === null) {
          return;
        }

        // Read file and upload using centralized uploadFileParam (with intent tracking)
        const fileBuffer = await readFilePromise(file, "ArrayBuffer");

        const uploadResult = await uploadFileParam({
          objectPath: item._objectPath,
          file: new Blob([fileBuffer as ArrayBuffer], { type: "application/CCP4-mtz-file" }),
          fileName: file.name,
          columnSelector: columnSelector || undefined,
        });

        // Handle response
        if (uploadResult?.success && uploadResult.data?.updated_item) {
          onChange?.(uploadResult.data.updated_item);
        }

        // Trigger additional mutations not handled by uploadFileParam
        await Promise.all([
          mutateJobs(),
          mutateFiles(),
          mutateDigest(),
        ]);
      } catch (error) {
        console.error("File upload failed:", error);
        // Could show an error toast/snackbar here
      }
    },
    [item, cootModule, onChange, uploadFileParam, mutateJobs, mutateFiles, mutateDigest]
  );

  const isVisible = useMemo(
    () =>
      !visibility ||
      (typeof visibility === "function" ? visibility() : visibility),
    [visibility]
  );

  if (!isVisible) return null;

  // Wrap async handler for the sync setFiles prop
  const setFiles = useCallback(
    (files: FileList | null) => {
      handleFileSelection(files);
    },
    [handleFileSelection]
  );

  return (
    <Stack direction="column">
      <CDataFileElement
        {...props}
        infoContent={infoContent}
        setFiles={setFiles}
      />
    </Stack>
  );
};
