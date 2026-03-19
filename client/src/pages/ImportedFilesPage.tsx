import {
  Paper,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TableSortLabel,
  TextField,
} from "@mui/material";
import React from "react";
import PageTemplate from "../components/PageTemplate";
import { useImportedFiles } from "../hooks/useApi";
import { useFilter } from "../hooks/useFilter";

type SortableKey = "name" | "source" | "entries" | "records" | "type";
type SortDirection = "asc" | "desc";

const ImportedFilesPage: React.FC = () => {
  const { filterSources, filterGroupTypes } = useFilter();
  const { data: importedFiles } = useImportedFiles(
    filterSources,
    filterGroupTypes,
  );

  const [searchTerm, setSearchTerm] = React.useState("");
  const [sortBy, setSortBy] = React.useState<SortableKey>("name");
  const [sortDirection, setSortDirection] =
    React.useState<SortDirection>("asc");

  const filteredAndSortedFiles = React.useMemo(() => {
    if (!importedFiles) {
      return [];
    }

    const normalizedSearchTerm = searchTerm.trim().toLowerCase();

    const filteredFiles = importedFiles.filter((file) => {
      if (!normalizedSearchTerm) {
        return true;
      }

      return [
        file.name,
        file.source,
        file.type,
        String(file.entries),
        String(file.records),
      ].some((value) => value.toLowerCase().includes(normalizedSearchTerm));
    });

    return [...filteredFiles].sort((a, b) => {
      const aValue = a[sortBy];
      const bValue = b[sortBy];

      if (typeof aValue === "number" && typeof bValue === "number") {
        return sortDirection === "asc" ? aValue - bValue : bValue - aValue;
      }

      const comparison = String(aValue).localeCompare(
        String(bValue),
        undefined,
        {
          sensitivity: "base",
          numeric: true,
        },
      );

      return sortDirection === "asc" ? comparison : -comparison;
    });
  }, [importedFiles, searchTerm, sortBy, sortDirection]);

  const handleSort = (column: SortableKey) => {
    if (sortBy === column) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
      return;
    }

    setSortBy(column);
    setSortDirection("asc");
  };

  return (
    <PageTemplate title="Imported Files">
      <Stack spacing={2} sx={{ mb: 2 }}>
        <TextField
          label="Search imported files"
          placeholder="Search by name, source, type, entries or records"
          size="small"
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
          fullWidth
        />
      </Stack>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell
                sortDirection={sortBy === "name" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "name"}
                  direction={sortBy === "name" ? sortDirection : "asc"}
                  onClick={() => handleSort("name")}
                >
                  File Name
                </TableSortLabel>
              </TableCell>
              <TableCell
                sortDirection={sortBy === "source" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "source"}
                  direction={sortBy === "source" ? sortDirection : "asc"}
                  onClick={() => handleSort("source")}
                >
                  Source
                </TableSortLabel>
              </TableCell>
              <TableCell
                align="right"
                sortDirection={sortBy === "entries" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "entries"}
                  direction={sortBy === "entries" ? sortDirection : "asc"}
                  onClick={() => handleSort("entries")}
                >
                  Entries
                </TableSortLabel>
              </TableCell>
              <TableCell
                align="right"
                sortDirection={sortBy === "records" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "records"}
                  direction={sortBy === "records" ? sortDirection : "asc"}
                  onClick={() => handleSort("records")}
                >
                  Records
                </TableSortLabel>
              </TableCell>
              <TableCell
                sortDirection={sortBy === "type" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "type"}
                  direction={sortBy === "type" ? sortDirection : "asc"}
                  onClick={() => handleSort("type")}
                >
                  Type
                </TableSortLabel>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredAndSortedFiles.map((file) => (
              <TableRow
                key={file.name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {file.name}
                </TableCell>
                <TableCell>{file.source}</TableCell>
                <TableCell align="right">{file.entries}</TableCell>
                <TableCell align="right">{file.records}</TableCell>
                <TableCell>{file.type}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </PageTemplate>
  );
};

export default ImportedFilesPage;
