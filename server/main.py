from contextlib import asynccontextmanager

# Import model package so all models are registered on Base.metadata
import model  # noqa: F401

# Import models package so all models are registered on Base.metadata
import models  # noqa: F401
from api.routes import router
from db.database import Base, engine
from db.seed import seed_database
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
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
