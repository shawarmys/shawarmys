import HomeIcon from "@mui/icons-material/Home";
import {
  AppBar,
  Box,
  Button,
  type SxProps,
  Toolbar,
  Typography,
} from "@mui/material";
import React from "react";
import { useLocation, useNavigate } from "react-router-dom";

const IconSX: SxProps = {
  mr: 0.5,
  fontSize: 16,
};

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const path = location.pathname;

  return (
    <AppBar position="static" color="default">
      <Toolbar>
        <Box
          sx={{ flexGrow: 1 }}
          style={{ marginTop: 8, cursor: "pointer" }}
          onClick={() => navigate("/home")}
        >
          <Typography variant="h6">epaCC Portal</Typography>
        </Box>

        <Box>
          <Button
            sx={{ mr: 1 }}
            color={path === "/home" ? "primary" : "inherit"}
            onClick={() => navigate("/home")}
          >
            <HomeIcon sx={IconSX} />
            Home
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
