FILE_KEYWORDS = ["device", "device_1hz", "epaAC", "icd", "labs", "medication", "nursing"]

class FileNameMatcher:
    @staticmethod
    def match_file_name(file_name: str) -> str:
        for keyword in FILE_KEYWORDS:
            if keyword in file_name.lower():
                return keyword
        return None
