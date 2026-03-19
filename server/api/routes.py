from api.metadata import ApiMetadata
from api.sources import DataSourceSummary, DataGroupSummary, ImportedFiles
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

@router.get("/api/data-sources-summary", response_model=list[DataSourceSummary])
def get_data_sources_summary(db: Session = Depends(get_db)) -> list[DataSourceSummary]:
    """Return summary of data sources with name and number of files."""
    result = db.execute(
        text(
            """
            SELECT source AS "name", COUNT(*) AS "numFiles"
            FROM files
            GROUP BY source
            ORDER BY "numFiles" DESC
            """
        )
    ).mappings().all()

    return [
        DataSourceSummary(name=row["name"], numFiles=row["numFiles"])
        for row in result
    ]

@router.get("/api/data-groups-summary", response_model=list[DataGroupSummary])
def get_data_groups_summary(db: Session = Depends(get_db)) -> list[DataGroupSummary]:
    """Return summary of data groups with group type and number of files."""
    result = db.execute(
        text(
            """
            SELECT group_type AS "groupType", COUNT(*) AS "numFiles"
            FROM files
            GROUP BY group_type
            ORDER BY "numFiles" DESC
            """
        )
    ).mappings().all()

    return [
        DataGroupSummary(groupType=row["groupType"], numFiles=row["numFiles"])
        for row in result
    ]
