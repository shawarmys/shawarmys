from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import Base, engine

# Import model package so all models are registered on Base.metadata
import model  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all tables on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="shawarmys-server", lifespan=lifespan)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Server is running"}
