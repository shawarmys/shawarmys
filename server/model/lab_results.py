from typing import Optional

from database import Base
from sqlalchemy import BigInteger, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class LabResults(Base):
    __tablename__ = "lab_results"

    id: Mapped[int] = mapped_column("id", BigInteger, primary_key=True, autoincrement=True)
    file_id: Mapped[Optional[int]] = mapped_column("file_id", ForeignKey("files.id"))
    case_id: Mapped[Optional[int]] = mapped_column("case_id", BigInteger)
    patient_id: Mapped[Optional[str]] = mapped_column("patient_id", BigInteger)
    sex: Mapped[Optional[str]] = mapped_column("sex", String(256))
    age_years: Mapped[Optional[int]] = mapped_column("age_years", Integer)
    specimen_datetime: Mapped[Optional[str]] = mapped_column("specimen_datetime", String(256))

    # Sodium
    sodium_mmol_L: Mapped[Optional[str]] = mapped_column("sodium_mmol_L", String(256))
    sodium_flag: Mapped[Optional[str]] = mapped_column("sodium_flag", String(256))
    sodium_ref_low: Mapped[Optional[str]] = mapped_column("sodium_ref_low", String(256))
    sodium_ref_high: Mapped[Optional[str]] = mapped_column("sodium_ref_high", String(256))

    # Potassium
    potassium_mmol_L: Mapped[Optional[str]] = mapped_column("potassium_mmol_L", String(256))
    potassium_flag: Mapped[Optional[str]] = mapped_column("potassium_flag", String(256))
    potassium_ref_low: Mapped[Optional[str]] = mapped_column("potassium_ref_low", String(256))
    potassium_ref_high: Mapped[Optional[str]] = mapped_column("potassium_ref_high", String(256))

    # Creatinine
    creatinine_mg_dL: Mapped[Optional[str]] = mapped_column("creatinine_mg_dL", String(256))
    creatinine_flag: Mapped[Optional[str]] = mapped_column("creatinine_flag", String(256))
    creatinine_ref_low: Mapped[Optional[str]] = mapped_column("creatinine_ref_low", String(256))
    creatinine_ref_high: Mapped[Optional[str]] = mapped_column("creatinine_ref_high", String(256))

    # eGFR
    egfr_mL_min_1_73m2: Mapped[Optional[str]] = mapped_column("egfr_mL_min_1_73m2", String(256))
    egfr_flag: Mapped[Optional[str]] = mapped_column("egfr_flag", String(256))
    egfr_ref_low: Mapped[Optional[str]] = mapped_column("egfr_ref_low", String(256))
    egfr_ref_high: Mapped[Optional[str]] = mapped_column("egfr_ref_high", String(256))

    # Glucose
    glucose_mg_dL: Mapped[Optional[str]] = mapped_column("glucose_mg_dL", String(256))
    glucose_flag: Mapped[Optional[str]] = mapped_column("glucose_flag", String(256))
    glucose_ref_low: Mapped[Optional[str]] = mapped_column("glucose_ref_low", String(256))
    glucose_ref_high: Mapped[Optional[str]] = mapped_column("glucose_ref_high", String(256))

    # Hemoglobin
    hemoglobin_g_dL: Mapped[Optional[str]] = mapped_column("hemoglobin_g_dL", String(256))
    hb_flag: Mapped[Optional[str]] = mapped_column("hb_flag", String(256))
    hb_ref_low: Mapped[Optional[str]] = mapped_column("hb_ref_low", String(256))
    hb_ref_high: Mapped[Optional[str]] = mapped_column("hb_ref_high", String(256))

    # WBC
    wbc_10e9_L: Mapped[Optional[str]] = mapped_column("wbc_10e9_L", String(256))
    wbc_flag: Mapped[Optional[str]] = mapped_column("wbc_flag", String(256))
    wbc_ref_low: Mapped[Optional[str]] = mapped_column("wbc_ref_low", String(256))
    wbc_ref_high: Mapped[Optional[str]] = mapped_column("wbc_ref_high", String(256))

    # Platelets
    platelets_10e9_L: Mapped[Optional[str]] = mapped_column("platelets_10e9_L", String(256))
    platelets_flag: Mapped[Optional[str]] = mapped_column("platelets_flag", String(256))
    plt_ref_low: Mapped[Optional[str]] = mapped_column("plt_ref_low", String(256))
    plt_ref_high: Mapped[Optional[str]] = mapped_column("plt_ref_high", String(256))

    # CRP
    crp_mg_L: Mapped[Optional[str]] = mapped_column("crp_mg_L", String(256))
    crp_flag: Mapped[Optional[str]] = mapped_column("crp_flag", String(256))
    crp_ref_low: Mapped[Optional[str]] = mapped_column("crp_ref_low", String(256))
    crp_ref_high: Mapped[Optional[str]] = mapped_column("crp_ref_high", String(256))

    # ALT
    alt_U_L: Mapped[Optional[str]] = mapped_column("alt_U_L", String(256))
    alt_flag: Mapped[Optional[str]] = mapped_column("alt_flag", String(256))
    alt_ref_low: Mapped[Optional[str]] = mapped_column("alt_ref_low", String(256))
    alt_ref_high: Mapped[Optional[str]] = mapped_column("alt_ref_high", String(256))

    # AST
    ast_U_L: Mapped[Optional[str]] = mapped_column("ast_U_L", String(256))
    ast_flag: Mapped[Optional[str]] = mapped_column("ast_flag", String(256))
    ast_ref_low: Mapped[Optional[str]] = mapped_column("ast_ref_low", String(256))
    ast_ref_high: Mapped[Optional[str]] = mapped_column("ast_ref_high", String(256))

    # Bilirubin
    bilirubin_mg_dL: Mapped[Optional[str]] = mapped_column("bilirubin_mg_dL", String(256))
    bilirubin_flag: Mapped[Optional[str]] = mapped_column("bilirubin_flag", String(256))
    bili_ref_low: Mapped[Optional[str]] = mapped_column("bili_ref_low", String(256))
    bili_ref_high: Mapped[Optional[str]] = mapped_column("bili_ref_high", String(256))

    # Albumin
    albumin_g_dL: Mapped[Optional[str]] = mapped_column("albumin_g_dL", String(256))
    albumin_flag: Mapped[Optional[str]] = mapped_column("albumin_flag", String(256))
    albumin_ref_low: Mapped[Optional[str]] = mapped_column("albumin_ref_low", String(256))
    albumin_ref_high: Mapped[Optional[str]] = mapped_column("albumin_ref_high", String(256))

    # INR
    inr: Mapped[Optional[str]] = mapped_column("inr", String(256))
    inr_flag: Mapped[Optional[str]] = mapped_column("inr_flag", String(256))
    inr_ref_low: Mapped[Optional[str]] = mapped_column("inr_ref_low", String(256))
    inr_ref_high: Mapped[Optional[str]] = mapped_column("inr_ref_high", String(256))

    # Lactate
    lactate_mmol_L: Mapped[Optional[str]] = mapped_column("lactate_mmol_L", String(256))
    lactate_flag: Mapped[Optional[str]] = mapped_column("lactate_flag", String(256))
    lactate_ref_low: Mapped[Optional[str]] = mapped_column("lactate_ref_low", String(256))
    lactate_ref_high: Mapped[Optional[str]] = mapped_column("lactate_ref_high", String(256))

    def __repr__(self) -> str:
        return f"<ImportLabsData id={self.id} case_id={self.case_id}>"
