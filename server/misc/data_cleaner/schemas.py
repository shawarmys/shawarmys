"""Pandera schemas derived from fingerprint files."""

import pandera.pandas as pa

from misc.config_loader import load_fingerprints
from pandera.engines.pandas_engine import DateTime as PanderaDateTime

EPAC_COLUMN_OVERRIDES = {
    "epaAC-Data-2_fingerprint": {
        "EPA0002": pa.Column(str, nullable=False),  # observed value "A"
    },
    # add more as you discover them
}

LABS_SCHEMA = pa.DataFrameSchema(
    {
        "case_id": pa.Column(str, nullable=False),
        "patient_id": pa.Column(int, nullable=False),
        "sex": pa.Column(str, nullable=True),
        "age_years": pa.Column(int, nullable=True),
        "specimen_datetime": pa.Column(pa.DateTime, nullable=True),

        "sodium_mmol_L": pa.Column(float, nullable=True),
        "sodium_flag": pa.Column(str, nullable=True),
        "sodium_ref_low": pa.Column(int, nullable=True),
        "sodium_ref_high": pa.Column(int, nullable=True),

        "potassium_mmol_L": pa.Column(float, nullable=True),
        "potassium_flag": pa.Column(str, nullable=True),
        "potassium_ref_low": pa.Column(float, nullable=True),
        "potassium_ref_high": pa.Column(float, nullable=True),

        "creatinine_mg_dL": pa.Column(float, nullable=True),
        "creatinine_flag": pa.Column(str, nullable=True),
        "creatinine_ref_low": pa.Column(float, nullable=True),
        "creatinine_ref_high": pa.Column(float, nullable=True),

        "egfr_mL_min_1_73m2": pa.Column(float, nullable=True),
        "egfr_flag": pa.Column(str, nullable=True),
        "egfr_ref_low": pa.Column(int, nullable=True),
        "egfr_ref_high": pa.Column(int, nullable=True),

        "glucose_mg_dL": pa.Column(float, nullable=True),
        "glucose_flag": pa.Column(str, nullable=True),
        "glucose_ref_low": pa.Column(int, nullable=True),
        "glucose_ref_high": pa.Column(int, nullable=True),

        "hemoglobin_g_dL": pa.Column(float, nullable=True),
        "hb_flag": pa.Column(str, nullable=True),
        "hb_ref_low": pa.Column(float, nullable=True),
        "hb_ref_high": pa.Column(float, nullable=True),

        "wbc_10e9_L": pa.Column(float, nullable=True),
        "wbc_flag": pa.Column(str, nullable=True),
        "wbc_ref_low": pa.Column(float, nullable=True),
        "wbc_ref_high": pa.Column(float, nullable=True),

        "platelets_10e9_L": pa.Column(float, nullable=True),
        "platelets_flag": pa.Column(str, nullable=True),
        "plt_ref_low": pa.Column(int, nullable=True),
        "plt_ref_high": pa.Column(int, nullable=True),

        "crp_mg_L": pa.Column(float, nullable=True),
        "crp_flag": pa.Column(str, nullable=True),
        "crp_ref_low": pa.Column(float, nullable=True),
        "crp_ref_high": pa.Column(float, nullable=True),

        "alt_U_L": pa.Column(float, nullable=True),
        "alt_flag": pa.Column(str, nullable=True),
        "alt_ref_low": pa.Column(int, nullable=True),
        "alt_ref_high": pa.Column(int, nullable=True),

        "ast_U_L": pa.Column(float, nullable=True),
        "ast_flag": pa.Column(str, nullable=True),
        "ast_ref_low": pa.Column(int, nullable=True),
        "ast_ref_high": pa.Column(int, nullable=True),

        "bilirubin_mg_dL": pa.Column(float, nullable=True),
        "bilirubin_flag": pa.Column(str, nullable=True),
        "bili_ref_low": pa.Column(float, nullable=True),
        "bili_ref_high": pa.Column(float, nullable=True),

        "albumin_g_dL": pa.Column(float, nullable=True),
        "albumin_flag": pa.Column(str, nullable=True),
        "albumin_ref_low": pa.Column(float, nullable=True),
        "albumin_ref_high": pa.Column(float, nullable=True),

        "inr": pa.Column(float, nullable=True),
        "inr_flag": pa.Column(str, nullable=True),
        "inr_ref_low": pa.Column(float, nullable=True),
        "inr_ref_high": pa.Column(float, nullable=True),

        "lactate_mmol_L": pa.Column(float, nullable=True),
        "lactate_flag": pa.Column(str, nullable=True),
        "lactate_ref_low": pa.Column(float, nullable=True),
        "lactate_ref_high": pa.Column(float, nullable=True),
    },
    strict=True,
    coerce=True,
    ordered=True,
)

