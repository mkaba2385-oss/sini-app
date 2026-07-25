# schéma ASCII de l'architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                   UTILISATEURS (paysans, coops)                        │
│                                                                        │
│    ┌──────────────────┐                  ┌──────────────────┐          │
│    │  PWA (mobile)    │                  │ Téléphone basique│          │
│    │  Bambara/FR      │                  │ (SMS seulement)  │          │
│    └────────┬─────────┘                  └────────┬─────────┘          │
│             │ HTTPS                               │                    │
│             │                                     │                    │
└─────────────┼─────────────────────────────────────┼────────────────────┘
              │                                     │
              ▼                                     ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        BACKEND SINI (API REST)                         │
│                                                                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Météo   │  │Diagnostic│  │   Prix   │  │ Journal  │  │   SMS    │  │
│  │ Service  │  │ Service  │  │ Service  │  │ Service  │  │ Gateway  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │             │             │             │        │
│       └─────────────┴─────────────┼─────────────┴─────────────┘        │
│                                   │                                    │
│                                   ▼                                    │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │   FastAPI + Auth JWT + Rate limit + Middlewares            │        │
│  └────────────────────────────────────────────────────────────┘        │
└──────────┬────────────────────────┬───────────────────┬────────────────┘
           │                        │                   │
           ▼                        ▼                   ▼
   ┌──────────────┐         ┌──────────────┐    ┌──────────────┐
   │  PostgreSQL  │         │    Redis     │    │  ML Service  │
   │  (données)   │         │   (cache,    │    │ (Diagnostic  │
   │              │         │  files SMS)  │    │    photo)    │
   └──────────────┘         └──────────────┘    └──────────────┘

   ┌────────────────────────────────────────────────────────────┐
   │                    SERVICES EXTERNES                       │
   │  OpenWeatherMap    Africa's Talking (SMS)    OMA (scraping)│
   └────────────────────────────────────────────────────────────┘
```

# Stack Technique


**Frontend :** React 18, Vite, Tailwind CSS, Zustand, PWA (`vite-plugin-pwa`), i18next (FR/BM)  
**Backend :** Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2 (async), Alembic, pytest  
**Bases de données & Cache :** PostgreSQL 16 (+ PostGIS), Redis 7  
**Machine Learning :** PyTorch, ResNet50 (Transfer Learning), Service d'inférence FastAPI dédié  
**DevOps & Infrastructure :** Docker, Docker Compose, GitHub Actions (CI/CD), Hetzner / Railway  

