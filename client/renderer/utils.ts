import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import $ from "jquery";
import useSWR, { KeyedMutator, mutate, SWRResponse } from "swr";

import { useApi } from "./api";
import {
  Job,
  JobCharValue,
  JobFloatValue,
  Project,
  File as DjangoFile,
} from "./types/models";
import { useRunCheck } from "./providers/run-check-provider";
import { useParameterChangeIntent } from "./providers/parameter-change-intent-provider";
import { apiJson, apiText } from "./api-fetch";

// ============================================================================
// Types and Interfaces
// ============================================================================

export interface SetParameterArg {
  object_path: string;
  value: any;
}

/**
 * New API response format for set_parameter endpoint.
 * Returns {success: true, data: {updated_item: ...}} on success.
 */
export type SetParameterResponse =
  | {
      success: true;
      data: {
        updated_item: any;
      };
    }
  | {
      success: false;
      error: string;
    };

/**
 * New API response format for create_task endpoint.
 * Returns {success: true, data: {new_job: ...}} on success.
 */
export interface CreateTaskResponse {
  success: boolean;
  data?: {
    new_job: Job;
  };
  error?: string;
}
export interface ValidationError {
  path: string;
  error: {
    maxSeverity: number;
    [key: string]: any;
  };
}

export interface TaskItem {
  item: any;
  value: any;
  update: (value: any) => Promise<boolean | Response>;
  updateNoMutate: (value: any) => Promise<boolean | Response>;
}

export interface ProjectData {
  project: Project | undefined;
  mutateProject: () => void;
  directory: any;
  mutateDirectory: () => void;
  jobs: Job[] | undefined;
  mutateJobs: KeyedMutator<Job[]>;
  files: DjangoFile[] | undefined;
  mutateFiles: KeyedMutator<DjangoFile[]>;
  jobCharValues: JobCharValue[] | undefined;
  mutateJobCharValues: () => void;
  jobFloatValues: JobFloatValue[] | undefined;
  mutateJobFloatValues: () => void;
}

/**
 * API response format for upload_file_param endpoint.
 */
export type UploadFileParamResponse =
  | {
      success: true;
      data: {
        updated_item: any;
      };
    }
  | {
      success: false;
      error: string;
    };

/**
 * Arguments for uploadFileParam function.
 */
export interface UploadFileParamArg {
  objectPath: string;
  file: Blob;
  fileName: string;
  columnSelector?: string;
}

export interface JobData {
  job: Job | undefined;
  mutateJob: () => void;
  container: any;
  mutateContainer: () => void;
  params_xml: any;
  mutateParams_xml: () => void;
  validation: any;
  mutateValidation: () => void;
  diagnostic_xml: any;
  mutateDiagnosticXml: () => void;
  def_xml: any;
  mutateDef_xml: () => void;
  setParameter: (
    arg: SetParameterArg
  ) => Promise<SetParameterResponse | undefined>;
  setParameterNoMutate: (
    arg: SetParameterArg
  ) => Promise<SetParameterResponse | undefined>;
  uploadFileParam: (
    arg: UploadFileParamArg
  ) => Promise<UploadFileParamResponse | undefined>;
  useTaskItem: (paramName: string) => TaskItem;
  createPeerTask: (taskName: string) => Promise<Job | undefined>;
  useFileContent: (paramName: string) => SWRResponse<string, Error>;
  getValidationColor: (item: any) => string;
  getErrors: (item: any) => ValidationError[];
  useFileDigest: (objectPath: string) => SWRResponse<any, Error>;
  getFileDigest: (objectPath: string) => any | null;
  fileItemToParameterArg: (
    value: DjangoFile,
    objectPath: string,
    projectJobs: Job[],
    projects: Project[]
  ) => SetParameterArg;
}

// ============================================================================
// Constants
// ============================================================================

const VALIDATION_COLORS = {
  SUCCESS: "success.light",
  WARNING: "warning.light",
  ERROR: "error.light",
} as const;

const SEVERITY_LEVELS = {
  SUCCESS: 0,
  WARNING: 1,
  ERROR: 2,
} as const;

const JOB_STATUS = {
  PENDING: 1,
} as const;

const FILE_DIRECTORIES = {
  JOB_OUTPUT: 1,
  IMPORTED: 2,
} as const;

const FILE_PATHS = {
  IMPORTED_FILES: "CCP4_IMPORTED_FILES",
  JOB_PREFIX: "job_",
  JOBS_DIR: "CCP4_JOBS",
} as const;

// ============================================================================
// Utility Functions
// ============================================================================

/**
 * Checks if the given path ends with the specified name, considering dot notation.
 */
const pathMatches = (
  path: string | null | undefined,
  name: string
): boolean => {
  if (!path || !name) return false;

  const normalizedName = `.${name}`.replace(/\.+/g, ".");
  const normalizedPath = `.${path}`.replace(/\.+/g, ".");

  return normalizedPath.endsWith(normalizedName);
};

/**
 * Safely checks if an object has a constructor matching the expected type.
 */
const hasConstructor = (obj: any, constructor: any): boolean => {
  return obj && typeof obj === "object" && obj.constructor === constructor;
};

