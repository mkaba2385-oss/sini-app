# Module Schemas (`sini.schemas`)

Ce module définit l'ensemble des structures de données (**DTOs – Data Transfer Objects**) utilisées par l'application **Sini**. Il s'appuie sur **Pydantic v2** afin d'assurer la validation des données en entrée et en sortie, la sérialisation JSON ainsi qu'un typage strict dans l'ensemble de l'application.

---

## Objectifs et principes de conception

Le module repose sur les principes suivants :

1. **Séparation des responsabilités (SoC)** : distinction claire entre les schémas de création (`*Create`), de mise à jour (`*Update`) et de lecture (`*Response`).
2. **Validation à la source** : empêcher l'introduction de données incohérentes ou malformées dans la couche métier.
3. **Typage métier et normalisation** : prise en compte des contraintes réelles du domaine (numéros de téléphone maliens, régions administratives, types de cultures, etc.).

---

## Choix de validation et d'implémentation

### 1. Gestion des énumérations (`Enum`)

Afin d'éviter toute ambiguïté sur les données saisies et de faciliter l'intégration avec les applications web et mobiles, plusieurs énumérations sont utilisées.

#### `RegionMali`

Limite les régions géographiques aux divisions administratives officielles du Mali.

Exemples :

- `SIKASSO`
- `SEGOU`
- `MOPTI`
- `KOULIKORO`
- `BAMAKO`

#### `CultureType`

Liste fermée des principales cultures prises en charge par l'application.

Valeurs disponibles :

- `Coton`
- `Maïs`
- `Riz`
- `Mil`
- `Sorgho`
- `Arachide`
- `Maraîchage`
- `Autre`

---

### 2. Validation des numéros de téléphone (`UserCreate`)

#### Problématique

Les numéros de téléphone doivent respecter le format officiel utilisé au Mali.

#### Règles de validation

- Validation via un `@field_validator("phone_number")`.
- Utilisation d'une expression régulière (`Regex`).
- Format accepté : **international obligatoire** (`+223XXXXXXXX`).
- Rejet des indicatifs incorrects (`+33`, `+225`, etc.).
- Vérification de la longueur et du préfixe opérateur.

#### Expression régulière utilisée

```python
^\+223[256789]\d{7}$
```

Si la valeur ne correspond pas à cette expression, une exception `ValueError` est levée.

---

### 3. Contraintes métier et validation numérique (`ParcelleCreate`)

#### Superficie

Le champ `superficie_ha` doit être strictement supérieur à zéro (`gt=0`).

Une parcelle ne peut donc pas avoir une superficie :

- nulle ;
- négative.

#### Nettoyage des chaînes de caractères

Les champs textuels tels que :

- `name`
- `culture`

sont automatiquement nettoyés (`strip`) afin d'éliminer les espaces inutiles avant leur enregistrement.

---

### 4. Séparation entre `Create` et `Response`

#### `ParcelleCreate`

Contient uniquement les données fournies par l'utilisateur lors de la création :

- nom ;
- superficie ;
- culture ;
- région ;
- identifiant du propriétaire.

#### `ParcelleResponse`

Étend le schéma précédent en ajoutant :

- `id: int` : identifiant généré automatiquement ;
- `created_at` : date de création ;
- `updated_at` : date de dernière modification.

Le modèle active également :

```python
model_config = ConfigDict(from_attributes=True)
```

Cette configuration permet la conversion directe depuis les modèles ORM.

---

## Structure du module

```text
src/
└── sini/
    └── schemas/
        ├── README.md         # Documentation de la couche Schemas
        ├── __init__.py       # Exporte les schémas principaux
        ├── user.py           # Schémas des utilisateurs
        ├── parcelle.py       # Schémas des parcelles agricoles
        ├── journal.py        # Schémas du journal des activités
        └── diagnostic.py     # Schémas des diagnostics
```

---

## Tests unitaires

Les principaux cas d'utilisation sont couverts par des tests unitaires dans :

```text
tests/test_schemas.py
```

Les tests vérifient notamment :

- la validation des numéros de téléphone maliens ;
- le rejet des superficies nulles ou négatives ;
- la validation des énumérations (`RegionMali`, `CultureType`) ;
- les contraintes des schémas `Create`, `Update` et `Response` ;
- la sérialisation et la validation des modèles Pydantic.