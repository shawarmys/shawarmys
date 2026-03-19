import {
  Backdrop,
  Box,
  CircularProgress,
  Container,
  Typography,
} from "@mui/material";
import React from "react";
import { useMetadata } from "../hooks/useApi";
import Navbar from "./Navbar";

interface PageTemplateProps {
  children: React.ReactNode;
  title?: string;
}

const PageTemplate: React.FC<PageTemplateProps> = ({ children, title }) => {
  const { isLoading: metadataIsLoading } = useMetadata();

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

      {/* Loader */}
      {metadataIsLoading && (
        <Backdrop
          open={true}
          sx={{
            color: "#fff",
            zIndex: (theme) => theme.zIndex.drawer + 1,
          }}
        >
          <CircularProgress color="inherit" size={32} />
        </Backdrop>
      )}
    </Box>
  );
};

export default PageTemplate;
