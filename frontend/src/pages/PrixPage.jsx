import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import PrixEvolutionChart from "../components/PrixEvolutionChart.jsx";
import { getPrix } from "../api/prix.js";

function PrixPage() {
  const [cultureFilter, setCultureFilter] = useState("");
  const [marcheFilter, setMarcheFilter] = useState("");
  const [graphCulture, setGraphCulture] = useState("");

  const {
    data: prix = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["prix"],
    queryFn: getPrix,
  });

  const cultures = useMemo(() => {
    return [...new Set(prix.map((item) => item.culture))].sort();
  }, [prix]);

  const marches = useMemo(() => {
    return [...new Set(prix.map((item) => item.marche))].sort();
  }, [prix]);

  const prixFiltres = useMemo(() => {
    return prix.filter((item) => {
      const cultureMatch =
        !cultureFilter || item.culture === cultureFilter;

      const marcheMatch =
        !marcheFilter || item.marche === marcheFilter;

      return cultureMatch && marcheMatch;
    });
  }, [prix, cultureFilter, marcheFilter]);

  const statistiques = useMemo(() => {
    const groupes = {};

    for (const item of prixFiltres) {
      if (!groupes[item.culture]) {
        groupes[item.culture] = [];
      }

      groupes[item.culture].push(Number(item.prix_moyen));
    }

    return Object.entries(groupes)
      .map(([culture, prixCulture]) => {
        const minimum = Math.min(...prixCulture);
        const maximum = Math.max(...prixCulture);

        const moyenne =
          prixCulture.reduce(
            (total, valeur) => total + valeur,
            0,
          ) / prixCulture.length;

        return {
          culture,
          nombre: prixCulture.length,
          minimum,
          moyenne,
          maximum,
        };
      })
      .sort((a, b) => a.culture.localeCompare(b.culture));
  }, [prixFiltres]);

  const culturesGraphique = useMemo(() => {
    return [
      ...new Set(
        prix
          .filter((item) => {
            if (!marcheFilter) {
              return true;
            }

            return item.marche === marcheFilter;
          })
          .map((item) => item.culture),
      ),
    ].sort();
  }, [prix, marcheFilter]);

  const cultureGraphique = useMemo(() => {
    if (
      graphCulture &&
      culturesGraphique.includes(graphCulture)
    ) {
      return graphCulture;
    }

    return culturesGraphique[0] || "";
  }, [graphCulture, culturesGraphique]);

  const prixGraphique = useMemo(() => {
    return prix.filter((item) => {
      const cultureMatch =
        item.culture === cultureGraphique;

      const marcheMatch =
        !marcheFilter || item.marche === marcheFilter;

      return cultureMatch && marcheMatch;
    });
  }, [prix, cultureGraphique, marcheFilter]);

  const derniereDate = useMemo(() => {
    if (prix.length === 0) {
      return null;
    }

    return Math.max(
      ...prix.map((item) =>
        new Date(item.date_releve).getTime(),
      ),
    );
  }, [prix]);

  function resetFilters() {
    setCultureFilter("");
    setMarcheFilter("");
    setGraphCulture("");
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-6xl">
          <div className="rounded-2xl bg-white p-6 shadow">
            <p className="text-gray-600">
              Chargement des prix du marché...
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-6xl">
          <div className="rounded-2xl bg-red-100 p-6 text-red-700 shadow">
            <h1 className="text-lg font-bold">
              Impossible de récupérer les prix.
            </h1>

            <p className="mt-2 text-sm">
              Vérifiez la connexion au serveur.
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 p-4 sm:p-6">
      <div className="mx-auto max-w-6xl">
        <header className="mb-6 sm:mb-8">
          <h1 className="text-2xl font-bold text-green-800 sm:text-3xl">
            Prix des marchés
          </h1>

          <p className="mt-2 text-sm text-gray-600 sm:text-base">
            Consultez les prix agricoles relevés par l'OMA.
          </p>
        </header>

        {/* Statistiques générales */}
        <section className="mb-6 sm:mb-8">
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
              <p className="text-sm font-medium text-gray-500">
                Relevés affichés
              </p>

              <p className="mt-2 text-3xl font-bold text-green-700 sm:text-4xl">
                {prixFiltres.length}
              </p>

              {prixFiltres.length !== prix.length && (
                <p className="mt-2 text-sm text-gray-500">
                  sur {prix.length} relevés disponibles
                </p>
              )}
            </div>

            <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
              <p className="text-sm font-medium text-gray-500">
                Source
              </p>

              <p className="mt-2 text-2xl font-bold text-green-700">
                OMA
              </p>
            </div>

            <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
              <p className="text-sm font-medium text-gray-500">
                Dernier relevé
              </p>

              <p className="mt-2 text-xl font-bold text-green-700">
                {derniereDate !== null
                  ? new Date(
                      derniereDate,
                    ).toLocaleDateString("fr-FR")
                  : "Aucun"}
              </p>
            </div>
          </div>
        </section>

        {/* Filtres */}
        <section className="mb-6 rounded-2xl bg-white p-5 shadow sm:mb-8 sm:p-6">
          <div className="mb-5">
            <h2 className="text-xl font-bold text-green-800">
              Filtrer les prix
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Sélectionnez une culture ou un marché.
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <label
                htmlFor="culture-filter"
                className="mb-2 block text-sm font-semibold text-gray-700"
              >
                Culture
              </label>

              <select
                id="culture-filter"
                value={cultureFilter}
                onChange={(event) =>
                  setCultureFilter(event.target.value)
                }
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-700 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              >
                <option value="">
                  Toutes les cultures
                </option>

                {cultures.map((culture) => (
                  <option key={culture} value={culture}>
                    {culture}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label
                htmlFor="marche-filter"
                className="mb-2 block text-sm font-semibold text-gray-700"
              >
                Marché
              </label>

              <select
                id="marche-filter"
                value={marcheFilter}
                onChange={(event) =>
                  setMarcheFilter(event.target.value)
                }
                className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-700 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              >
                <option value="">
                  Tous les marchés
                </option>

                {marches.map((marche) => (
                  <option key={marche} value={marche}>
                    {marche}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <button
                type="button"
                onClick={resetFilters}
                className="w-full rounded-lg bg-gray-100 px-4 py-3 font-semibold text-gray-700 transition hover:bg-gray-200"
              >
                Réinitialiser les filtres
              </button>
            </div>
          </div>
        </section>

        {/* Évolution des prix */}
        <section className="mb-6 rounded-2xl bg-white p-5 shadow sm:mb-8 sm:p-6">
          <div className="mb-5">
            <h2 className="text-xl font-bold text-green-800">
              Évolution des prix
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Consultez l'évolution du prix moyen d'une
              culture.
            </p>
          </div>

          <div className="mb-6">
            <label
              htmlFor="graph-culture"
              className="mb-2 block text-sm font-semibold text-gray-700"
            >
              Culture à afficher
            </label>

            <select
              id="graph-culture"
              value={cultureGraphique}
              onChange={(event) =>
                setGraphCulture(event.target.value)
              }
              className="w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-700 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100 sm:max-w-md"
            >
              {culturesGraphique.length === 0 ? (
                <option value="">
                  Aucune culture disponible
                </option>
              ) : (
                culturesGraphique.map((culture) => (
                  <option key={culture} value={culture}>
                    {culture}
                  </option>
                ))
              )}
            </select>
          </div>

          {cultureGraphique ? (
            <PrixEvolutionChart data={prixGraphique} />
          ) : (
            <div className="rounded-xl bg-gray-50 p-6 text-center text-gray-500">
              Aucune donnée disponible pour afficher
              l'évolution des prix.
            </div>
          )}
        </section>

        {/* Statistiques par culture */}
        <section className="mb-6 rounded-2xl bg-white p-5 shadow sm:mb-8 sm:p-6">
          <div className="mb-5">
            <h2 className="text-xl font-bold text-green-800">
              Statistiques par culture
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Comparaison des prix minimum, moyen et maximum.
            </p>
          </div>

          {statistiques.length > 0 ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {statistiques.map((statistique) => (
                <article
                  key={statistique.culture}
                  className="rounded-xl border border-gray-200 p-4"
                >
                  <div>
                    <h3 className="text-lg font-bold text-green-800">
                      {statistique.culture}
                    </h3>

                    <p className="mt-1 text-sm text-gray-500">
                      {statistique.nombre} relevé
                      {statistique.nombre > 1 ? "s" : ""}
                    </p>
                  </div>

                  <div className="mt-4 space-y-3">
                    <div className="flex items-center justify-between gap-4">
                      <span className="text-sm text-gray-500">
                        Prix minimum
                      </span>

                      <span className="font-semibold text-gray-800">
                        {statistique.minimum.toLocaleString(
                          "fr-FR",
                        )}{" "}
                        FCFA
                      </span>
                    </div>

                    <div className="flex items-center justify-between gap-4">
                      <span className="text-sm text-gray-500">
                        Prix moyen
                      </span>

                      <span className="font-bold text-green-700">
                        {statistique.moyenne.toLocaleString(
                          "fr-FR",
                          {
                            maximumFractionDigits: 0,
                          },
                        )}{" "}
                        FCFA
                      </span>
                    </div>

                    <div className="flex items-center justify-between gap-4">
                      <span className="text-sm text-gray-500">
                        Prix maximum
                      </span>

                      <span className="font-semibold text-gray-800">
                        {statistique.maximum.toLocaleString(
                          "fr-FR",
                        )}{" "}
                        FCFA
                      </span>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="rounded-xl bg-gray-50 p-6 text-center text-gray-500">
              Aucune statistique disponible pour les filtres
              sélectionnés.
            </div>
          )}
        </section>

        {/* Relevés */}
        <section className="rounded-2xl bg-white shadow">
          <div className="border-b border-gray-200 p-5 sm:p-6">
            <h2 className="text-xl font-bold text-green-800">
              Relevés de prix
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Prix moyens relevés sur les marchés.
            </p>
          </div>

          {/* Version mobile */}
          <div className="space-y-4 p-4 md:hidden">
            {prixFiltres.map((item) => (
              <article
                key={item.id}
                className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm"
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-lg font-bold text-green-800">
                      {item.culture}
                    </h3>

                    <p className="mt-1 text-sm text-gray-500">
                      {item.variete ||
                        "Variété non renseignée"}
                    </p>
                  </div>

                  <span className="shrink-0 rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                    {item.source}
                  </span>
                </div>

                <div className="mt-4 rounded-xl bg-green-50 p-4">
                  <p className="text-sm font-medium text-gray-500">
                    Prix moyen
                  </p>

                  <p className="mt-1 text-2xl font-bold text-green-700">
                    {Number(
                      item.prix_moyen,
                    ).toLocaleString("fr-FR")}{" "}
                    FCFA
                  </p>

                  <p className="mt-1 text-sm text-gray-500">
                    par {item.unite}
                  </p>
                </div>

                <div className="mt-4 space-y-2 text-sm">
                  <div className="flex justify-between gap-4">
                    <span className="text-gray-500">
                      Marché
                    </span>

                    <span className="text-right font-semibold text-gray-800">
                      {item.marche}
                    </span>
                  </div>

                  <div className="flex justify-between gap-4">
                    <span className="text-gray-500">
                      Date
                    </span>

                    <span className="font-semibold text-gray-800">
                      {new Date(
                        item.date_releve,
                      ).toLocaleDateString("fr-FR")}
                    </span>
                  </div>
                </div>
              </article>
            ))}
          </div>

          {/* Version desktop */}
          <div className="hidden overflow-x-auto md:block">
            <table className="w-full text-left">
              <thead className="bg-green-50">
                <tr>
                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Culture
                  </th>

                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Variété
                  </th>

                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Marché
                  </th>

                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Prix moyen
                  </th>

                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Unité
                  </th>

                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Date
                  </th>

                  <th className="px-6 py-4 text-sm font-semibold text-green-800">
                    Source
                  </th>
                </tr>
              </thead>

              <tbody>
                {prixFiltres.map((item) => (
                  <tr
                    key={item.id}
                    className="border-t border-gray-100 hover:bg-gray-50"
                  >
                    <td className="px-6 py-4 font-medium text-gray-800">
                      {item.culture}
                    </td>

                    <td className="px-6 py-4 text-gray-600">
                      {item.variete || "—"}
                    </td>

                    <td className="px-6 py-4 text-gray-600">
                      {item.marche}
                    </td>

                    <td className="px-6 py-4 font-bold text-green-700">
                      {Number(
                        item.prix_moyen,
                      ).toLocaleString("fr-FR")}{" "}
                      FCFA
                    </td>

                    <td className="px-6 py-4 text-gray-600">
                      {item.unite}
                    </td>

                    <td className="px-6 py-4 text-gray-600">
                      {new Date(
                        item.date_releve,
                      ).toLocaleDateString("fr-FR")}
                    </td>

                    <td className="px-6 py-4">
                      <span className="rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                        {item.source}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {prixFiltres.length === 0 && (
            <div className="p-8 text-center text-gray-500">
              Aucun relevé ne correspond aux filtres
              sélectionnés.
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

export default PrixPage;