/**
 * Recursively searches for items within a container that match a specified name.
 */
const findItemsRecursively = (
  name: string,
  container: any,
  multiple: boolean = true,
  accumulator: any[] = []
): any[] => {
  if (!container || !name) return accumulator;

  const initialLength = accumulator.length;

  try {
    // Check if current container matches
    if (pathMatches(container?._objectPath, name)) {
      accumulator.push(container);
      if (!multiple) return accumulator;
    }

    // Handle CList containers
    if (container._baseClass === "CList" && Array.isArray(container._value)) {
      for (const item of container._value) {
        if (pathMatches(item?._objectPath, name)) {
          accumulator.push(item);
          if (!multiple) return accumulator;
        }

        // Recursive search
        findItemsRecursively(name, item, multiple, accumulator);
        if (!multiple && accumulator.length > initialLength) {
          return accumulator;
        }
      }
    }
    // Handle object containers
    else if (hasConstructor(container._value, Object)) {
      for (const key of Object.keys(container._value)) {
        const item = container._value[key];

        if (pathMatches(item?._objectPath, name)) {
          accumulator.push(item);
          if (!multiple) return accumulator;
        }

        // Recursive search
        findItemsRecursively(name, item, multiple, accumulator);
        if (!multiple && accumulator.length > initialLength) {
          return accumulator;
        }
      }
    }
  } catch (error) {
    console.error(`Error searching for items with name "${name}":`, error);
  }

  return accumulator;
};

/**
 * Extracts validation errors for a given item based on the provided validation object.
 */
const extractValidationErrors = (
  item: any,
  validation: any
): ValidationError[] => {
  if (!validation || !item?._objectPath) {
    return [];
  }

  const itemPath = item._objectPath;
  const matchingErrors: ValidationError[] = [];

  try {
    for (const validationPath of Object.keys(validation)) {
      if (
        validationPath === itemPath ||
        validationPath.startsWith(`${itemPath}.`) ||
        validationPath.startsWith(`${itemPath}[`)
      ) {
        matchingErrors.push({
          path: validationPath,
          error: validation[validationPath],
        });
      }
    }
  } catch (error) {
    console.error("Error extracting validation errors:", error);
  }

  return matchingErrors;
};

/**
 * Determines the appropriate validation color based on error severity.
 */
const determineValidationColor = (
  fieldErrors: ValidationError[] | any
): string => {
  if (
    !fieldErrors ||
    !Array.isArray(fieldErrors) ||
    (Array.isArray(fieldErrors) && fieldErrors.length === 0)
  ) {
    return VALIDATION_COLORS.SUCCESS;
  }

  let maxSeverity: number = SEVERITY_LEVELS.SUCCESS;

  try {
    if (Array.isArray(fieldErrors)) {
      maxSeverity = fieldErrors.reduce((highest, error) => {
        const currentSeverity =
          error?.error?.maxSeverity ?? SEVERITY_LEVELS.SUCCESS;
        return Math.max(highest, currentSeverity);
      }, SEVERITY_LEVELS.SUCCESS);
    } else {
      if (
        fieldErrors &&
        typeof fieldErrors === "object" &&
        "maxSeverity" in fieldErrors
      ) {
        maxSeverity =
          (fieldErrors as { maxSeverity: number }).maxSeverity ??
          SEVERITY_LEVELS.SUCCESS;
      } else {
        maxSeverity = SEVERITY_LEVELS.SUCCESS;
      }
    }
  } catch (error) {
    console.error("Error determining validation color:", error);
    return VALIDATION_COLORS.ERROR;
  }

  if (maxSeverity === SEVERITY_LEVELS.SUCCESS) {
    return VALIDATION_COLORS.SUCCESS;
  } else if (maxSeverity === SEVERITY_LEVELS.WARNING) {
    return VALIDATION_COLORS.WARNING;
  } else {
    return VALIDATION_COLORS.ERROR;
  }
};

/**
 * Recursively extracts values from complex data structures.
 */
const extractValueRecursively = (item: any): any => {
  if (!item) return null;

  const { _value } = item;

  // Handle primitive values
  if (
    _value === undefined ||
    _value === null ||
    typeof _value === "string" ||
    typeof _value === "number" ||
    typeof _value === "boolean"
  ) {
    return _value;
  }

  // Handle objects
  if (hasConstructor(_value, Object)) {
    const result: Record<string, any> = {};
    try {
      for (const key of Object.keys(_value)) {
        result[key] = extractValueRecursively(_value[key]);
      }
    } catch (error) {
      console.error("Error extracting object values:", error);
    }
    return result;
  }

  // Handle arrays
  if (Array.isArray(_value)) {
    if (_value.length === 0) return [];

    try {
      return _value.map((value) => extractValueRecursively(value));
    } catch (error) {
      console.error("Error extracting array values:", error);
      return [];
    }
  }

  console.warn("Unknown item type:", _value);
  return _value;
};

/**
 * Creates a safe file reader promise with proper error handling.
 */
