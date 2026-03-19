import CheckIcon from "@mui/icons-material/Check";
import DownloadIcon from "@mui/icons-material/Download";
import ReportProblemIcon from "@mui/icons-material/ReportProblem";
import {
  Box,
  Divider,
  Grid,
  Link,
  List,
  ListItem,
  ListItemText,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
  type SxProps,
} from "@mui/material";
import { BarChart } from "@mui/x-charts";
import { PieChart } from "@mui/x-charts/PieChart";
import React from "react";
import { useNavigate } from "react-router-dom";
import CustomCard from "../components/CustomCard";
import PageTemplate from "../components/PageTemplate";
import {
  useAlerts,
  useDataGroupsSummary,
  useDataSourcesSummary,
  useMetadata,
} from "../hooks/useApi";
import { useFilter } from "../hooks/useFilter";

const IconSX: SxProps = {
  mr: 1.5,
  verticalAlign: "center",
};

const ALERT_LEVEL_PRIORITY: Record<string, number> = {
  severe: 0,
  warning: 1,
  info: 2,
};

const CardListItem: React.FC<{
  icon: React.ReactNode;
  number: string;
  label: string;
  sx?: SxProps;
  onClick?: () => void;
}> = ({ icon, number, label, sx, onClick }) => {
  return (
    <ListItem>
      <ListItemText
        sx={onClick ? { cursor: "pointer" } : undefined}
        onClick={onClick}
      >
        <Typography variant="h6" sx={sx}>
          {icon}
          {number}
          <Typography component="span" variant="body2" sx={{ ml: 2 }}>
            {label}
          </Typography>
        </Typography>
      </ListItemText>
    </ListItem>
  );
};

const HomePage: React.FC = () => {
  const navigate = useNavigate();
  const { filterSources, filterGroupTypes } = useFilter();
  const { data: metadata, isLoading: metadataIsLoading } = useMetadata(
    filterSources,
    filterGroupTypes,
  );
  const { data: dataSourcesSummary, isLoading: dataSourcesSummaryIsLoading } =
    useDataSourcesSummary(filterSources, filterGroupTypes);
  const { data: dataGroupsSummary, isLoading: dataGroupsSummaryIsLoading } =
    useDataGroupsSummary(filterSources, filterGroupTypes);
  const { data: alerts, isLoading: alertsIsLoading } = useAlerts(
    filterSources,
    filterGroupTypes,
  );

  return (
    <PageTemplate title="">
      <Grid container spacing={2}>
        {/* *** First Overview Card *** */}
        <Grid size={4}>
          <CustomCard loading={metadataIsLoading}>
            <List>
              {/* Imported Files */}
              <CardListItem
                icon={<DownloadIcon sx={IconSX} />}
                number={metadata?.importedFiles.toString() || ""}
                label="Imported Files"
                onClick={() => navigate("/imported-files")}
              />

              <Divider variant="middle" component="li" />

              {/* Successful Mappings */}
              <CardListItem
                icon={<CheckIcon sx={IconSX} />}
                number={metadata?.successfulMappings.toString() || ""}
                label="Successful Mappings"
                sx={{ color: "success.main" }}
              />

              <Divider variant="middle" component="li" />

              {/* Mapping Alerts */}
              <CardListItem
                icon={<ReportProblemIcon sx={IconSX} />}
                number={metadata?.mappingAlerts.toString() || ""}
                label="Mapping Alerts"
                sx={{ color: "warning.main" }}
                onClick={() => navigate("/alerts")}
              />
            </List>
          </CustomCard>
        </Grid>

        {/* *** Data Sources *** */}
        <Grid size={4}>
          <CustomCard
            title="Data Sources"
            loading={dataSourcesSummaryIsLoading}
          >
            <PieChart
              series={[
                {
                  data:
                    dataSourcesSummary?.map((dataSource, idx) => {
                      return {
                        id: idx,
                        value: dataSource.numFiles,
                        label: dataSource.name,
                      };
                    }) || [],
                },
              ]}
              width={200}
              height={200}
            />
          </CustomCard>
        </Grid>

        {/* *** Data Groups *** */}
        <Grid size={4}>
          <CustomCard title="Data Groups" loading={dataGroupsSummaryIsLoading}>
            <PieChart
              series={[
                {
                  data:
                    dataGroupsSummary?.map((dataGroup, idx) => {
                      return {
                        id: idx,
                        value: dataGroup.numFiles,
                        label: dataGroup.groupType,
                      };
                    }) || [],
                },
              ]}
              width={200}
              height={200}
            />
          </CustomCard>
        </Grid>

        {/* *** Alerts *** */}
        <Grid size={12}>
          <CustomCard title="Alerts" loading={alertsIsLoading}>
            {/* Table with pagination of the alerts */}
            {(alerts && alerts.length > 0 && (
              <>
                <Box sx={{ overflow: "auto", maxHeight: 300 }}>
                  <Table sx={{ minWidth: 650 }} aria-label="simple table">
                    <TableHead
                      sx={{
                        position: "sticky",
                        top: 0,
                        zIndex: 2,
                        backgroundColor: "background.paper",
                      }}
                    >
                      <TableRow>
                        <TableCell>Timestamp</TableCell>
                        <TableCell>Level</TableCell>
                        <TableCell>Message</TableCell>
                        <TableCell></TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {[...alerts]
                        .sort(
                          (a, b) =>
                            (ALERT_LEVEL_PRIORITY[a.level] ?? 999) -
                            (ALERT_LEVEL_PRIORITY[b.level] ?? 999),
                        )
                        .map((alert) => (
                          <TableRow
                            key={alert.timestamp}
                            sx={{
                              "&:last-child td, &:last-child th": { border: 0 },
                              cursor: "pointer",
                            }}
                            onClick={() => {
                              confirm(alert.tableReference);
                            }}
                          >
                            <TableCell component="th" scope="row">
                              {alert.timestamp}
                            </TableCell>
                            <TableCell>
                              <Typography
                                color={
                                  alert.level === "severe"
                                    ? "error"
                                    : alert.level === "warning"
                                      ? "warning"
                                      : "primary"
                                }
                              >
                                {alert.level}
                              </Typography>
                            </TableCell>
                            <TableCell>{alert.message}</TableCell>
                          </TableRow>
                        ))}
                    </TableBody>
                  </Table>
                </Box>
                <Link
                  style={{ cursor: "pointer" }}
                  onClick={() => navigate("/alerts")}
                >
                  <Typography sx={{ my: 2 }}>Show more</Typography>
                </Link>
              </>
            )) || (
              <Typography sx={{ my: 2 }}>
                No alerts found for the current filters.
              </Typography>
            )}
          </CustomCard>
        </Grid>

        {/* *** Data Quality *** */}
        <Grid size={12}>
          <CustomCard title="Data Quality">
            <BarChart
              layout="horizontal"
              height={350}
              series={[
                {
                  data: [70, 60, 40],
                  label: "Clean Data",
                  id: "cd",
                  stack: "total",
                },
                {
                  data: [20, 20, 45],
                  label: "Incorrect Values",
                  id: "iv",
                  stack: "total",
                },
                {
                  data: [10, 20, 15],
                  label: "Missing Values",
                  id: "mv",
                  stack: "total",
                },
              ]}
              yAxis={[
                {
                  data: ["A", "B", "C"],
                  scaleType: "band",
                },
              ]}
              xAxis={[{}]}
            />
          </CustomCard>
        </Grid>
      </Grid>
    </PageTemplate>
  );
};

export default HomePage;
