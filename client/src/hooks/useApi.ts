import useSWR from "swr";
import {
  getDataGroupsSummary,
  getDataSourcesSummary,
  getImportedFiles,
  getMetadata,
} from "../api/api";

// *** Metadata ***

export function useMetadata() {
  const { data, error, isLoading, mutate } = useSWR("/metadata", async () =>
    getMetadata(),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Imported Files ***

export function useImportedFiles() {
  const { data, error, isLoading, mutate } = useSWR(
    "/imported-files",
    async () => getImportedFiles(),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Data Source Summary ***

export function useDataSourcesSummary() {
  const { data, error, isLoading, mutate } = useSWR(
    "/data-sources-summary",
    async () => getDataSourcesSummary(),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}

// *** Data Groups Summary ***

export function useDataGroupsSummary() {
  const { data, error, isLoading, mutate } = useSWR(
    "/data-groups-summary",
    async () => getDataGroupsSummary(),
  );

  return {
    data,
    isLoading,
    isError: error,
    mutate,
  };
}
