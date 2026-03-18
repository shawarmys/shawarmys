from fastapi import FastAPI

app = FastAPI(title="shawarmys-server")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Server is running"}
