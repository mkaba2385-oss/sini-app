from fastapi import FastAPI

app = FastAPI(
    title="Sini API",
    description="Backend API pour l'application Sini",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"status": "ok", "app": "sini"}
