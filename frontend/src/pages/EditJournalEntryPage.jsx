import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import {
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router-dom";

import {
  getJournalByParcelle,
  updateJournalEntry,
} from "../api/journal.js";

const actionTypes = [
  "Semis",
  "Irrigation",
  "Fertilisation",
  "Traitement phytosanitaire",
  "Désherbage",
  "Récolte",
  "Observation",
];

function EditJournalEntryPage() {
  const navigate = useNavigate();
  const { entryId } = useParams();
  const [searchParams] = useSearchParams();
  const queryClient = useQueryClient();

  const parcelleId = searchParams.get("parcelle");

  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const {
    data: entries = [],
    isLoading,
    isError,
  } = useQuery({
    queryKey: ["journal", parcelleId],
    queryFn: () => getJournalByParcelle(parcelleId),
    enabled: Boolean(parcelleId),
  });

  const entry = entries.find(
    (item) => item.id === Number(entryId),
  );

  const [form, setForm] = useState(() => ({
    action_type: entry?.action_type || "Observation",
    title: entry?.title || "",
    description: entry?.description || "",
    cout_fcfa: entry ? String(entry.cout_fcfa) : "0",
  }));

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));

    if (name === "cout_fcfa") {
      setError("");
    }
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!parcelleId) {
      setError("Aucune parcelle sélectionnée.");
      return;
    }

    const coutFcfa = Number(form.cout_fcfa);

    if (!Number.isFinite(coutFcfa) || coutFcfa < 0) {
      setError(
        "Le coût doit être un montant positif ou égal à 0 FCFA.",
      );
      return;
    }

    if (!Number.isInteger(coutFcfa)) {
      setError("Le coût doit être un nombre entier en FCFA.");
      return;
    }

    if (coutFcfa % 5 !== 0) {
      setError("Le coût doit être un multiple de 5 FCFA.");
      return;
    }

    setSaving(true);
    setError("");

    try {
      await updateJournalEntry(Number(entryId), {
        action_type: form.action_type,
        title: form.title,
        description: form.description || null,
        cout_fcfa: coutFcfa,
      });

      await queryClient.invalidateQueries({
        queryKey: ["journal", parcelleId],
      });

      navigate(`/parcelles/${parcelleId}/journal`);
    } catch (err) {
      console.error(err);

      setError("Impossible de modifier cette activité.");
    } finally {
      setSaving(false);
    }
  }

  function handleCancel() {
    if (parcelleId) {
      navigate(`/parcelles/${parcelleId}/journal`);
    } else {
      navigate("/parcelles");
    }
  }

  if (isLoading) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-green-50 to-white p-4 sm:p-6">
        <div className="mx-auto max-w-2xl">
          <div className="rounded-3xl border border-green-100 bg-white p-6 shadow-lg shadow-green-900/5 sm:p-8">
            <div className="flex items-center gap-3">
              <div className="h-5 w-5 animate-pulse rounded-full bg-green-200" />

              <p className="text-sm font-medium text-gray-600 sm:text-base">
                Chargement de l'activité...
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
        <div className="mx-auto max-w-2xl">
          <div className="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700 sm:p-6 sm:text-base">
            <p className="font-semibold">
              Impossible de récupérer cette activité.
            </p>

            <button
              type="button"
              onClick={handleCancel}
              className="mt-4 font-semibold text-red-800 underline underline-offset-2"
            >
              Retour au journal
            </button>
          </div>
        </div>
      </main>
    );
  }

  if (!entry) {
    return (
      <main className="min-h-screen bg-gradient-to-b from-green-50 to-white p-4 sm:p-6">
        <div className="mx-auto max-w-2xl">
          <div className="rounded-2xl border border-red-200 bg-red-50 p-5 text-sm text-red-700 sm:p-6 sm:text-base">
            <p className="font-semibold">
              Activité introuvable.
            </p>

            <button
              type="button"
              onClick={handleCancel}
              className="mt-4 font-semibold text-red-800 underline underline-offset-2"
            >
              Retour au journal
            </button>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-green-50 to-white p-4 sm:p-6">
      <div className="mx-auto max-w-2xl">
        {/* Retour */}
        <button
          type="button"
          onClick={handleCancel}
          className="mb-5 inline-flex items-center gap-2 text-sm font-semibold text-green-700 transition hover:text-green-900 sm:mb-6 sm:text-base"
        >
          <span className="text-lg">←</span>
          Retour au journal
        </button>

        {/* Carte principale */}
        <div className="overflow-hidden rounded-3xl border border-green-100 bg-white shadow-lg shadow-green-900/5">
          {/* En-tête */}
          <div className="border-b border-green-100 bg-gradient-to-r from-green-700 to-green-600 px-5 py-6 text-white sm:px-8 sm:py-7">
            <div className="flex items-start gap-4">
              <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-white/15 text-2xl backdrop-blur-sm">
                ✏️
              </div>

              <div className="min-w-0">
                <h1 className="text-2xl font-bold sm:text-3xl">
                  Modifier l'activité
                </h1>

                <p className="mt-1 text-sm text-green-50 sm:text-base">
                  Modifiez les informations enregistrées
                  dans votre journal.
                </p>
              </div>
            </div>
          </div>

          {/* Formulaire */}
          <form
            onSubmit={handleSubmit}
            className="p-5 sm:p-8"
          >
            {error && (
              <div
                role="alert"
                className="mb-6 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 sm:text-base"
              >
                <div className="flex items-start gap-3">
                  <span className="text-lg">!</span>

                  <p className="font-medium">
                    {error}
                  </p>
                </div>
              </div>
            )}

            <div className="space-y-6">
              {/* Type d'activité */}
              <div>
                <label
                  htmlFor="action_type"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Type d'activité
                </label>

                <select
                  id="action_type"
                  name="action_type"
                  value={form.action_type}
                  onChange={handleChange}
                  className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 text-base text-gray-800 outline-none transition focus:border-green-600 focus:ring-4 focus:ring-green-100"
                >
                  {actionTypes.map((actionType) => (
                    <option
                      key={actionType}
                      value={actionType}
                    >
                      {actionType}
                    </option>
                  ))}
                </select>
              </div>

              {/* Titre */}
              <div>
                <label
                  htmlFor="title"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Titre
                </label>

                <input
                  id="title"
                  name="title"
                  type="text"
                  value={form.title}
                  onChange={handleChange}
                  placeholder="Ex : Apport d'engrais NPK"
                  required
                  minLength={3}
                  maxLength={150}
                  className="w-full rounded-xl border border-gray-300 px-4 py-3 text-base text-gray-800 outline-none transition placeholder:text-gray-400 focus:border-green-600 focus:ring-4 focus:ring-green-100"
                />
              </div>

              {/* Description */}
              <div>
                <div className="mb-2 flex items-center justify-between gap-3">
                  <label
                    htmlFor="description"
                    className="block text-sm font-semibold text-gray-700"
                  >
                    Description
                  </label>

                  <span className="text-xs text-gray-400">
                    Facultatif
                  </span>
                </div>

                <textarea
                  id="description"
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  placeholder="Décrivez ce qui a été réalisé sur la parcelle..."
                  maxLength={1000}
                  rows={5}
                  className="w-full resize-y rounded-xl border border-gray-300 px-4 py-3 text-base text-gray-800 outline-none transition placeholder:text-gray-400 focus:border-green-600 focus:ring-4 focus:ring-green-100"
                />

                <p className="mt-2 text-xs text-gray-400">
                  Vous pouvez modifier ou compléter les
                  détails de l'activité.
                </p>
              </div>

              {/* Coût */}
              <div>
                <label
                  htmlFor="cout_fcfa"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Coût de l'activité
                </label>

                <div className="relative">
                  <input
                    id="cout_fcfa"
                    name="cout_fcfa"
                    type="number"
                    min="0"
                    step="5"
                    value={form.cout_fcfa}
                    onChange={handleChange}
                    required
                    className={`w-full rounded-xl border bg-white px-4 py-3 pr-20 text-base text-gray-800 outline-none transition focus:ring-4 ${
                      error
                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                        : "border-gray-300 focus:border-green-600 focus:ring-green-100"
                    }`}
                  />

                  <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-sm font-semibold text-gray-500">
                    FCFA
                  </span>
                </div>

                <p className="mt-2 text-xs text-gray-500">
                  Le montant doit être un nombre entier et
                  un multiple de 5 FCFA.
                </p>
              </div>

              {/* Séparateur */}
              <div className="border-t border-gray-100 pt-2" />

              {/* Actions */}
              <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
                <button
                  type="button"
                  onClick={handleCancel}
                  disabled={saving}
                  className="w-full rounded-xl border border-gray-300 px-5 py-3.5 font-semibold text-gray-700 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:min-w-36"
                >
                  Annuler
                </button>

                <button
                  type="submit"
                  disabled={saving}
                  className="w-full rounded-xl bg-green-700 px-5 py-3.5 font-semibold text-white shadow-sm transition hover:bg-green-800 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:min-w-48"
                >
                  {saving
                    ? "Enregistrement..."
                    : "Enregistrer les modifications"}
                </button>
              </div>
            </div>
          </form>
        </div>

        <p className="mt-4 text-center text-xs text-gray-400">
          Les modifications seront visibles dans le journal
          de la parcelle.
        </p>
      </div>
    </main>
  );
}

export default EditJournalEntryPage;