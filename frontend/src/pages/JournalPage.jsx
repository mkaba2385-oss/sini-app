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
return ( <main className="min-h-screen bg-green-50 p-6"> <div className="mx-auto max-w-4xl"> <p className="text-gray-600">
Chargement du journal... </p> </div> </main>
);
}

if (parcelleError || journalError) {
return ( <main className="min-h-screen bg-green-50 p-6"> <div className="mx-auto max-w-4xl"> <div className="rounded-xl bg-red-100 p-4 text-red-700">
Impossible de récupérer le journal. </div> </div> </main>
);
}

return ( <main className="min-h-screen bg-green-50 p-6"> <div className="mx-auto max-w-4xl">


    {/* En-tête */}
    <div className="mb-8 flex items-center justify-between">
      <div>
        <Link
          to="/parcelles"
          className="text-green-700 hover:text-green-900"
        >
          ← Mes parcelles
        </Link>

        <h1 className="mt-3 text-3xl font-bold text-green-800">
          Journal 🌱
        </h1>

        <p className="mt-2 text-gray-600">
          {parcelle?.name}
        </p>
      </div>

      <Link
        to={`/journal/new?parcelle=${parcelleId}`}
        className="rounded-lg bg-green-700 px-4 py-3 font-semibold text-white hover:bg-green-800"
      >
        + Ajouter
      </Link>
    </div>

    {/* Statistiques */}
    <section className="mb-8">
      <h2 className="mb-4 text-xl font-bold text-green-800">
        Statistiques 📊
      </h2>

      {loadingStats ? (
        <div className="rounded-2xl bg-white p-6 shadow">
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
          <div className="rounded-2xl bg-white p-6 shadow">
            <p className="text-sm font-medium text-gray-500">
              Activités
            </p>

            <p className="mt-2 text-3xl font-bold text-green-700">
              {stats.nombre_entrees}
            </p>
          </div>

          {/* Coût total */}
          <div className="rounded-2xl bg-white p-6 shadow">
            <p className="text-sm font-medium text-gray-500">
              Coût total
            </p>

            <p className="mt-2 text-3xl font-bold text-green-700">
              {Number(
                stats.cout_total_fcfa,
              ).toLocaleString("fr-FR")}{" "}
              FCFA
            </p>
          </div>

        </div>
      ) : (
        <div className="rounded-2xl bg-white p-6 shadow">
          <p className="text-gray-600">
            Aucune statistique disponible.
          </p>
        </div>
      )}
    </section>

    {/* Liste des activités */}
    <section>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-bold text-green-800">
          Activités agricoles
        </h2>

        <span className="text-sm text-gray-500">
          {entries.length} activité(s)
        </span>
      </div>

      {entries.length === 0 ? (
        <div className="rounded-2xl bg-white p-8 text-center shadow">
          <p className="mb-4 text-gray-600">
            Aucune activité enregistrée pour cette parcelle.
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
              className="rounded-2xl bg-white p-6 shadow"
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-semibold text-green-800">
                    {entry.action_type}
                  </span>

                  <h3 className="mt-3 text-xl font-bold text-gray-800">
                    {entry.title}
                  </h3>
                </div>

                <span className="text-sm text-gray-500">
                  {new Date(
                    entry.created_at,
                  ).toLocaleDateString("fr-FR")}
                </span>
              </div>

              {entry.description && (
                <p className="mt-3 text-gray-600">
                  {entry.description}
                </p>
              )}

              <p className="mt-3 font-semibold text-green-700">
                Coût :{" "}
                {Number(entry.cout_fcfa).toLocaleString(
                  "fr-FR",
                )}{" "}
                FCFA
              </p>

              <div className="mt-5 flex gap-3">
                <Link
                  to={`/journal/${entry.id}/edit?parcelle=${parcelleId}`}
                  className="flex-1 rounded-lg bg-blue-600 px-4 py-2 text-center font-semibold text-white hover:bg-blue-700"
                >
                  Modifier
                </Link>

                <button
                  type="button"
                  onClick={() => handleDelete(entry)}
                  className="flex-1 rounded-lg bg-red-600 px-4 py-2 font-semibold text-white hover:bg-red-700"
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
