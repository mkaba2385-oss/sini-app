-- Nombre de diagnostics par niveau de sévérité et culture.
-- La jointure permet de relier le diagnostic à la parcelle concernée.

SELECT
    pa.culture,
    d.niveau_severite,
    COUNT(d.id) AS nombre_diagnostics,
    AVG(d.score_confiance) AS confiance_moyenne,
    MIN(d.score_confiance) AS confiance_minimale,
    MAX(d.score_confiance) AS confiance_maximale
FROM diagnostics AS d
JOIN parcelles AS pa ON pa.id = d.parcelle_id
GROUP BY pa.culture, d.niveau_severite
HAVING COUNT(d.id) > 0
ORDER BY pa.culture, d.niveau_severite;
