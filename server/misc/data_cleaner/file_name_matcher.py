FILE_KEYWORDS = ["device_raw", "device", "epaAC", "icd", "labs", "medication", "nursing"]


class FileNameMatcher:
    @staticmethod
    def match_file_name(file_name: str) -> str:
        # Check for device_1hz FIRST before other device keywords
        if "device_raw_1hz" in file_name.lower() or "device_1hz" in file_name.lower():
            return "device_1hz"

        for keyword in FILE_KEYWORDS:
            if keyword in file_name.lower():
                return keyword
        return None
