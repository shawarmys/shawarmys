from contextlib import asynccontextmanager

# Import model package so all models are registered on Base.metadata
import model  # noqa: F401
from api.metadata import ApiMetadata
from database import Base, engine, get_db
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="shawarmys-server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:80",
        "http://127.0.0.1:80",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/")
def root() -> dict[str, str]:
    return {"message": "Server is running"}

@app.get("/api/metadata")
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
        importedFiles=100,
        successfulMappings=successful_mappings,
        mappingAlerts=5,
    )
