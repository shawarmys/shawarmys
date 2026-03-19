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
import { useTableData } from "../hooks/useTableData";

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

  const [files, setFiles] = React.useState<File[]>([]);
  const [isDragActive, setIsDragActive] = React.useState(false);
  const [isUploading, setIsUploading] = React.useState(false);
  const [errorMessage, setErrorMessage] = React.useState<string | null>(null);
  const [successMessage, setSuccessMessage] = React.useState<string | null>(
    null,
  );

  const { setTableData } = useTableData();

  const addFiles = (incomingFiles: FileList | File[]) => {
    const nextFiles = Array.from(incomingFiles);

    const validFiles = nextFiles.filter((file) => {
      const extension = file.name.split(".").pop()?.toLowerCase() ?? "";
      return ALLOWED_EXTENSIONS.includes(extension);
    });

    if (validFiles.length !== nextFiles.length) {
      setErrorMessage(
        `Only ${ALLOWED_EXTENSIONS.join(", ")} files are allowed. Unsupported files were ignored.`,
      );
    } else {
      setErrorMessage(null);
    }

    setSuccessMessage(null);
    setFiles((previous) => {
      const existingKeys = new Set(
        previous.map(
          (file) => `${file.name}:${file.size}:${file.lastModified}`,
        ),
      );

      const uniqueNewFiles = validFiles.filter((file) => {
        const key = `${file.name}:${file.size}:${file.lastModified}`;
        if (existingKeys.has(key)) {
          return false;
        }
        existingKeys.add(key);
        return true;
      });

      return [...previous, ...uniqueNewFiles];
    });
  };

  const onFileInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (!event.target.files) {
      return;
    }

    addFiles(event.target.files);
    event.target.value = "";
  };

  const removeFile = (fileToRemove: File) => {
    setFiles((previous) => previous.filter((file) => file !== fileToRemove));
  };

  const clearFiles = () => {
    setFiles([]);
    setErrorMessage(null);
    setSuccessMessage(null);
  };

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
    if (files.length === 0) {
      setErrorMessage("Please select at least one file before uploading.");
      return;
    }

    setIsUploading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const formData = new FormData();
      files.forEach((file) => formData.append("files", file));

      const response = await apiClient.post("/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setTableData(response.data.tableData as string[][]);
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
          <Typography variant="h6">Drag & Drop files here</Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            or click to browse ({ALLOWED_EXTENSIONS.join(", ")})
          </Typography>
          <input
            ref={fileInputRef}
            hidden
            type="file"
            multiple
            accept={ALLOWED_EXTENSIONS.map((ext) => `.${ext}`).join(",")}
            onChange={onFileInputChange}
          />
        </Box>

        {isUploading && <LinearProgress />}

        {errorMessage && <Alert severity="error">{errorMessage}</Alert>}
        {successMessage && <Alert severity="success">{successMessage}</Alert>}

        <Box>
          <Typography variant="subtitle1" sx={{ mb: 1 }}>
            Selected Files ({files.length})
          </Typography>

          {files.length === 0 ? (
            <Typography variant="body2" color="text.secondary">
              No files selected.
            </Typography>
          ) : (
            <List disablePadding>
              {files.map((file) => (
                <ListItem
                  key={`${file.name}:${file.size}:${file.lastModified}`}
                  secondaryAction={
                    <Button
                      size="small"
                      color="error"
                      startIcon={<DeleteOutlineIcon />}
                      onClick={() => removeFile(file)}
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
              ))}
            </List>
          )}
        </Box>

        <Stack direction="row" spacing={1.5}>
          <Button
            variant="outlined"
            onClick={clearFiles}
            disabled={isUploading}
          >
            Clear
          </Button>
          <Button
            variant="contained"
            onClick={uploadFiles}
            disabled={isUploading || files.length === 0}
          >
            Upload
          </Button>
        </Stack>
      </Stack>
    </PageTemplate>
  );
};

export default UploadPage;
