from contextlib import asynccontextmanager

# Import model package so all models are registered on Base.metadata
import model  # noqa: F401
from api.imported_files import ImportedFiles
from api.metadata import ApiMetadata
from database import Base, engine, get_db
from fastapi import Depends, FastAPI
# Import models package so all models are registered on Base.metadata
import models  # noqa: F401
from api.routes import router
from db.database import Base, engine
from db.seed import is_db_empty, seed_database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if is_db_empty():
        print("Database is empty — seeding from CSV files …")
        seed_database()
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

app.include_router(router)

@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/")
def root() -> dict[str, str]:
    return {"message": "Server is running"}


@app.get("/api/metadata", response_model=ApiMetadata)
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

@app.get("/api/imported-files", response_model=list[ImportedFiles])
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
