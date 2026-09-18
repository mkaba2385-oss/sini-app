import { useEffect, useState } from "react";

import api from "../api/client.js";

function PlantDiagnosisPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    return () => {
      if (preview) {
        URL.revokeObjectURL(preview);
      }
    };
  }, [preview]);

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0] ?? null;

    setResult(null);
    setError("");

    if (!selectedFile) {
      setFile(null);
      setPreview(null);
      return;
    }

    if (!selectedFile.type.startsWith("image/")) {
      setFile(null);
      setPreview(null);
      setError("Veuillez sélectionner une image.");
      return;
    }

    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
  }

  async function handlePredict() {
    if (!file) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await api.post(
        "/plant-diagnosis/predict",
        formData,
      );

      setResult(response.data);
    } catch (requestError) {
      const detail = requestError.response?.data?.detail;

      const message =
        typeof detail === "string"
          ? detail
          : "Une erreur est survenue lors de l'analyse de la photo.";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  function handleRemovePhoto() {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError("");
  }

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
                Diagnostic agricole
              </div>

              <h1 className="text-3xl font-bold tracking-tight text-white sm:text-4xl">
                Diagnostiquer une plante
              </h1>

              <p className="mt-3 max-w-2xl text-sm leading-6 text-green-100 sm:text-base">
                Prenez une photo de votre plante ou importez une image pour
                identifier une maladie et obtenir une recommandation adaptée.
              </p>
            </div>
          </div>
        </section>

        {/* ==================== PHOTO ==================== */}

        <section className="mb-8">
          <div className="mb-4">
            <h2 className="text-xl font-bold tracking-tight text-slate-900">
              Photo de la plante
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Prenez une photo avec votre appareil photo ou importez une image
              depuis votre appareil.
            </p>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-7">
            {/* ==================== ACTIONS ==================== */}

            {!preview && (
              <div className="grid gap-4 sm:grid-cols-2">
                {/* Appareil photo */}

                <label
                  htmlFor="plant-camera"
                  className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-green-300 bg-green-50/50 px-6 py-10 text-center transition-colors hover:border-green-500 hover:bg-green-50"
                >
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-green-100 text-green-700">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.8"
                      className="h-7 w-7"
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M4 7.5A2.5 2.5 0 0 1 6.5 5h2l1-1.5h5L15.5 5h2A2.5 2.5 0 0 1 20 7.5v9A2.5 2.5 0 0 1 17.5 19h-11A2.5 2.5 0 0 1 4 16.5v-9Z"
                      />

                      <circle cx="12" cy="12" r="3.5" />
                    </svg>
                  </div>

                  <p className="mt-4 font-semibold text-slate-900">
                    Prendre une photo
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Utiliser l'appareil photo
                  </p>

                  <input
                    id="plant-camera"
                    type="file"
                    accept="image/*"
                    capture="environment"
                    onChange={handleFileChange}
                    className="sr-only"
                  />
                </label>

                {/* Importer */}

                <label
                  htmlFor="plant-file"
                  className="flex cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-slate-300 px-6 py-10 text-center transition-colors hover:border-green-400 hover:bg-green-50/50"
                >
                  <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-slate-100 text-slate-700">
                    <svg
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.8"
                      className="h-7 w-7"
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M4 7.5A2.5 2.5 0 0 1 6.5 5h3l1.5-2h4L16.5 5h1A2.5 2.5 0 0 1 20 7.5v9A2.5 2.5 0 0 1 17.5 19h-11A2.5 2.5 0 0 1 4 16.5v-9Z"
                      />

                      <circle cx="12" cy="12" r="3.5" />

                      <path
                        strokeLinecap="round"
                        d="M17 8h.01"
                      />
                    </svg>
                  </div>

                  <p className="mt-4 font-semibold text-slate-900">
                    Importer une photo
                  </p>

                  <p className="mt-1 text-sm text-slate-500">
                    Depuis votre galerie ou vos fichiers
                  </p>

                  <input
                    id="plant-file"
                    type="file"
                    accept="image/*"
                    onChange={handleFileChange}
                    className="sr-only"
                  />
                </label>
              </div>
            )}

            {/* ==================== APERÇU ==================== */}

            {preview && (
              <div>
                <div className="mb-3 flex items-center justify-between gap-4">
                  <p className="text-sm font-semibold text-slate-700">
                    Photo sélectionnée
                  </p>

                  {file && (
                    <p className="max-w-[60%] truncate text-xs text-slate-400">
                      {file.name}
                    </p>
                  )}
                </div>

                <div className="overflow-hidden rounded-2xl border border-slate-200 bg-slate-50">
                  <img
                    src={preview}
                    alt="Plante sélectionnée"
                    className="mx-auto max-h-[420px] w-full object-contain"
                  />
                </div>

                <div className="mt-5 flex flex-col gap-3 sm:flex-row">
                  <button
                    type="button"
                    onClick={handlePredict}
                    disabled={loading}
                    className="w-full rounded-xl bg-green-700 px-5 py-3 font-semibold text-white transition-colors hover:bg-green-800 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
                  >
                    {loading ? "Analyse en cours..." : "Analyser la plante"}
                  </button>

                  <button
                    type="button"
                    onClick={handleRemovePhoto}
                    disabled={loading}
                    className="w-full rounded-xl border border-slate-200 bg-white px-5 py-3 font-semibold text-slate-600 transition-colors hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto"
                  >
                    Choisir une autre photo
                  </button>
                </div>
              </div>
            )}

            {/* ==================== ERREUR ==================== */}

            {error && (
              <div className="mt-5 rounded-xl border border-red-200 bg-red-50 p-4">
                <div className="flex gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-red-100 font-bold text-red-600">
                    !
                  </div>

                  <div>
                    <p className="font-semibold text-red-800">
                      Une erreur est survenue
                    </p>

                    <p className="mt-1 text-sm text-red-700">{error}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </section>

        {/* ==================== DIAGNOSTIC ==================== */}

        {result && (
          <section>
            <div className="mb-4">
              <h2 className="text-xl font-bold tracking-tight text-slate-900">
                Résultat du diagnostic
              </h2>

              <p className="mt-1 text-sm text-slate-500">
                Analyse réalisée à partir de la photo envoyée.
              </p>
            </div>

            <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
              {/* Maladie */}

              <div className="border-b border-slate-100 p-6 sm:p-7">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-orange-50 text-orange-600">
                    !
                  </div>

                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Maladie détectée
                    </p>

                    <p className="mt-1 text-2xl font-bold tracking-tight text-slate-900">
                      {result.maladie}
                    </p>
                  </div>
                </div>
              </div>

              {/* Confiance */}

              <div className="border-b border-slate-100 p-6 sm:p-7">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
                      Niveau de confiance
                    </p>

                    <p className="mt-1 text-2xl font-bold text-slate-900">
                      {(result.confiance * 100).toFixed(1)} %
                    </p>
                  </div>

                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600">
                    %
                  </div>
                </div>

                <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-100">
                  <div
                    className="h-full rounded-full bg-green-600"
                    style={{
                      width: `${result.confiance * 100}%`,
                    }}
                  />
                </div>
              </div>

              {/* Traitement */}

              <div className="bg-green-50 p-6 sm:p-7">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-green-100 text-green-700">
                    ✓
                  </div>

                  <div>
                    <p className="text-xs font-semibold uppercase tracking-wide text-green-700">
                      Traitement recommandé
                    </p>

                    <p className="mt-2 leading-7 text-green-950">
                      {result.traitement}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}
      </div>
    </main>
  );
}

export default PlantDiagnosisPage;