const createFileReaderPromise = (
  file: File,
  readAs: "Text" | "ArrayBuffer" | "File" = "Text"
): Promise<string | ArrayBuffer | File> => {
  return new Promise((resolve, reject) => {
    if (readAs === "File") {
      resolve(file);
      return;
    }

    const reader = new FileReader();

    const cleanup = () => {
      reader.onabort = null;
      reader.onerror = null;
      reader.onloadend = null;
    };

    reader.onabort = () => {
      cleanup();
      reject(new Error("File reading was aborted"));
    };

    reader.onerror = () => {
      cleanup();
      reject(new Error("File reading failed"));
    };

    reader.onloadend = () => {
      cleanup();
      if (reader.result !== null) {
        resolve(reader.result);
      } else {
        reject(new Error("File reading returned null"));
      }
    };

    try {
      if (readAs === "Text") {
        reader.readAsText(file);
      } else if (readAs === "ArrayBuffer") {
        reader.readAsArrayBuffer(file);
      }
    } catch (error) {
      cleanup();
      reject(error);
    }
  });
};

/**
 * Prettifies XML using XSLT transformation with error handling.
 */
const prettifyXmlSafely = (sourceXml: Document | Element): string => {
  if (!sourceXml) return "";

  try {
    let targetNode: Document | Element | undefined = sourceXml;

    // Handle jQuery nodes
    if (!targetNode?.nodeName) {
      try {
        const node = $(sourceXml).get(0);
        if (node && node.nodeType === Node.ELEMENT_NODE) {
          targetNode = node as Element;
        } else if (node && node.nodeType === Node.DOCUMENT_NODE) {
          targetNode = node as Document;
        } else {
          console.error(
            "Cannot extract HTML element from jQuery object: unexpected node type"
          );
          return "";
        }
      } catch (error) {
        console.error("Cannot extract HTML element from jQuery object:", error);
        return "";
      }
    }

    if (!targetNode) return "";

    const xsltStylesheet = [
      '<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">',
      '  <xsl:strip-space elements="*"/>',
      '  <xsl:template match="para[content-style][not(text())]">',
      '    <xsl:value-of select="normalize-space(.)"/>',
      "  </xsl:template>",
      '  <xsl:template match="node()|@*">',
      '    <xsl:copy><xsl:apply-templates select="node()|@*"/></xsl:copy>',
      "  </xsl:template>",
      '  <xsl:output indent="yes"/>',
      "</xsl:stylesheet>",
    ].join("\n");

    const xsltDoc = new DOMParser().parseFromString(
      xsltStylesheet,
      "application/xml"
    );
    const xsltProcessor = new XSLTProcessor();
    xsltProcessor.importStylesheet(xsltDoc);

    const resultDoc = xsltProcessor.transformToDocument(targetNode);
    return new XMLSerializer().serializeToString(resultDoc);
  } catch (error) {
    console.error("Error prettifying XML:", error);
    return "";
  }
};

// ============================================================================
// Exported Functions
// ============================================================================

/**
 * Retrieves items from a container that match the specified name.
 */
export const itemsForName = (
  name: string,
  container: any,
  multiple: boolean = true
): any[] => {
  if (!name || !container) return [];
  return findItemsRecursively(name, container, multiple);
};

/**
 * Extracts the value of an item, handling various data types.
 */
export const valueOfItem = extractValueRecursively;

/**
 * Determines the appropriate validation color based on field errors.
 */
export const validationColor = determineValidationColor;

/**
 * Reads file contents with proper error handling.
 */
export const readFilePromise = createFileReaderPromise;

/**
 * Prettifies XML with error handling.
 */
export const prettifyXml = prettifyXmlSafely;

/**
 * Custom hook for async effects with proper cleanup.
 */
export const useAsyncEffect = (
  effect: () => Promise<void>,
  dependencies: any[]
): void => {
  useEffect(() => {
    let cancelled = false;

    const executeEffect = async () => {
      try {
        if (!cancelled) {
          await effect();
        }
      } catch (error) {
        if (!cancelled) {
          console.error("Async effect error:", error);
        }
      }
    };

    executeEffect();

    return () => {
      cancelled = true;
    };
  }, dependencies);
};

// ============================================================================
// Custom Hooks
// ============================================================================

/**
 * Custom hook that returns the previous value of the given input.
 */
export const usePrevious = <T>(value: T): T | undefined => {
  const ref = useRef<T | undefined>(undefined);

  useEffect(() => {
    ref.current = value;
  }, [value]);

  return ref.current;
};

/**
 * Custom hook to fetch and manage project-related data.
 */
