import { create } from "zustand";

interface FilterState {
  showFilterModal: boolean;
  toggleFilterModal: () => void;

  filterSources: string[];
  setFilterSources: (sources: string[]) => void;

  filterGroupTypes: string[];
  setFilterGroupTypes: (groupTypes: string[]) => void;
}

export const useFilter = create<FilterState>((set) => ({
  showFilterModal: false,
  toggleFilterModal: () =>
    set((state) => ({
      showFilterModal: !state.showFilterModal,
    })),

  filterSources: [],
  setFilterSources: (sources: string[]) =>
    set(() => ({
      filterSources: sources,
    })),

  filterGroupTypes: [],
  setFilterGroupTypes: (groupTypes: string[]) =>
    set(() => ({
      filterGroupTypes: groupTypes,
    })),
}));
