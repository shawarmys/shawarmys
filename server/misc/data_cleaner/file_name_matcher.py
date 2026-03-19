FILE_KEYWORDS = ["device_raw", "device", "icd", "labs", "medication", "nursing"]


class FileNameMatcher:
    @staticmethod
    def match_file_name(file_name: str) -> str:
        name = file_name.lower()

        # specific first
        if "device_raw_1hz" in name or "device_1hz" in name:
            return "device_1hz"

        if "epaac-data-1" in name:
            return "epac_data_1"
        if "epaac-data-2" in name:
            return "epac_data_2"
        if "epaac-data-3" in name:
            return "epac_data_3"
        if "epaac-data-4" in name:
            return "epac_data_4"
        if "epaac-data-5" in name:
            return "epac_data_5"

        for keyword in FILE_KEYWORDS:
            if keyword in name:
                return keyword
        return None