import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link, useParams } from "react-router-dom";

import {
  deleteJournalEntry,
  getJournalByParcelle,
  getJournalStats,
} from "../api/journal.js";
import { getParcelle } from "../api/parcelles.js";

function JournalPage() {
  const { parcelleId } = useParams();
  const queryClient = useQueryClient();

  const {
    data: parcelle,
    isLoading: loadingParcelle,
    isError: parcelleError,
  } = useQuery({
    queryKey: ["parcelle", parcelleId],
    queryFn: () => getParcelle(parcelleId),
  });

  const {
    data: entries = [],
    isLoading: loadingJournal,
    isError: journalError,
  } = useQuery({
    queryKey: ["journal", parcelleId],
    queryFn: () => getJournalByParcelle(parcelleId),
  });

  const {
    data: stats,
    isLoading: loadingStats,
    isError: statsError,
  } = useQuery({
    queryKey: ["journal-stats", parcelleId],
    queryFn: () => getJournalStats(parcelleId),
  });

  async function handleDelete(entry) {
    const confirmed = window.confirm(
      `Voulez-vous vraiment supprimer "${entry.title}" ?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteJournalEntry(entry.id);

      await queryClient.invalidateQueries({
        queryKey: ["journal", parcelleId],
      });

      await queryClient.invalidateQueries({
        queryKey: ["journal-stats", parcelleId],
      });
    } catch (error) {
      console.error(error);
      window.alert("Impossible de supprimer cette activité.");
    }
  }

  if (loadingParcelle || loadingJournal) {
    return (
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-4xl">
          <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
            <p className="text-gray-600">
              Chargement du journal...
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (parcelleError || journalError) {
    return (
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-4xl">
          <div className="rounded-xl bg-red-100 p-4 text-red-700">
            Impossible de récupérer le journal.
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 p-4 sm:p-6">
      <div className="mx-auto max-w-4xl">
        {/* En-tête */}
        <div className="mb-6 flex flex-col gap-4 sm:mb-8 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <Link
              to="/parcelles"
              className="text-sm font-medium text-green-700 hover:text-green-900 sm:text-base"
            >
              ← Mes parcelles
            </Link>

            <h1 className="mt-3 text-2xl font-bold text-green-800 sm:text-3xl">
              Journal 🌱
            </h1>

            <p className="mt-2 text-sm text-gray-600 sm:text-base">
              {parcelle?.name}
            </p>
          </div>

          <Link
            to={`/journal/new?parcelle=${parcelleId}`}
            className="w-full rounded-lg bg-green-700 px-4 py-3 text-center font-semibold text-white hover:bg-green-800 sm:w-auto"
          >
            + Ajouter
          </Link>
        </div>

        {/* Statistiques */}
        <section className="mb-6 sm:mb-8">
          <div className="mb-4 flex items-center justify-between gap-3">
            <h2 className="text-xl font-bold text-green-800">
              Statistiques 📊
            </h2>
          </div>

          {loadingStats ? (
            <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
              <p className="text-gray-600">
                Chargement des statistiques...
              </p>
            </div>
          ) : statsError ? (
            <div className="rounded-2xl bg-red-100 p-4 text-red-700">
              Impossible de récupérer les statistiques.
            </div>
          ) : stats ? (
            <div className="grid gap-4 md:grid-cols-2">
              {/* Nombre d'activités */}
              <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
                <p className="text-sm font-medium text-gray-500">
                  Activités
                </p>

                <p className="mt-2 text-3xl font-bold text-green-700">
                  {stats.nombre_entrees}
                </p>
              </div>

              {/* Coût total */}
              <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
                <p className="text-sm font-medium text-gray-500">
                  Coût total
                </p>

                <p className="mt-2 break-words text-2xl font-bold text-green-700 sm:text-3xl">
                  {Number(
                    stats.cout_total_fcfa,
                  ).toLocaleString("fr-FR")}{" "}
                  FCFA
                </p>
              </div>
            </div>
          ) : (
            <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
              <p className="text-gray-600">
                Aucune statistique disponible.
              </p>
            </div>
          )}
        </section>

        {/* Liste des activités */}
        <section>
          <div className="mb-4 flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
            <h2 className="text-xl font-bold text-green-800">
              Activités agricoles
            </h2>

            <span className="text-sm text-gray-500">
              {entries.length} activité(s)
            </span>
          </div>

          {entries.length === 0 ? (
            <div className="rounded-2xl bg-white p-6 text-center shadow sm:p-8">
              <p className="mb-4 text-gray-600">
                Aucune activité enregistrée pour cette
                parcelle.
              </p>

              <Link
                to={`/journal/new?parcelle=${parcelleId}`}
                className="font-semibold text-green-700 hover:text-green-800"
              >
                Ajouter la première activité →
              </Link>
            </div>
          ) : (
            <div className="space-y-4">
              {entries.map((entry) => (
                <article
                  key={entry.id}
                  className="rounded-2xl bg-white p-4 shadow sm:p-6"
                >
                  {/* Informations principales */}
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between sm:gap-4">
                    <div className="min-w-0">
                      <span className="inline-block max-w-full break-words rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-800">
                        {entry.action_type}
                      </span>

                      <h3 className="mt-3 break-words text-xl font-bold text-gray-800">
                        {entry.title}
                      </h3>
                    </div>

                    <span className="shrink-0 text-sm text-gray-500">
                      {new Date(
                        entry.created_at,
                      ).toLocaleDateString("fr-FR")}
                    </span>
                  </div>

                  {/* Description */}
                  {entry.description && (
                    <div className="mt-4 rounded-xl bg-gray-50 p-4">
                      <p className="break-words text-sm leading-6 text-gray-600 sm:text-base">
                        {entry.description}
                      </p>
                    </div>
                  )}

                  {/* Coût */}
                  <div className="mt-4 rounded-xl bg-green-50 p-4">
                    <p className="text-sm text-gray-500">
                      Coût
                    </p>

                    <p className="mt-1 break-words text-lg font-bold text-green-700">
                      {Number(
                        entry.cout_fcfa,
                      ).toLocaleString("fr-FR")}{" "}
                      FCFA
                    </p>
                  </div>

                  {/* Actions */}
                  <div className="mt-5 grid gap-2 sm:grid-cols-2">
                    <Link
                      to={`/journal/${entry.id}/edit?parcelle=${parcelleId}`}
                      className="rounded-lg bg-blue-600 px-4 py-3 text-center font-semibold text-white hover:bg-blue-700"
                    >
                      Modifier
                    </Link>

                    <button
                      type="button"
                      onClick={() => handleDelete(entry)}
                      className="rounded-lg bg-red-600 px-4 py-3 font-semibold text-white hover:bg-red-700"
                    >
                      Supprimer
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}

export default JournalPage;