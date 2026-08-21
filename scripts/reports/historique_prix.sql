-- Historique des prix par culture et marché.
-- LAG permet de comparer chaque relevé au relevé précédent.

SELECT
    p.culture,
    p.marche,
    p.date_releve,
    p.prix_moyen,
    p.unite,
    LAG(p.prix_moyen) OVER (
        PARTITION BY p.culture, p.marche, p.unite
        ORDER BY p.date_releve
    ) AS prix_precedent,
    p.prix_moyen - LAG(p.prix_moyen) OVER (
        PARTITION BY p.culture, p.marche, p.unite
        ORDER BY p.date_releve
    ) AS variation_prix
FROM prices AS p
ORDER BY p.culture, p.marche, p.date_releve;