export const useProject = (projectId: number): ProjectData => {
  const api = useApi();

  const { data: project, mutate: mutateProject } = api.get_endpoint<Project>({
    type: "projects",
    id: projectId,
    endpoint: "",
  });

  const { data: directory, mutate: mutateDirectory } = api.get_endpoint<any>({
    type: "projects",
    id: projectId,
    endpoint: "directory",
  });

  const { data: jobs, mutate: mutateJobs } = api.get_endpoint<Job[]>({
    type: "projects",
    id: projectId,
    endpoint: "jobs",
  });

  const { data: files, mutate: mutateFiles } = api.get_endpoint<DjangoFile[]>({
    type: "projects",
    id: projectId,
    endpoint: "files",
  });

  const { data: jobFloatValues, mutate: mutateJobFloatValues } =
    api.get_endpoint<JobFloatValue[]>({
      type: "projects",
      id: projectId,
      endpoint: "job_float_values/",
    });

  const { data: jobCharValues, mutate: mutateJobCharValues } = api.get_endpoint<
    JobCharValue[]
  >({
    type: "projects",
    id: projectId,
    endpoint: "job_char_values/",
  });

  return {
    project,
    mutateProject,
    directory,
    mutateDirectory,
    jobs,
    mutateJobs,
    files,
    mutateFiles,
    jobCharValues,
    mutateJobCharValues,
    jobFloatValues,
    mutateJobFloatValues,
  };
};

// ============================================================================
// Parameter Setting Queue
// ============================================================================

interface QueuedParameterOperation {
  id: string;
  operation: () => Promise<SetParameterResponse | undefined>;
  resolve: (value: SetParameterResponse | undefined) => void;
  reject: (error: any) => void;
}

class ParameterQueue {
  private queue: QueuedParameterOperation[] = [];
  private isProcessing = false;

  async enqueue(
    operation: () => Promise<SetParameterResponse | undefined>
  ): Promise<SetParameterResponse | undefined> {
    return new Promise((resolve, reject) => {
      const queueItem: QueuedParameterOperation = {
        id: `param_${Date.now()}_${Math.random()}`,
        operation,
        resolve,
        reject,
      };

      this.queue.push(queueItem);
      this.processQueue();
    });
  }

  private async processQueue(): Promise<void> {
    if (this.isProcessing || this.queue.length === 0) {
      return;
    }

    this.isProcessing = true;

    while (this.queue.length > 0) {
      const item = this.queue.shift();
      if (!item) break;

      try {
        console.log(`Processing parameter operation ${item.id}`);
        const result = await item.operation();
        item.resolve(result);
      } catch (error) {
        console.error(`Error in parameter operation ${item.id}:`, error);
        item.reject(error);
      }
    }

    this.isProcessing = false;
  }

  getQueueLength(): number {
    return this.queue.length;
  }

  isQueueProcessing(): boolean {
    return this.isProcessing;
  }
}

// Global parameter queue instance
const parameterQueue = new ParameterQueue();

// ============================================================================
// Modified useJob Hook
// ============================================================================

