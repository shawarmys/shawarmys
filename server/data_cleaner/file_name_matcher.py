class FileNameMatcher:
    @staticmethod
    def match_file_name(file_name: str) -> str:
        keywords = ["device", "device_1hz", "epaAC", "icd", "labs", "medication", "nursing"]
        for keyword in keywords:
            if keyword in file_name.lower():
                return keyword
        return None
