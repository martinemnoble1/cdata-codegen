"use client";

import React, {
  SyntheticEvent,
  useCallback,
  useEffect,
  useMemo,
  useReducer,
  useState,
} from "react";
import {
  Autocomplete,
  AutocompleteChangeReason,
  Button,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControlLabel,
  Radio,
  RadioGroup,
  Stack,
  TextField,
} from "@mui/material";
import SimpleDialog from "@mui/material/Dialog";
import { createRoot } from "react-dom/client";
import { v4 as uuid4 } from "uuid";

// Constants
const SIGNATURE_MAP: Record<string, string> = {
  KMKM: "Intensity Friedel pairs",
  GLGL: "Structure factor Friedel pairs",
  JQ: "Intensities",
  FQ: "Structure factors",
} as const;

const GENERIC_SIGNATURES = ["KMKM", "GLGL", "JQ", "FQ"] as const;

// Types
interface ColumnOptions {
  [signature: string]: string[];
}

interface ColumnNames {
  [columnLabel: string]: string;
}

interface ColumnCounters {
  [columnType: string]: number;
}

interface ValuesState {
  [signature: string]: string;
}

interface ValuesAction {
  type: "SET_VALUE";
  signature: string;
  value: string;
}

interface ItemQualifiers {
  correctColumns?: string[];
}

interface MtzItem {
  _class?: string;
  _objectPath?: string;
  _qualifiers?: ItemQualifiers;
}

interface MtzColumnDialogProps {
  columnNames: ColumnNames;
  item: MtzItem;
  onAccept: (columnSelector: string) => void;
  onCancel: () => void;
}

// Reducer
const valuesReducer = (
  state: ValuesState,
  action: ValuesAction
): ValuesState => {
  switch (action.type) {
    case "SET_VALUE":
      return {
        ...state,
        [action.signature]: action.value,
      };
    default:
      return state;
  }
};

// Helper functions
const createSignatureOptions = (
  signature: string,
  sortedColumnNames: Record<string, string[]>
): string[] => {
  const signatureOptions: string[][] = [];
  let optionIndex = 0;

  const columnCounters: ColumnCounters = {};
  Object.keys(sortedColumnNames).forEach((key) => {
    columnCounters[key] = 0;
  });

  let shouldContinue = true;

  while (shouldContinue) {
    signatureOptions[optionIndex] = [];

    for (let i = 0; i < signature.length; i++) {
      const columnType = signature.charAt(i);

      if (!Object.keys(sortedColumnNames).includes(columnType)) {
        shouldContinue = false;
        break;
      }

      if (columnCounters[columnType] >= sortedColumnNames[columnType].length) {
        shouldContinue = false;
        break;
      }

      signatureOptions[optionIndex].push(
        sortedColumnNames[columnType][columnCounters[columnType]]
      );
      columnCounters[columnType] += 1;
    }

    optionIndex += 1;
  }

  return signatureOptions
    .filter((option) => option.length > 0)
    .map((option) => `/*/*/[${option.join(",")}]`);
};

const buildColumnOptions = (
  allColumnNames: ColumnNames,
  item: MtzItem
): ColumnOptions => {
  const sortedColumnNames: Record<string, string[]> = {};

  // Group columns by type
  Object.entries(allColumnNames).forEach(([label, columnType]) => {
    if (!sortedColumnNames[columnType]) {
      sortedColumnNames[columnType] = [];
    }
    sortedColumnNames[columnType].push(label);
  });

  // Determine signatures to process
  // CGenericReflDataFile is a general container without specific column types
  // so it uses the generic signatures. Other types use their correctColumns qualifier.
  // Note: CMtzDataFile is handled earlier in selectMtzColumns() - it skips the dialog entirely.
  const signatures =
    item._class === "CGenericReflDataFile"
      ? [...GENERIC_SIGNATURES]
      : [...(item._qualifiers?.correctColumns || [])];

  const options: ColumnOptions = {};

  signatures.forEach((signature) => {
    const signatureOptions = createSignatureOptions(
      signature,
      sortedColumnNames
    );
    if (signatureOptions.length > 0) {
      options[signature] = signatureOptions;
    }
  });

  return options;
};

const getSignatureLabel = (signature: string): string => {
  return SIGNATURE_MAP[signature] || signature;
};

