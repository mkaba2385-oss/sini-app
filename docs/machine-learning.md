# Machine Learning — Prédiction des prix

## Objectif

Prédire le prix d'une culture sur un marché donné à partir des relevés historiques.

Les modèles comparés sont :

- Baseline : moyenne mobile + saisonnalité
- Ridge Regression
- Random Forest Regression

## Données

Les données proviennent des relevés de prix de l'OMA.

- 450 relevés disponibles
- 6 cultures
- plusieurs marchés
- prix principalement en FCFA/kg

Pour le Machine Learning, les données sont regroupées par culture et marché.

Les variables utilisées sont :

- les 3 derniers prix ;
- le mois ;
- l'année ;
- la culture ;
- le marché.

Les variables catégorielles sont encodées avec `OneHotEncoder`.

## Comparaison des modèles

| Modèle | MAE | RMSE |
|---|---:|---:|
| Baseline | 43.05 | 57.40 |
| Ridge Regression | 42.25 | 52.61 |
| **Random Forest** | **31.91** | **43.36** |

Le Random Forest est le meilleur modèle sur le jeu de test.

Par rapport au modèle baseline :

- MAE améliorée d'environ **25,9 %**
- RMSE améliorée d'environ **24,5 %**

## Modèle retenu

Le modèle retenu est **Random Forest Regression**.

Configuration utilisée :

```text
n_estimators = 100
max_depth = None
min_samples_leaf = 4