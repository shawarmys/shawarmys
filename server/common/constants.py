DIRECT_MAPPING_TABLES = ["lab_results", "icd10_data", "nursing_daily_reports"]
INDIRECT_MAPPING_TABLES = ["device_motions", "device_1hz_motions", "medication_events"]
FILE_METADATA_BY_TABLE: dict[str, tuple[str, str, str]] = {
    "lab_results": ("synth_labs_1000_cases.csv", "Unknown", "Lab Results"),
    "icd10_data": ("synthetic_cases_icd10_ops.csv", "Unknown", "ICD10"),
    "nursing_daily_reports": (
        "synthetic_nursing_daily_reports_en.csv",
        "Unknown",
        "Nursing Report",
    ),
    "medication_events": (
        "synthetic_medication_raw_inpatient.csv",
        "Unknown",
        "Medication",
    ),
    "device_motions": (
        "synthetic_device_motion_fall_data.csv",
        "Unknown",
        "Device Motion",
    ),
    "device_1hz_motions": (
        "synthetic_device_raw_1hz_motion_fall.csv",
        "Unknown",
        "Device 1Hz Motion",
    ),
    "tbImportAcData": ("epaAC-Data.csv", "Unknown", "Assessment"),
}