from api.metadata import ApiMetadata
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/")
def root() -> dict[str, str]:
    return {"message": "Server is running"}


@router.get("/metadata")
def get_metadata(db: Session = Depends(get_db)) -> ApiMetadata:
    """Return imported File count, succesful Mapping count, mapping Alert count."""
    imported_tables = [
        "lab_results",
        "icd10_data",
        "nursing_daily_reports",
        "medication_events",
        "device_motions",
        "device_1hz_motions",
    ]

    imported_files = 0
    for table in imported_tables:
        has_rows = db.execute(
            text(f"SELECT EXISTS (SELECT 1 FROM {table} LIMIT 1)")
        ).scalar()
        imported_files += 1 if has_rows else 0

    successful_mappings = db.execute(
        text(
            """
            SELECT COUNT(*)
            FROM cases c
            WHERE EXISTS (SELECT 1 FROM lab_results l WHERE l.case_id = c.id)
              AND EXISTS (SELECT 1 FROM icd10_data i WHERE i.case_id = c.id)
              AND EXISTS (SELECT 1 FROM nursing_daily_reports n WHERE n.case_id = c.id)
            """
        )
    ).scalar_one()

    # TODO: Implement imported Files, mappingAlerts and succesful mappings based on all datasets
    return ApiMetadata(
        importedFiles=0,
        successfulMappings=successful_mappings,
        mappingAlerts=0,
    )
