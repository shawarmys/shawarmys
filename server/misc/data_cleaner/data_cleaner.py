import argparse
import json
import tempfile
from pathlib import Path
from typing import Tuple

import pandas as pd

from misc.config_loader import load_fingerprints
from misc.data_cleaner.adjusted_boxplot import adjusted_boxplot
from misc.data_cleaner.file_name_matcher import FileNameMatcher, FILE_KEYWORDS
from misc.data_cleaner.iqr import get_outliers
from misc.data_cleaner.schemas import (
    LABS_SCHEMA, ICD10_SCHEMA, DEVICE_MOTION_SCHEMA, DEVICE_RAW_1HZ_SCHEMA,
    MEDICATION_SCHEMA, NURSING_SCHEMA,
    EPAC_DATA_1_SCHEMA, EPAC_DATA_2_SCHEMA, EPAC_DATA_3_SCHEMA,
    EPAC_DATA_4_SCHEMA, EPAC_DATA_5_SCHEMA
)
from misc.header_cleaner.CsvExcelReader import CsvExcelReader


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

    def _preprocess_ids(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
        out = df.copy()

        for col in out.columns:
            col_l = col.lower()
            if "case_id" in col_l or "patient_id" in col_l or "fallid" in col_l:
                s = out[col].astype("string").str.strip()

                if "case_id" in col_l or "fallid" in col_l:
                    s = s.str.replace(r"(?i)^case-", "", regex=True)
                if "patient_id" in col_l:
                    s = s.str.replace(r"(?i)^pat-", "", regex=True)

                # Nullable integer dtype: invalid parses become <NA>
                out[col] = pd.to_numeric(s, errors="coerce").astype("Int64")

        # Track rows with null IDs
        id_issues = []
        case_cols = [c for c in out.columns if "case_id" in c.lower() or "fallid" in c.lower()]
        patient_cols = [c for c in out.columns if "patient_id" in c.lower()]

        if case_cols and patient_cols:
            col_to_idx = {name: int(i) for i, name in enumerate(out.columns)}

            # Check if any case_id/fallid OR patient_id is null
            rows_with_null_ids = out[case_cols + patient_cols].isna().any(axis=1)

            for row_idx in out[rows_with_null_ids].index:
                null_cols = []
                for col in case_cols + patient_cols:
                    if pd.isna(out.loc[row_idx, col]):
                        null_cols.append(f"{col} (col {col_to_idx[col]})")

                id_issues.append({
                    "row": int(row_idx),
                    "column": None,
                    "header": None,
                    "value": None,
                    "error": "missing_required_id",
                    "message": f"Row dropped: null ID value(s) in {', '.join(null_cols)}"
                })

            # Drop rows with null IDs
            if rows_with_null_ids.sum() > 0:
                print(f"Dropping {rows_with_null_ids.sum()} row(s) with null ID values")
                out = out[~rows_with_null_ids].reset_index(drop=True)

        return out, id_issues

    def clean_csv(self):
        print(f"Cleaning CSV file: {self.file_path}")
        # Depending on file type, apply schema
        df = CsvExcelReader(self.file_path).read_csv()
        schema = self.file_type_to_schema[self.file_type]
        df = self._map_null_like_values_for_nullable_columns(df, schema)
        df, issues = self._preprocess_ids(df)
        schema_cols = [c for c in schema.columns.keys() if c in df.columns]
        col_to_idx = {name: int(i) for i, name in enumerate(df.columns)}

        for row_idx, row in df.iterrows():
            for col in schema_cols:
                col_schema = schema.columns[col]
                value = row[col]
                col_idx = col_to_idx[col]

                if pd.isna(value):
                    issues.append({
                        "row": int(row_idx),
                        "column": col_idx,
                        "header": col,
                        "value": None,
                        "error": "null_value",
                        "message": "Empty value"
                    })
                    continue
                expected = str(col_schema.dtype).lower()

                try:
                    if "datetime" in expected:
                        pd.to_datetime([value], errors="raise", dayfirst=True)
                    elif "int" in expected:
                        num = pd.to_numeric([value], errors="raise")[0]

                        if pd.isna(num) or float(num) != int(num):
                            raise ValueError("not an integer value")
                    elif "float" in expected:
                        pd.to_numeric([value], errors="raise")
                    elif "bool" in expected:
                        if str(value).strip().lower() not in {"true", "false", "0", "1"}:
                            raise ValueError("not a boolean-like value")
                    else:
                        str(value)
                except Exception as e:
                    issues.append({
                        "row": int(row_idx),
                        "column": col_idx,
                        "header": col,
                        "value": str(value),
                        "error": "type_conversion_failed",
                        "message": self._normalize_error_message(str(e)),
                    })
        outliers_per_column = adjusted_boxplot(df)  # { "col_name": [row_idx, ...], ... }

        for col, row_indices in outliers_per_column.items():
            col_idx = col_to_idx.get(col)
            for row_idx in row_indices:
                value = df.at[row_idx, col]
                issues.append({
                    "row": int(row_idx),
                    "column": col_idx,
                    "header": col,
                    "value": None if pd.isna(value) else str(value),
                    "error": "outlier",
                    "message": "Outlier Value",
                })
        return {"df": df, "errors": issues, "error_count": len(issues)}

    def _normalize_error_message(self, error_msg: str) -> str:
        """Remove pandas-specific context like 'at position 0' from error messages."""
        import re
        # Strip " at position \d+" suffix
        normalized = re.sub(r'\s+at position\s+\d+\s*$', '', error_msg)
        return normalized.strip()

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
    parser.add_argument(
        "--json",
        required=False,
        action="store_true",
        help="Whether to dump CSV to JSON"
    )

    args = parser.parse_args()

    out = DataCleaner(args.file_path).clean_data()

    df = out["df"]
    errors = out["errors"]
    errors_path = ""
    csv_path = ""
    json_path = ""
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

    if df is not None:
        if args.json:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".json",
                prefix="cleaned_",
                delete=False,
                newline=""
            ) as tmp_json:
                df.to_json(tmp_json.name, index=False)
                json_path = tmp_json.name

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

    print(csv_path + ";" + errors_path + ";" + json_path)