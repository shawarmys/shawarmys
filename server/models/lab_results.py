from typing import Optional

from db.database import Base
from sqlalchemy import BigInteger, DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class LabResults(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    case_id: Mapped[Optional[int]] = mapped_column("case_id", BigInteger)
    patient_id: Mapped[Optional[str]] = mapped_column("patient_id", BigInteger)
    sex: Mapped[Optional[str]] = mapped_column("sex", String(256))
    age_years: Mapped[Optional[int]] = mapped_column("age_years", Integer)
    specimen_datetime: Mapped[Optional[DateTime]] = mapped_column("specimen_datetime", DateTime)

    # Sodium
    sodium_mmol_L: Mapped[Optional[float]] = mapped_column("sodium_mmol_L", Float)
    sodium_flag: Mapped[Optional[str]] = mapped_column("sodium_flag", String(256))
    sodium_ref_low: Mapped[Optional[float]] = mapped_column("sodium_ref_low", Float)
    sodium_ref_high: Mapped[Optional[float]] = mapped_column("sodium_ref_high", Float)

    # Potassium
    potassium_mmol_L: Mapped[Optional[float]] = mapped_column("potassium_mmol_L", Float)
    potassium_flag: Mapped[Optional[str]] = mapped_column("potassium_flag", String(256))
    potassium_ref_low: Mapped[Optional[float]] = mapped_column("potassium_ref_low", Float)
    potassium_ref_high: Mapped[Optional[float]] = mapped_column("potassium_ref_high", Float)

    # Creatinine
    creatinine_mg_dL: Mapped[Optional[float]] = mapped_column("creatinine_mg_dL", Float)
    creatinine_flag: Mapped[Optional[str]] = mapped_column("creatinine_flag", String(256))
    creatinine_ref_low: Mapped[Optional[float]] = mapped_column("creatinine_ref_low", Float)
    creatinine_ref_high: Mapped[Optional[float]] = mapped_column("creatinine_ref_high", Float)

    # eGFR
    egfr_mL_min_1_73m2: Mapped[Optional[float]] = mapped_column("egfr_mL_min_1_73m2", Float)
    egfr_flag: Mapped[Optional[str]] = mapped_column("egfr_flag", String(256))
    egfr_ref_low: Mapped[Optional[float]] = mapped_column("egfr_ref_low", Float)
    egfr_ref_high: Mapped[Optional[float]] = mapped_column("egfr_ref_high", Float)

    # Glucose
    glucose_mg_dL: Mapped[Optional[float]] = mapped_column("glucose_mg_dL", Float)
    glucose_flag: Mapped[Optional[str]] = mapped_column("glucose_flag", String(256))
    glucose_ref_low: Mapped[Optional[float]] = mapped_column("glucose_ref_low", Float)
    glucose_ref_high: Mapped[Optional[float]] = mapped_column("glucose_ref_high", Float)

    # Hemoglobin
    hemoglobin_g_dL: Mapped[Optional[float]] = mapped_column("hemoglobin_g_dL", Float)
    hb_flag: Mapped[Optional[str]] = mapped_column("hb_flag", String(256))
    hb_ref_low: Mapped[Optional[float]] = mapped_column("hb_ref_low", Float)
    hb_ref_high: Mapped[Optional[float]] = mapped_column("hb_ref_high", Float)

    # WBC
    wbc_10e9_L: Mapped[Optional[float]] = mapped_column("wbc_10e9_L", Float)
    wbc_flag: Mapped[Optional[str]] = mapped_column("wbc_flag", String(256))
    wbc_ref_low: Mapped[Optional[float]] = mapped_column("wbc_ref_low", Float)
    wbc_ref_high: Mapped[Optional[float]] = mapped_column("wbc_ref_high", Float)

    # Platelets
    platelets_10e9_L: Mapped[Optional[float]] = mapped_column("platelets_10e9_L", Float)
    platelets_flag: Mapped[Optional[str]] = mapped_column("platelets_flag", String(256))
    plt_ref_low: Mapped[Optional[float]] = mapped_column("plt_ref_low", Float)
    plt_ref_high: Mapped[Optional[float]] = mapped_column("plt_ref_high", Float)

    # CRP
    crp_mg_L: Mapped[Optional[float]] = mapped_column("crp_mg_L", Float)
    crp_flag: Mapped[Optional[str]] = mapped_column("crp_flag", String(256))
    crp_ref_low: Mapped[Optional[float]] = mapped_column("crp_ref_low", Float)
    crp_ref_high: Mapped[Optional[float]] = mapped_column("crp_ref_high", Float)

    # ALT
    alt_U_L: Mapped[Optional[float]] = mapped_column("alt_U_L", Float)
    alt_flag: Mapped[Optional[str]] = mapped_column("alt_flag", String(256))
    alt_ref_low: Mapped[Optional[float]] = mapped_column("alt_ref_low", Float)
    alt_ref_high: Mapped[Optional[float]] = mapped_column("alt_ref_high", Float)

    # AST
    ast_U_L: Mapped[Optional[float]] = mapped_column("ast_U_L", Float)
    ast_flag: Mapped[Optional[str]] = mapped_column("ast_flag", String(256))
    ast_ref_low: Mapped[Optional[float]] = mapped_column("ast_ref_low", Float)
    ast_ref_high: Mapped[Optional[float]] = mapped_column("ast_ref_high", Float)

    # Bilirubin
    bilirubin_mg_dL: Mapped[Optional[float]] = mapped_column("bilirubin_mg_dL", Float)
    bilirubin_flag: Mapped[Optional[str]] = mapped_column("bilirubin_flag", String(256))
    bili_ref_low: Mapped[Optional[float]] = mapped_column("bili_ref_low", Float)
    bili_ref_high: Mapped[Optional[float]] = mapped_column("bili_ref_high", Float)

    # Albumin
    albumin_g_dL: Mapped[Optional[float]] = mapped_column("albumin_g_dL", Float)
    albumin_flag: Mapped[Optional[str]] = mapped_column("albumin_flag", String(256))
    albumin_ref_low: Mapped[Optional[float]] = mapped_column("albumin_ref_low", Float)
    albumin_ref_high: Mapped[Optional[float]] = mapped_column("albumin_ref_high", Float)

    # INR
    inr: Mapped[Optional[float]] = mapped_column("inr", Float)
    inr_flag: Mapped[Optional[str]] = mapped_column("inr_flag", String(256))
    inr_ref_low: Mapped[Optional[float]] = mapped_column("inr_ref_low", Float)
    inr_ref_high: Mapped[Optional[float]] = mapped_column("inr_ref_high", Float)

    # Lactate
    lactate_mmol_L: Mapped[Optional[float]] = mapped_column("lactate_mmol_L", Float)
    lactate_flag: Mapped[Optional[str]] = mapped_column("lactate_flag", String(256))
    lactate_ref_low: Mapped[Optional[float]] = mapped_column("lactate_ref_low", Float)
    lactate_ref_high: Mapped[Optional[float]] = mapped_column("lactate_ref_high", Float)

    def __repr__(self) -> str:
        return f"<ImportLabsData id={self.id} case_id={self.case_id}>"
