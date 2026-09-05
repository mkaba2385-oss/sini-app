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
      <main className="min-h-screen bg-gradient-to-b from-green-50 to-white p-4 sm:p-6">
        <div className="mx-auto max-w-7xl">
          <div className="rounded-3xl border border-green-100 bg-white p-6 shadow-lg shadow-green-900/5 sm:p-8">
            <div className="flex items-center gap-3">
              <div className="h-5 w-5 animate-pulse rounded-full bg-green-200" />

              <p className="text-sm font-medium text-gray-600 sm:text-base">
                Chargement des prix du marché...
              </p>
            </div>
          </div>
        </div>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-green-50 to-white p-4 sm:p-6">
        <div className="mx-auto max-w-7xl">
          <div className="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700 shadow-sm sm:p-8">
            <div className="flex items-start gap-4">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-100 text-lg font-bold">
                !
              </div>

              <div>
                <h1 className="text-lg font-bold">
                  Impossible de récupérer les prix.
                </h1>

                <p className="mt-2 text-sm">
                  Vérifiez la connexion au serveur puis
                  réessayez.
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-green-50 to-white p-4 sm:p-6">
      <div className="mx-auto max-w-7xl">
        {/* En-tête */}
        <header className="mb-6 sm:mb-8">
          <div className="rounded-3xl border border-green-100 bg-white p-5 shadow-lg shadow-green-900/5 sm:p-8">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-green-100 text-2xl">
                📈
              </div>

              <div>
                <h1 className="text-2xl font-bold text-green-800 sm:text-3xl">
                  Prix des marchés
                </h1>

                <p className="mt-2 max-w-2xl text-sm leading-6 text-gray-600 sm:text-base">
                  Consultez les prix agricoles relevés par
                  l&apos;OMA et suivez leur évolution selon
                  les cultures et les marchés.
                </p>
              </div>
            </div>
          </div>
        </header>

        {/* Statistiques générales */}
        <section className="mb-6 sm:mb-8">
          <div className="grid gap-4 sm:grid-cols-3">
            <div className="rounded-2xl border border-green-100 bg-white p-5 shadow-sm transition hover:shadow-md sm:p-6">
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

            <div className="rounded-2xl border border-green-100 bg-white p-5 shadow-sm transition hover:shadow-md sm:p-6">
              <p className="text-sm font-medium text-gray-500">
                Source des données
              </p>

              <div className="mt-2 flex items-center gap-2">
                <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-green-100 text-sm font-bold text-green-700">
                  O
                </span>

                <p className="text-2xl font-bold text-green-700">
                  OMA
                </p>
              </div>
            </div>

            <div className="rounded-2xl border border-green-100 bg-white p-5 shadow-sm transition hover:shadow-md sm:p-6">
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
        <section className="mb-6 rounded-3xl border border-green-100 bg-white p-5 shadow-lg shadow-green-900/5 sm:mb-8 sm:p-6">
          <div className="mb-5 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 className="text-xl font-bold text-green-800 sm:text-2xl">
                Filtrer les prix
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Affinez les relevés par culture ou par
                marché.
              </p>
            </div>

            {(cultureFilter || marcheFilter) && (
              <span className="self-start rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                Filtres actifs
              </span>
            )}
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
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-base text-gray-700 outline-none transition focus:border-green-600 focus:ring-4 focus:ring-green-100"
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
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-base text-gray-700 outline-none transition focus:border-green-600 focus:ring-4 focus:ring-green-100"
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
                className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 font-semibold text-gray-700 transition hover:bg-gray-100"
              >
                Réinitialiser les filtres
              </button>
            </div>
          </div>
        </section>

        {/* Évolution des prix */}
        <section className="mb-6 overflow-hidden rounded-3xl border border-green-100 bg-white shadow-lg shadow-green-900/5 sm:mb-8">
          <div className="border-b border-green-100 p-5 sm:p-6">
            <div className="flex items-start gap-3">
              <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-green-100">
                📊
              </div>

              <div>
                <h2 className="text-xl font-bold text-green-800 sm:text-2xl">
                  Évolution des prix
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                  Consultez l&apos;évolution du prix moyen
                  d&apos;une culture.
                </p>
              </div>
            </div>
          </div>

          <div className="p-5 sm:p-6">
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
                className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-base text-gray-700 outline-none transition focus:border-green-600 focus:ring-4 focus:ring-green-100 sm:max-w-md"
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
              <div className="overflow-hidden rounded-2xl border border-gray-100 bg-gray-50 p-2 sm:p-4">
                <PrixEvolutionChart data={prixGraphique} />
              </div>
            ) : (
              <div className="rounded-2xl bg-gray-50 p-8 text-center text-gray-500">
                Aucune donnée disponible pour afficher
                l&apos;évolution des prix.
              </div>
            )}
          </div>
        </section>

        {/* Statistiques par culture */}
        <section className="mb-6 rounded-3xl border border-green-100 bg-white p-5 shadow-lg shadow-green-900/5 sm:mb-8 sm:p-6">
          <div className="mb-5">
            <h2 className="text-xl font-bold text-green-800 sm:text-2xl">
              Statistiques par culture
            </h2>

            <p className="mt-1 text-sm text-gray-500">
              Comparez les prix minimum, moyen et maximum.
            </p>
          </div>

          {statistiques.length > 0 ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {statistiques.map((statistique) => (
                <article
                  key={statistique.culture}
                  className="rounded-2xl border border-gray-200 bg-gray-50/50 p-5 transition hover:border-green-200 hover:bg-green-50/40 hover:shadow-sm"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <h3 className="text-lg font-bold text-green-800">
                        {statistique.culture}
                      </h3>

                      <p className="mt-1 text-sm text-gray-500">
                        {statistique.nombre} relevé
                        {statistique.nombre > 1 ? "s" : ""}
                      </p>
                    </div>

                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-green-100 text-sm">
                      🌾
                    </div>
                  </div>

                  <div className="mt-5 space-y-3">
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

                    <div className="flex items-center justify-between gap-4 rounded-xl bg-green-50 px-3 py-2">
                      <span className="text-sm font-medium text-gray-600">
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
            <div className="rounded-2xl bg-gray-50 p-8 text-center text-gray-500">
              Aucune statistique disponible pour les
              filtres sélectionnés.
            </div>
          )}
        </section>

        {/* Relevés */}
        <section className="overflow-hidden rounded-3xl border border-green-100 bg-white shadow-lg shadow-green-900/5">
          <div className="border-b border-green-100 p-5 sm:p-6">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-xl font-bold text-green-800 sm:text-2xl">
                  Relevés de prix
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                  Prix moyens relevés sur les marchés.
                </p>
              </div>

              <span className="self-start rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-700">
                {prixFiltres.length} relevé
                {prixFiltres.length > 1 ? "s" : ""}
              </span>
            </div>
          </div>

          {/* Version mobile */}
          <div className="space-y-4 bg-gray-50/50 p-4 md:hidden">
            {prixFiltres.map((item) => (
              <article
                key={item.id}
                className="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <h3 className="break-words text-lg font-bold text-green-800">
                      {item.culture}
                    </h3>

                    <p className="mt-1 break-words text-sm text-gray-500">
                      {item.variete ||
                        "Variété non renseignée"}
                    </p>
                  </div>

                  <span className="shrink-0 rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700">
                    {item.source}
                  </span>
                </div>

                <div className="mt-4 rounded-2xl bg-green-50 p-4">
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

                <div className="mt-4 space-y-3">
                  <div className="flex items-start justify-between gap-4 text-sm">
                    <span className="text-gray-500">
                      Marché
                    </span>

                    <span className="max-w-[65%] break-words text-right font-semibold text-gray-800">
                      {item.marche}
                    </span>
                  </div>

                  <div className="flex items-center justify-between gap-4 text-sm">
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
                    className="border-t border-gray-100 transition hover:bg-green-50/40"
                  >
                    <td className="px-6 py-4 font-semibold text-gray-800">
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
            <div className="border-t border-gray-100 p-8 text-center text-gray-500">
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