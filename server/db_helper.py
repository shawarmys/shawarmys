"""
Helper module for inserting parsed DataFrames into the database.

When run directly:
    python db_helper.py

It will parse all CSVs via the parser module and insert them into Postgres.
"""

import os
from parser.parser import main as parse_all

import model  # noqa: F401 — registers all models on Base.metadata
import pandas as pd
from database import Base  # noqa: E402
from sqlalchemy import create_engine, inspect, text

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://shawarmys:shawarmys@localhost:5432/shawarmys",
)

_engine = create_engine(DATABASE_URL)


def get_engine():
    return _engine


def ensure_tables():
    """Create all tables defined in the SQLAlchemy models (if they don't exist)."""
    Base.metadata.create_all(bind=_engine)
    ensure_files_table()
    ensure_file_tracking_columns()


# ── Which tables carry case_id / patient_id that need parent-row upserts ──

_HAS_CASE_AND_PATIENT = {"lab_results", "icd10_data", "nursing_daily_reports"}
_HAS_PATIENT_ONLY = {"device_motions", "device_1hz_motions", "medication_events"}

_FILE_METADATA_BY_TABLE: dict[str, tuple[str, str]] = {
    "lab_results": ("synth_labs_1000_cases.csv", "Lab Results"),
    "icd10_data": ("synthetic_cases_icd10_ops.csv", "ICD10"),
    "nursing_daily_reports": ("synthetic_nursing_daily_reports_en.csv", "Nursing Report"),
    "medication_events": ("synthetic_medication_raw_inpatient.csv", "Medication"),
    "device_motions": ("synthetic_device_motion_fall_data.csv", "Device Motion"),
    "device_1hz_motions": ("synthetic_device_raw_1hz_motion_fall.csv", "Device 1Hz Motion"),
    "tbImportAcData": ("epaAC-Data.csv", "Assessment"),
}


def create_file_record(table_name: str) -> int:
    """Create one row in files for this dataset and return the inserted ID."""
    file_type, origin_type = _FILE_METADATA_BY_TABLE.get(
        table_name,
        (f"{table_name}.csv", "Unknown"),
    )

    with _engine.begin() as conn:
        return conn.execute(
            text(
                """
                INSERT INTO files (file_type, origin_type)
                VALUES (:file_type, :origin_type)
                RETURNING id
                """
            ),
            {"file_type": file_type, "origin_type": origin_type},
        ).scalar_one()


def ensure_files_table():
    """Create files table explicitly for environments with stale metadata imports."""
    with _engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS files (
                    id BIGSERIAL PRIMARY KEY,
                    file_type VARCHAR(256) NOT NULL,
                    origin_type VARCHAR(256) NOT NULL
                )
                """
            )
        )


def ensure_file_tracking_columns():
    """Backfill file_id columns/FKs for existing DBs where tables already existed."""
    tracked_tables = [
        "lab_results",
        "icd10_data",
        "nursing_daily_reports",
        "medication_events",
        "device_motions",
        "device_1hz_motions",
        "tbImportAcData",
    ]

    inspector = inspect(_engine)
    with _engine.begin() as conn:
        for table_name in tracked_tables:
            if table_name not in inspector.get_table_names():
                continue

            existing_columns = {
                col["name"] for col in inspector.get_columns(table_name)
            }
            if "file_id" not in existing_columns:
                conn.execute(
                    text(f'ALTER TABLE "{table_name}" ADD COLUMN file_id BIGINT')
                )

            constraint_name = f"{table_name}_file_id_fkey"
            fk_exists = conn.execute(
                text(
                    "SELECT 1 FROM pg_constraint WHERE conname = :constraint_name LIMIT 1"
                ),
                {"constraint_name": constraint_name},
            ).scalar()

            if not fk_exists:
                conn.execute(
                    text(
                        f'ALTER TABLE "{table_name}" '
                        f'ADD CONSTRAINT "{constraint_name}" '
                        "FOREIGN KEY (file_id) REFERENCES files(id)"
                    )
                )


def upsert_patients(patient_ids: pd.Series):
    """
    Ensure every unique patient_id in the Series exists in the patients table.
    Inserts missing ones; ignores duplicates.
    """
    unique = patient_ids.dropna().unique()
    if len(unique) == 0:
        return

    with _engine.begin() as conn:
        existing = set(
            row[0]
            for row in conn.execute(text("SELECT id FROM patients")).fetchall()
        )
        new_ids = [int(pid) for pid in unique if int(pid) not in existing]
        if new_ids:
            conn.execute(
                text("INSERT INTO patients (id) VALUES (:id)"),
                [{"id": pid} for pid in new_ids],
            )
            print(f"  ↳ inserted {len(new_ids)} new patient(s)")


def upsert_cases(case_ids: pd.Series, patient_ids: pd.Series):
    """
    Ensure every unique case_id exists in the cases table.
    Uses the first patient_id found for each case_id.
    """
    df = pd.DataFrame({"case_id": case_ids, "patient_id": patient_ids}).dropna(
        subset=["case_id"]
    )
    unique = df.drop_duplicates(subset=["case_id"])
    if unique.empty:
        return

    with _engine.begin() as conn:
        existing = set(
            row[0] for row in conn.execute(text("SELECT id FROM cases")).fetchall()
        )
        new_rows = unique[~unique["case_id"].astype(int).isin(existing)]
        if not new_rows.empty:
            conn.execute(
                text("INSERT INTO cases (id, patient_id) VALUES (:id, :patient_id)"),
                [
                    {"id": int(row.case_id), "patient_id": int(row.patient_id)}
                    for _, row in new_rows.iterrows()
                ],
            )
            print(f"  ↳ inserted {len(new_rows)} new case(s)")


def insert_dataframe(df: pd.DataFrame, table_name: str):
    """
    Bulk-insert a DataFrame into the given table.
    Columns in the DataFrame must match column names in the DB table.
    An 'id' column (auto-increment PK) is dropped if present in the DF.
    """
    if "id" in df.columns:
        df = df.drop(columns=["id"])

    df.to_sql(table_name, _engine, if_exists="append", index=False, method="multi")
    print(f"  ↳ inserted {len(df)} rows into '{table_name}'")


def resolve_and_insert(table_name: str, df: pd.DataFrame):
    """Upsert parent rows (patients/cases) then insert the data."""
    if table_name in _HAS_CASE_AND_PATIENT:
        upsert_cases(df["case_id"], df["patient_id"])
    elif table_name in _HAS_PATIENT_ONLY:
        pass

    file_id = create_file_record(table_name)
    df = df.copy()
    df["file_id"] = file_id

    insert_dataframe(df, table_name)


def main():
    """Parse all CSVs and insert them into the database."""
    ensure_tables()

    print("Parsing CSV files …")
    dfs = parse_all()

    if not dfs:
        print("No DataFrames returned by the parser.")
        return

    print(f"\nInserting {len(dfs)} dataset(s) into the database:\n")
    for table_name, df in dfs.items():
        print(f"📄 {table_name}  ({len(df)} rows)")
        resolve_and_insert(table_name, df)
        print()

    print("✅ Done — all data inserted.")


if __name__ == "__main__":
    main()
