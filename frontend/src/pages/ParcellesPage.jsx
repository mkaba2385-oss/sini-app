import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { deleteParcelle, getParcelles } from "../api/parcelles.js";
import { getWeather } from "../api/weather.js";

function ParcelleWeather({ region }) {
  const {
    data: weather,
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["weather", region],
    queryFn: () => getWeather(region),
    enabled: Boolean(region),
  });

  if (isLoading) {
    return (
      <div className="mt-5 rounded-xl bg-gray-50 p-4">
        <p className="text-sm text-gray-500">
          Chargement de la météo...
        </p>
      </div>
    );
  }

  if (isError || !weather) {
    return (
      <div className="mt-5 rounded-xl bg-red-50 p-4">
        <p className="text-sm text-red-600">
          Météo indisponible.
        </p>
      </div>
    );
  }

  return (
    <div className="mt-5 rounded-xl bg-blue-50 p-4">
      <h3 className="mb-3 font-semibold text-blue-800">
        🌤️ Météo
      </h3>

      <div className="grid grid-cols-2 gap-3 text-sm">
        <div>
          <p className="text-gray-500">Température</p>
          <p className="font-bold text-gray-800">
            {Number(weather.temperature).toFixed(1)} °C
          </p>
        </div>

        <div>
          <p className="text-gray-500">Humidité</p>
          <p className="font-bold text-gray-800">
            {weather.humidite} %
          </p>
        </div>

        <div>
          <p className="text-gray-500">Pluie</p>
          <p className="font-bold text-gray-800">
            {weather.pluie_mm} mm
          </p>
        </div>

        <div>
          <p className="text-gray-500">Vent</p>
          <p className="font-bold text-gray-800">
            {Number(weather.vent_kmh).toFixed(1)} km/h
          </p>
        </div>
      </div>

      {weather.alerte_secheresse && (
        <div className="mt-4 rounded-lg bg-orange-100 p-3">
          <p className="text-sm font-semibold text-orange-800">
            ⚠️ Alerte sécheresse
          </p>
        </div>
      )}

      {!weather.alerte_secheresse && (
        <div className="mt-4 rounded-lg bg-green-100 p-3">
          <p className="text-sm font-semibold text-green-800">
            ✅ Pas d'alerte sécheresse
          </p>
        </div>
      )}
    </div>
  );
}

function ParcellesPage() {
  const queryClient = useQueryClient();

  const {
    data: parcelles = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["parcelles"],
    queryFn: getParcelles,
  });

  async function handleDelete(parcelle) {
    const confirmed = window.confirm(
      `Voulez-vous vraiment supprimer la parcelle "${parcelle.name}" ?`,
    );

    if (!confirmed) {
      return;
    }

    try {
      await deleteParcelle(parcelle.id);

      await queryClient.invalidateQueries({
        queryKey: ["parcelles"],
      });
    } catch (error) {
      console.error(error);
      window.alert("Impossible de supprimer la parcelle.");
    }
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-green-50 p-6">
        <div className="mx-auto max-w-4xl">
          <p className="text-gray-600">
            Chargement des parcelles...
          </p>
        </div>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="min-h-screen bg-green-50 p-6">
        <div className="mx-auto max-w-4xl">
          <div className="rounded-xl bg-red-100 p-4 text-red-700">
            Impossible de récupérer vos parcelles.
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 p-6">
      <div className="mx-auto max-w-4xl">
        {/* En-tête */}
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-green-800">
              Mes parcelles 🌱
            </h1>

            <p className="mt-2 text-gray-600">
              Retrouvez ici toutes vos parcelles.
            </p>
          </div>

          <Link
            to="/parcelles/new"
            className="rounded-lg bg-green-700 px-4 py-3 font-semibold text-white hover:bg-green-800"
          >
            + Ajouter
          </Link>
        </div>

        {/* Aucune parcelle */}
        {parcelles.length === 0 ? (
          <div className="rounded-2xl bg-white p-8 text-center shadow">
            <p className="mb-4 text-gray-600">
              Vous n'avez encore aucune parcelle.
            </p>

            <Link
              to="/parcelles/new"
              className="font-semibold text-green-700 hover:text-green-800"
            >
              Ajouter ma première parcelle →
            </Link>
          </div>
        ) : (
          /* Liste des parcelles */
          <div className="grid gap-6 md:grid-cols-2">
            {parcelles.map((parcelle) => (
              <article
                key={parcelle.id}
                className="rounded-2xl bg-white p-6 shadow"
              >
                <h2 className="text-xl font-bold text-green-800">
                  {parcelle.name}
                </h2>

                <div className="mt-4 space-y-2 text-gray-700">
                  <p>
                    <strong>Culture :</strong>{" "}
                    {parcelle.culture}
                  </p>

                  <p>
                    <strong>Superficie :</strong>{" "}
                    {parcelle.superficie_ha} ha
                  </p>

                  <p>
                    <strong>Région :</strong>{" "}
                    {parcelle.region}
                  </p>

                  {parcelle.commune && (
                    <p>
                      <strong>Commune :</strong>{" "}
                      {parcelle.commune}
                    </p>
                  )}
                </div>

                {/* Météo de la région */}
                <ParcelleWeather region={parcelle.region} />

                {/* Actions */}
                <div className="mt-6 grid grid-cols-3 gap-2">
                  <Link
                    to={`/parcelles/${parcelle.id}/journal`}
                    className="rounded-lg bg-green-600 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-green-700"
                  >
                    Journal
                  </Link>

                  <Link
                    to={`/parcelles/${parcelle.id}/edit`}
                    className="rounded-lg bg-blue-600 px-3 py-2 text-center text-sm font-semibold text-white hover:bg-blue-700"
                  >
                    Modifier
                  </Link>

                  <button
                    type="button"
                    onClick={() => handleDelete(parcelle)}
                    className="rounded-lg bg-red-600 px-3 py-2 text-sm font-semibold text-white hover:bg-red-700"
                  >
                    Supprimer
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </main>
  );
}

export default ParcellesPage;
