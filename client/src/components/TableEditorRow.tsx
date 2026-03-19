import CloseIcon from "@mui/icons-material/Close";
import SaveIcon from "@mui/icons-material/Save";
import {
  IconButton,
  InputAdornment,
  TableCell,
  TableRow,
  TextField,
  Tooltip,
  type SxProps,
  type Theme,
} from "@mui/material";
import React from "react";
import type { TableDataError } from "../hooks/useTableData";

interface TableEditorRowProps {
  row: string[];
  rowIdx: number;
  errors: TableDataError[];
  editModeRow?: boolean[];
  editingValues: Record<string, string>;
  getCellKey: (row: number, col: number) => string;
  setEditingValues: React.Dispatch<
    React.SetStateAction<Record<string, string>>
  >;
  startEditingCell: (row: number, col: number, initialValue: string) => void;
  saveCellValue: (row: number, col: number) => void;
  cancelCellEditing: (row: number, col: number) => void;
  unsetError: (row: number, col: number) => void;
  tableCellSx?: SxProps<Theme>;
}

const TableEditorRow: React.FC<TableEditorRowProps> = ({
  row,
  rowIdx,
  errors,
  editModeRow,
  editingValues,
  getCellKey,
  setEditingValues,
  startEditingCell,
  saveCellValue,
  cancelCellEditing,
  unsetError,
  tableCellSx = {},
}) => {
  return (
    <TableRow
      sx={{
        "&:last-child td, &:last-child th": { border: 0 },
        backgroundColor: rowIdx % 2 === 1 ? "action.hover" : "background.paper",
      }}
    >
      {row.map((cell, cellIdx) => (
        <Tooltip
          key={cellIdx}
          title={
            errors.find(
              (error) => error.row === rowIdx && error.col === cellIdx,
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
            sx={Object.assign(
              {
                position: "relative",
                overflow: "visible",
                backgroundColor: errors.some(
                  (error) => error.row === rowIdx && error.col === cellIdx,
                )
                  ? "error.light"
                  : undefined,
              },
              tableCellSx,
            )}
            // Show error message as tooltip on hover if this cell has an error
            title={
              errors.find(
                (error) => error.row === rowIdx && error.col === cellIdx,
              )?.msg
            }
          >
            {editModeRow?.[cellIdx] ? (
              <TextField
                id="outlined-size-small"
                value={editingValues[getCellKey(rowIdx, cellIdx)] ?? cell}
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
                  // position: "absolute",
                  // left: 0,
                  // top: "50%",
                  // transform: "translateY(-50%)",
                  // zIndex: 100,
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
                        onClick={() => cancelCellEditing(rowIdx, cellIdx)}
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
                onClick={() => startEditingCell(rowIdx, cellIdx, cell)}
              >
                {cell}
              </span>
            )}
          </TableCell>
        </Tooltip>
      ))}
    </TableRow>
  );
};

export default TableEditorRow;
