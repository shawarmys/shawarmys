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

  def clean_value(self, value):
    if not value:
        return None

    # 1. Replace newlines and carriage returns with a single space
    value = re.sub(r'[\r\n]+', ' ', value)

    # 2. Remove leading/trailing whitespace, colons, and semicolons
    # The strip() characters include: space, tab, newline, colon, semicolon
    value = value.strip(' :;\t\n\r')

    # 3. Collapse multiple internal spaces into one
    value = re.sub(r'\s+', ' ', value)

    return value

  def find_match(self, full_text, search_term, regex_pattern):
    if search_term not in full_text:
        return None

    # 1. Split the entire text by the search term
    parts = full_text.split(search_term, 1)
    content_after = parts[1]

    # 2. Specific Regex Match
    if regex_pattern and regex_pattern != ".*":
        match = re.search(regex_pattern, content_after, re.MULTILINE | re.IGNORECASE)
        raw_value = match.group(0) if match else None

    # 3. Free Text / Remainder
    else:
        raw_value = content_after

    # Use the cleanup function for all returned values
    return self.clean_value(raw_value)

  def map_values_to_attributes(self, extracted_text):
    results = {}
    for key, value in self.config.items():
        search_term = value[0]
        regex = value[1]
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
