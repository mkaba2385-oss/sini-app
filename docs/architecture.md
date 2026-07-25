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

```
Frontend    
- PWA (Progressive Web App)   
  * Framework : React 18 avec Vite   
  * Style : Tailwind CSS (léger)   
  * State Management : Zustand (plus simple que Redux)   
  * i18n : react-i18next   
  * Cache Offline : Workbox (service worker) + IndexedDB via Dexie   
  * Formulaires : React Hook Form + Zod validation   
  * Fetching : TanStack Query (React Query)   

  Pourquoi PWA plutôt que native (React Native, Flutter) ?   
  * Une seule codebase pour tous les appareils   
  * Pas besoin de passer par Play Store (mises à jour instantanées)   
  * Plus léger à télécharger et installer   
  * Le paysan peut essayer sans installer, puis installer si convaincu   
  * Convient parfaitement au stack qu'on apprend en Phase 3   

Backend — API REST   
- Framework : FastAPI (Phase 3)   
- ORM : SQLAlchemy 2 avec async support   
- Validation : Pydantic v2   
- Migrations : Alembic   
- Auth : JWT + OTP SMS    
- Tests : pytest   

Base de données & Stockage   
- PostgreSQL 16 (relationnel) : compte, parcelles, journal, prix, diagnostics   
  * Extension PostGIS : pour la géolocalisation   
- Redis 7 : cache météo, cache prix, sessions, rate limiting, file d'attente SMS   
- Object storage : Cloudflare R2 ou S3 pour les photos (moins cher que de stocker en base)   

Service ML — Diagnostic photo   
- Framework : PyTorch   
- Modèle : ResNet50 pré-entraîné + fine-tuning sur dataset combiné (Phase 5)   
- Serving : FastAPI dédié (isolé du backend principal pour scalabilité)   
- Inference : CPU (pas besoin de GPU en production initiale, ~500ms par image)   

Services externes   
- Météo : OpenWeatherMap   
- SMS : Africa's Talking (couvre Mali, tarifs compétitifs)   
- Push notifications : Firebase Cloud Messaging (gratuit)   
- Monitoring : Sentry (erreurs) + Grafana Cloud (métriques)    

Infrastructure & DevOps  
- Hébergement : Railway (Phase 3) ou Fly.io pour v1  
- À terme : passage vers un VPS Hetzner (bien moins cher, latence bonne vers l'Afrique)  
- CI/CD : GitHub Actions (Phase 6)   
- Containerisation : Docker + docker-compose (Phase 6)  
- SSL : Let's Encrypt  

```
