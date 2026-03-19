import { useIsLoading } from "../hooks/isLoading";
import { type NavigateFunction } from "react-router-dom";

export const navigate = (path: string, navigateFn: NavigateFunction) => {
  useIsLoading.getState().setIsLoading(true);

  navigateFn(path);
};