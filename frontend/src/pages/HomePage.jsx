import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { getParcelles } from "../api/parcelles.js";
import { getJournalByParcelle } from "../api/journal.js";
import { getWeather } from "../api/weather.js";
import useAuthStore from "../store/authStore.js";

function HomePage() {
  const { t } = useTranslation();
  const user = useAuthStore((state) => state.user);

  // ==================== PARCELLES ====================

  const {
    data: parcelles = [],
    isLoading: loadingParcelles,
  } = useQuery({
    queryKey: ["parcelles"],
    queryFn: getParcelles,
  });

  // ==================== JOURNAL ====================

  const {
    data: journalEntries = [],
    isLoading: loadingJournal,
  } = useQuery({
    queryKey: [
      "journal-home",
      parcelles.map((parcelle) => parcelle.id),
    ],
    queryFn: async () => {
      const journals = await Promise.all(
        parcelles.map((parcelle) =>
          getJournalByParcelle(parcelle.id),
        ),
      );

      return journals.flat();
    },
    enabled: parcelles.length > 0,
  });

  // ==================== MÉTÉO ====================

  const {
    data: weather,
    isLoading: loadingWeather,
    isError: weatherError,
  } = useQuery({
    queryKey: ["weather", user?.region],
    queryFn: () => getWeather(user.region),
    enabled: Boolean(user?.region),
  });

  return (
    <main className="min-h-screen bg-green-50 p-6">
      <div className="mx-auto max-w-6xl">

        {/* ==================== EN-TÊTE ==================== */}

        <header className="mb-8">
          <h1 className="text-3xl font-bold text-green-800">
            {t("app.name")} 🌱
          </h1>

          <p className="mt-2 text-gray-600">
            Bienvenue {user?.full_name || ""} !
          </p>

          {user?.region && (
            <p className="mt-1 text-sm text-gray-500">
              📍 Région : {user.region}
            </p>
          )}
        </header>

        {/* ==================== ACTIONS RAPIDES ==================== */}

        <section className="mb-8">
          <h2 className="mb-4 text-xl font-bold text-green-800">
            Accès rapides
          </h2>

          <div className="grid gap-4 md:grid-cols-3">

            <Link
              to="/parcelles"
              className="rounded-2xl bg-white p-6 shadow transition hover:-translate-y-1 hover:shadow-lg"
            >
              <div className="text-3xl">🌱</div>

              <h3 className="mt-3 text-lg font-bold text-green-800">
                Mes parcelles
              </h3>

              <p className="mt-1 text-sm text-gray-600">
                Voir et gérer mes parcelles
              </p>
            </Link>

            <Link
              to="/parcelles/new"
              className="rounded-2xl bg-white p-6 shadow transition hover:-translate-y-1 hover:shadow-lg"
            >
              <div className="text-3xl">➕</div>

              <h3 className="mt-3 text-lg font-bold text-green-800">
                Ajouter une parcelle
              </h3>

              <p className="mt-1 text-sm text-gray-600">
                Enregistrer une nouvelle parcelle
              </p>
            </Link>

            <Link
              to="/parcelles"
              className="rounded-2xl bg-white p-6 shadow transition hover:-translate-y-1 hover:shadow-lg"
            >
              <div className="text-3xl">📖</div>

              <h3 className="mt-3 text-lg font-bold text-green-800">
                Journal agricole
              </h3>

              <p className="mt-1 text-sm text-gray-600">
                Consulter les activités de mes parcelles
              </p>
            </Link>

          </div>
        </section>

        {/* ==================== STATISTIQUES ==================== */}

        <section className="mb-8">
          <h2 className="mb-4 text-xl font-bold text-green-800">
            Vue d'ensemble
          </h2>

          <div className="grid gap-4 md:grid-cols-3">

            {/* Nombre de parcelles */}

            <div className="rounded-2xl bg-white p-6 shadow">
              <p className="text-sm font-medium text-gray-500">
                Nombre de parcelles
              </p>

              <p className="mt-2 text-4xl font-bold text-green-700">
                {loadingParcelles ? "..." : parcelles.length}
              </p>

              <Link
                to="/parcelles"
                className="mt-3 inline-block text-sm font-semibold text-green-700 hover:text-green-900"
              >
                Voir mes parcelles →
              </Link>
            </div>

            {/* Activités agricoles */}

            <div className="rounded-2xl bg-white p-6 shadow">
              <p className="text-sm font-medium text-gray-500">
                Activités agricoles
              </p>

              <p className="mt-2 text-4xl font-bold text-green-700">
                {loadingJournal ? "..." : journalEntries.length}
              </p>

              <Link
                to="/parcelles"
                className="mt-3 inline-block text-sm font-semibold text-green-700 hover:text-green-900"
              >
                Voir mon journal →
              </Link>
            </div>

            {/* Région */}

            <div className="rounded-2xl bg-white p-6 shadow">
              <p className="text-sm font-medium text-gray-500">
                Région
              </p>

              <p className="mt-2 text-2xl font-bold text-green-700">
                {user?.region || "Non renseignée"}
              </p>

              <p className="mt-2 text-sm text-gray-500">
                Région utilisée pour les données météo.
              </p>
            </div>

          </div>
        </section>

        {/* ==================== MÉTÉO ==================== */}

        <section>
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-bold text-green-800">
              🌤️ Météo du jour
            </h2>

            {user?.region && (
              <span className="text-sm text-gray-500">
                {user.region}
              </span>
            )}
          </div>

          {/* Chargement */}

          {loadingWeather && (
            <div className="rounded-2xl bg-white p-6 shadow">
              <p className="text-gray-600">
                Chargement de la météo...
              </p>
            </div>
          )}

          {/* Erreur */}

          {weatherError && (
            <div className="rounded-2xl bg-red-100 p-5 text-red-700 shadow">
              <p className="font-semibold">
                Impossible de récupérer la météo.
              </p>

              <p className="mt-1 text-sm">
                Vérifiez la connexion au serveur météo.
              </p>
            </div>
          )}

          {/* Météo */}

          {weather && (
            <div className="rounded-2xl bg-white p-6 shadow">

              <div className="grid gap-4 md:grid-cols-4">

                {/* Température */}

                <div className="rounded-xl bg-orange-50 p-5">
                  <p className="text-sm text-gray-500">
                    Température
                  </p>

                  <p className="mt-2 text-3xl font-bold text-orange-700">
                    {Number(weather.temperature).toFixed(1)} °C
                  </p>
                </div>

                {/* Humidité */}

                <div className="rounded-xl bg-blue-50 p-5">
                  <p className="text-sm text-gray-500">
                    Humidité
                  </p>

                  <p className="mt-2 text-3xl font-bold text-blue-700">
                    {weather.humidite} %
                  </p>
                </div>

                {/* Pluie */}

                <div className="rounded-xl bg-sky-50 p-5">
                  <p className="text-sm text-gray-500">
                    Pluie
                  </p>

                  <p className="mt-2 text-3xl font-bold text-sky-700">
                    {weather.pluie_mm} mm
                  </p>
                </div>

                {/* Vent */}

                <div className="rounded-xl bg-gray-50 p-5">
                  <p className="text-sm text-gray-500">
                    Vent
                  </p>

                  <p className="mt-2 text-3xl font-bold text-gray-700">
                    {Number(weather.vent_kmh).toFixed(1)} km/h
                  </p>
                </div>

              </div>

              {/* Alerte sécheresse */}

              {weather.alerte_secheresse ? (
                <div className="mt-5 rounded-xl bg-orange-100 p-4">
                  <p className="font-bold text-orange-800">
                    ⚠️ Alerte sécheresse
                  </p>

                  <p className="mt-1 text-sm text-orange-700">
                    Surveillez l'humidité de vos parcelles et
                    pensez à vos besoins en irrigation.
                  </p>
                </div>
              ) : (
                <div className="mt-5 rounded-xl bg-green-100 p-4">
                  <p className="font-semibold text-green-800">
                    ✅ Aucune alerte sécheresse actuellement.
                  </p>
                </div>
              )}

            </div>
          )}
        </section>

      </div>
    </main>
  );
}

export default HomePage;