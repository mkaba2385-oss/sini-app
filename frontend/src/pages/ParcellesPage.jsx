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
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-4xl">
          <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
            <p className="text-gray-600">
              Chargement des parcelles...
            </p>
          </div>
        </div>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-4xl">
          <div className="rounded-xl bg-red-100 p-4 text-red-700 sm:p-5">
            Impossible de récupérer vos parcelles.
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
            <h1 className="text-2xl font-bold text-green-800 sm:text-3xl">
              Mes parcelles 🌱
            </h1>

            <p className="mt-2 text-sm text-gray-600 sm:text-base">
              Retrouvez ici toutes vos parcelles.
            </p>
          </div>

          <Link
            to="/parcelles/new"
            className="w-full rounded-lg bg-green-700 px-4 py-3 text-center font-semibold text-white hover:bg-green-800 sm:w-auto"
          >
            + Ajouter
          </Link>
        </div>

        {/* Aucune parcelle */}
        {parcelles.length === 0 ? (
          <div className="rounded-2xl bg-white p-6 text-center shadow sm:p-8">
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
          <div className="grid gap-4 sm:gap-6 md:grid-cols-2">
            {parcelles.map((parcelle) => (
              <article
                key={parcelle.id}
                className="rounded-2xl bg-white p-4 shadow sm:p-6"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <h2 className="break-words text-xl font-bold text-green-800">
                      {parcelle.name}
                    </h2>

                    <p className="mt-1 text-sm text-gray-500">
                      {parcelle.culture}
                    </p>
                  </div>
                </div>

                <div className="mt-4 rounded-xl bg-gray-50 p-4">
                  <div className="grid gap-3 text-sm sm:grid-cols-2">
                    <div>
                      <p className="text-gray-500">
                        Culture
                      </p>

                      <p className="mt-1 font-semibold text-gray-800">
                        {parcelle.culture}
                      </p>
                    </div>

                    <div>
                      <p className="text-gray-500">
                        Superficie
                      </p>

                      <p className="mt-1 font-semibold text-gray-800">
                        {parcelle.superficie_ha} ha
                      </p>
                    </div>

                    <div>
                      <p className="text-gray-500">
                        Région
                      </p>

                      <p className="mt-1 font-semibold text-gray-800">
                        {parcelle.region}
                      </p>
                    </div>

                    {parcelle.commune && (
                      <div>
                        <p className="text-gray-500">
                          Commune
                        </p>

                        <p className="mt-1 font-semibold text-gray-800">
                          {parcelle.commune}
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Météo de la région */}
                <ParcelleWeather
                  region={parcelle.region}
                />

                {/* Actions */}
                <div className="mt-6 grid gap-2 sm:grid-cols-3">
                  <Link
                    to={`/parcelles/${parcelle.id}/journal`}
                    className="rounded-lg bg-green-600 px-3 py-3 text-center text-sm font-semibold text-white hover:bg-green-700"
                  >
                    Journal
                  </Link>

                  <Link
                    to={`/parcelles/${parcelle.id}/edit`}
                    className="rounded-lg bg-blue-600 px-3 py-3 text-center text-sm font-semibold text-white hover:bg-blue-700"
                  >
                    Modifier
                  </Link>

                  <button
                    type="button"
                    onClick={() => handleDelete(parcelle)}
                    className="rounded-lg bg-red-600 px-3 py-3 text-sm font-semibold text-white hover:bg-red-700"
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