ICD10_SCHEMA = pa.DataFrameSchema(
    {
        "case_id": pa.Column(str, nullable=False),
        "patient_id": pa.Column(str, nullable=False),

        "ward": pa.Column(str, nullable=True),
        "admission_date": pa.Column(pa.DateTime, nullable=True),
        "discharge_date": pa.Column(pa.DateTime, nullable=True),
        "length_of_stay_days": pa.Column(int, nullable=True),

        "primary_icd10_code": pa.Column(str, nullable=True),
        "primary_icd10_description_en": pa.Column(str, nullable=True),
        "secondary_icd10_codes": pa.Column(str, nullable=True),
        "secondary_icd10_descriptions_en": pa.Column(str, nullable=True),
        "ops_codes": pa.Column(str, nullable=True),
        "ops_descriptions_en": pa.Column(str, nullable=True),
    },
    strict=True,
    coerce=True,
    ordered=True,
)

DEVICE_MOTION_SCHEMA = pa.DataFrameSchema(
    {
        "patient_id": pa.Column(str, nullable=False),
        "timestamp": pa.Column(pa.DateTime, nullable=True),
        "movement_index_0_100": pa.Column(float, nullable=True),
        "micro_movements_count": pa.Column(int, nullable=True),
        "bed_exit_detected_0_1": pa.Column(int, nullable=True),
        "fall_event_0_1": pa.Column(int, nullable=True),
        "impact_magnitude_g": pa.Column(float, nullable=True),
        "post_fall_immobility_minutes": pa.Column(float, nullable=True),
    },
    strict=True,
    coerce=True,
    ordered=True,
)

DEVICE_RAW_1HZ_SCHEMA = pa.DataFrameSchema(
    {
        "patient_id": pa.Column(str, nullable=False),
        "device_id": pa.Column(str, nullable=False),  # Changed from nullable=True
        "timestamp": pa.Column(pa.DateTime, nullable=False),  # Changed from nullable=True
        "bed_occupied_0_1": pa.Column(int, nullable=False),  # Changed from nullable=True
        "movement_score_0_100": pa.Column(float, nullable=False),  # Changed from nullable=True
        "accel_x_m_s2": pa.Column(float, nullable=False),  # Changed from nullable=True
        "accel_y_m_s2": pa.Column(float, nullable=False),  # Changed from nullable=True
        "accel_z_m_s2": pa.Column(float, nullable=False),  # Changed from nullable=True
        "accel_magnitude_g": pa.Column(float, nullable=False),  # Changed from nullable=True
        "pressure_zone1_0_100": pa.Column(float, nullable=False),  # Changed from nullable=True
        "pressure_zone2_0_100": pa.Column(float, nullable=False),  # Changed from nullable=True
        "pressure_zone3_0_100": pa.Column(float, nullable=False),  # Changed from nullable=True
        "pressure_zone4_0_100": pa.Column(float, nullable=False),  # Changed from nullable=True
        "bed_exit_event_0_1": pa.Column(int, nullable=False),  # Changed from nullable=True
        "bed_return_event_0_1": pa.Column(int, nullable=False),  # Changed from nullable=True
        "fall_event_0_1": pa.Column(int, nullable=False),  # Changed from nullable=True
        "impact_magnitude_g": pa.Column(float, nullable=True),  # Correct: is_nullable=true in fingerprint
        "event_id": pa.Column(str, nullable=True),  # Correct: is_nullable=true in fingerprint
    },
    strict=True,
    coerce=True,
    ordered=True,
)


