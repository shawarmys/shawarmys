import os
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).parent.parent.parent.resolve()
DEFAULT_DATA_FOLDER = PROJECT_ROOT / "data" / "Endtestdaten_ohne_Fehler_ einheitliche ID"


def resolve_data_folder() -> Path:
    """Resolve data folder from env var or project-root default."""
    print(f"Resolving data folder... {PROJECT_ROOT}")
    configured = os.getenv("DATA_FOLDER", DEFAULT_DATA_FOLDER)
    print(f"Using data folder: {configured}")
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_absolute():
            candidate = (PROJECT_ROOT / candidate).resolve()
    else:
        candidate = DEFAULT_DATA_FOLDER

    if not candidate.exists():
        raise FileNotFoundError(
            f"Data folder not found: {candidate}. "
            "Set DATA_FOLDER to an absolute path, or a path relative to project root."
        )
    return candidate

def clean_case_id(df: pd.DataFrame) -> pd.DataFrame:
    df["case_id"] = df["case_id"].str.replace("CASE-", "").astype(int)
    return df

def clean_patient_id(df: pd.DataFrame) -> pd.DataFrame:
    # If starts with PAT and followed by digits, remove the "PAT-" prefix and convert to int, otherwise only convert to int
    df["patient_id"] = df["patient_id"].apply(lambda x: int(x.replace("PAT-", "")) if isinstance(x, str) and x.startswith("PAT-") else int(x))
    return df

def parse_lab_results(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_case_id(df)
    df = clean_patient_id(df)
    return df

def parse_icd10(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_case_id(df)
    df = clean_patient_id(df)
    return df

def parse_device_motion(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_patient_id(df)
    return df

def parse_device_1hz_motion(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_patient_id(df)
    return df

def parse_medication_events(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_patient_id(df)
    return df

def parse_nursing_daily_reports(df: pd.DataFrame) -> pd.DataFrame:
    df = clean_case_id(df)
    df = clean_patient_id(df)
    return df

def main():
    data_folder = resolve_data_folder()
    dfs = {}
    # Iterate through all files in the data folder
    for file in os.listdir(data_folder):
        if file.endswith(".csv"):
            if file == "synth_labs_1000_cases.csv":
                df = pd.read_csv(data_folder / file)
                df = parse_lab_results(df)
                dfs["lab_results"] = df
            elif file == "synthetic_cases_icd10_ops.csv":
                df = pd.read_csv(data_folder / file)
                df = parse_icd10(df)
                dfs["icd10_data"] = df
            elif file == "synthetic_device_motion_fall_data.csv":
                df = pd.read_csv(data_folder / file)
                df = parse_device_motion(df)
                dfs["device_motions"] = df
            elif file == "synthetic_device_raw_1hz_motion_fall.csv":
                df = pd.read_csv(data_folder / file)
                df = parse_device_1hz_motion(df)
                dfs["device_1hz_motions"] = df
            elif file == "synthetic_medication_raw_inpatient.csv":
                df = pd.read_csv(data_folder / file)
                df = parse_medication_events(df)
                dfs["medication_events"] = df
            elif file == "synthetic_nursing_daily_reports_en.csv":
                df = pd.read_csv(data_folder / file)
                df = parse_nursing_daily_reports(df)
                dfs["nursing_daily_reports"] = df
    return dfs

if __name__ == "__main__":
    main()
