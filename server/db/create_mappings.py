import pandas as pd
from db.database import engine
from sqlalchemy import text

# Mappings:
# Direct tables (lab_results, icd10_data, nursing_daily_reports) have a case_id column.
# Indirect tables (device_motions, device_1hz_motions, medication_events) only have
# patient_id + timestamps — we infer the case by matching against admission/discharge.

# Which timestamp column to use per indirect table
INDIRECT_TIMESTAMP_COLS: dict[str, list[str]] = {
    "device_motions": ["timestamp"],
    "device_1hz_motions": ["timestamp"],
    "medication_events": ["admission_datetime", "discharge_datetime"],
}


def create_direct_mappings(direct_dfs: dict[str, pd.DataFrame]) -> [pd.DataFrame, list[int]]:
    """
    Collect all (case_id, patient_id) pairs across every direct-mapping DF,
    enrich with admission/discharge dates from ``icd10_data``, perform a
    single bulk insert into the ``cases`` table, and return the resulting
    cases DataFrame for downstream use.
    """
    # 1. Gather unique (case_id, patient_id) pairs from all direct DFs
    pair_frames = []
    for df in direct_dfs.values():
        if "case_id" in df.columns and "patient_id" in df.columns:
            pairs = (
                df[["case_id", "patient_id"]]
                .dropna(subset=["case_id"])
                .drop_duplicates(subset=["case_id"])
            )
            pair_frames.append(pairs)

    if not pair_frames:
        return pd.DataFrame(
            columns=["case_id", "patient_id", "admission_date", "discharge_date"]
        ), []

    cases_df = pd.concat(pair_frames).drop_duplicates(subset=["case_id"])
    cases_df["case_id"] = cases_df["case_id"].astype(int)
    cases_df["patient_id"] = cases_df["patient_id"].astype(int)

    # 2. Pull admission/discharge dates from icd10_data
    if "icd10_data" in direct_dfs:
        icd = direct_dfs["icd10_data"]
        if "admission_date" in icd.columns and "discharge_date" in icd.columns:
            dates = (
                icd[["case_id", "admission_date", "discharge_date"]]
                .dropna(subset=["case_id"])
                .drop_duplicates(subset=["case_id"])
            )
            dates["case_id"] = dates["case_id"].astype(int)
            cases_df = cases_df.merge(dates, on="case_id", how="left")

    # Ensure date columns exist even when icd10_data is absent
    alert_cases = []
    for col in ("admission_date", "discharge_date"):
        # create alert objects
        if col not in cases_df.columns:
            alert_cases.append(cases_df["case_id"])
            cases_df[col] = None

    # 3. Single bulk insert
    with engine.begin() as conn:
        existing = {
            row[0]
            for row in conn.execute(text("SELECT id FROM cases")).fetchall()
        }
        new_cases = cases_df[~cases_df["case_id"].isin(existing)]
        if not new_cases.empty:
            conn.execute(
                text(
                    "INSERT INTO cases (id, patient_id, admission_date, discharge_date) "
                    "VALUES (:id, :patient_id, :admission_date, :discharge_date)"
                ),
                [
                    {
                        "id": int(row.case_id),
                        "patient_id": int(row.patient_id),
                        "admission_date": (
                            row.admission_date
                            if pd.notna(row.admission_date)
                            else None
                        ),
                        "discharge_date": (
                            row.discharge_date
                            if pd.notna(row.discharge_date)
                            else None
                        ),
                    }
                    for _, row in new_cases.iterrows()
                ],
            )
            print(f"  ↳ inserted {len(new_cases)} case(s)")

    return cases_df, alert_cases


def create_indirect_mappings(
    indirect_dfs: dict[str, pd.DataFrame],
    cases_df: pd.DataFrame,
) -> dict[str, pd.DataFrame]:
    """
    cases_df: DataFrame with columns [case_id, patient_id, admission_date, discharge_date]
    For tables that lack a ``case_id``, infer the case by matching
    ``patient_id`` + a timestamp column against the admission/discharge
    range in *cases_df*.  Everything stays in-memory — no DB round-trips.

    Returns a dict of ``{table_name: DataFrame}`` where each DF has a
    ``case_id`` column added.
    """
    print("Creating indirect mappings …")
    cases = cases_df.copy()
    cases["admission_date"] = pd.to_datetime(cases["admission_date"]).dt.normalize()
    cases["discharge_date"] = (
        pd.to_datetime(cases["discharge_date"]).dt.normalize()
        + pd.Timedelta(hours=23, minutes=59, seconds=59)
    )

    result: dict[str, pd.DataFrame] = {}

    for table_name, df in indirect_dfs.items():
        print(f"Processing {table_name} with {len(df)} rows …")
        ts_cols = INDIRECT_TIMESTAMP_COLS.get(table_name)
        if ts_cols is None or any(ts_col not in df.columns for ts_col in ts_cols):
            print("colum doesnt exist or ts_col is none")
            result[table_name] = df
            continue

        df = df.copy()
        for ts_col in ts_cols:
            print(f" unparsed timesamps {df[ts_col]}")
            df[ts_col] = pd.to_datetime(df[ts_col])
            print(f" parsed timesamps {df[ts_col]}")

        # Merge with cases on patient_id (may fan out if patient has
        # multiple cases — the date filter below collapses it back).
        merged = df.merge(
            cases[["case_id", "patient_id", "admission_date", "discharge_date"]],
            on="patient_id",
            how="left",
        )
        print(f"  ↳ merged to cases, resulting in {len(merged)} rows")

        if len(merged) < len(df):
            print("  ↳ not all matching patient_id found in cases, skipping timestamp filtering")
            #alert


        if len(ts_cols) > 1:
            valid = merged[(merged[ts_cols[0]] >= merged["admission_date"])
            & (merged[ts_cols[1]] <= merged["discharge_date"])]
        else:
            valid = merged[
                (merged[ts_cols[0]] >= merged["admission_date"])
                & (merged[ts_cols[0]] <= merged["discharge_date"])
            ].drop(columns=["admission_date", "discharge_date"])

        print(f"  ↳ {table_name}: matched {len(valid)}/{len(df)} rows to cases")

        if len(valid) < len(df):
            print(f"  ↳ WARNING: {len(df) - len(valid)} rows in {table_name} could not be mapped to any case based on patient_id and timestamps")
            # alert
        result[table_name] = valid

    return result
