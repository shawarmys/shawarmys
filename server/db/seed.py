"""Helper module for inserting parsed DataFrames into the database."""

from parser.parser import main as parse_all

import pandas as pd
from common import DIRECT_MAPPING_TABLES, INDIRECT_MAPPING_TABLES
from db.create_mappings import create_direct_mappings, create_indirect_mappings
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


# Tables whose rows carry a case_id we can use in integration_mappings.
_MAPPING_COLUMNS: dict[str, str] = {
    "lab_results": "lab_results_id",
    "icd10_data": "icd10_data_id",
    "nursing_daily_reports": "nursing_daily_reports_id",
    "medication_events": "medication_events_id",
    "device_motions": "device_motions_id",
    "device_1hz_motions": "device_1hz_motions_id",
}


def build_integration_mappings():
    """
    Query every data table for its (id, case_id) pairs and insert one
    integration_mappings row per pair.  This gives a many-to-one view:
    one case can have many rows in each data table, all retrievable from
    the integration_mappings table.
    """
    with engine.begin() as conn:
        rows_to_insert = []
        for table_name, fk_col in _MAPPING_COLUMNS.items():
            pairs = conn.execute(
                text(f"SELECT id, case_id FROM {table_name} WHERE case_id IS NOT NULL")
            ).fetchall()
            for row_id, case_id in pairs:
                rows_to_insert.append({"case_id": case_id, fk_col: row_id})

        if rows_to_insert:
            # Build a single INSERT with all nullable FK columns
            conn.execute(
                text(
                    "INSERT INTO integration_mappings "
                    "(case_id, lab_results_id, icd10_data_id, "
                    "nursing_daily_reports_id, medication_events_id, "
                    "device_motions_id, device_1hz_motions_id) "
                    "VALUES (:case_id, :lab_results_id, :icd10_data_id, "
                    ":nursing_daily_reports_id, :medication_events_id, "
                    ":device_motions_id, :device_1hz_motions_id)"
                ),
                [
                    {
                        "case_id": r["case_id"],
                        "lab_results_id": r.get("lab_results_id"),
                        "icd10_data_id": r.get("icd10_data_id"),
                        "nursing_daily_reports_id": r.get("nursing_daily_reports_id"),
                        "medication_events_id": r.get("medication_events_id"),
                        "device_motions_id": r.get("device_motions_id"),
                        "device_1hz_motions_id": r.get("device_1hz_motions_id"),
                    }
                    for r in rows_to_insert
                ],
            )
            print(f"  ↳ inserted {len(rows_to_insert)} integration mapping(s)")


def seed_database():
    """Parse all CSVs and insert them into the database."""
    print("Parsing CSV files …")
    dfs = parse_all()

    if not dfs:
        print("No DataFrames returned by the parser.")
        return

    print(f"\nInserting {len(dfs)} dataset(s) into the database:\n")
    direct_mapping_dfs = {k: v for k, v in dfs.items() if k in DIRECT_MAPPING_TABLES}
    indirect_mapping_dfs = {k: v for k, v in dfs.items() if k in INDIRECT_MAPPING_TABLES}

    # 1. Upsert cases (from direct tables + icd10 dates)
    cases_df, alert_cases = create_direct_mappings(direct_mapping_dfs)

    # 2. Insert direct-mapping DataFrames
    for table_name, df in direct_mapping_dfs.items():
        print(f"📄 {table_name}  ({len(df)} rows)")
        insert_dataframe(df, table_name)

    # 3. Resolve case_id for indirect tables, then insert them
    resolved_indirect = create_indirect_mappings(indirect_mapping_dfs, cases_df)
    for table_name, df in resolved_indirect.items():
        print(f"📄 {table_name}  ({len(df)} rows)")
        insert_dataframe(df, table_name)

    # 4. Build and insert integration_mappings
    print("\nBuilding integration mappings …")
    build_integration_mappings()

    print("\n✅ Done — all data inserted.")


if __name__ == "__main__":
    seed_database()