export const useJob = (jobId: number | null | undefined): JobData => {
  const api = useApi();

  const { data: job, mutate: mutateJob } = api.get_endpoint<Job>(
    {
      type: "jobs",
      id: jobId,
      endpoint: "",
    },
    10000
  );

  const { data: container, mutate: mutateContainer } =
    api.get_wrapped_endpoint_json<any>({
      type: "jobs",
      id: jobId,
      endpoint: "container",
    });

  const { data: params_xml, mutate: mutateParams_xml } =
    api.get_pretty_endpoint_xml({
      type: "jobs",
      id: jobId,
      endpoint: "params_xml",
    });

  const { processedErrors, setProcessedErrors } = useRunCheck();

  // Get mutateValidation from useSWR
  const { data: validation, mutate: mutateValidation } = api.get_validation({
    type: "jobs",
    id: jobId,
    endpoint: "validation",
  });

  // Decorate mutateValidation so it always resets processed errors
  const mutateValidationWithProcessedErrors = useCallback(
    async (...args: any[]) => {
      setProcessedErrors(null);
      return mutateValidation(...args);
    },
    [mutateValidation, setProcessedErrors]
  );

  const { data: diagnostic_xml, mutate: mutateDiagnosticXml } =
    api.get_pretty_endpoint_xml({
      type: "jobs",
      id: jobId,
      endpoint: "diagnostic_xml",
    });

  const { data: def_xml, mutate: mutateDef_xml } = api.get_pretty_endpoint_xml({
    type: "jobs",
    id: jobId,
    endpoint: "def_xml",
  });

  const { mutateJobs } = useProject(job?.project || 0);
  const { setIntent, setIntentForPath, clearIntentForPath } = useParameterChangeIntent();

  // Memoized functions
  const setParameter = useCallback(
    async (
      setParameterArg: SetParameterArg
    ): Promise<SetParameterResponse | undefined> => {
      if (job?.status !== JOB_STATUS.PENDING) {
        console.warn(
          "Attempting to edit interface of task not in pending state"
        );
        return undefined;
      }

      const objectPath = setParameterArg.object_path;

      // Record intent BEFORE making the API call
      // This prevents the container refetch from overwriting local state
      // Get previous value from container lookup if available
      const previousValue = container?.lookup?.[objectPath]?._value;
      setIntentForPath({
        jobId: job.id,
        parameterPath: objectPath,
        reason: "UserEdit",
        previousValue,
      });

      // Enqueue the operation to ensure sequential execution
      return parameterQueue.enqueue(async () => {
        try {
          console.log(
            "Executing setParameter for:",
            objectPath
          );

          const result = await api.post<SetParameterResponse>(
            `jobs/${job.id}/set_parameter`,
            setParameterArg
          );
          setProcessedErrors(null);
          // Update all related data
          await Promise.all([
            mutateValidation(),
            mutateContainer(),
            mutateParams_xml(),
          ]);

          // Clear intent after successful update
          clearIntentForPath(objectPath);

          console.log("Parameter set successfully:", result);
          return result;
        } catch (error) {
          // Clear intent on error so future syncs work
          clearIntentForPath(objectPath);
          console.error("Error setting parameter:", error);
          throw error;
        }
      });
    },
    [
      job,
      container,
      mutateContainer,
      mutateValidation,
      mutateParams_xml,
      api,
      setProcessedErrors,
      setIntentForPath,
      clearIntentForPath,
    ]
  );

  const setParameterNoMutate = useCallback(
    async (
      setParameterArg: SetParameterArg
    ): Promise<SetParameterResponse | undefined> => {
      if (job?.status !== JOB_STATUS.PENDING) {
        console.warn(
          "Attempting to edit interface of task not in pending state"
        );
        return undefined;
      }

      const objectPath = setParameterArg.object_path;

      // Record intent even for no-mutate calls
      // This is important for derived updates (e.g., CImportUnmergedElement)
      // where multiple fields are updated before a single mutateContainer()
      const previousValue = container?.lookup?.[objectPath]?._value;
      setIntentForPath({
        jobId: job.id,
        parameterPath: objectPath,
        reason: "UserEdit",
        previousValue,
      });

      // Enqueue the operation to ensure sequential execution
      return parameterQueue.enqueue(async () => {
        try {
          console.log(
            "Executing setParameterNoMutate for:",
            objectPath
          );

          const result = await api.post<SetParameterResponse>(
            `jobs/${job.id}/set_parameter`,
            setParameterArg
          );

          // Note: We don't clear intent here because the caller will typically
          // call mutateContainer() later, and we want the intent to persist
          // until that refetch completes. The auto-cleanup will handle stale intents.

          return result;
        } catch (error) {
          // Clear intent on error
          clearIntentForPath(objectPath);
          console.error("Error setting parameter (no mutate):", error);
          throw error;
        }
      });
    },
    [job, container, mutateParams_xml, mutateValidation, api, setIntentForPath, clearIntentForPath]
  );

  /**
   * Upload a file to a CDataFile parameter with intent tracking.
   * This is the centralized function for all file uploads that should
   * integrate with the intent tracking mechanism.
   */
  const uploadFileParam = useCallback(
    async (
      uploadArg: UploadFileParamArg
    ): Promise<UploadFileParamResponse | undefined> => {
      if (job?.status !== JOB_STATUS.PENDING) {
        console.warn(
          "Attempting to upload file to task not in pending state"
        );
        return undefined;
      }

      const { objectPath, file, fileName, columnSelector } = uploadArg;

      // Record intent BEFORE making the API call
      // This prevents the container refetch from overwriting local state
      const previousValue = container?.lookup?.[objectPath]?._value;
      setIntentForPath({
        jobId: job.id,
        parameterPath: objectPath,
        reason: "FileUpload",
        previousValue,
      });

      // Enqueue the operation to ensure sequential execution
      return parameterQueue.enqueue(async () => {
        try {
          console.log("Executing uploadFileParam for:", objectPath);

          const formData = new FormData();
          formData.append("objectPath", objectPath);
          formData.append("file", file, fileName);
          if (columnSelector?.trim()) {
            formData.append("column_selector", columnSelector);
          }

          const result = await api.post<UploadFileParamResponse>(
            `jobs/${job.id}/upload_file_param`,
            formData
          );

          setProcessedErrors(null);

          // Update all related data
          await Promise.all([
            mutateValidation(),
            mutateContainer(),
            mutateParams_xml(),
          ]);

          // Invalidate the file digest cache for this objectPath
          // This triggers re-fetch of the digest, which task interfaces can use
          // to extract metadata like wavelength from the uploaded file
          const digestKey = `jobs/${job.id}/digest?object_path=${objectPath}/`;
          await mutate(digestKey);

          // Clear intent after successful update
          clearIntentForPath(objectPath);

          console.log("File uploaded successfully:", result);
          return result;
        } catch (error) {
          // Clear intent on error so future syncs work
          clearIntentForPath(objectPath);
          console.error("Error uploading file:", error);
          throw error;
        }
      }) as Promise<UploadFileParamResponse | undefined>;
    },
    [
      job,
      container,
      mutateContainer,
      mutateValidation,
      mutateParams_xml,
      api,
      setProcessedErrors,
      setIntentForPath,
      clearIntentForPath,
    ]
  );

  const useTaskItem = useMemo(() => {
    return (paramName: string): TaskItem => {
      if (!paramName?.length || !container?.lookup) {
        return {
          item: null,
          value: null,
          update: async () => false,
          updateNoMutate: async () => false,
        };
      }

      const item = container.lookup[paramName];
      const value = valueOfItem(item);

      const update = async (newValue: any): Promise<boolean | Response> => {
        if (!job || job.status !== JOB_STATUS.PENDING) return false;

        // Check if value actually changed
        if (JSON.stringify({ value }) === JSON.stringify({ value: newValue })) {
          return false;
        }

        // Note: Intent is now recorded inside setParameter, no need to call setIntent here

        // Use the queued setParameter instead of direct fetch
        try {
          const result = await setParameter({
            object_path: item._objectPath,
            value: newValue,
          });

          return result?.success ? true : false;
        } catch (error) {
          console.error("Error updating task item:", error);
          return false;
        }
      };

      const updateNoMutate = async (
        newValue: any
      ): Promise<boolean | Response> => {
        if (!job || job.status !== JOB_STATUS.PENDING) return false;

        // Check if value actually changed
        if (JSON.stringify({ value }) === JSON.stringify({ value: newValue })) {
          return false;
        }

        // Use the queued setParameter instead of direct fetch
        try {
          const result = await setParameterNoMutate({
            object_path: item._objectPath,
            value: newValue,
          });

          return result?.success ? true : false;
        } catch (error) {
          console.error("Error updating task item:", error);
          return false;
        }
      };

      return { item, value, update, updateNoMutate };
    };
  }, [container, job, setParameter]);

  const createPeerTask = useCallback(
    async (taskName: string): Promise<Job | undefined> => {
      if (!job || !mutateJobs) {
        console.warn("Cannot create peer task: missing job or mutateJobs");
        return undefined;
      }

      try {
        console.log(`Creating ${taskName} task...`);

        const result = await api.post<CreateTaskResponse>(
          `projects/${job.project}/create_task/`,
          {
            task_name: taskName,
          }
        );

        if (result?.success && result.data?.new_job) {
          const createdJob: Job = result.data.new_job;
          await mutateJobs();
          return createdJob;
        }

        console.warn("Failed to create peer task:", result);
        return undefined;
      } catch (error) {
        console.error("Error creating peer task:", error);
        return undefined;
      }
    },
    [job, api, mutateJobs]
  );

  const getFileDigest = useMemo(() => {
    return (paramName: string): Promise<any | undefined> => {
      const dbFileId = container?.lookup?.[paramName]?.dbFileId;
      if (!dbFileId) {
        console.warn(`Parameter ${paramName} not found in container`);
        return Promise.resolve(null);
      }
      return apiJson(`files/${dbFileId}/digest_by_uuid`).catch((error) => {
        console.error(`Error fetching file digest for ${paramName}:`, error);
        return null;
      });
    };
  }, [container]);

  // Custom hook to fetch file content using SWR
  const useFileContent = (paramName: string): SWRResponse<string, Error> => {
    // Create a unique key for SWR caching
    const item = container?.lookup[paramName];
    const dbFileId = valueOfItem(item)?.dbFileId;

    //console.log("dbFileId", JSON.stringify(dbFileId));
    // Return null key when dbFileId is falsey - this prevents SWR from fetching
    const swrKey = dbFileId ? `files/${dbFileId}/download_by_uuid` : null;

    const fetcher = async (): Promise<string> => {
      if (!swrKey) {
        throw new Error(
          `Parameter "${paramName}" not found or has no dbFileId`
        );
      }
      return apiText(swrKey);
    };

    return useSWR<string, Error>(swrKey, swrKey ? fetcher : null, {
      // SWR options
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      errorRetryCount: 3,
      errorRetryInterval: 1000,
      // Cache for 5 minutes
      dedupingInterval: 5 * 60 * 1000,
      onError: (error) => {
        console.warn(
          `Error fetching file content for parameter "${paramName}":`,
          error
        );
        // Clear the cache for this key
        mutate(swrKey, null, false); // false = don't revalidate
      },
    });
  };

  // Custom hook to fetch file digest using SWR
  // Note: objectPath should be the full path like "prosmart_refmac.inputData.F_SIGF"
  const useFileDigest = (objectPath: string): SWRResponse<any, Error> => {
    // Create a unique key for SWR caching
    const swrKey = objectPath
      ? `jobs/${job?.id}/digest?object_path=${objectPath}`
      : null;
    const fetcher = async (): Promise<string> => {
      if (!swrKey) {
        throw new Error("Parameter not found");
      }
      return apiJson(swrKey);
    };

    return useSWR<string, Error>(swrKey, swrKey ? fetcher : null, {
      // SWR options
      revalidateOnFocus: false,
      revalidateOnReconnect: true,
      errorRetryCount: 3,
      errorRetryInterval: 1000,
      // Cache for 5 minutes
      dedupingInterval: 5 * 60 * 1000,
      onError: () => {
        // Clear the cache for this key
        mutate(swrKey, null, false); // false = don't revalidate
      },
    });
  };

  const getValidationColor = useMemo(() => {
    return (item: any): string => {
      const fieldErrors = extractValidationErrors(
        item,
        processedErrors || validation || {}
      );
      return determineValidationColor(fieldErrors);
    };
  }, [processedErrors, validation]);

  const getErrors = useMemo(() => {
    return (item: any): ValidationError[] => {
      return extractValidationErrors(item, processedErrors || validation || {});
    };
  }, [processedErrors, validation]);

  const fileItemToParameterArg = useCallback(
    (
      value: DjangoFile,
      objectPath: string,
      projectJobs: Job[],
      projects: Project[]
    ): SetParameterArg => {
      // Base parameter structure
      const setParameterArg: SetParameterArg = {
        object_path: objectPath,
        value: {
          dbFileId: value.uuid.replace(/-/g, ""),
          subType: value.sub_type,
          contentFlag: value.content,
          annotation: value.annotation,
          baseName: value.name,
        },
      };

      // Handle different file directory types
      const handleFileDirectory = () => {
        if (value.directory === FILE_DIRECTORIES.IMPORTED) {
          setParameterArg.value.relPath = FILE_PATHS.IMPORTED_FILES;
        } else if (value.directory === FILE_DIRECTORIES.JOB_OUTPUT) {
          const jobOfFile = projectJobs?.find(
            (theJob) => theJob.id === value.job
          );
          if (jobOfFile) {
            const jobDir = jobOfFile.number
              .split(".")
              .map((element) => `${FILE_PATHS.JOB_PREFIX}${element}`)
              .join("/");

            setParameterArg.value.relPath = `${FILE_PATHS.JOBS_DIR}/${jobDir}`;
          }
        }

        // Set project for both directory types (moved outside the if/else)
        const jobOfFile = projectJobs?.find(
          (theJob) => theJob.id === value.job
        );
        if (jobOfFile) {
          const project = projects?.find(
            (theProject) => theProject.id === jobOfFile.project
          );
          if (project) {
            setParameterArg.value.project = project.uuid.replace(/-/g, "");
          }
        }
      };

      // Apply directory-specific handling only if job context exists
      if (job && projectJobs) {
        handleFileDirectory();
      }

      return setParameterArg;
    },
    [job]
  );

  return {
    job,
    mutateJob,
    container,
    mutateContainer,
    params_xml,
    mutateParams_xml,
    validation,
    mutateValidation: mutateValidationWithProcessedErrors, // use the decorated version
    diagnostic_xml,
    mutateDiagnosticXml,
    def_xml,
    mutateDef_xml,
    setParameter,
    setParameterNoMutate,
    uploadFileParam,
    useTaskItem,
    createPeerTask,
    useFileContent,
    getValidationColor,
    getErrors,
    useFileDigest,
    getFileDigest,
    fileItemToParameterArg,
  };
};

