import argparse
import json
import tempfile
from pathlib import Path
from typing import Tuple

import pandas as pd
from pandera.errors import SchemaErrors

from misc.config_loader import load_fingerprints
from misc.data_cleaner.file_name_matcher import FileNameMatcher, FILE_KEYWORDS
from misc.data_cleaner.schemas import (
    LABS_SCHEMA, ICD10_SCHEMA, DEVICE_MOTION_SCHEMA, DEVICE_RAW_1HZ_SCHEMA,
    MEDICATION_SCHEMA, NURSING_SCHEMA,
    EPAC_DATA_1_SCHEMA, EPAC_DATA_2_SCHEMA, EPAC_DATA_3_SCHEMA,
    EPAC_DATA_4_SCHEMA, EPAC_DATA_5_SCHEMA
)

from misc.header_cleaner.error_detection.CsvExcelReader import CsvExcelReader


class DataCleaner:
    NULL_LIKE_TOKENS = {
        "null", "missing", "unknown", "nan", "n/a", "",
        "00.00.0000", "00:00:00", "0000-00-00"
    }

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_extension = self.get_file_extension(self.file_path)
        self.file_type = FileNameMatcher.match_file_name(Path(file_path).name)
        if self.file_type == None:
            raise Exception
        self.fingerprints = load_fingerprints()
        self.file_type_to_schema = {
            "labs": LABS_SCHEMA,
            "icd": ICD10_SCHEMA,
            "device": DEVICE_MOTION_SCHEMA,
            "device_1hz": DEVICE_RAW_1HZ_SCHEMA,
            "medication": MEDICATION_SCHEMA,
            "nursing": NURSING_SCHEMA,
            "epac_data_1": EPAC_DATA_1_SCHEMA,
            "epac_data_2": EPAC_DATA_2_SCHEMA,
            "epac_data_3": EPAC_DATA_3_SCHEMA,
            "epac_data_4": EPAC_DATA_4_SCHEMA,
            "epac_data_5": EPAC_DATA_5_SCHEMA,
        }

    def get_file_extension(self, file_path: str) -> str:
        filename = file_path.split('/')[-1]  # Get the last part of the path
        if '.' in filename:
            return filename.split('.')[-1].lower()  # Return the extension in lowercase
        else:
            return ''  # No extension found

    def _map_null_like_values_for_nullable_columns(self, df: pd.DataFrame, schema) -> pd.DataFrame:
        out = df.copy()

        nullable_columns = [
            col_name
            for col_name, col_schema in schema.columns.items()
            if col_schema.nullable and col_name in out.columns
        ]

        for col_name in nullable_columns:
            original = out[col_name]
            normalized = original.astype("string").str.strip()
            is_null_like = normalized.str.lower().isin(self.NULL_LIKE_TOKENS) | normalized.eq("")
            out[col_name] = original.mask(is_null_like, pd.NA)

        return out

    def clean_csv(self):
        print(f"Cleaning CSV file: {self.file_path}")
        # Depending on file type, apply schema
        df = CsvExcelReader(self.file_path).read_csv()
        schema = self.file_type_to_schema[self.file_type]
        df = self._map_null_like_values_for_nullable_columns(df, schema)

        try:
            # Use lazy=True to collect ALL errors instead of failing on first
            schema.validate(df, lazy=True)
            print(f"✓ Validation passed")
            return df, None

        except SchemaErrors as e:
            errors = self._extract_validation_errors_from_schema_errors(e)
            print(f"✗ Validation failed with {len(errors['errors'])} error(s)")
            return None, errors

    def _extract_validation_errors_from_schema_errors(self, schema_errors):
        """Extract errors from a SchemaErrors exception (lazy validation)."""
        all_errors = []
        for schema_error in schema_errors.schema_errors:
            error_info = self._extract_single_error(schema_error)
            all_errors.append(error_info)

        return {
            "errors": all_errors,
            "error_count": len(all_errors)
        }

    def _extract_single_error(self, schema_error):
        """Extract a single SchemaError into structured format."""
        # Pandera SchemaError stores the message as a string representation
        # Access attributes that actually exist: check, reason_code, failure_cases
        error_str = str(schema_error)

        return {
            #"message": error_str,  # The full error message from string conversion
            "reason_code": getattr(schema_error, 'reason_code', None),
            #"check": getattr(schema_error, 'check', None),
            "column": getattr(schema_error, 'column', None),
            "row": getattr(schema_error, 'row', None),  # added
            "failure_cases": str(schema_error.failure_cases) if hasattr(schema_error,
                                                                        'failure_cases') and schema_error.failure_cases is not None else None
        }

    def clean_data(self) -> Tuple[pd.DataFrame, any]:
        if self.file_extension == 'csv':
            return self.clean_csv()
        else:
            raise ValueError(f"Unsupported file type: {self.file_extension}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean and validate EPAC/Labs/Device CSV/XLSX files"
    )
    parser.add_argument(
        "--file_path",
        type=str,
        help="Path to CSV to clean"
    )

    args = parser.parse_args()

    df, errors = DataCleaner(args.file_path).clean_data()

    # TODO: Save CSV, Save JSON with errors, return by printing with delimiter ';'
    errors_path = None
    if errors is not None:
        with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".json",
                prefix="errors_",
                delete=False,
        ) as tmp_json:
            json.dump(errors, tmp_json, ensure_ascii=False, indent=2, default=str)
            errors_path = tmp_json.name

    csv_path = None
    if df is not None:
        with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".csv",
                prefix="cleaned_",
                delete=False,
                newline=""
        ) as tmp_csv:
            df.to_csv(tmp_csv.name, index=False)
            csv_path = tmp_csv.name
    else:
        csv_path = args.file_path

    print(csv_path + ";" + errors_path)