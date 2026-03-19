import { apiClient } from "./apiClient";

export const getMetadata = async () => {
  await apiClient.get("/metadata/");
};
