import FilterListIcon from "@mui/icons-material/FilterList";
import {
  AppBar,
  Badge,
  Box,
  IconButton,
  Toolbar,
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
        <FilterModal />
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
