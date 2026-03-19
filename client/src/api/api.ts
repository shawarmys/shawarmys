import { apiClient } from "./apiClient";

// *** Metadata ***

export interface apiMetadata {
  importedFiles: number;
  successfulMappings: number;
  mappingAlerts: number;
}

export const getMetadata = async () => {
  const response = await apiClient.get("/metadata/");
  return response.data as apiMetadata;
};

// *** Imported Files ***

export interface apiImportedFile {
  name: string;
  source: string;
  entries: number;
  records: number; // values per entry
  type: "csv" | "pdf" | "xslx";
}

export const getImportedFiles = async () => {
  const response = await apiClient.get("/imported-files/");
  return response.data as apiImportedFile[];
};
