import { Box, CircularProgress, Typography } from "@mui/material";
import Paper from "@mui/material/Paper";
import { styled } from "@mui/material/styles";

const CustomPaper = styled(Paper)(({ theme }) => ({
  backgroundColor: "#fff",
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: "center",
  color: (theme.vars ?? theme).palette.text.secondary,
  ...theme.applyStyles("dark", {
    backgroundColor: "#1A2027",
  }),
}));

const CustomCard: React.FC<{
  title?: string;
  children: React.ReactNode;
  loading?: boolean;
}> = ({ title, children, loading = false }) => {
  return (
    <CustomPaper sx={{ position: "relative", overflow: "hidden" }}>
      {title && (
        <Typography variant="h6" sx={{ mb: 1.5, mt: 0.5 }}>
          {title}
        </Typography>
      )}
      {children}
      {loading && (
        <Box
          sx={{
            position: "absolute",
            inset: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            backgroundColor: "rgba(0, 0, 0, 0.6)",
            zIndex: 1,
          }}
        >
          <CircularProgress size={32} thickness={4} />
        </Box>
      )}
    </CustomPaper>
  );
};

export default CustomCard;
