FILE_KEYWORDS = ["device_raw", "device", "icd", "labs", "medication", "nursing"]

class FileNameMatcher:
    @staticmethod
    def match_file_name(file_name: str) -> str:
        name = file_name.lower()

        # 1. Check for specific EPAC patterns
        # Matches 'epaAC-Data-1_fingerprint.json'
        for i in range(1, 6):
            if f"epaac-data-{i}" in name:
                return f"epaac-data-{i}"

        # 2. Check for Device specific patterns
        if "device_raw_1hz" in name or "device_1hz" in name:
            return "synthetic_device_raw_1hz_motion_fall"

        if "device" in name and "motion" in name:
            return "synthetic_device_motion_fall_data"

        # 3. Handle Labs, ICD, Medication, and Nursing based on your folder screenshot
        if "labs" in name:
            return "synth_labs_1000_cases"

        if "clinic" in name and "icd" in name:
            return "synthetic_device_motion_fall_data"

        if "icd" in name:
            return "synthetic_cases_icd10_ops"

        if "medication" in name:
            return "synthetic_medication_raw_inpatient"

        if "nursing" in name:
            return "synthetic_nursing_daily_reports_en"

        # Fallback keyword search
        for keyword in FILE_KEYWORDS:
            if keyword in name:
                return keyword

        return None
