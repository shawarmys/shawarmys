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
from sqlalchemy import create_engine, text

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


# ── Which tables carry case_id / patient_id that need parent-row upserts ──

_HAS_CASE_AND_PATIENT = {"lab_results", "icd10_data", "nursing_daily_reports"}
_HAS_PATIENT_ONLY = {"device_motions", "device_1hz_motions", "medication_events"}


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
