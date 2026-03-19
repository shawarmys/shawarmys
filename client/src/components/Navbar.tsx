import { AppBar, Box, Toolbar, Typography } from "@mui/material";
import React from "react";
import { useNavigate } from "react-router-dom";

const Navbar: React.FC = () => {
  const navigate = useNavigate();

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
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