// ============================================================================
// Digest Effect Hooks - Simplified patterns for reacting to file digest changes
// ============================================================================

/**
 * Options for useDigestEffect hook
 */
export interface UseDigestEffectOptions<T> {
  /**
   * Only run the effect when job is in pending status (status === 1).
   * Default: true
   *
   * Set to false if you need to react to digest changes regardless of job status.
   */
  onlyWhenPending?: boolean;

  /**
   * Custom equality function to determine if the extracted value has changed.
   * Default: JSON.stringify comparison
   *
   * @example
   * // Custom comparison for floating point tolerance
   * isEqual: (a, b) => Math.abs(a - b) < 0.001
   */
  isEqual?: (prev: T | null, next: T) => boolean;

  /**
   * Enable debug logging to console.
   * Default: false
   */
  debug?: boolean;

  /**
   * Label for debug logging (helps identify which effect is logging).
   */
  debugLabel?: string;
}

/**
 * Hook to react to file digest changes with automatic duplicate prevention.
 *
 * This hook simplifies the common pattern of:
 * 1. Watching a file digest for changes
 * 2. Extracting a value from the digest
 * 3. Calling an update function only when the value actually changes
 * 4. Preventing duplicate updates (e.g., from React strict mode or re-renders)
 *
 * The hook handles all the boilerplate including:
 * - Unwrapping the API response format ({success: true, data: {...}})
 * - Tracking previously set values via useRef
 * - Checking job status (only updates pending jobs by default)
 * - Null/undefined safety throughout
 *
 * @param digest - The SWR response from useFileDigest (or similar)
 * @param extract - Function to extract the desired value from digest data.
 *                  Return undefined/null to skip the update.
 * @param update - Function to call when the extracted value changes.
 *                 This is typically from useTaskItem("PARAM").update
 * @param jobStatus - Current job status (from job.status or props.job.status)
 * @param options - Optional configuration (see UseDigestEffectOptions)
 *
 * @example
 * // Basic usage: Extract wavelength from MTZ file digest
 * const { data: F_SIGFDigest } = useFileDigest(F_SIGFItem?._objectPath);
 * const { update: updateWAVELENGTH } = useTaskItem("WAVELENGTH");
 *
 * useDigestEffect(
 *   F_SIGFDigest,
 *   (digestData) => {
 *     const wavelength = digestData.wavelengths?.at(-1);
 *     // Return undefined to skip update if value is invalid
 *     if (!wavelength || wavelength <= 0 || wavelength >= 9) return undefined;
 *     return wavelength;
 *   },
 *   updateWAVELENGTH,
 *   job?.status
 * );
 *
 * @example
 * // With validation and debug logging
 * useDigestEffect(
 *   SEQINDigest,
 *   (digestData) => {
 *     if (!digestData.sequence) return undefined;
 *     return `>${digestData.identifier || ""}\n${digestData.sequence}`;
 *   },
 *   setSEQUENCETEXT,
 *   job?.status,
 *   { debug: true, debugLabel: "ProvideSequence" }
 * );
 *
 * @example
 * // Extract cell parameters (object value)
 * useDigestEffect(
 *   HKLINDigest,
 *   (digestData) => digestData.cell,
 *   updateCell,
 *   job?.status
 * );
 */
