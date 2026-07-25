# schéma ASCII de l'architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                   INTERFACE UTILISATEUR (PWA / SMS)              │
└─────────────────────────────────┬────────────────────────────────┘
                                  │ HTTPS / SMS
                                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                   BACKEND FASTAPI (API REST)                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │   Météo    │  │ Diagnostic │  │    Prix    │  │  Journal   │  │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  │
└────────┼───────────────┼───────────────┼───────────────┼───────── 

         ▼               ▼               ▼               ▼
┌────────────────┐ ┌────────────┐ ┌──────────────┐ ┌──────────────┐
│ OpenWeatherMap │ │ Service ML │ │ PostgreSQL   │ │    Redis     │
│ & SMS Gateway  │ │ PyTorch    │ │ & PostGIS    │ │ Cache / Jobs │
└────────────────┘ └────────────┘ └──────────────┘ └──────────────┘
```

# Stack Technique


**Frontend :** React 18, Vite, Tailwind CSS, Zustand, PWA (`vite-plugin-pwa`), i18next (FR/BM)  
**Backend :** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 (async), Alembic, pytest  
**Bases de données & Cache :** PostgreSQL 16 (+ PostGIS), Redis 7  
**Machine Learning :** PyTorch, ResNet50 (Transfer Learning), Service d'inférence FastAPI dédié  
**DevOps & Infrastructure :** Docker, Docker Compose, GitHub Actions (CI/CD), Hetzner / Railway  

