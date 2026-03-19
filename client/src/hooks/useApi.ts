import useSWR from "swr";
import { getImportedFiles, getMetadata } from "../api/api";

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
