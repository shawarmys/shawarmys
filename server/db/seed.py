"""Helper module for inserting parsed DataFrames into the database."""

from parser.parser import main as parse_all

import pandas as pd
from common import DIRECT_MAPPING_TABLES, INDIRECT_MAPPING_TABLES
from db.database import engine
from sqlalchemy import text


def upsert_cases(
    case_ids: pd.Series,
    patient_ids: pd.Series,
    admission_dates: pd.Series | None = None,
    discharge_dates: pd.Series | None = None,
):
    """
    Ensure every unique case_id exists in the cases table.
    Uses the first patient_id found for each case_id.
    """
    data = {"case_id": case_ids, "patient_id": patient_ids}
    if admission_dates is not None:
        data["admission_date"] = admission_dates
    if discharge_dates is not None:
        data["discharge_date"] = discharge_dates

    df = pd.DataFrame(data).dropna(subset=["case_id"])
    unique = df.drop_duplicates(subset=["case_id"])
    if unique.empty:
        return

    has_dates = "admission_date" in unique.columns

    with engine.begin() as conn:
        existing = set(
            row[0] for row in conn.execute(text("SELECT id FROM cases")).fetchall()
        )
        new_rows = unique[~unique["case_id"].astype(int).isin(existing)]
        if not new_rows.empty:
            if has_dates:
                conn.execute(
                    text(
                        "INSERT INTO cases (id, patient_id, admission_date, discharge_date) "
                        "VALUES (:id, :patient_id, :admission_date, :discharge_date)"
                    ),
                    [
                        {
                            "id": int(row.case_id),
                            "patient_id": int(row.patient_id),
                            "admission_date": row.get("admission_date") or None,
                            "discharge_date": row.get("discharge_date") or None,
                        }
                        for _, row in new_rows.iterrows()
                    ],
                )
            else:
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

    df.to_sql(table_name, engine, if_exists="append", index=False, method="multi")
    print(f"  ↳ inserted {len(df)} rows into '{table_name}'")


def resolve_and_insert(table_name: str, df: pd.DataFrame):
    """Upsert parent rows (patients/cases) then insert the data."""
    if table_name in DIRECT_MAPPING_TABLES:
        admission = df["admission_date"] if "admission_date" in df.columns else None
        discharge = df["discharge_date"] if "discharge_date" in df.columns else None
        upsert_cases(df["case_id"], df["patient_id"], admission, discharge)
    elif table_name in INDIRECT_MAPPING_TABLES:
        pass

    insert_dataframe(df, table_name)


def is_db_empty() -> bool:
    """Return True if the cases table has no rows (i.e. DB has not been seeded)."""
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM cases")).scalar()
        return result == 0


def seed_database():
    """Parse all CSVs and insert them into the database."""
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
    seed_database()
