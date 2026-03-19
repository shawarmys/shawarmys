import pandas as pd
import numpy as np
import scipy.stats as stats
import json
import os
import csv
from Levenshtein import distance as lev_dist

class TargetSchemaEncoder:
    def __init__(self):
        self.gold_fingerprints = {}

    def encode_target_table(self, table_name, df):
        """Creates a deterministic fingerprint based on structure and metadata."""
        table_profile = {
            "table_metadata": {
                "column_count": len(df.columns),
                "ordered_headers": list(df.columns)
            },
            "column_fingerprints": {}
        }

        for col_name in df.columns:
            col_data = df[col_name]
            clean_data = col_data.dropna().astype(str)

            table_profile["column_fingerprints"][col_name] = {
                # 1. Header Anatomy
                "header_structure": self._profile_string_composition(col_name),

                # 2. Data Type & Nulls
                "expected_types": self._duck_type_waterfall(col_data),
                "is_nullable": col_data.isnull().any(),
                "null_markers_found": self._detect_null_strings(clean_data),

                # 3. Statistical DNA
                "cardinality_ratio": col_data.nunique() / len(df) if len(df) > 0 else 0,
                "entropy": self._calculate_shannon_entropy(col_data),

                # 4. Data Shape (Lengths)
                "length_stats": self._get_length_stats(clean_data),
                "has_leading_trailing_spaces": self._check_whitespace_noise(clean_data)
            }

        self.gold_fingerprints[table_name] = table_profile

        # Save the fingerprint for later use in mapping
        self.save_fingerprint(table_name)

    def save_fingerprint(self, table_name, directory='goldFingerPrints'):
        # This finds the directory where TargetSchemaEncoder.py actually lives
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Join that with your desired folder name
        target_path = os.path.join(script_dir, directory)
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path, f"{table_name}_fingerprint.json")
        with open(file_path, 'w') as f:
            json.dump(self.gold_fingerprints[table_name], f, indent=4, cls=NumpyEncoder)

    # --- Helper Methods for the Fingerprint ---

    def _profile_string_composition(self, text):
        """
        User Request: Compare count of numbers, chars, and symbols in headers.
        """
        return {
            "len": len(text),
            "digit_count": sum(c.isdigit() for c in text),
            "alpha_count": sum(c.isalpha() for c in text),
            "special_count": sum(not c.isalnum() for c in text),
            "space_count": sum(c.isspace() for c in text),
            "underscore_count": text.count('_'),
            "is_all_caps": text.isupper(),
            "is_snake_case": "_" in text and text.islower()
        }

    def _get_length_stats(self, clean_series):
        """Profiles the 'physical size' of the data in the column."""
        if clean_series.empty:
            return {"min": 0, "max": 0, "mean": 0}
        lengths = clean_series.str.len()
        return {
            "min": int(lengths.min()),
            "max": int(lengths.max()),
            "mean": float(lengths.mean())
        }

    def _detect_null_strings(self, clean_series):
        """Checks for 'human' nulls like 'N/A', 'None', 'NULL'."""
        null_patterns = ['n/a', 'nan', 'null', 'none', '-', '']
        matches = clean_series.str.lower().isin(null_patterns)
        return matches.mean() # Percentage of rows that are 'fake' nulls

    def _check_whitespace_noise(self, clean_series):
        """Detects if columns have messy trailing/leading spaces."""
        if clean_series.empty: return False
        return (clean_series.str.strip() != clean_series).any()

    def _calculate_shannon_entropy(self, col_data):
        if col_data.empty: return 0
        probabilities = col_data.value_counts(normalize=True)
        return stats.entropy(probabilities, base=2)

    def _duck_type_waterfall(self, col_data):
        if col_data.empty:
            return {"empty": 1.0}

        # Drop NaNs for the type detection sample so they don't skew results
        sample = col_data.dropna().head(100)
        total = len(sample)

        if total == 0:
            return {"nulls_only": 1.0}

        counts = {"int": 0, "float": 0, "datetime": 0, "bool": 0, "string": 0}

        for val in sample:
            # Convert to string once for checks
            s_val = str(val).strip()

            # 1. Boolean check (most specific)
            if s_val.lower() in ['true', 'false', 'yes', 'no']:
                counts["bool"] += 1

            # 2. Integer check
            elif s_val.isdigit() or (s_val.startswith('-') and s_val[1:].isdigit()):
                # Special case: '1' and '0' can be bool or int.
                # Usually, we treat them as int unless the whole column is 1/0.
                counts["int"] += 1

            # 3. Float check
            else:
                try:
                    float(s_val)
                    counts["float"] += 1
                except ValueError:
                    # 4. Datetime check
                    try:
                        # Avoid parsing simple numbers as dates
                        if len(s_val) > 4:
                            pd.to_datetime(s_val)
                            counts["datetime"] += 1
                        else:
                            counts["string"] += 1
                    except:
                        counts["string"] += 1

        return {k: v / total for k, v in counts.items()}


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.bool_, np.ndarray, np.generic)):
            return obj.item() # Converts numpy types to native python types
        return super(NumpyEncoder, self).default(obj)

if __name__ == "__main__":
    # Create FIngerprints for all csv and excel files in the 'goldStandard' directory
    target_encoder = TargetSchemaEncoder()
    gold_standard_dir = os.path.join(os.path.dirname(__file__), 'csvFiles/goldStandard')
    for filename in os.listdir(gold_standard_dir):
        if filename.endswith(('.csv', '.xlsx')):
            table_name = os.path.splitext(filename)[0]
            file_path = os.path.join(gold_standard_dir, filename)

            with open(file_path, 'r') as f:
                try:
                    dialect = csv.Sniffer().sniff(f.read(2048))
                    delimiter = dialect.delimiter
                except:
                    delimiter = ','


            if filename.endswith('.csv'):
                try:
                    # sep=None + engine='python' enables the "auto-sniffer"
                    df = pd.read_csv(
                        file_path,
                        sep=delimiter,
                        engine='python',
                        encoding='utf-8'
                    )
                except UnicodeDecodeError:
                    # Fallback for German/Windows-encoded files
                    df = pd.read_csv(
                        file_path,
                        sep=delimiter,
                        engine='python',
                        encoding='latin1'
                    )
                #try:
                #    df = pd.read_excel(file_path, engine=None)
                #except Exception as e:
                #    print(f"Error loading Excel file '{filename}': {e}")
                #    continue

            target_encoder.encode_target_table(table_name, df)
