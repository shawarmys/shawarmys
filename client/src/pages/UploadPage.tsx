import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import DeleteOutlineIcon from "@mui/icons-material/DeleteOutline";
import {
  Alert,
  Box,
  Button,
  Chip,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Stack,
  Typography,
} from "@mui/material";
import axios from "axios";
import React from "react";
import { useNavigate } from "react-router-dom";
import { apiClient } from "../api/apiClient";
import PageTemplate from "../components/PageTemplate";
import { useTableData, type TableDataError } from "../hooks/useTableData";

const ALLOWED_EXTENSIONS = ["csv", "pdf", "xlsx"];

const formatBytes = (bytes: number): string => {
  if (bytes === 0) return "0 B";

  const units = ["B", "KB", "MB", "GB"];
  const unitIndex = Math.min(
    Math.floor(Math.log(bytes) / Math.log(1024)),
    units.length - 1,
  );
  const value = bytes / 1024 ** unitIndex;

  return `${value.toFixed(value >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
};

const UploadPage: React.FC = () => {
  const navigate = useNavigate();
  const fileInputRef = React.useRef<HTMLInputElement | null>(null);

  const [file, setFile] = React.useState<File | null>(null);
  const [isDragActive, setIsDragActive] = React.useState(false);
  const [isUploading, setIsUploading] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);
  const [successMessage, setSuccessMessage] = React.useState<string | null>(
    null,
  );

  const { setTableData, setFileName, setErrors, setOutliers } = useTableData();

  const addFiles = (incomingFiles: FileList | File[]) => {
    const nextFiles = Array.from(incomingFiles);
    const selectedFile = nextFiles[0];

    if (!selectedFile) {
      return;
    }

    const extension = selectedFile.name.split(".").pop()?.toLowerCase() ?? "";
    const isValidFile = ALLOWED_EXTENSIONS.includes(extension);

    if (!isValidFile) {
      setErrorMessage(
        `Only ${ALLOWED_EXTENSIONS.join(", ")} file are allowed.`,
      );
      setSuccessMessage(null);
      return;
    }

    if (nextFiles.length > 1) {
      setErrorMessage(
        "Only one file can be uploaded at a time. Using the first selected file.",
      );
    } else {
      setErrorMessage(null);
    }

    setSuccessMessage(null);
    setFile(selectedFile);
  };

  const onFileInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    addFiles(event.target.files);
    event.target.value = "";
  };

  const removeFile = () => setFile(null);

  const onDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragActive(true);
  };

  const onDragLeave = () => {
    setIsDragActive(false);
  };

  const onDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragActive(false);

    if (event.dataTransfer.files?.length) {
      addFiles(event.dataTransfer.files);
    }
  };

  const uploadFiles = async () => {
    if (!file) {
      setErrorMessage("Please select a file before uploading.");
      return;
    }

    setIsUploading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await apiClient.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTableData(response.data.tableData as string[][]);
      setErrors(response.data.errors as TableDataError[]);
      setOutliers(response.data.outliers as TableDataError[]);
      setFileName(file.name);

      navigate("/table-editor");
    } catch (error) {
      if (axios.isAxiosError(error)) {
        setErrorMessage(
          error.response?.data?.detail ??
            "Upload failed. Please check if the upload endpoint is available.",
        );
      } else {
        setErrorMessage("Upload failed due to an unexpected error.");
      }
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <PageTemplate title="File Upload">
      <Stack spacing={2.5}>
        <Box
          onDragOver={onDragOver}
          onDragLeave={onDragLeave}
          onDrop={onDrop}
          onClick={() => fileInputRef.current?.click()}
          sx={{
            border: "2px dashed",
            borderColor: isDragActive ? "primary.main" : "divider",
            borderRadius: 2,
            p: 4,
            textAlign: "center",
            cursor: "pointer",
            transition: "border-color 0.2s ease, background-color 0.2s ease",
            backgroundColor: isDragActive ? "action.hover" : "transparent",
          }}
        >
          <CloudUploadIcon color="primary" sx={{ fontSize: 40, mb: 1 }} />
          <Typography variant="h6">Drag & Drop a file here</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            or click to browse a single file ({ALLOWED_EXTENSIONS.join(", ")})
          </Typography>
          <input
            ref={fileInputRef}
            hidden
            type="file"
            accept={ALLOWED_EXTENSIONS.map((ext) => `.${ext}`).join(",")}
            onChange={onFileInputChange}
          />
        </Box>

        {isUploading && <LinearProgress />}

        {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
        {successMessage && <Alert severity="success">{successMessage}</Alert>}

        <Box>
          <Typography variant="subtitle1" sx={{ mb: 1 }}>
            Selected File
          </Typography>

          {!file ? (
            <Typography variant="body2" color="text.secondary">
              No file selected.
            </Typography>
          ) : (
            <List disablePadding>
              <ListItem
                key={`${file.name}:${file.size}:${file.lastModified}`}
                secondaryAction={
                  <Button
                    size="small"
                    color="error"
                    startIcon={<DeleteOutlineIcon />}
                    onClick={() => removeFile()}
                  >
                    Remove
                  </Button>
                }
                sx={{ px: 0 }}
              >
                <ListItemText
                  primary={file.name}
                  secondary={
                    <Stack direction="row" spacing={1} sx={{ mt: 0.5 }}>
                      <Chip label={formatBytes(file.size)} size="small" />
                    </Stack>
                  }
                />
              </ListItem>
            </List>
          )}
        </Box>

        <Stack direction="row" spacing={1.5}>
          <Button
            variant="contained"
            onClick={uploadFiles}
            disabled={isUploading || !file}
          >
            Upload
          </Button>
        </Stack>
      </Stack>
    </PageTemplate>
  );
};

export default UploadPage;
