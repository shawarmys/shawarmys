import CloseIcon from "@mui/icons-material/Close";
import SaveIcon from "@mui/icons-material/Save";
import {
  Alert,
  Button,
  IconButton,
  InputAdornment,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Tooltip,
} from "@mui/material";
import React from "react";
import PageTemplate from "../components/PageTemplate";
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
    setErrors([{ row: 5, col: 5, msg: "This is a mock error message." }]);
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

  return (
    <PageTemplate
      title="Table Editor"
      wide={true}
      topRightAction={
        <>
          {errors.length > 0 && (
            <Alert severity="error">
              {errors.length} error{errors.length > 1 ? "s" : ""} remaining.
              <Link
                sx={{ cursor: "pointer", ml: 1 }}
                onClick={() =>
                  document
                    .getElementById(
                      `error-cell-${errors[0].row}-${errors[0].col}`,
                    )
                    ?.scrollIntoView({ behavior: "smooth" })
                }
              >
                Show me
              </Link>
            </Alert>
          )}
          <Button variant="contained" disabled={errors.length > 0}>
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
        >
          <TableHead></TableHead>
          <TableBody>
            {tableData?.map((row, rowIdx) => {
              return (
                <TableRow
                  key={rowIdx}
                  sx={{
                    "&:last-child td, &:last-child th": { border: 0 },
                    backgroundColor:
                      rowIdx % 2 === 1 ? "action.hover" : "background.paper",
                  }}
                >
                  {row?.map((cell, cellIdx) => (
                    <Tooltip
                      title={
                        errors.find(
                          (error) =>
                            error.row === rowIdx && error.col === cellIdx,
                        )?.msg || ""
                      }
                      placement="top"
                      arrow
                      slotProps={{
                        tooltip: {
                          sx: {
                            bgcolor: "error.main",
                            color: "common.white",
                          },
                        },
                        arrow: {
                          sx: {
                            color: "error.main",
                          },
                        },
                      }}
                    >
                      <TableCell
                        id={`error-cell-${rowIdx}-${cellIdx}`}
                        scope="row"
                        key={cellIdx}
                        sx={{
                          position: "relative",
                          overflow: "visible",
                          backgroundColor: errors.some(
                            (error) =>
                              error.row === rowIdx && error.col === cellIdx,
                          )
                            ? "error.light"
                            : undefined,
                        }}
                        // Show error message as tooltip on hover if this cell has an error
                        title={
                          errors.find(
                            (error) =>
                              error.row === rowIdx && error.col === cellIdx,
                          )?.msg
                        }
                      >
                        {editModeTableData?.[rowIdx]?.[cellIdx] ? (
                          <TextField
                            id="outlined-size-small"
                            value={
                              editingValues[getCellKey(rowIdx, cellIdx)] ?? cell
                            }
                            onChange={(event) => {
                              const cellKey = getCellKey(rowIdx, cellIdx);
                              setEditingValues((previous) => ({
                                ...previous,
                                [cellKey]: event.target.value,
                              }));
                            }}
                            size="small"
                            sx={{
                              width: 240,
                              position: "absolute",
                              left: 0,
                              top: "50%",
                              transform: "translateY(-50%)",
                              zIndex: 10,
                              bgcolor: "background.paper",
                              boxShadow: 2,
                            }}
                            InputProps={{
                              endAdornment: (
                                <InputAdornment position="end">
                                  <IconButton
                                    size="small"
                                    aria-label="save cell"
                                    onClick={() => {
                                      saveCellValue(rowIdx, cellIdx);
                                      unsetError(rowIdx, cellIdx);
                                    }}
                                  >
                                    <SaveIcon fontSize="small" />
                                  </IconButton>
                                  <IconButton
                                    size="small"
                                    aria-label="cancel editing"
                                    onClick={() =>
                                      cancelCellEditing(rowIdx, cellIdx)
                                    }
                                  >
                                    <CloseIcon fontSize="small" />
                                  </IconButton>
                                </InputAdornment>
                              ),
                            }}
                          />
                        ) : (
                          <span
                            style={{ cursor: "pointer" }}
                            onClick={() =>
                              startEditingCell(rowIdx, cellIdx, cell)
                            }
                          >
                            {cell}
                          </span>
                        )}
                      </TableCell>
                    </Tooltip>
                  ))}
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
    </PageTemplate>
  );
};

export default TableEditorPage;
