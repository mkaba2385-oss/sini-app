# Sini - Frontend

Interface web de l'application **Sini**, développée avec React et Vite.

Le frontend permet aux utilisateurs de gérer leurs parcelles agricoles, leur journal de suivi et d'accéder aux fonctionnalités de l'application via l'API backend.

## Fonctionnalités

Le frontend permet actuellement de :

- créer un compte utilisateur ;
- se connecter avec un numéro de téléphone et un code OTP ;
- gérer l'authentification avec des tokens d'accès et de rafraîchissement ;
- consulter les informations de l'utilisateur connecté ;
- créer, consulter, modifier et supprimer des parcelles ;
- consulter les entrées du journal agricole d'une parcelle ;
- ajouter, modifier et supprimer une entrée du journal ;
- consulter les statistiques du journal ;
- consulter les informations météo ;
- protéger les pages nécessitant une authentification ;
- gérer automatiquement le renouvellement du token d'accès ;
- préparer le support du français et du bambara.

## Technologies utilisées

- React
- Vite
- React Router
- Axios
- Zustand
- TanStack Query
- Tailwind CSS
- i18next

## Installation

### Prérequis

Il faut avoir installé :

- Node.js
- npm

Depuis le dossier `frontend` :

```bash
npm install
```

## Configuration

Créer un fichier `.env` dans le dossier `frontend` :

```env
VITE_API_URL=https://sini-app-production.up.railway.app
```

Cette variable permet au frontend de connaître l'adresse de l'API backend.

Le fichier `.env` ne doit pas être ajouté au dépôt Git.

## Lancer le projet en développement

Depuis le dossier `frontend` :

```bash
npm run dev
```

Vite démarre alors le serveur de développement et affiche l'adresse locale dans le terminal.

## Vérifications

### Linter

Pour vérifier le code avec ESLint :

```bash
npm run lint
```

### Build

Pour vérifier que le frontend peut être compilé correctement :

```bash
npm run build
```

## Structure du projet

```text
frontend/
├── src/
│   ├── api/
│   │   ├── auth.js
│   │   ├── client.js
│   │   ├── journal.js
│   │   ├── parcelles.js
│   │   └── weather.js
│   │
│   ├── components/
│   │   └── Navbar.jsx
│   │
│   ├── i18n/
│   │   ├── locales/
│   │   │   ├── bm.json
│   │   │   └── fr.json
│   │   └── index.js
│   │
│   ├── pages/
│   │   ├── AddJournalEntryPage.jsx
│   │   ├── AddParcellePage.jsx
│   │   ├── EditJournalEntryPage.jsx
│   │   ├── EditParcellePage.jsx
│   │   ├── HomePage.jsx
│   │   ├── JournalPage.jsx
│   │   ├── LoginOtpPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── OtpPage.jsx
│   │   ├── ParcellesPage.jsx
│   │   └── RegisterPage.jsx
│   │
│   ├── router/
│   │   ├── ProtectedRoute.jsx
│   │   └── index.jsx
│   │
│   ├── store/
│   │   └── authStore.js
│   │
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── .env
├── package.json
├── vite.config.js
└── README.md
```

## Organisation du frontend

Le frontend est organisé par responsabilité.

### `api/`

Contient les fonctions qui communiquent avec l'API backend.

Par exemple :

- `auth.js` pour l'authentification ;
- `parcelles.js` pour la gestion des parcelles ;
- `journal.js` pour le journal agricole ;
- `weather.js` pour la météo ;
- `client.js` pour la configuration Axios et la gestion des tokens.

### `components/`

Contient les composants réutilisables de l'application.

Par exemple, la barre de navigation est dans :

```text
src/components/Navbar.jsx
```

### `pages/`

Contient les différentes pages accessibles dans l'application.

Chaque page correspond à une fonctionnalité ou à une étape du parcours utilisateur.

### `router/`

Contient la configuration des routes React.

Le composant `ProtectedRoute` permet notamment de vérifier qu'un utilisateur possède un token d'accès avant d'accéder aux pages protégées.

### `store/`

Contient l'état global de l'application.

Le store Zustand permet notamment de conserver :

- le token d'accès ;
- le token de rafraîchissement ;
- les informations de l'utilisateur connecté.

### `i18n/`

Contient la configuration de l'internationalisation.

Les fichiers de traduction actuellement présents sont :

```text
src/i18n/locales/fr.json
src/i18n/locales/bm.json
```

Le français est actuellement utilisé comme langue principale.

## Authentification

L'authentification fonctionne avec un système OTP.

Le parcours est :

```text
Utilisateur
    |
    v
Numéro de téléphone
    |
    v
Demande de code OTP
    |
    v
Vérification du code
    |
    v
Access token + Refresh token
    |
    v
Application protégée
```

Le token d'accès est automatiquement ajouté aux requêtes API.

Lorsqu'un token d'accès expire, le frontend tente automatiquement d'utiliser le refresh token pour obtenir de nouveaux tokens.

Si le renouvellement échoue, la session est supprimée et l'utilisateur est redirigé vers la page de connexion.

## Communication avec le backend

Le frontend communique avec l'API FastAPI grâce à Axios.

L'adresse de l'API est définie dans :

```env
VITE_API_URL=https://sini-app-production.up.railway.app
```

Les appels API sont centralisés dans le dossier :

```text
src/api/
```

Cela permet de séparer la communication avec le backend du code des pages React.

## Routes principales

Les routes publiques comprennent notamment :

```text
/login
/register
/verify-login-otp
/verify-otp
```

Les routes protégées comprennent notamment :

```text
/
/parcelles
/parcelles/new
/parcelles/:id/edit
/parcelles/:parcelleId/journal
/journal/new
/journal/:entryId/edit
```

Les routes protégées nécessitent une authentification.

## Architecture générale

Le frontend suit une séparation simple entre l'interface, l'état de l'application et la communication avec le backend.

```text
Utilisateur
    |
    v
Pages React
    |
    +------------------+
    |                  |
    v                  v
Components          Store Zustand
    |                  |
    +--------+---------+
             |
             v
          API Axios
             |
             v
       Backend FastAPI
             |
             v
          Base de données
```

Cette organisation permet de modifier une partie de l'application sans devoir modifier tout le reste du code.

## Scripts disponibles

Depuis le dossier `frontend` :

### Démarrer le serveur de développement

```bash
npm run dev
```

### Vérifier le code

```bash
npm run lint
```

### Construire l'application

```bash
npm run build
```

### Prévisualiser le build

```bash
npm run preview
```

## État du projet

Le frontend couvre actuellement les principales fonctionnalités développées pour Sini :

- authentification OTP ;
- gestion des utilisateurs connectés ;
- gestion des parcelles ;
- gestion du journal agricole ;
- statistiques du journal ;
- météo ;
- navigation protégée ;
- renouvellement automatique des tokens ;
- préparation de l'internationalisation.

Les vérifications suivantes passent actuellement :

```bash
npm run lint
npm run build
```

## Développement

Pour contribuer au frontend :

1. installer les dépendances avec `npm install` ;
2. configurer le fichier `.env` ;
3. lancer le serveur avec `npm run dev` ;
4. effectuer les modifications nécessaires ;
5. vérifier le code avec `npm run lint` ;
6. vérifier le build avec `npm run build`.

Le code doit rester organisé par responsabilité afin de conserver une architecture simple et maintenable.

## Projet

**Sini** est une application destinée à accompagner les agriculteurs dans le suivi de leurs activités agricoles.

Le frontend React constitue l'interface utilisateur et communique avec le backend FastAPI pour accéder aux données et aux différents services de l'application.
