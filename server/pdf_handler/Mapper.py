import json
import re
import os

from TextExtractor import TextExtractor

class Mapper:
    def __init__(self):
        self.config = {}

    def read_filename(self, file_path):
        # Using os.path for cross-platform compatibility (Windows vs Mac/Linux)
        return os.path.splitext(os.path.basename(file_path))[0]

    def load_schema(self, schema_name):
        # Ensure the directory exists or handle the path correctly
        path = f"FileSchemas/{schema_name}.json"
        with open(path, "r") as f:
            self.config = json.load(f)

    def find_match(self, text, search_term, regex_pattern):
        for line in text.split("\n"):
            if search_term in line:
                # 1. Get everything AFTER the search term
                # We split by the term and take the last part
                parts = line.split(search_term, 1)
                content_after_term = parts[1].strip()

                # Remove leading colons or spaces common in PDFs
                content_after_term = re.sub(r'^[:\s]+', '', content_after_term)

                # 2. If regex is empty, return the rest of the line
                if not regex_pattern:
                    print(f"{search_term}Content after term:")
                    print(content_after_term)
                    return content_after_term

                # 3. Apply regex to the remaining string
                match = re.search(regex_pattern, content_after_term, re.IGNORECASE)
                if match:
                    return match.group(0)

        return None

    def map_data(self, extracted_text):
        """Helper method to run the whole schema against the text"""
        results = {}
        for key, (search_term, regex) in self.config.items():
            results[key] = self.find_match(extracted_text, search_term, regex)
        return results


if __name__ == "__main__":
    # 1. Extract text
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "clinic_4_nursing.pdf")
    extractor = TextExtractor(file_path)
    raw_text = extractor.extract_text()

    # 2. Map data
    mapper = Mapper()
    mapper.load_schema("nursing_config")
    final_data = mapper.map_data(raw_text)

    print(final_data)
