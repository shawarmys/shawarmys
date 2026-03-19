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
import { useMetadata } from "../hooks/useApi";

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
  const { data, isLoading, isError } = useMetadata();

  return (
    <PageTemplate title="">
      <Grid container spacing={2}>
        {/* *** First Overview Card *** */}
        <Grid size={4}>
          <CustomCard>
            <List>
              {/* Imported Files */}
              <CardListItem
                icon={<DownloadIcon sx={IconSX} />}
                number={
                  !isLoading && !isError && data?.importedFiles
                    ? data.importedFiles.toString()
                    : ""
                }
                label="Imported Files"
                onClick={() => navigate("/imported-files")}
              />

              <Divider variant="middle" component="li" />

              {/* Successful Mappings */}
              <CardListItem
                icon={<CheckIcon sx={IconSX} />}
                number={
                  !isLoading && !isError && data?.successfulMappings
                    ? data.successfulMappings.toString()
                    : ""
                }
                label="Successful Mappings"
                sx={{ color: "success.main" }}
              />

              <Divider variant="middle" component="li" />

              {/* Mapping Alerts */}
              <CardListItem
                icon={<ReportProblemIcon sx={IconSX} />}
                number={
                  !isLoading && !isError && data?.mappingAlerts
                    ? data.mappingAlerts.toString()
                    : ""
                }
                label="Mapping Alerts"
                sx={{ color: "warning.main" }}
              />
            </List>
          </CustomCard>
        </Grid>

        {/* *** Data Sources *** */}
        {/* TODO: Chart, onClick */}
        <Grid size={4}>
          <CustomCard title="Data Sources">
            <PieChart
              series={[
                {
                  data: [
                    { id: 0, value: 10, label: "series A" },
                    { id: 1, value: 15, label: "series B" },
                    { id: 2, value: 20, label: "series C" },
                  ],
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
