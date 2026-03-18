import { blue } from "@mui/material/colors";
import { createTheme, ThemeProvider } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    // mode: "dark",
    primary: {
      main: blue[500],
    },
  },
});

interface ThemeProps {
  children: React.ReactNode;
}

const Theme: React.FC<ThemeProps> = ({ children }) => {
  return <ThemeProvider theme={theme}>{children}</ThemeProvider>;
};

export default Theme;
