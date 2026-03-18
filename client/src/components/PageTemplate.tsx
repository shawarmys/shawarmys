import { Box, Container, Typography } from "@mui/material";
import React from "react";
import Navbar from "./Navbar";

interface PageTemplateProps {
  children: React.ReactNode;
  title: string;
}

const PageTemplate: React.FC<PageTemplateProps> = ({ children, title }) => {
  return (
    <Box>
      <Navbar />
      <Container sx={{ mt: 4 }}>
        {title && <Typography variant="h4">{title}</Typography>}
        {children}
      </Container>
    </Box>
  );
};

export default PageTemplate;
