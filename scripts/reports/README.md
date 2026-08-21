# Reports SQL

Les requêtes de ce dossier sont prévues pour être exécutées sur la base PostgreSQL de Sini après la migration Alembic et le seed de développement.

## Reports disponibles

- `historique_prix.sql` : historique des prix par culture et marché avec `LAG()` pour calculer la variation entre deux relevés.
- `couts_par_parcelle.sql` : coûts cumulés et moyens par parcelle avec `JOIN`, `SUM`, `AVG`, `GROUP BY` et `HAVING`.
- `activite_par_parcelle.sql` : nombre d'opérations et de diagnostics par parcelle.
- `diagnostics_par_severite.sql` : statistiques de confiance des diagnostics par culture et niveau de sévérité.

## Rendement par culture

Le projet actuel ne possède pas encore de table contenant une quantité récoltée associée à une superficie et à une saison. Il est donc impossible de calculer honnêtement un rendement agricole à partir des tables actuelles.

La formule attendue serait par exemple :

```text
rendement = quantité_récoltée / superficie_ha
```

Une évolution minimale du modèle devra introduire une donnée de récolte et une saison avant de créer le report `rendement_par_culture.sql`.

### `rendement_par_culture.sql`

Calcule le rendement moyen en kg/ha par culture et par saison à partir des récoltes enregistrées en kilogrammes.
