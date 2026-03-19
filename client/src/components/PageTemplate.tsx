import { Box, Container, Typography } from "@mui/material";
import React from "react";
import Navbar from "./Navbar";

interface PageTemplateProps {
  children: React.ReactNode;
  title?: string;
}

const PageTemplate: React.FC<PageTemplateProps> = ({ children, title }) => {
  return (
    <Box>
      <Navbar />
      <Container sx={{ mt: 4, mb: 6 }}>
        {title && (
          <Typography variant="h4" sx={{ mb: 1 }}>
            {title}
          </Typography>
        )}
        {children}
      </Container>
    </Box>
  );
};

export default PageTemplate;