// Dialog Component (internal)
const MtzColumnDialogComponent: React.FC<MtzColumnDialogProps> = ({
  columnNames,
  item,
  onAccept,
  onCancel,
}) => {
  const [open, setOpen] = useState(true);
  const [selectedGroup, setSelectedGroup] = useState<string | null>(null);
  const [values, dispatch] = useReducer(valuesReducer, {});

  // Build column options on mount
  const columnOptions = useMemo(
    () => buildColumnOptions(columnNames, item),
    [columnNames, item]
  );

  // Initialize values and selected group
  useEffect(() => {
    if (Object.keys(columnOptions).length > 0) {
      const initialValues: ValuesState = {};
      Object.entries(columnOptions).forEach(([signature, signatureOptions]) => {
        initialValues[signature] = signatureOptions[0];
      });

      Object.entries(initialValues).forEach(([signature, value]) => {
        dispatch({ type: "SET_VALUE", signature, value });
      });

      setSelectedGroup(Object.keys(columnOptions)[0]);
    }
  }, [columnOptions]);

  const handleGroupChange = useCallback(
    (_event: SyntheticEvent<Element, Event>, newValue: string | null) => {
      setSelectedGroup(newValue);
    },
    []
  );

  const handleColumnChange = useCallback(
    (signature: string) =>
      (
        _event: SyntheticEvent<Element, Event>,
        value: string | null,
        _reason: AutocompleteChangeReason
      ) => {
        dispatch({
          type: "SET_VALUE",
          signature,
          value: value || "",
        });
      },
    []
  );

  const handleAccept = useCallback(() => {
    if (selectedGroup && values[selectedGroup]) {
      setOpen(false);
      onAccept(values[selectedGroup]);
    }
  }, [selectedGroup, values, onAccept]);

  const handleCancel = useCallback(() => {
    setOpen(false);
    onCancel();
  }, [onCancel]);

  const isAcceptDisabled = !selectedGroup || !values[selectedGroup];

  // If no options available, auto-cancel
  useEffect(() => {
    if (Object.keys(columnOptions).length === 0) {
      handleCancel();
    }
  }, [columnOptions, handleCancel]);

  return (
    <SimpleDialog
      open={open}
      onClose={handleCancel}
      slotProps={{
        paper: {
          sx: { width: "80%", maxWidth: "none" },
        },
      }}
    >
      <DialogTitle>{item._objectPath}</DialogTitle>

      <DialogContent>
        <RadioGroup value={selectedGroup} onChange={handleGroupChange}>
          {Object.entries(columnOptions).map(
            ([signature, options]) =>
              options.length > 0 && (
                <Stack key={signature} direction="row" spacing={2}>
                  <FormControlLabel
                    sx={{ minWidth: "20rem" }}
                    value={signature}
                    control={<Radio size="small" />}
                    label={getSignatureLabel(signature)}
                  />

                  <Autocomplete
                    options={options}
                    value={values[signature] || ""}
                    onChange={handleColumnChange(signature)}
                    renderInput={(params) => (
                      <TextField
                        sx={{ my: 2, minWidth: "20rem" }}
                        {...params}
                        label="Columns"
                      />
                    )}
                  />
                </Stack>
              )
          )}
        </RadioGroup>
      </DialogContent>

      <DialogActions>
        <Button disabled={isAcceptDisabled} onClick={handleAccept}>
          OK
        </Button>
        <Button onClick={handleCancel}>Cancel</Button>
      </DialogActions>
    </SimpleDialog>
  );
};

// Types for the public API
export interface MtzColumnResult {
  columnSelector: string;
}

export interface ParseMtzOptions {
  file: File;
  item: MtzItem;
  cootModule: any; // The coot WASM module
}

/**
 * Parse an MTZ file and get column names using coot's WASM module.
 * Returns the parsed column names or null if parsing fails.
 */
export async function parseMtzColumns(
  file: File,
  cootModule: any
): Promise<ColumnNames | null> {
  try {
    // Read file as ArrayBuffer
    const fileContent = await new Promise<ArrayBuffer>((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result as ArrayBuffer);
      reader.onerror = () => reject(reader.error);
      reader.readAsArrayBuffer(file);
    });

    if (!fileContent) {
      return null;
    }

    const fileName = `File_${uuid4()}`;
    const byteArray = new Uint8Array(fileContent);

    // Write to coot's virtual filesystem
    cootModule.FS_createDataFile(".", fileName, byteArray, true, true);

    // Get column info
    const headerInfo = cootModule.get_mtz_columns(fileName);

    // Clean up
    cootModule.FS_unlink(`./${fileName}`);

    // Parse columns
    const columns: ColumnNames = {};
    for (let i = 0; i < headerInfo.size(); i += 2) {
      columns[headerInfo.get(i + 1)] = headerInfo.get(i);
    }

    if (Object.keys(columns).length === 0) {
      return null;
    }

    return columns;
  } catch (error) {
    console.error("Failed to parse MTZ file:", error);
    return null;
  }
}

/**
 * Show the MTZ column selection dialog.
 * Returns a Promise that resolves with the selected column selector string,
 * or null if the user cancels.
 */
export function showMtzColumnDialog(
  columnNames: ColumnNames,
  item: MtzItem
): Promise<string | null> {
  return new Promise((resolve) => {
    // Create a container for the dialog
    const container = document.createElement("div");
    container.id = `mtz-dialog-${Date.now()}`;
    document.body.appendChild(container);

    const root = createRoot(container);

    const cleanup = () => {
      // Small delay to allow dialog close animation
      setTimeout(() => {
        root.unmount();
        container.remove();
      }, 300);
    };

    const handleAccept = (columnSelector: string) => {
      cleanup();
      resolve(columnSelector);
    };

    const handleCancel = () => {
      cleanup();
      resolve(null);
    };

    root.render(
      <MtzColumnDialogComponent
        columnNames={columnNames}
        item={item}
        onAccept={handleAccept}
        onCancel={handleCancel}
      />
    );
  });
}

/**
 * Complete flow: parse MTZ file and show column selection dialog if needed.
 * Returns the column selector string, or null if cancelled/failed.
 *
 * For non-MTZ files, returns a default column selector.
 * For CMtzDataFile (general container), skips column selection entirely.
 */
export async function selectMtzColumns(
  options: ParseMtzOptions
): Promise<string | null> {
  const { file, item, cootModule } = options;

  // Check if it's an MTZ file
  const isMtzFile = file.name.toLowerCase().endsWith(".mtz");

  if (!isMtzFile) {
    // For non-MTZ files, return a default
    return "/*/*/[FP,SIGFP]";
  }

  // CMtzDataFile is a general container that stores the intact reflection file
  // without separating out columns - no column selection needed
  if (item._class === "CMtzDataFile") {
    return "";  // Empty string signals "store whole file as-is"
  }

  // Parse the MTZ file
  const columnNames = await parseMtzColumns(file, cootModule);

  if (!columnNames) {
    // Parsing failed
    return null;
  }

  // Show the dialog and get user selection
  return showMtzColumnDialog(columnNames, item);
}
