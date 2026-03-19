import { Box, Container, Typography } from "@mui/material";
import React from "react";
import Navbar from "./Navbar";

interface PageTemplateProps {
  children: React.ReactNode;
  title?: string;
  wide?: boolean;
  topRightAction?: React.ReactNode;
}

const PageTemplate: React.FC<PageTemplateProps> = ({
  children,
  title,
  wide,
  topRightAction,
}) => {
  return (
    <Box>
      <Navbar />
      <Container maxWidth={wide ? "xl" : "lg"} sx={{ mt: 4, mb: 6 }}>
        {(title || topRightAction) && (
          <Box
            sx={{
              mb: 1,
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: 2,
            }}
          >
            {title ? <Typography variant="h4">{title}</Typography> : <span />}
            {topRightAction}
          </Box>
        )}
        {children}
      </Container>
    </Box>
  );
};

export default PageTemplate;
