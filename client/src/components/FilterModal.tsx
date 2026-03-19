import CloseIcon from "@mui/icons-material/Close";
import type { SelectChangeEvent } from "@mui/material";
import {
  Button,
  Chip,
  FormControl,
  InputLabel,
  MenuItem,
  OutlinedInput,
  Select,
} from "@mui/material";
import Box from "@mui/material/Box";
import IconButton from "@mui/material/IconButton";
import Modal from "@mui/material/Modal";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import { useDataGroupsSummary, useDataSourcesSummary } from "../hooks/useApi";
import { useFilter } from "../hooks/useFilter";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  boxShadow: 24,
  p: 4,
};

export default function FilterModal() {
  const {
    showFilterModal,
    toggleFilterModal,
    filterSources,
    setFilterSources,
    filterGroupTypes,
    setFilterGroupTypes,
  } = useFilter();
  const { data: dataSourcesSummary } = useDataSourcesSummary([], []);
  const { data: dataGroupsSummary } = useDataGroupsSummary([], []);

  const availableSources = Array.from(
    new Set((dataSourcesSummary ?? []).map((source) => source.name)),
  );

  const availableGroupTypes = Array.from(
    new Set((dataGroupsSummary ?? []).map((group) => group.groupType)),
  );

  const handleSourcesChange = (event: SelectChangeEvent<string[]>) => {
    const value = event.target.value;
    setFilterSources(typeof value === "string" ? value.split(",") : value);
  };

  const handleGroupTypesChange = (event: SelectChangeEvent<string[]>) => {
    const value = event.target.value;
    setFilterGroupTypes(typeof value === "string" ? value.split(",") : value);
  };

  return (
    <Modal
      open={showFilterModal}
      onClose={toggleFilterModal}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Stack
          direction="row"
          alignItems="center"
          justifyContent="space-between"
          sx={{ mb: 1 }}
        >
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Filter
          </Typography>
          <IconButton
            aria-label="Close filter modal"
            size="small"
            onClick={toggleFilterModal}
          >
            <CloseIcon fontSize="small" />
          </IconButton>
        </Stack>

        {/* Data Sources Filter */}
        <FormControl sx={{ width: "100%" }}>
          <InputLabel id="filter-sources-label">Sources</InputLabel>
          <Select
            labelId="filter-sources-label"
            multiple
            value={filterSources}
            onChange={handleSourcesChange}
            input={<OutlinedInput label="Sources" />}
            renderValue={(selected) => (
              <Box sx={{ display: "flex", gap: "0.25rem", flexWrap: "wrap" }}>
                {selected.map((selectedOption) => (
                  <Chip
                    key={selectedOption}
                    color="primary"
                    label={selectedOption}
                  />
                ))}
              </Box>
            )}
          >
            {availableSources.map((sourceName) => (
              <MenuItem key={sourceName} value={sourceName}>
                {sourceName}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Data Groups Filter */}
        <FormControl sx={{ width: "100%", mt: 2 }}>
          <InputLabel id="filter-groups-label">Groups</InputLabel>
          <Select
            labelId="filter-groups-label"
            multiple
            value={filterGroupTypes}
            onChange={handleGroupTypesChange}
            input={<OutlinedInput label="Groups" />}
            renderValue={(selected) => (
              <Box sx={{ display: "flex", gap: "0.25rem", flexWrap: "wrap" }}>
                {selected.map((selectedOption) => (
                  <Chip
                    key={selectedOption}
                    color="primary"
                    label={selectedOption}
                  />
                ))}
              </Box>
            )}
          >
            {availableGroupTypes.map((groupType) => (
              <MenuItem key={groupType} value={groupType}>
                {groupType}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Button to clear filters */}
        <Button
          variant="outlined"
          color="warning"
          onClick={() => {
            setFilterSources([]);
            setFilterGroupTypes([]);
            toggleFilterModal();
          }}
          sx={{ mt: 2 }}
        >
          Clear Filters
        </Button>
      </Box>
    </Modal>
  );
}
