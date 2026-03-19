import CheckIcon from "@mui/icons-material/Check";
import DownloadIcon from "@mui/icons-material/Download";
import ReportProblemIcon from "@mui/icons-material/ReportProblem";
import {
  Divider,
  Grid,
  List,
  ListItem,
  ListItemText,
  Typography,
  type SxProps,
} from "@mui/material";
import { BarChart } from "@mui/x-charts";
import { PieChart } from "@mui/x-charts/PieChart";
import React from "react";
import { useNavigate } from "react-router-dom";
import CustomCard from "../components/CustomCard";
import PageTemplate from "../components/PageTemplate";
import { useDataSourcesSummary, useMetadata } from "../hooks/useApi";
import { useFilter } from "../hooks/useFilter";

const IconSX: SxProps = {
  mr: 1.5,
  verticalAlign: "center",
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
              />
            </List>
          </CustomCard>
        </Grid>

        {/* *** Data Sources *** */}
        {/* TODO: Chart, onClick */}
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

        {/* *** Manual Correction *** */}
        <Grid size={4}>
          <CustomCard title="Manual Correction">
            <></>
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
