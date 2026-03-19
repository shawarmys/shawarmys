from pathlib import Path

import pandas as pd

from misc.config_loader import load_fingerprints
from misc.data_cleaner.file_name_matcher import FileNameMatcher, FILE_KEYWORDS
from misc.data_cleaner.schemas import LABS_SCHEMA, ICD10_SCHEMA, DEVICE_MOTION_SCHEMA, DEVICE_RAW_1HZ_SCHEMA, \
    MEDICATION_SCHEMA, NURSING_SCHEMA

from misc.header_cleaner.error_detection.CsvExcelReader import CsvExcelReader


class DataCleaner:
    NULL_LIKE_TOKENS = {"null", "missing", "unknown", "nan", "n/a"}

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
        if self.file_type == "device_raw":
            pass
        # Depending on file type, apply schema
        df = CsvExcelReader(self.file_path).read_csv()
        schema = self.file_type_to_schema[self.file_type]
        df = self._map_null_like_values_for_nullable_columns(df, schema)
        schema.validate(df)
        return df

    def clean_data(self):
        if self.file_extension == 'csv':
            self.clean_csv()
        else:
            raise ValueError(f"Unsupported file type: {self.file_extension}")

if __name__ == "__main__":
    base_dir = Path(
        "C:/Users/trist/PycharmProjects/shawarmys/data/Endtestdaten_ohne_Fehler_ einheitliche ID"
    )

    for file_path in base_dir.iterdir():
        if not file_path.is_file():
            continue

        if file_path.suffix.lower() != ".csv":
            print(f"Skipping unsupported file type: {file_path.name}")
            continue

        print(f"\nProcessing: {file_path.name}")
        try:
            cleaner = DataCleaner(str(file_path))
            cleaner.clean_data()
        except Exception as exc:
            print(f"Failed on {file_path.name}: {exc}")
            continue