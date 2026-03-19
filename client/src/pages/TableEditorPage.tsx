import {
  Alert,
  Button,
  Link,
  Paper,
  Table,
  TableBody,
  TableContainer,
  TableHead,
} from "@mui/material";
import React from "react";
import { apiClient } from "../api/apiClient";
import PageTemplate from "../components/PageTemplate";
import TableEditorRow from "../components/TableEditorRow";
import { useTableData } from "../hooks/useTableData";

const TableEditorPage: React.FC = () => {
  const {
    setTableDataEntry,
    tableData,
    editModeTableData,
    setEditModeTableDataEntry,
    errors,
    unsetError,
    setErrors,
    outliers,
    unsetOutlier,
    setOutliers,
    fileName,
  } = useTableData();

  //!--[
  //! Mock data until we implement file upload and parsing
  React.useEffect(() => {
    const a = ["a", "b", "c", "d", "e", "f", "g", "h"];
    a.concat(a)
      .concat(a)
      .concat(a)
      .forEach((_, rowIdx) => {
        for (let cellIdx = 0; cellIdx < 100; cellIdx++) {
          setTableDataEntry(rowIdx, cellIdx, `R${rowIdx + 1}C${cellIdx + 1}`);
        }
      });
    setErrors([
      { row: 5, col: 5, msg: "This is a mock error message." },
      { row: 10, col: 10, msg: "This is a mock error message." },
      { row: 15, col: 15, msg: "This is a mock error message." },
    ]);
    setOutliers([
      { row: 6, col: 5, msg: "This is a mock error message." },
      { row: 11, col: 10, msg: "This is a mock error message." },
      { row: 13, col: 15, msg: "This is a mock error message." },
    ]);
  }, [setTableDataEntry]);
  //!--]

  const [editingValues, setEditingValues] = React.useState<
    Record<string, string>
  >({});

  const getCellKey = React.useCallback((row: number, col: number) => {
    return `${row}:${col}`;
  }, []);

  const startEditingCell = (row: number, col: number, initialValue: string) => {
    const cellKey = getCellKey(row, col);
    setEditingValues((previous) => ({ ...previous, [cellKey]: initialValue }));
    setEditModeTableDataEntry(row, col, true);
  };

  const saveCellValue = (row: number, col: number) => {
    const cellKey = getCellKey(row, col);
    setTableDataEntry(row, col, editingValues[cellKey] ?? "");
    setEditModeTableDataEntry(row, col, false);
  };

  const cancelCellEditing = (row: number, col: number) => {
    const cellKey = getCellKey(row, col);
    setEditingValues((previous) => {
      const next = { ...previous };
      delete next[cellKey];
      return next;
    });
    setEditModeTableDataEntry(row, col, false);
  };

  const [isUploading, setIsUploading] = React.useState(false);
  const uploadTableData = async () => {
    try {
      setIsUploading(true);
      const body = {
        tableData,
        fileName: fileName,
      };
      await apiClient.post("/upload/array", {
        body,
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <PageTemplate
      title="Table Editor"
      wide={true}
      topRightAction={
        <>
          {outliers.length > 0 && (
            <Alert severity="warning">
              {outliers.length} potential outlier
              {outliers.length > 1 ? "s" : ""} found.
              <Link
                sx={{ cursor: "pointer", ml: 1 }}
                onClick={() =>
                  document
                    .getElementById(
                      `cell-${outliers[0].row}-${outliers[0].col}`,
                    )
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Show me
              </Link>
            </Alert>
          )}
          {errors.length > 0 && (
            <Alert severity="error">
              {errors.length} error{errors.length > 1 ? "s" : ""} remaining.
              <Link
                sx={{ cursor: "pointer", ml: 1 }}
                onClick={() =>
                  document
                    .getElementById(`cell-${errors[0].row}-${errors[0].col}`)
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Show me
              </Link>
            </Alert>
          )}
          <Button
            variant="contained"
            disabled={errors.length > 0}
            loading={isUploading}
            onClick={uploadTableData}
          >
            Save Table
          </Button>
        </>
      }
    >
      <TableContainer component={Paper}>
        <Table
          sx={{
            width: "100%",
            overflow: "auto",
            maxHeight: "80vh",
            display: "block",
          }}
          aria-label="simple table"
          stickyHeader
        >
          <TableHead
            sx={{ fontWeight: "bold", backgroundColor: "background.default" }}
          >
            {tableData?.slice(0, 1).map((row, rowIdx) => {
              return (
                <TableEditorRow
                  row={row}
                  rowIdx={rowIdx}
                  errors={errors}
                  outliers={outliers}
                  editModeRow={editModeTableData?.[rowIdx]}
                  editingValues={editingValues}
                  getCellKey={getCellKey}
                  setEditingValues={setEditingValues}
                  startEditingCell={startEditingCell}
                  saveCellValue={saveCellValue}
                  cancelCellEditing={cancelCellEditing}
                  unsetError={unsetError}
                  unsetOutlier={unsetOutlier}
                  tableCellSx={{ fontWeight: "bold" }}
                />
              );
            })}
          </TableHead>
          <TableBody>
            {tableData?.slice(1).map((row, rowIdx) => {
              return (
                <TableEditorRow
                  row={row}
                  rowIdx={rowIdx + 1}
                  errors={errors}
                  outliers={outliers}
                  editModeRow={editModeTableData?.[rowIdx + 1]}
                  editingValues={editingValues}
                  getCellKey={getCellKey}
                  setEditingValues={setEditingValues}
                  startEditingCell={startEditingCell}
                  saveCellValue={saveCellValue}
                  cancelCellEditing={cancelCellEditing}
                  unsetError={unsetError}
                  unsetOutlier={unsetOutlier}
                />
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </PageTemplate>
  );
};

export default TableEditorPage;
