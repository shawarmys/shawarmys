import useSWR from "swr";
import { getMetadata } from "../api/metadata";

export function useMetadata() {
  const { data, error, isLoading, mutate } = useSWR("/metadata", async () =>
    getMetadata(),
  );

  return {
    metadata: data,
    isLoading,
    isError: error,
    mutate,
  };
}
