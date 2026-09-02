# Sini

Sini est une application destinée à accompagner les agriculteurs dans le suivi de leurs cultures.

L'objectif est de centraliser plusieurs informations utiles dans une même application : météo, parcelles, journal agricole et, à terme, diagnostic des maladies, prix des récoltes et alertes.

## Fonctionnalités actuelles

Le projet dispose actuellement de plusieurs fonctionnalités fonctionnelles :

- inscription et authentification par numéro de téléphone et OTP ;
- gestion des access tokens et refresh tokens ;
- récupération de l'utilisateur connecté ;
- création, consultation, modification et suppression de parcelles ;
- journal agricole lié aux parcelles ;
- ajout et modification des entrées du journal ;
- suppression des entrées du journal ;
- statistiques du journal agricole ;
- consultation de la météo selon la région de l'utilisateur ;
- alerte sécheresse ;
- préparation de l'internationalisation français / bambara.

## Architecture

Le projet est organisé autour d'un backend FastAPI et d'un frontend React.

### Structure du projet

sini/
├── backend/
│   └── ...
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── i18n/
│   │   ├── pages/
│   │   ├── router/
│   │   └── store/
│   ├── package.json
│   └── ...
├── docs/
│   ├── architecture.md
│   ├── roadmap.md
│   └── vision.md
├── tests/
├── alembic/
├── scripts/
├── pyproject.toml
├── requirements.txt
└── README.md

### Backend

Le backend est développé avec :

- Python ;
- FastAPI ;
- Pydantic ;
- SQLAlchemy ;
- Alembic ;
- JWT pour l'authentification ;
- pytest pour les tests ;
- Ruff pour le linting et le formatage ;
- mypy en mode strict.

L'architecture sépare notamment les responsabilités entre :

- les routers pour les endpoints HTTP ;
- les services pour la logique métier ;
- les repositories pour l'accès aux données ;
- les modèles et schémas pour la représentation et la validation des données.

### Frontend

Le frontend est développé avec :

- React ;
- Vite ;
- React Router ;
- Axios ;
- TanStack Query ;
- Zustand ;
- Tailwind CSS ;
- i18next / react-i18next.

Le frontend communique avec l'API FastAPI via Axios.

L'authentification est gérée côté client avec Zustand et la persistance des tokens.

## Installation

### Prérequis

- Python 3.12 ;
- Node.js et npm ;
- une base de données PostgreSQL pour l'environnement complet.

### Backend

Créer et activer l'environnement virtuel :

    python3.12 -m venv .venv
    source .venv/bin/activate

Installer les dépendances :

    pip install -r requirements.txt

Configurer les variables d'environnement nécessaires dans `.env`.

Lancer le backend :

    uvicorn backend.main:app --reload

L'API sera alors disponible sur :

    http://127.0.0.1:8000

La documentation interactive FastAPI est disponible sur :

    http://127.0.0.1:8000/docs

### Frontend

Se placer dans le dossier frontend :

    cd frontend

Installer les dépendances :

    npm install

Créer/configurer le fichier `.env` avec l'URL de l'API :

    VITE_API_URL=http://127.0.0.1:8000

Lancer le serveur de développement :

    npm run dev

## Vérifications

### Backend

Lancer les tests :

    pytest

Lancer Ruff :

    ruff check .

Vérifier les types :

    mypy src

### Frontend

Vérifier le linting :

    npm run lint

Construire le frontend pour la production :

    npm run build

## Git et qualité du code

Le projet utilise des outils de vérification automatique afin de garder une base de code propre :

- Ruff ;
- mypy ;
- pytest ;
- pre-commit.

Avant de créer un commit, il est recommandé de vérifier :

    ruff check .
    mypy src
    pytest

Pour exécuter les hooks pre-commit :

    pre-commit run --all-files

## Documentation

La documentation complémentaire se trouve dans `docs/` :

- `docs/vision.md` : vision et objectifs du projet ;
- `docs/architecture.md` : architecture technique ;
- `docs/roadmap.md` : évolution prévue du projet.

## État du projet

Sini est actuellement en développement.

Les fonctionnalités de base liées à l'authentification, aux parcelles, au journal agricole et à la météo sont déjà intégrées.

D'autres fonctionnalités sont prévues pour les prochaines étapes, notamment :

- diagnostic des maladies des plantes ;
- recommandations de traitements ;
- suivi des prix des récoltes ;
- alertes et notifications ;
- amélioration du fonctionnement avec une connexion limitée.

## Contribution

Pour contribuer au projet :

1. créer une branche dédiée ;
2. effectuer les modifications ;
3. vérifier le linting, les types et les tests ;
4. vérifier que le frontend se construit correctement ;
5. créer un commit clair ;
6. pousser la branche et ouvrir une pull request si nécessaire.

## Licence

Licence à définir.