MEDICATION_SCHEMA = pa.DataFrameSchema(
    {
        "record_type": pa.Column(str, nullable=True),
        "patient_id": pa.Column(str, nullable=False),
        "encounter_id": pa.Column(str, nullable=True),
        "ward": pa.Column(str, nullable=True),
        "admission_datetime": pa.Column(pa.DateTime, nullable=True),
        "discharge_datetime": pa.Column(pa.DateTime, nullable=True),
        "order_id": pa.Column(str, nullable=True),
        "order_uuid": pa.Column(str, nullable=True),
        "medication_code_atc": pa.Column(str, nullable=True),
        "medication_name": pa.Column(str, nullable=True),
        "route": pa.Column(str, nullable=True),
        "dose": pa.Column(float, nullable=True),
        "dose_unit": pa.Column(str, nullable=True),
        "frequency": pa.Column(str, nullable=True),
        "order_start_datetime": pa.Column(pa.DateTime, nullable=True),
        "order_stop_datetime": pa.Column(pa.DateTime, nullable=True),
        "is_prn_0_1": pa.Column(int, nullable=True),
        "indication": pa.Column(str, nullable=True),
        "prescriber_role": pa.Column(str, nullable=True),
        "order_status": pa.Column(str, nullable=True),
        "administration_datetime": pa.Column(pa.DateTime, nullable=True),
        "administered_dose": pa.Column(float, nullable=True),
        "administered_unit": pa.Column(str, nullable=True),
        "administration_status": pa.Column(str, nullable=True),
        "note": pa.Column(str, nullable=True),
    },
    strict=True,
    coerce=True,
    ordered=True,
)

NURSING_SCHEMA = pa.DataFrameSchema(
    {
        "case_id": pa.Column(str, nullable=False),
        "patient_id": pa.Column(str, nullable=False),
        "ward": pa.Column(str, nullable=False),
        "report_date": pa.Column(pa.DateTime, nullable=False),
        "shift": pa.Column(str, nullable=False),
        "nursing_note_free_text": pa.Column(str, nullable=False),
    },
    strict=True,
    coerce=True,
    ordered=True,
)

EPAC_DATA_1_SCHEMA = pa.DataFrameSchema(
    {
        "FallID": pa.Column(str, nullable=True),
        "PID": pa.Column(int, nullable=False),
        "Einschätzung": pa.Column(pa.DateTime, nullable=False),
        "Aufnahme": pa.Column(pa.DateTime, nullable=False),
        "Entlassund": pa.Column(str, nullable=True),  # nulls_only column
        "Station": pa.Column(str, nullable=False),
        "Account": pa.Column(str, nullable=False),
        "SID": pa.Column(float, nullable=False),
        "SID_value": pa.Column(float, nullable=True),  # Mixed int/float/string
    },
    strict=True,
    coerce=True,
    ordered=True,
)

_TYPE_MAP = {
    "int": int,
    "float": float,
    "bool": bool,
    "string": str,
}



def _dtype_from_expected_types(expected_types: dict) -> object:
    if not expected_types or expected_types.get("nulls_only", 0) == 1.0:
        return str

    int_p = float(expected_types.get("int", 0) or 0)
    float_p = float(expected_types.get("float", 0) or 0)
    dt_p = float(expected_types.get("datetime", 0) or 0)
    bool_p = float(expected_types.get("bool", 0) or 0)
    str_p = float(expected_types.get("string", 0) or 0)

    # Key fix: if strings are materially present with numeric types, use string.
    if str_p > 0 and (int_p > 0 or float_p > 0):
        return str

    candidates = {
        "int": int_p,
        "float": float_p,
        "datetime": dt_p,
        "bool": bool_p,
        "string": str_p,
    }
    best_type = max(candidates, key=candidates.get, default="string")

    if best_type == "datetime":
        return "datetime"
    return _TYPE_MAP.get(best_type, str)


