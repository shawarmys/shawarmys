import { create } from "zustand";

export interface TableDataError {
  row: number;
  col: number;
  msg: string;
}

interface TableDataState {
  tableData: string[][];
  setTableData: (data: string[][]) => void;
  setTableDataEntry: (row: number, col: number, value: string) => void;

  errors: TableDataError[];
  setErrors: (errors: TableDataError[]) => void;
  unsetError: (row: number, col: number) => void;

  outliers: TableDataError[];
  setOutliers: (outliers: TableDataError[]) => void;
  unsetOutlier: (row: number, col: number) => void;

  editModeTableData: boolean[][];
  setEditModeTableDataEntry: (row: number, col: number, value: boolean) => void;

  fileName: string;
  setFileName: (name: string) => void;
}

export const useTableData = create<TableDataState>((set) => ({
  tableData: [],
  setTableData: (data: string[][]) => {
    set(() => ({
      tableData: data,
    }));

    // Initialize edit mode data with false
    set(() => ({
      editModeTableData: data.map((row) => row.map(() => false)),
    }));
  },
  setTableDataEntry: (row: number, col: number, value: string) =>
    set((state) => {
      const newData = [...state.tableData];
      if (!newData[row]) {
        newData[row] = [];
      }
      newData[row][col] = value;
      return { tableData: newData };
    }),

  errors: [],
  setErrors: (errors: TableDataError[]) => set(() => ({ errors })),
  unsetError: (row: number, col: number) =>
    set((state) => {
      const newErrors = state.errors.filter(
        (error) => !(error.row === row && error.col === col),
      );
      return { errors: newErrors };
    }),

  outliers: [],
  setOutliers: (outliers: TableDataError[]) => set(() => ({ outliers })),
  unsetOutlier: (row: number, col: number) =>
    set((state) => {
      const newOutliers = state.outliers.filter(
        (outlier) => !(outlier.row === row && outlier.col === col),
      );
      return { outliers: newOutliers };
    }),

  editModeTableData: [],
  setEditModeTableDataEntry: (row: number, col: number, value: boolean) =>
    set((state) => {
      const newEditModeData = [...state.editModeTableData];
      if (!newEditModeData[row]) {
        newEditModeData[row] = [];
      }
      newEditModeData[row][col] = value;
      return { editModeTableData: newEditModeData };
    }),

  fileName: "",
  setFileName: (name: string) => set(() => ({ fileName: name })),
}));
