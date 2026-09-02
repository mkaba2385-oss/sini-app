from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sini.api.routers.auth import router as auth_router
from sini.api.routers.diagnostics import router as diagnostics_router
from sini.api.routers.harvests import router as harvests_router
from sini.api.routers.journal import router as journal_router
from sini.api.routers.parcelles import router as parcelles_router
from sini.api.routers.photos import router as photos_router
from sini.api.routers.prix import router as prix_router
from sini.api.routers.seasons import router as seasons_router
from sini.api.routers.users import router as users_router
from sini.api.routers.weather import router as weather_router

app = FastAPI(
    title="Sini API",
    description="Backend API pour l'application Sini",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://sini-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(parcelles_router)
app.include_router(journal_router)
app.include_router(diagnostics_router)
app.include_router(photos_router)
app.include_router(prix_router)
app.include_router(harvests_router)
app.include_router(seasons_router)
app.include_router(auth_router)
app.include_router(weather_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "status": "ok",
        "app": "sini",
    }
