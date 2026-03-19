from api.imported_files import ImportedFiles
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


@router.get("/api/metadata", response_model=ApiMetadata)
def get_metadata(db: Session = Depends(get_db)) -> ApiMetadata:
    """Return imported File count, succesful Mapping count, mapping Alert count."""
    imported_files = db.execute(text("SELECT COUNT(*) FROM files")).scalar_one()

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

    # TODO: Correct mapping alerts
    return ApiMetadata(
        importedFiles=imported_files,
        successfulMappings=successful_mappings,
        mappingAlerts=0,
    )

@router.get("/api/imported-files", response_model=list[ImportedFiles])
def get_imported_files(db: Session = Depends(get_db)) -> list[ImportedFiles]:
    """Return list of imported files with name, source, entries, records, type."""
    result = db.execute(
        text(
            """
            SELECT name, source, group_type AS "groupType", entries, records, type
            FROM files
            ORDER BY created_at DESC
            """
        )
    ).mappings().all()

    return [
        ImportedFiles(
            name=row["name"],
            source=row["source"],
            groupType=row["groupType"],
            entries=row["entries"],
            records=row["records"],
            type=row["type"],
        )
        for row in result
    ]
