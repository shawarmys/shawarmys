import useSWR from "swr";
import {
  getAlerts,
  getDataGroupsSummary,
  getDataSourcesSummary,
  getImportedFiles,
  getMetadata,
} from "../api/api";

// *** Metadata ***

export function useMetadata(
  filterSources: string[],
  filterGroupTypes: string[],
) {
  const { data, error, isLoading, mutate } = useSWR(
    `/metadata:${filterSources.join(",")}:${filterGroupTypes.join(",")}`,
    async () => getMetadata(filterSources, filterGroupTypes),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Imported Files ***

export function useImportedFiles(
  filterSources: string[],
  filterGroupTypes: string[],
) {
  const { data, error, isLoading, mutate } = useSWR(
    `/imported-files:${filterSources.join(",")}:${filterGroupTypes.join(",")}`,
    async () => getImportedFiles(filterSources, filterGroupTypes),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Data Source Summary ***

export function useDataSourcesSummary(
  filterSources: string[],
  filterGroupTypes: string[],
) {
  const { data, error, isLoading, mutate } = useSWR(
    `/data-sources-summary:${filterSources.join(",")}:${filterGroupTypes.join(",")}`,
    async () => getDataSourcesSummary(filterSources, filterGroupTypes),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Data Groups Summary ***

export function useDataGroupsSummary(
  filterSources: string[],
  filterGroupTypes: string[],
) {
  const { data, error, isLoading, mutate } = useSWR(
    `/data-groups-summary:${filterSources.join(",")}:${filterGroupTypes.join(",")}`,
    async () => getDataGroupsSummary(filterSources, filterGroupTypes),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Alerts ***
export function useAlerts(filterSources: string[], filterGroupTypes: string[]) {
  const { data, error, isLoading, mutate } = useSWR(
    `/alerts:${filterSources.join(",")}:${filterGroupTypes.join(",")}`,
    async () => getAlerts(filterSources, filterGroupTypes),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}
