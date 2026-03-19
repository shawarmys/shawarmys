import { apiClient } from "./apiClient";

// *** Metadata ***

export interface apiMetadata {
  importedFiles: number;
  successfulMappings: number;
  mappingAlerts: number;
}

export const getMetadata = async (
  filterSources: string[],
  filterGroupTypes: string[],
) => {
  const params = new URLSearchParams();
  if (filterSources.length > 0)
    params.append("sources", filterSources.join(","));

  if (filterGroupTypes.length > 0)
    params.append("groupTypes", filterGroupTypes.join(","));

  const response = await apiClient.get(`/metadata?${params.toString()}`);
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

export const getImportedFiles = async (
  filterSources: string[],
  filterGroupTypes: string[],
) => {
  const params = new URLSearchParams();
  if (filterSources.length > 0)
    params.append("sources", filterSources.join(","));

  if (filterGroupTypes.length > 0)
    params.append("groupTypes", filterGroupTypes.join(","));

  const response = await apiClient.get(`/imported-files?${params.toString()}`);
  return response.data as apiImportedFile[];
};

// *** Data Source Summary ***

export interface apiDataSourceSummary {
  name: string;
  numFiles: number;
}

export const getDataSourcesSummary = async (
  filterSources: string[],
  filterGroupTypes: string[],
) => {
  const params = new URLSearchParams();
  if (filterSources.length > 0)
    params.append("sources", filterSources.join(","));

  if (filterGroupTypes.length > 0)
    params.append("groupTypes", filterGroupTypes.join(","));

  const response = await apiClient.get(
    `/data-sources-summary?${params.toString()}`,
  );
  return response.data as apiDataSourceSummary[];
};

// *** Data Groups Summary ***

export interface apiDataGroupSummary {
  groupType: string;
  numFiles: number;
}

export const getDataGroupsSummary = async (
  filterSources: string[],
  filterGroupTypes: string[],
) => {
  const params = new URLSearchParams();
  if (filterSources.length > 0)
    params.append("sources", filterSources.join(","));

  if (filterGroupTypes.length > 0)
    params.append("groupTypes", filterGroupTypes.join(","));

  const response = await apiClient.get(
    `/data-groups-summary?${params.toString()}`,
  );
  return response.data as apiDataGroupSummary[];
};

// *** Alerts ***
export interface apiAlert {
  timestamp: string; // "YYYY-MM-DD HH:mm:ss"
  level: "info" | "warning" | "severe";
  message: string;
  tableReference: string; // Backend reference to edit the corresponding tuple
}

export const getAlerts = async (
  filterSources: string[],
  filterGroupTypes: string[],
) => {
  const params = new URLSearchParams();
  if (filterSources.length > 0)
    params.append("sources", filterSources.join(","));

  if (filterGroupTypes.length > 0)
    params.append("groupTypes", filterGroupTypes.join(","));

  const response = await apiClient.get(`/alerts?${params.toString()}`);
  return response.data as apiAlert[];
};
