from fastapi import FastAPI

from sini.api.routers.diagnostics import router as diagnostics_router
from sini.api.routers.harvests import router as harvests_router
from sini.api.routers.journal import router as journal_router
from sini.api.routers.parcelles import router as parcelles_router
from sini.api.routers.photos import router as photos_router
from sini.api.routers.prix import router as prix_router
from sini.api.routers.seasons import router as seasons_router
from sini.api.routers.users import router as users_router

app = FastAPI(
    title="Sini API",
    description="Backend API pour l'application Sini",
    version="0.1.0",
)

app.include_router(users_router)
app.include_router(parcelles_router)
app.include_router(journal_router)
app.include_router(diagnostics_router)
app.include_router(photos_router)
app.include_router(prix_router)
app.include_router(harvests_router)
app.include_router(seasons_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "status": "ok",
        "app": "sini",
    }
