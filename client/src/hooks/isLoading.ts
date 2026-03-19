import { create } from "zustand";

interface IsLoadingStore {
  isLoading: boolean;
  setIsLoading: (loading: boolean) => void;
}

export const useIsLoading = create<IsLoadingStore>((set) => ({
  isLoading: false,
  setIsLoading: (loading) => set({ isLoading: loading }),
}));
