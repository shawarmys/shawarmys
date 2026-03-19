import pandas as pd
import numpy as np
import scipy.stats as stats
import re
import os
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
        return table_profile

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
        # ... (Same as previous implementation) ...
        return {"string": 1.0}


if __name__ == "__main__":
    # Example usage
    target_encoder = TargetSchemaEncoder()
    readme_path = os.path.join(os.path.dirname(__file__), 'csvFiles/goldStandard', 'clinic_1_device.csv')
    df_target = pd.read_csv(readme_path)
    target_profile = target_encoder.encode_target_table("target_table", df_target)
    for col, profile in target_profile["column_fingerprints"].items():
        print(f"Column: {col}")
        print(profile)
        print("-" * 40)