def _datetime_kwargs_from_meta(meta: dict) -> dict:
    # Use fixed german formats where detectable, fallback to dayfirst parsing.
    length_stats = meta.get("length_stats", {}) or {}
    mean_len = length_stats.get("mean", None)

    if mean_len == 10:
        return {"format": "%d.%m.%Y", "dayfirst": True}
    if mean_len == 16:
        return {"format": "%d.%m.%Y %H:%M", "dayfirst": True}
    if mean_len == 19:
        return {"format": "%d.%m.%Y %H:%M:%S", "dayfirst": True}
    return {"dayfirst": True}

def _schema_from_fingerprint(fingerprint: dict, fingerprint_name: str | None = None) -> pa.DataFrameSchema:
    ordered_headers = fingerprint["table_metadata"]["ordered_headers"]
    col_fp = fingerprint["column_fingerprints"]
    overrides = EPAC_COLUMN_OVERRIDES.get(fingerprint_name or "", {})

    columns = {}
    for col in ordered_headers:
        if col in overrides:
            columns[col] = overrides[col]
            continue

        meta = col_fp[col]
        expected = meta.get("expected_types", {})
        nullable = bool(meta.get("is_nullable", True))
        inferred = _dtype_from_expected_types(expected)

        has_mixed_datetime_string = (
            inferred == "datetime" and float(expected.get("string", 0) or 0) > 0
        )
        effective_nullable = nullable or has_mixed_datetime_string

        if inferred == "datetime":
            col_schema = pa.Column(
                PanderaDateTime(to_datetime_kwargs=_datetime_kwargs_from_meta(meta)),
                nullable=effective_nullable,
            )
        else:
            col_schema = pa.Column(inferred, nullable=effective_nullable)

        columns[col] = col_schema

    return pa.DataFrameSchema(columns, strict=True, coerce=True, ordered=True)



_FPS = load_fingerprints()

EPAC_DATA_1_SCHEMA = pa.DataFrameSchema(
    {
        "FallID": pa.Column(str, nullable=True),
        "PID": pa.Column(int, nullable=False),
        "Einschätzung": pa.Column(
            PanderaDateTime(to_datetime_kwargs={"format": "%d.%m.%Y %H:%M", "dayfirst": True}),
            nullable=False,
        ),
        "Aufnahme": pa.Column(
            PanderaDateTime(to_datetime_kwargs={"format": "%d.%m.%Y %H:%M", "dayfirst": True}),
            nullable=False,
        ),
        "Entlassund": pa.Column(str, nullable=True),
        "Station": pa.Column(str, nullable=False),
        "Account": pa.Column(str, nullable=False),
        "SID": pa.Column(str, nullable=False),         # was float, but values are like 08_02
        "SID_value": pa.Column(str, nullable=True),    # mixed values (08_02_01, 70, etc.)
    },
    strict=True,
    coerce=True,
    ordered=True,
)

EPAC_DATA_2_SCHEMA = _schema_from_fingerprint(_FPS["epaAC-Data-2_fingerprint"], "epaAC-Data-2_fingerprint")
EPAC_DATA_3_SCHEMA = _schema_from_fingerprint(_FPS["epaAC-Data-3_fingerprint"], "epaAC-Data-3_fingerprint")
EPAC_DATA_4_SCHEMA = _schema_from_fingerprint(_FPS["epaAC-Data-4_fingerprint"], "epaAC-Data-4_fingerprint")
EPAC_DATA_5_SCHEMA = _schema_from_fingerprint(_FPS["epaAC-Data-5_fingerprint"], "epaAC-Data-5_fingerprint")



