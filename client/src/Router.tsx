import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Theme from "./components/Theme";
import AlertsPage from "./pages/AlertsPage";
import HomePage from "./pages/HomePage";
import ImportedFilesPage from "./pages/ImportedFilesPage";
import NotFoundPage from "./pages/NotFoundPage";
import UploadPage from "./pages/UploadPage";

const Router = () => {
  return (
    <BrowserRouter>
      <Theme>
        <CssBaseline />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/imported-files" element={<ImportedFilesPage />} />
          <Route path="/alerts" element={<AlertsPage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </Theme>
    </BrowserRouter>
  );
};

export default Router;
