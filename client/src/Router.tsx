import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import Theme from "./components/theme";
import HomePage from "./pages/homePage";

const Router = () => {
  return (
    <BrowserRouter>
      <Theme>
        <CssBaseline />
        <Routes>
          <Route path="/" element={<Navigate to="/home" replace />} />
          <Route path="/home" element={<HomePage />} />
          {/* <Route path="*" element={<NotFoundPage />} /> */}
        </Routes>
      </Theme>
    </BrowserRouter>
  );
};

export default Router;
