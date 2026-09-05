import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { getParcelles } from "../api/parcelles.js";
import { getJournalByParcelle } from "../api/journal.js";
import { getWeather } from "../api/weather.js";
import useAuthStore from "../store/authStore.js";

function HomePage() {
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
    <main className="min-h-screen bg-slate-50">
      <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8 lg:py-8">

        {/* ==================== HERO ==================== */}

        <section className="mb-8 overflow-hidden rounded-3xl bg-green-800 shadow-sm">
          <div className="relative px-6 py-8 sm:px-8 lg:px-10 lg:py-10">

            <div className="absolute -right-16 -top-20 h-64 w-64 rounded-full bg-green-700 opacity-50" />
            <div className="absolute -bottom-24 right-24 h-48 w-48 rounded-full bg-green-900 opacity-30" />

            <div className="relative max-w-3xl">
              <div className="mb-4 inline-flex items-center rounded-full bg-white/10 px-3 py-1.5 text-sm font-medium text-green-50 backdrop-blur">
                Tableau de bord agricole
              </div>

              <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Bonjour{" "}
                {user?.full_name?.split(" ")[0] || "agriculteur"}.
              </h1>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-green-100 sm:text-base">
                Retrouvez en un coup d'œil vos parcelles, vos
                activités agricoles et les conditions météo de
                votre région.
              </p>

              {user?.region && (
                <div className="mt-6 inline-flex items-center gap-2 rounded-xl bg-white/10 px-4 py-2.5 text-sm font-medium text-white backdrop-blur">
                  <span className="flex h-2.5 w-2.5 rounded-full bg-green-300" />
                  {user.region}
                </div>
              )}
            </div>
          </div>
        </section>

        {/* ==================== STATISTIQUES ==================== */}

        <section className="mb-8">
          <div className="mb-4">
            <h2 className="text-xl font-bold tracking-tight text-slate-900">
              Vue d'ensemble
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Les informations principales de votre exploitation
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

            {/* Parcelles */}

            <Link
              to="/parcelles"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-green-200 hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-green-50 text-green-700">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="h-6 w-6"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M7.5 13.5c2.5-.5 5-.2 7.2 1.2M9 9.5c2.2-.5 4.3 0 5.8 1.2"
                    />
                  </svg>
                </div>

                <span className="text-slate-300 transition-colors group-hover:text-green-600">
                  →
                </span>
              </div>

              <p className="mt-5 text-sm font-medium text-slate-500">
                Mes parcelles
              </p>

              <p className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
                {loadingParcelles ? "..." : parcelles.length}
              </p>

              <p className="mt-2 text-sm text-slate-500">
                Parcelle{parcelles.length > 1 ? "s" : ""} enregistrée
                {parcelles.length > 1 ? "s" : ""}
              </p>
            </Link>

            {/* Activités */}

            <Link
              to="/parcelles"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md"
            >
              <div className="flex items-start justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-blue-700">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="h-6 w-6"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M8 6h11M8 12h11M8 18h11"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M4.5 6h.01M4.5 12h.01M4.5 18h.01"
                    />
                  </svg>
                </div>

                <span className="text-slate-300 transition-colors group-hover:text-blue-600">
                  →
                </span>
              </div>

              <p className="mt-5 text-sm font-medium text-slate-500">
                Activités agricoles
              </p>

              <p className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
                {loadingJournal ? "..." : journalEntries.length}
              </p>

              <p className="mt-2 text-sm text-slate-500">
                Activité{journalEntries.length > 1 ? "s" : ""} dans
                le journal
              </p>
            </Link>

            {/* Région */}

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm sm:col-span-2 lg:col-span-1">
              <div className="flex items-start justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-amber-50 text-amber-700">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="h-6 w-6"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 21s7-5.2 7-11a7 7 0 1 0-14 0c0 5.8 7 11 7 11Z"
                    />
                    <circle cx="12" cy="10" r="2.3" />
                  </svg>
                </div>
              </div>

              <p className="mt-5 text-sm font-medium text-slate-500">
                Région
              </p>

              <p className="mt-1 truncate text-2xl font-bold tracking-tight text-slate-900">
                {user?.region || "Non renseignée"}
              </p>

              <p className="mt-2 text-sm text-slate-500">
                Zone utilisée pour les données météo.
              </p>
            </div>
          </div>
        </section>

        {/* ==================== MÉTÉO ==================== */}

        <section className="mb-8">
          <div className="mb-4 flex items-end justify-between gap-4">
            <div>
              <h2 className="text-xl font-bold tracking-tight text-slate-900">
                Météo du jour
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Conditions actuelles pour votre région
              </p>
            </div>

            {user?.region && (
              <span className="hidden rounded-lg bg-white px-3 py-2 text-sm font-medium text-slate-600 shadow-sm ring-1 ring-slate-200 sm:block">
                {user.region}
              </span>
            )}
          </div>

          {/* Chargement */}

          {loadingWeather && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="animate-pulse">
                <div className="h-5 w-32 rounded bg-slate-200" />

                <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  <div className="h-28 rounded-xl bg-slate-100" />
                  <div className="h-28 rounded-xl bg-slate-100" />
                  <div className="h-28 rounded-xl bg-slate-100" />
                  <div className="h-28 rounded-xl bg-slate-100" />
                </div>
              </div>
            </div>
          )}

          {/* Erreur */}

          {weatherError && (
            <div className="rounded-2xl border border-red-200 bg-red-50 p-6">
              <div className="flex gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-red-100 text-red-600">
                  !
                </div>

                <div>
                  <p className="font-semibold text-red-800">
                    Impossible de récupérer la météo.
                  </p>

                  <p className="mt-1 text-sm text-red-700">
                    Vérifiez la connexion au serveur météo puis
                    réessayez.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Météo */}

          {weather && (
            <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">

              {/* Résumé météo */}

              <div className="border-b border-slate-100 bg-gradient-to-r from-slate-50 to-white p-6 sm:p-7">
                <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-sm font-medium text-slate-500">
                      Conditions actuelles
                    </p>

                    <div className="mt-2 flex items-baseline gap-2">
                      <span className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">
                        {Number(weather.temperature).toFixed(1)}°
                      </span>

                      <span className="text-lg font-medium text-slate-500">
                        C
                      </span>
                    </div>

                    <p className="mt-2 text-sm text-slate-500">
                      Température actuelle
                    </p>
                  </div>

                  <div className="rounded-2xl bg-green-50 px-5 py-4">
                    <p className="text-xs font-semibold uppercase tracking-wider text-green-700">
                      Région
                    </p>

                    <p className="mt-1 font-semibold text-green-900">
                      {user?.region || "Non renseignée"}
                    </p>
                  </div>
                </div>
              </div>

              {/* Indicateurs */}

              <div className="grid sm:grid-cols-2 lg:grid-cols-4">

                {/* Humidité */}

                <div className="border-b border-slate-100 p-5 sm:border-r lg:border-b-0">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        className="h-5 w-5"
                        aria-hidden="true"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M12 3s6 6.2 6 11a6 6 0 1 1-12 0c0-4.8 6-11 6-11Z"
                        />
                      </svg>
                    </div>

                    <div>
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                        Humidité
                      </p>

                      <p className="mt-0.5 text-xl font-bold text-slate-900">
                        {weather.humidite} %
                      </p>
                    </div>
                  </div>
                </div>

                {/* Pluie */}

                <div className="border-b border-slate-100 p-5 lg:border-b-0 lg:border-r">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-sky-50 text-sky-600">
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        className="h-5 w-5"
                        aria-hidden="true"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M7 17.5 5.5 20M12 17.5 10.5 20M17 17.5 15.5 20"
                        />
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M18 14H6a4 4 0 1 1 1.3-7.8A5.5 5.5 0 0 1 18 9.5a2.5 2.5 0 0 1 0 4.5Z"
                        />
                      </svg>
                    </div>

                    <div>
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                        Pluie
                      </p>

                      <p className="mt-0.5 text-xl font-bold text-slate-900">
                        {weather.pluie_mm} mm
                      </p>
                    </div>
                  </div>
                </div>

                {/* Vent */}

                <div className="border-b border-slate-100 p-5 sm:border-r lg:border-b-0">
                  <div className="flex items-center gap-3">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-100 text-slate-600">
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        className="h-5 w-5"
                        aria-hidden="true"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M4 8h11a3 3 0 1 0-3-3"
                        />
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M4 12h14a3 3 0 1 1-3 3"
                        />
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M4 16h7"
                        />
                      </svg>
                    </div>

                    <div>
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                        Vent
                      </p>

                      <p className="mt-0.5 text-xl font-bold text-slate-900">
                        {Number(weather.vent_kmh).toFixed(1)} km/h
                      </p>
                    </div>
                  </div>
                </div>

                {/* État */}

                <div className="p-5">
                  <div className="flex items-center gap-3">
                    <div
                      className={`flex h-10 w-10 items-center justify-center rounded-xl ${
                        weather.alerte_secheresse
                          ? "bg-orange-50 text-orange-600"
                          : "bg-green-50 text-green-600"
                      }`}
                    >
                      {weather.alerte_secheresse ? "!" : "✓"}
                    </div>

                    <div>
                      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                        État
                      </p>

                      <p
                        className={`mt-0.5 text-sm font-bold ${
                          weather.alerte_secheresse
                            ? "text-orange-700"
                            : "text-green-700"
                        }`}
                      >
                        {weather.alerte_secheresse
                          ? "Alerte sécheresse"
                          : "Conditions normales"}
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Alerte */}

              {weather.alerte_secheresse ? (
                <div className="border-t border-orange-100 bg-orange-50 px-6 py-4">
                  <p className="font-semibold text-orange-800">
                    Alerte sécheresse
                  </p>

                  <p className="mt-1 text-sm text-orange-700">
                    Surveillez l'humidité de vos parcelles et
                    pensez à vos besoins en irrigation.
                  </p>
                </div>
              ) : (
                <div className="border-t border-green-100 bg-green-50 px-6 py-4">
                  <p className="font-semibold text-green-800">
                    Aucune alerte sécheresse actuellement.
                  </p>

                  <p className="mt-1 text-sm text-green-700">
                    Les conditions météo actuelles ne signalent
                    pas de risque de sécheresse.
                  </p>
                </div>
              )}
            </div>
          )}
        </section>

        {/* ==================== ACCÈS RAPIDES ==================== */}

        <section>
          <div className="mb-4">
            <h2 className="text-xl font-bold tracking-tight text-slate-900">
              Accès rapides
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Les actions les plus utiles pour votre exploitation
            </p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">

            {/* Parcelles */}

            <Link
              to="/parcelles"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-green-200 hover:shadow-md"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-green-50 text-green-700">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="h-6 w-6"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18Z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M7.5 13.5c2.5-.5 5-.2 7.2 1.2M9 9.5c2.2-.5 4.3 0 5.8 1.2"
                    />
                  </svg>
                </div>

                <span className="text-slate-300 transition-colors group-hover:text-green-600">
                  →
                </span>
              </div>

              <h3 className="mt-5 font-bold text-slate-900">
                Mes parcelles
              </h3>

              <p className="mt-1 text-sm leading-5 text-slate-500">
                Voir et gérer vos parcelles agricoles.
              </p>
            </Link>

            {/* Ajouter */}

            <Link
              to="/parcelles/new"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-green-200 hover:shadow-md"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-green-700 text-white">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    className="h-6 w-6"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 5v14M5 12h14"
                    />
                  </svg>
                </div>

                <span className="text-slate-300 transition-colors group-hover:text-green-600">
                  →
                </span>
              </div>

              <h3 className="mt-5 font-bold text-slate-900">
                Ajouter une parcelle
              </h3>

              <p className="mt-1 text-sm leading-5 text-slate-500">
                Enregistrer une nouvelle parcelle dans Sini.
              </p>
            </Link>

            {/* Journal */}

            <Link
              to="/parcelles"
              className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-md"
            >
              <div className="flex items-center justify-between">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-blue-50 text-blue-700">
                  <svg
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.8"
                    className="h-6 w-6"
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M6 4.5h9a3 3 0 0 1 3 3V20H9a3 3 0 0 0-3 3V4.5Z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M6 20h12"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M9 8h6M9 11.5h6"
                    />
                  </svg>
                </div>

                <span className="text-slate-300 transition-colors group-hover:text-blue-600">
                  →
                </span>
              </div>

              <h3 className="mt-5 font-bold text-slate-900">
                Journal agricole
              </h3>

              <p className="mt-1 text-sm leading-5 text-slate-500">
                Consulter les activités de vos parcelles.
              </p>
            </Link>
          </div>
        </section>

      </div>
    </main>
  );
}

export default HomePage;