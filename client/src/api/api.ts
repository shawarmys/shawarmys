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
  //!--[ Mock
  return [
    {
      timestamp: "2024-08-02 09:15:00",
      level: "info",
      message:
        "Failed to parse date in 'date_of_birth' column for entry ID 789.",
      tableReference: "data-groups/456/entries/789",
    },
    {
      timestamp: "2024-08-01 14:30:00",
      level: "warning",
      message: "Missing value in 'age' column for entry ID 123.",
      tableReference: "data-groups/456/entries/123",
    },
    {
      timestamp: "2024-08-02 09:15:00",
      level: "severe",
      message:
        "Failed to parse date in 'date_of_birth' column for entry ID 789.",
      tableReference: "data-groups/456/entries/789",
    },
  ] as apiAlert[];
  //!--]
  const params = new URLSearchParams();
  if (filterSources.length > 0)
    params.append("sources", filterSources.join(","));

  if (filterGroupTypes.length > 0)
    params.append("groupTypes", filterGroupTypes.join(","));

  const response = await apiClient.get(`/alerts?${params.toString()}`);
  return response.data as apiAlert[];
};
