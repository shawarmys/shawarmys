import csv
import os

from Levenshtein import distance as lev_dist
import json
import pandas as pd
from TableSchemaEncoder import TableSchemaEncoder


class HeaderValidator:
    def __init__(self, gold_standard_fingerprint):
        self.gold = gold_standard_fingerprint
        self.gold_headers = self.gold["table_metadata"]["ordered_headers"]
        self.gold_col_count = self.gold["table_metadata"]["column_count"]
        self.header_error_indicators = {
            "completely_wrong": 0,
            "no_header_but_data": 0,
            "wrong_labels": 0,
        }

    def validate_header_row(self, incoming_row_1, incoming_row_2=None):
        """
        Analyzes Row 1 to determine its validity.
        Returns a detailed report with a likelihood score.
        """
        results = {
            "matchmaking_required": False,
            "message": "",
        }

        # Check if the first row exactly matches the gold standard headers
        if incoming_row_1 == self.gold_headers:
            results["matchmaking_required"] = False
            results["message"] = "Header row is valid and matches the gold standard."
            return results["matchmaking_required"], results["message"]

        # Check if the first row has the same headers but in a different order
        if sorted(incoming_row_1) == sorted(self.gold_headers):
            results["matchmaking_required"] = True
            results["message"] = "Header row has the correct headers but in a different order."
            return results["matchmaking_required"], results["message"]

        # Column Count Check
        incoming_col_count = len(incoming_row_1)
        count_diff = abs(incoming_col_count - self.gold_col_count)
        if count_diff > 0:
            self.header_error_indicators["column_count_mismatch"] += 1
            self.header_error_indicators["completely_wrong"] += 1

        # We check how many headers match their expected positions
        matches = 0
        total_dist = 0
        for i, header in enumerate(incoming_row_1):
            if i < len(self.gold_headers):
                dist = lev_dist(str(header), self.gold_headers[i])
                total_dist += dist
                if dist <= 2:
                    matches += 1
                else:
                    self.header_error_indicators["wrong_labels"] += 1
                    self.header_error_indicators["completely_wrong"] += 1

        match_ratio = matches / self.gold_col_count if self.gold_col_count > 0 else 0
        if match_ratio < 0.5:
            self.header_error_indicators["completely_wrong"] += 1

        # Composition Check (Is Row 1 actually Data?)
        row1_composition = self._get_composition(incoming_row_1)
        is_numeric_heavy = row1_composition["digit_count"] > row1_composition["alpha_count"]
        if is_numeric_heavy:
            self.header_error_indicators["no_header_but_data"] += 1

        # 4. Compare Row 1 vs Row 2
        is_row1_data_like = False
        if incoming_row_2:
            row2_composition = self._get_composition(incoming_row_2)
            # If Row 1 and Row 2 look almost identical structurally, Row 1 is likely data
            if self._compositions_are_similar(row1_composition, row2_composition):
                is_row1_data_like = True
                self.header_error_indicators["no_header_but_data"] += 1

        # Error suggestions based on indicators
        if self.header_error_indicators["no_header_but_data"] > 0:
            results["message"] = "Row 1 appears to contain data, not headers."
            return True, results["message"]

        if self.header_error_indicators["completely_wrong"] > 0:
            results["message"] = "Header row is completely wrong. Consider using matchmaking to reorder/rename columns."
            return True, results["message"]

        if self.header_error_indicators["wrong_labels"] > 0:
            results["message"] = "Header row has wrong labels. Consider using matchmaking to reorder/rename columns."
            return True, results["message"]

        results["message"] = "Header row has some issues but is not completely wrong. Consider reviewing the headers."
        return True, results["message"]

    def _get_composition(self, row):
        """Aggregated composition of an entire row."""
        text = "".join(map(str, row))
        return {
            "digit_count": sum(c.isdigit() for c in text),
            "alpha_count": sum(c.isalpha() for c in text),
            "special_count": sum(not c.isalnum() for c in text)
        }

    def _compositions_are_similar(self, comp1, comp2, tolerance=0.15):
        """Checks if two rows share a similar 'DNA' of characters."""
        total1 = sum(comp1.values()) or 1
        total2 = sum(comp2.values()) or 1

        # Compare ratios of digits/alphas
        d1, d2 = comp1["digit_count"]/total1, comp2["digit_count"]/total2
        a1, a2 = comp1["alpha_count"]/total1, comp2["alpha_count"]/total2

        return abs(d1 - d2) < tolerance and abs(a1 - a2) < tolerance

if __name__ == "__main__":
    # Example usage

    # Load a gold standard fingerprint (this would be created by TargetSchemaEncoder)
    with open('C:\\Users\\marti\\Documents\\shawarmys\\server\\error_handler\\error_detection\\goldFingerPrints\\synthetic_device_raw_1hz_motion_fall_fingerprint.json', 'r') as f:
        gold_fingerprint = json.load(f)

    # Get the data from the input file and create the TargetScshemaEncoder fingerprint
    target_encoder = TargetSchemaEncoder()
    file_path = 'C:\\Users\\marti\\Documents\\shawarmys\\server\\error_handler\\error_detection\\csvFiles\\errorousFiles\\NoHeader_synth_device_raw_1hz_motion_fall.csv'

    with open(file_path, 'r') as f:
        try:
            dialect = csv.Sniffer().sniff(f.read(2048))
            delimiter = dialect.delimiter
        except:
            delimiter = ','

    try:
        df = pd.read_csv(
            file_path,
            sep=delimiter,
            engine='python',
            encoding='utf-8',
            dayfirst=False,
            on_bad_lines='warn'
        )
    except UnicodeDecodeError:
        # Fallback for German/Windows-encoded files
        df = pd.read_csv(
            file_path,
            sep=delimiter,
            engine='python',
            encoding='latin1',
            dayfirst=False,
            on_bad_lines='warn'
        )
    #try:
    #    df = pd.read_excel(file_path, engine=None)
    #except Exception as e:
    #    print(f"Error loading Excel file '{filename}': {e}")
    #    continue
    table_profile = target_encoder.encode_target_table(os.path.basename(file_path), df)

    # Validate the header row
    header_validator = HeaderValidator(gold_fingerprint)
    validation_result = header_validator.validate_header_row(df.columns.tolist(), df.iloc[1].tolist() if len(df) > 1 else None)

    # Print the validation results
    print(json.dumps(validation_result, indent=4))
