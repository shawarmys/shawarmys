"""Helper module for inserting parsed DataFrames into the database."""
from common.constants import FILE_METADATA_BY_TABLE
from parser.parser import main as parse_all

import pandas as pd
from common import DIRECT_MAPPING_TABLES, INDIRECT_MAPPING_TABLES
from db.database import engine, Base
from sqlalchemy import text, inspect


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

    inspector = inspect(engine)
    with engine.begin() as conn:
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


def ensure_case_columns():
    """Backfill case date columns for DBs created before case model changes."""
    with engine.begin() as conn:
        conn.execute(
            text("ALTER TABLE cases ADD COLUMN IF NOT EXISTS admission_date DATE")
        )
        conn.execute(
            text("ALTER TABLE cases ADD COLUMN IF NOT EXISTS discharge_date DATE")
        )


def ensure_tables():
    """Create all tables defined in the SQLAlchemy models (if they don't exist)."""
    Base.metadata.create_all(bind=engine)
    ensure_case_columns()
    ensure_files_table()
    ensure_file_tracking_columns()

def infer_source_from_filename(file_name: str) -> str:
    """Infer source token from filename, falling back to a labeled unknown value."""
    stem = file_name.rsplit(".", 1)[0].strip().lower()
    if not stem:
        return "Unknown"

    # Common dataset prefixes we currently use.
    if stem.startswith("synthetic"):
        return "synthetic"
    if stem.startswith("synth"):
        return "synth"

    return "Unknown"

def create_file_record(table_name: str, row_count: int) -> int:
    """Create one row in files for this dataset and return the inserted ID."""
    file_name, source, group_type = FILE_METADATA_BY_TABLE.get(
        table_name,
        (f"{table_name}.csv", "Unknown", "Unknown"),
    )
    file_type = file_name.rsplit(".", 1)[-1].lower() if "." in file_name else "csv"
    inferred_source = infer_source_from_filename(file_name)
    resolved_source = inferred_source if inferred_source != "Unknown" else source

    with engine.begin() as conn:
        return conn.execute(
            text(
                """
                INSERT INTO files (
                    name,
                    source,
                    group_type,
                    entries,
                    records,
                    type,
                    file_type,
                    origin_type
                )
                VALUES (
                    :name,
                    :source,
                    :group_type,
                    :entries,
                    :records,
                    :type,
                    :file_type,
                    :origin_type
                )
                RETURNING id
                """
            ),
            {
                "name": file_name,
                "source": resolved_source,
                "group_type": group_type,
                "entries": row_count,
                "records": row_count,
                "type": file_type,
                "file_type": file_type,
                "origin_type": group_type,
            },
        ).scalar_one()

def ensure_files_table():
    """Create files table explicitly for environments with stale metadata imports."""
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS files (
                    id BIGSERIAL PRIMARY KEY,
                    name VARCHAR(512) NOT NULL,
                    source VARCHAR(256) NOT NULL,
                    group_type VARCHAR(256) NOT NULL,
                    entries INTEGER NOT NULL,
                    records INTEGER NOT NULL,
                    type VARCHAR(16) NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT NOW()
                )
                """
            )
        )

        # Backfill columns for older files schema variants.
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS name VARCHAR(512)"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS source VARCHAR(256)"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS group_type VARCHAR(256)"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS file_type VARCHAR(256)"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS origin_type VARCHAR(256)"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS entries INTEGER"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS records INTEGER"))
        conn.execute(text("ALTER TABLE files ADD COLUMN IF NOT EXISTS type VARCHAR(16)"))
        conn.execute(
            text(
                "ALTER TABLE files ADD COLUMN IF NOT EXISTS created_at "
                "TIMESTAMP NOT NULL DEFAULT NOW()"
            )
        )

        conn.execute(
            text(
                """
                UPDATE files
                SET
                    name = COALESCE(name, source, 'unknown.csv'),
                    source = COALESCE(source, 'Unknown'),
                    group_type = COALESCE(group_type, 'Unknown'),
                    file_type = COALESCE(file_type, type, 'csv'),
                    origin_type = COALESCE(origin_type, group_type, 'Unknown'),
                    entries = COALESCE(entries, 0),
                    records = COALESCE(records, 0),
                    type = COALESCE(type, 'csv')
                WHERE name IS NULL
                   OR source IS NULL
                   OR group_type IS NULL
                   OR file_type IS NULL
                   OR origin_type IS NULL
                   OR entries IS NULL
                   OR records IS NULL
                   OR type IS NULL
                """
            )
        )

        conn.execute(text("ALTER TABLE files ALTER COLUMN name SET NOT NULL"))
        conn.execute(text("ALTER TABLE files ALTER COLUMN source SET NOT NULL"))
        conn.execute(text("ALTER TABLE files ALTER COLUMN group_type SET NOT NULL"))
        conn.execute(text("ALTER TABLE files ALTER COLUMN entries SET NOT NULL"))
        conn.execute(text("ALTER TABLE files ALTER COLUMN records SET NOT NULL"))
        conn.execute(text("ALTER TABLE files ALTER COLUMN type SET NOT NULL"))


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

    file_id = create_file_record(table_name, len(df))
    df = df.copy()
    df["file_id"] = file_id

    insert_dataframe(df, table_name)


def is_db_empty() -> bool:
    """Return True if the cases table has no rows (i.e. DB has not been seeded)."""
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM cases")).scalar()
        return result == 0


def seed_database():
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
    seed_database()
