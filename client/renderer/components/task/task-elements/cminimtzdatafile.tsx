import { Stack } from "@mui/material";
import { CDataFileElement } from "./cdatafile";
import { CCP4i2TaskElementProps } from "./task-element";
import { useCallback, useMemo } from "react";
import { useApi } from "../../../api";
import { BaseSpacegroupCellElement } from "./base-spacegroup-cell-element";
import { readFilePromise, useJob } from "../../../utils";
import { Job } from "../../../types/models";
import { useCCP4i2Window } from "../../../app-context";
import { selectMtzColumns } from "./mtz-column-dialog";

export const CMiniMtzDataFileElement: React.FC<CCP4i2TaskElementProps> = (
  props
) => {
  const { job, itemName, onChange, visibility } = props;
  const api = useApi();
  const { useTaskItem, useFileDigest } = useJob(job.id);
  const { item } = useTaskItem(itemName);
  const { cootModule } = useCCP4i2Window();

  // Mutation hooks
  const mutators = {
    jobs: api.get_endpoint<Job[]>({
      type: "projects",
      id: job.project,
      endpoint: "jobs",
    }).mutate,
    container: api.get_wrapped_endpoint_json<any>({
      type: "jobs",
      id: job.id,
      endpoint: "container",
    }).mutate,
    validation: api.get_endpoint_xml({
      type: "jobs",
      id: job.id,
      endpoint: "validation",
    }).mutate,
    files: api.get<File[]>(`projects/${job.project}/files`).mutate,
  };

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
   * 2. Uploading the file with the selected columns
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

        // Read file and upload
        const fileBuffer = await readFilePromise(file, "ArrayBuffer");

        const formData = new FormData();
        if (columnSelector?.trim()) {
          formData.append("column_selector", columnSelector);
        }
        formData.append("objectPath", item._objectPath);
        formData.append(
          "file",
          new Blob([fileBuffer as string], { type: "application/CCP4-mtz-file" }),
          file.name
        );

        const uploadResult = await api.post<any>(
          `jobs/${job.id}/upload_file_param`,
          formData
        );

        // Handle new standardized API response format: {success: true, data: {...}}
        const resultData = uploadResult.data || uploadResult;
        onChange?.(resultData.updated_item);

        // Trigger all mutations
        await Promise.all([
          mutators.jobs(),
          mutators.files(),
          mutators.container(),
          mutators.validation(),
          mutateDigest(),
        ]);
      } catch (error) {
        console.error("File upload failed:", error);
        // Could show an error toast/snackbar here
      }
    },
    [job.id, item, cootModule, onChange, api, mutators, mutateDigest]
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