export function useDigestEffect<T>(
  digest: SWRResponse<any, Error> | { data?: any } | null | undefined,
  extract: (digestData: any) => T | undefined | null,
  update: ((value: T) => unknown) | undefined | null,
  jobStatus: number | undefined,
  options: UseDigestEffectOptions<T> = {}
): void {
  const {
    onlyWhenPending = true,
    isEqual = (a, b) => JSON.stringify(a) === JSON.stringify(b),
    debug = false,
    debugLabel = "useDigestEffect",
  } = options;

  // Track the last value we set to prevent duplicate updates
  const lastSetValueRef = useRef<T | null>(null);

  useEffect(() => {
    // Guard: need update function
    if (!update) {
      if (debug) console.log(`[${debugLabel}] Skipping: no update function`);
      return;
    }

    // Guard: check job status if required
    if (onlyWhenPending && jobStatus !== 1) {
      if (debug)
        console.log(
          `[${debugLabel}] Skipping: job status is ${jobStatus}, not pending (1)`
        );
      return;
    }

    // Unwrap API response format: {success: true, data: {...}}
    const digestData = digest?.data?.data ?? digest?.data;
    if (!digestData) {
      if (debug) console.log(`[${debugLabel}] Skipping: no digest data`);
      return;
    }

    // Extract the value using the provided function
    const extractedValue = extract(digestData);

    // Guard: extraction returned null/undefined (indicates skip)
    if (extractedValue === undefined || extractedValue === null) {
      if (debug)
        console.log(`[${debugLabel}] Skipping: extract returned null/undefined`);
      return;
    }

    // Guard: value hasn't changed (prevent duplicate updates)
    if (
      lastSetValueRef.current !== null &&
      isEqual(lastSetValueRef.current, extractedValue)
    ) {
      if (debug)
        console.log(`[${debugLabel}] Skipping: value unchanged`, extractedValue);
      return;
    }

    // Update!
    if (debug)
      console.log(`[${debugLabel}] Updating with value:`, extractedValue);
    lastSetValueRef.current = extractedValue;
    update(extractedValue);
  }, [digest, update, jobStatus, extract, onlyWhenPending, isEqual, debug, debugLabel]);
}

