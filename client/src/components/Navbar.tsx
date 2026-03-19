import FileUploadIcon from "@mui/icons-material/FileUpload";
import FilterListIcon from "@mui/icons-material/FilterList";
import HomeIcon from "@mui/icons-material/Home";
import {
  AppBar,
  Badge,
  Box,
  IconButton,
  Toolbar,
  Tooltip,
  Typography,
} from "@mui/material";
import React from "react";
import { useNavigate } from "react-router-dom";
import { useFilter } from "../hooks/useFilter";
import FilterModal from "./FilterModal";

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const { toggleFilterModal, filterSources, filterGroupTypes } = useFilter();

  return (
    <AppBar position="static" color="default">
      <Toolbar>
        <Box
          sx={{ flexGrow: 1 }}
          style={{ marginTop: 8, cursor: "pointer" }}
          onClick={() => navigate("/")}
        >
          <Typography variant="h6">epaCC Dashboard</Typography>
        </Box>

        {window.location.pathname !== "/" && (
          <Tooltip title="Home">
            <IconButton size="large" onClick={() => navigate("/")}>
              <HomeIcon />
            </IconButton>
          </Tooltip>
        )}

        <Tooltip title="Upload File">
          <IconButton size="large" onClick={() => navigate("/upload")}>
            <FileUploadIcon />
          </IconButton>
        </Tooltip>

        <Tooltip title="Filter">
          <IconButton size="large" onClick={toggleFilterModal}>
            <FilterListIcon />
            {/* Show a badge with the number of set filters */}
            {filterSources.length > 0 || filterGroupTypes.length > 0 ? (
              <Badge
                badgeContent={filterSources.length + filterGroupTypes.length}
                color="error"
                sx={{ mt: 2 }}
              />
            ) : null}
          </IconButton>
        </Tooltip>
        <FilterModal />
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
