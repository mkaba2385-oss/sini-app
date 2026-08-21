-- Coûts cumulés par parcelle.
-- JOIN + SUM + GROUP BY + HAVING permettent d'identifier les parcelles
-- ayant dépassé un seuil de dépenses.

SELECT
    pa.id AS parcelle_id,
    pa.name AS parcelle,
    u.full_name AS proprietaire,
    pa.culture,
    COUNT(j.id) AS nombre_operations,
    COALESCE(SUM(j.cout_fcfa), 0) AS cout_total_fcfa,
    COALESCE(AVG(j.cout_fcfa), 0) AS cout_moyen_fcfa
FROM parcelles AS pa
JOIN users AS u ON u.id = pa.owner_id
LEFT JOIN journal_entries AS j ON j.parcelle_id = pa.id
GROUP BY pa.id, pa.name, u.full_name, pa.culture
HAVING COALESCE(SUM(j.cout_fcfa), 0) >= 0
ORDER BY cout_total_fcfa DESC;
