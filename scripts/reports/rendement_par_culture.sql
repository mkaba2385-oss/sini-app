-- Rendement moyen par culture et saison.
-- Le rendement est calculé en kg/ha lorsque les récoltes sont enregistrées en kg.
WITH harvests_in_kg AS (
    SELECT
        h.parcelle_id,
        h.season_id,
        h.quantite_recoltee AS quantite_kg,
        p.culture,
        p.superficie_ha
    FROM harvests AS h
    INNER JOIN parcelles AS p ON p.id = h.parcelle_id
    WHERE h.unite = 'kg'
)
SELECT
    culture,
    season_id,
    COUNT(*) AS nombre_recoltes,
    SUM(quantite_kg) AS quantite_totale_kg,
    ROUND((SUM(quantite_kg) / NULLIF(SUM(superficie_ha), 0))::numeric, 2)
        AS rendement_moyen_kg_ha
FROM harvests_in_kg
GROUP BY culture, season_id
HAVING SUM(quantite_kg) > 0
ORDER BY culture, season_id;
