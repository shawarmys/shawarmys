import {
  Box,
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
import { useAlerts } from "../hooks/useApi";
import { useFilter } from "../hooks/useFilter";

type SortableKey = "timestamp" | "level" | "message";
type SortDirection = "asc" | "desc";

const ALERT_LEVEL_PRIORITY: Record<string, number> = {
  severe: 0,
  warning: 1,
  info: 2,
};
// TODO onclick
const AlertsPage: React.FC = () => {
  const { filterSources, filterGroupTypes } = useFilter();
  const { data: alerts } = useAlerts(filterSources, filterGroupTypes);

  const [searchTerm, setSearchTerm] = React.useState("");
  const [sortBy, setSortBy] = React.useState<SortableKey>("level");
  const [sortDirection, setSortDirection] =
    React.useState<SortDirection>("asc");

  const filteredAndSortedAlerts = React.useMemo(() => {
    if (!alerts) {
      return [];
    }

    const normalizedSearchTerm = searchTerm.trim().toLowerCase();

    const filteredAlerts = alerts.filter((alert) => {
      if (!normalizedSearchTerm) {
        return true;
      }

      return [alert.timestamp, alert.level, alert.message].some((value) =>
        value.toLowerCase().includes(normalizedSearchTerm),
      );
    });

    return [...filteredAlerts].sort((a, b) => {
      if (sortBy === "level") {
        const levelOrderDiff =
          (ALERT_LEVEL_PRIORITY[a.level] ?? 999) -
          (ALERT_LEVEL_PRIORITY[b.level] ?? 999);
        return sortDirection === "asc" ? levelOrderDiff : -levelOrderDiff;
      }

      const aValue = a[sortBy];
      const bValue = b[sortBy];

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
  }, [alerts, searchTerm, sortBy, sortDirection]);

  const handleSort = (column: SortableKey) => {
    if (sortBy === column) {
      setSortDirection((prev) => (prev === "asc" ? "desc" : "asc"));
      return;
    }

    setSortBy(column);
    setSortDirection("asc");
  };

  return (
    <PageTemplate title="Alerts">
      <Stack spacing={2} sx={{ mb: 2 }}>
        <TextField
          label="Search alerts"
          placeholder="Search by timestamp, level or message"
          size="small"
          value={searchTerm}
          onChange={(event) => setSearchTerm(event.target.value)}
          fullWidth
        />
      </Stack>
      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="alerts table">
          <TableHead>
            <TableRow>
              <TableCell
                sortDirection={sortBy === "timestamp" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "timestamp"}
                  direction={sortBy === "timestamp" ? sortDirection : "asc"}
                  onClick={() => handleSort("timestamp")}
                >
                  Timestamp
                </TableSortLabel>
              </TableCell>
              <TableCell
                sortDirection={sortBy === "level" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "level"}
                  direction={sortBy === "level" ? sortDirection : "asc"}
                  onClick={() => handleSort("level")}
                >
                  Level
                </TableSortLabel>
              </TableCell>
              <TableCell
                sortDirection={sortBy === "message" ? sortDirection : false}
              >
                <TableSortLabel
                  active={sortBy === "message"}
                  direction={sortBy === "message" ? sortDirection : "asc"}
                  onClick={() => handleSort("message")}
                >
                  Message
                </TableSortLabel>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredAndSortedAlerts.map((alert, idx) => (
              <TableRow
                key={`${alert.timestamp}-${alert.level}-${idx}`}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {alert.timestamp}
                </TableCell>
                <TableCell>
                  <Box
                    component="span"
                    sx={{
                      color:
                        alert.level === "severe"
                          ? "error.main"
                          : alert.level === "warning"
                            ? "warning.main"
                            : "primary.main",
                      fontWeight: 600,
                    }}
                  >
                    {alert.level}
                  </Box>
                </TableCell>
                <TableCell>{alert.message}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </PageTemplate>
  );
};

export default AlertsPage;
