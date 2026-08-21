-- Activité agricole enregistrée par parcelle.
-- Cette requête combine les entrées du journal et les diagnostics.

SELECT
    pa.id AS parcelle_id,
    pa.name AS parcelle,
    pa.culture,
    COUNT(DISTINCT j.id) AS nombre_entrees_journal,
    COUNT(DISTINCT d.id) AS nombre_diagnostics,
    MAX(j.created_at) AS derniere_activite,
    MAX(d.created_at) AS dernier_diagnostic
FROM parcelles AS pa
LEFT JOIN journal_entries AS j ON j.parcelle_id = pa.id
LEFT JOIN diagnostics AS d ON d.parcelle_id = pa.id
GROUP BY pa.id, pa.name, pa.culture
ORDER BY derniere_activite DESC NULLS LAST;
