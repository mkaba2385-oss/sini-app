import { useQuery, useQueryClient } from "@tanstack/react-query";
import { Link } from "react-router-dom";

import { deleteParcelle, getParcelles } from "../api/parcelles.js";
import { getWeather } from "../api/weather.js";

function Icon({ children, className = "" }) {
  return (
    <div
      className={`flex h-11 w-11 items-center justify-center rounded-xl ${className}`}
    >
      {children}
    </div>
  );
}

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
      <div className="mt-5 rounded-2xl border border-slate-100 bg-slate-50 p-5">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 animate-pulse rounded-xl bg-slate-200" />

          <div className="flex-1">
            <div className="h-3 w-24 animate-pulse rounded bg-slate-200" />
            <div className="mt-2 h-3 w-36 animate-pulse rounded bg-slate-200" />
          </div>
        </div>
      </div>
    );
  }

  if (isError || !weather) {
    return (
      <div className="mt-5 rounded-2xl border border-red-100 bg-red-50 p-5">
        <p className="text-sm font-medium text-red-700">
          Météo indisponible pour cette région.
        </p>
      </div>
    );
  }

  return (
    <div className="mt-5 overflow-hidden rounded-2xl border border-slate-100 bg-slate-50">
      {/* En-tête météo */}
      <div className="flex items-center justify-between border-b border-slate-100 bg-white px-5 py-4">
        <div className="flex items-center gap-3">
          <Icon className="bg-blue-50 text-xl">☁️</Icon>

          <div>
            <p className="text-sm font-semibold text-slate-900">
              Conditions météo
            </p>

            <p className="text-xs text-slate-500">
              {region}
            </p>
          </div>
        </div>

        <span className="text-xs font-medium text-slate-400">
          Aujourd'hui
        </span>
      </div>

      {/* Données météo */}
      <div className="grid grid-cols-2 divide-x divide-y divide-slate-200 sm:grid-cols-4 sm:divide-y-0">
        <div className="p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Température
          </p>

          <p className="mt-1 text-lg font-bold text-slate-900">
            {Number(weather.temperature).toFixed(1)} °C
          </p>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Humidité
          </p>

          <p className="mt-1 text-lg font-bold text-slate-900">
            {weather.humidite} %
          </p>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Pluie
          </p>

          <p className="mt-1 text-lg font-bold text-slate-900">
            {weather.pluie_mm} mm
          </p>
        </div>

        <div className="p-4">
          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
            Vent
          </p>

          <p className="mt-1 text-lg font-bold text-slate-900">
            {Number(weather.vent_kmh).toFixed(1)} km/h
          </p>
        </div>
      </div>

      {/* État sécheresse */}
      {weather.alerte_secheresse ? (
        <div className="border-t border-orange-100 bg-orange-50 px-5 py-4">
          <p className="text-sm font-semibold text-orange-800">
            Alerte sécheresse
          </p>

          <p className="mt-1 text-xs text-orange-700">
            Surveillez les conditions de votre parcelle.
          </p>
        </div>
      ) : (
        <div className="border-t border-green-100 bg-green-50 px-5 py-4">
          <p className="text-sm font-semibold text-green-800">
            Conditions normales
          </p>

          <p className="mt-1 text-xs text-green-700">
            Aucune alerte sécheresse actuellement.
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

  /* ==================== CHARGEMENT ==================== */

  if (isLoading) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="rounded-3xl border border-slate-200 bg-white p-8 shadow-sm">
            <div className="animate-pulse">
              <div className="h-8 w-56 rounded-lg bg-slate-200" />
              <div className="mt-3 h-4 w-80 max-w-full rounded bg-slate-200" />

              <div className="mt-8 grid gap-5 md:grid-cols-2">
                <div className="h-72 rounded-2xl bg-slate-100" />
                <div className="h-72 rounded-2xl bg-slate-100" />
              </div>
            </div>
          </div>
        </div>
      </main>
    );
  }

  /* ==================== ERREUR ==================== */

  if (isError) {
    return (
      <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-6xl">
          <div className="rounded-3xl border border-red-100 bg-red-50 p-6">
            <p className="font-semibold text-red-800">
              Impossible de récupérer vos parcelles.
            </p>

            <p className="mt-1 text-sm text-red-600">
              Vérifiez votre connexion puis réessayez.
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-8 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-6xl">

        {/* ==================== EN-TÊTE ==================== */}

        <header className="mb-8">
          <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <div className="mb-3 inline-flex items-center gap-2 rounded-full bg-green-100 px-4 py-2 text-sm font-semibold text-green-800">
                <span>🌱</span>
                <span>Mon exploitation</span>
              </div>

              <h1 className="text-3xl font-bold tracking-tight text-slate-950 sm:text-4xl">
                Mes parcelles
              </h1>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500 sm:text-base">
                Retrouvez et gérez facilement vos parcelles agricoles
                depuis Sini.
              </p>
            </div>

            <Link
              to="/parcelles/new"
              className="inline-flex items-center justify-center gap-2 rounded-xl bg-green-700 px-5 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-green-800 hover:shadow-md focus:outline-none focus:ring-2 focus:ring-green-600 focus:ring-offset-2"
            >
              <span className="text-lg leading-none">+</span>
              <span>Ajouter une parcelle</span>
            </Link>
          </div>
        </header>

        {/* ==================== STATISTIQUES ==================== */}

        <section className="mb-8">
          <div className="grid gap-4 sm:grid-cols-3">

            {/* Nombre de parcelles */}

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <Icon className="bg-green-50 text-green-700">
                  🌱
                </Icon>

                <span className="text-sm text-slate-300">
                  →
                </span>
              </div>

              <p className="mt-5 text-sm font-medium text-slate-500">
                Total des parcelles
              </p>

              <p className="mt-1 text-3xl font-bold text-slate-950">
                {parcelles.length}
              </p>
            </div>

            {/* Cultures */}

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <Icon className="bg-blue-50 text-blue-700">
                  ☘️
                </Icon>

                <span className="text-sm text-slate-300">
                  →
                </span>
              </div>

              <p className="mt-5 text-sm font-medium text-slate-500">
                Cultures enregistrées
              </p>

              <p className="mt-1 text-3xl font-bold text-slate-950">
                {new Set(parcelles.map((parcelle) => parcelle.culture)).size}
              </p>
            </div>

            {/* Superficie */}

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-start justify-between">
                <Icon className="bg-amber-50 text-amber-700">
                  ◫
                </Icon>

                <span className="text-sm text-slate-300">
                  →
                </span>
              </div>

              <p className="mt-5 text-sm font-medium text-slate-500">
                Superficie totale
              </p>

              <p className="mt-1 text-3xl font-bold text-slate-950">
                {parcelles
                  .reduce(
                    (total, parcelle) =>
                      total + Number(parcelle.superficie_ha || 0),
                    0,
                  )
                  .toFixed(1)}{" "}
                <span className="text-lg font-semibold text-slate-500">
                  ha
                </span>
              </p>
            </div>

          </div>
        </section>

        {/* ==================== LISTE ==================== */}

        <section>
          <div className="mb-5 flex items-end justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-950">
                Vos parcelles
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Informations et conditions actuelles
              </p>
            </div>

            {parcelles.length > 0 && (
              <span className="hidden rounded-full bg-white px-3 py-1.5 text-xs font-semibold text-slate-500 shadow-sm ring-1 ring-slate-200 sm:inline-block">
                {parcelles.length}{" "}
                {parcelles.length > 1 ? "parcelles" : "parcelle"}
              </span>
            )}
          </div>

          {/* ==================== AUCUNE PARCELLE ==================== */}

          {parcelles.length === 0 ? (
            <div className="rounded-3xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center shadow-sm">
              <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-green-50 text-3xl">
                🌱
              </div>

              <h3 className="mt-5 text-lg font-bold text-slate-950">
                Aucune parcelle enregistrée
              </h3>

              <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500">
                Commencez par ajouter votre première parcelle pour
                suivre vos cultures et vos activités agricoles.
              </p>

              <Link
                to="/parcelles/new"
                className="mt-6 inline-flex items-center justify-center rounded-xl bg-green-700 px-5 py-3 text-sm font-semibold text-white transition hover:bg-green-800"
              >
                Ajouter ma première parcelle
              </Link>
            </div>
          ) : (
            /* ==================== CARTES ==================== */

            <div className="grid gap-5 lg:grid-cols-2">
              {parcelles.map((parcelle) => (
                <article
                  key={parcelle.id}
                  className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-sm transition duration-200 hover:-translate-y-0.5 hover:shadow-md"
                >
                  {/* En-tête de carte */}

                  <div className="border-b border-slate-100 px-5 py-5 sm:px-6">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex min-w-0 items-center gap-4">
                        <Icon className="shrink-0 bg-green-50 text-xl">
                          🌱
                        </Icon>

                        <div className="min-w-0">
                          <h3 className="break-words text-xl font-bold text-slate-950">
                            {parcelle.name}
                          </h3>

                          <p className="mt-1 text-sm font-medium text-green-700">
                            {parcelle.culture}
                          </p>
                        </div>
                      </div>

                      <span className="shrink-0 rounded-full bg-green-50 px-3 py-1 text-xs font-semibold text-green-700">
                        Active
                      </span>
                    </div>
                  </div>

                  {/* Informations */}

                  <div className="px-5 py-5 sm:px-6">
                    <div className="grid grid-cols-2 gap-3">

                      <div className="rounded-2xl bg-slate-50 p-4">
                        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                          Culture
                        </p>

                        <p className="mt-1 text-sm font-semibold text-slate-900">
                          {parcelle.culture}
                        </p>
                      </div>

                      <div className="rounded-2xl bg-slate-50 p-4">
                        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                          Superficie
                        </p>

                        <p className="mt-1 text-sm font-semibold text-slate-900">
                          {parcelle.superficie_ha} ha
                        </p>
                      </div>

                      <div className="rounded-2xl bg-slate-50 p-4">
                        <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                          Région
                        </p>

                        <p className="mt-1 text-sm font-semibold text-slate-900">
                          {parcelle.region}
                        </p>
                      </div>

                      {parcelle.commune ? (
                        <div className="rounded-2xl bg-slate-50 p-4">
                          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                            Commune
                          </p>

                          <p className="mt-1 break-words text-sm font-semibold text-slate-900">
                            {parcelle.commune}
                          </p>
                        </div>
                      ) : (
                        <div className="rounded-2xl bg-slate-50 p-4">
                          <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
                            Localisation
                          </p>

                          <p className="mt-1 text-sm font-semibold text-slate-400">
                            Non renseignée
                          </p>
                        </div>
                      )}

                    </div>

                    {/* Météo */}

                    <ParcelleWeather
                      region={parcelle.region}
                    />
                  </div>

                  {/* Actions */}

                  <div className="border-t border-slate-100 bg-slate-50/60 px-5 py-4 sm:px-6">
                    <div className="grid gap-2 sm:grid-cols-3">

                      <Link
                        to={`/parcelles/${parcelle.id}/journal`}
                        className="inline-flex items-center justify-center rounded-xl bg-green-700 px-3 py-3 text-sm font-semibold text-white transition hover:bg-green-800"
                      >
                        Journal
                      </Link>

                      <Link
                        to={`/parcelles/${parcelle.id}/edit`}
                        className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-white px-3 py-3 text-sm font-semibold text-slate-700 transition hover:bg-slate-100"
                      >
                        Modifier
                      </Link>

                      <button
                        type="button"
                        onClick={() => handleDelete(parcelle)}
                        className="inline-flex items-center justify-center rounded-xl border border-red-100 bg-white px-3 py-3 text-sm font-semibold text-red-600 transition hover:bg-red-50"
                      >
                        Supprimer
                      </button>

                    </div>
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

export default ParcellesPage;