/**
 * Convenience hook for the common pattern of extracting a single field from digest.
 *
 * This is a simplified version of useDigestEffect for the most common case:
 * extracting a single field by path and optionally validating it.
 *
 * @param digest - The SWR response from useFileDigest
 * @param fieldPath - Dot-separated path to the field (e.g., "wavelengths.-1" for last item)
 * @param update - Update function from useTaskItem
 * @param jobStatus - Current job status
 * @param validate - Optional validation function. Return false to skip update.
 *
 * @example
 * // Extract last wavelength with validation
 * useDigestField(
 *   F_SIGFDigest,
 *   "wavelengths.-1",  // -1 means last element
 *   updateWAVELENGTH,
 *   job?.status,
 *   (w) => w > 0 && w < 9  // validation
 * );
 *
 * @example
 * // Extract cell parameters (no validation needed)
 * useDigestField(HKLINDigest, "cell", updateCell, job?.status);
 */
export function useDigestField<T>(
  digest: SWRResponse<any, Error> | { data?: any } | null | undefined,
  fieldPath: string,
  update: ((value: T) => void | Promise<void>) | undefined | null,
  jobStatus: number | undefined,
  validate?: (value: T) => boolean
): void {
  const extract = useCallback(
    (digestData: any): T | undefined => {
      // Navigate the field path
      const parts = fieldPath.split(".");
      let value: any = digestData;

      for (const part of parts) {
        if (value === null || value === undefined) return undefined;

        // Handle negative indices for arrays (e.g., -1 for last element)
        if (Array.isArray(value) && /^-?\d+$/.test(part)) {
          const index = parseInt(part, 10);
          value = index < 0 ? value.at(index) : value[index];
        } else {
          value = value[part];
        }
      }

      // Apply validation if provided
      if (value !== undefined && value !== null && validate) {
        return validate(value) ? value : undefined;
      }

      return value;
    },
    [fieldPath, validate]
  );

  useDigestEffect(digest, extract, update, jobStatus);
}

// ============================================================================
// Optional: Queue Status Hooks
// ============================================================================

/**
 * Hook to monitor parameter queue status
 */
export const useParameterQueueStatus = () => {
  const [queueLength, setQueueLength] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setQueueLength(parameterQueue.getQueueLength());
      setIsProcessing(parameterQueue.isQueueProcessing());
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return { queueLength, isProcessing };
};
