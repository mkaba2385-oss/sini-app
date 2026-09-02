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
  }

  async function handleSubmit(event) {
    event.preventDefault();

    if (!parcelleId) {
      setError("Aucune parcelle sélectionnée.");
      return;
    }

    setSaving(true);
    setError("");

    try {
      await updateJournalEntry(Number(entryId), {
        action_type: form.action_type,
        title: form.title,
        description: form.description || null,
        cout_fcfa: Number(form.cout_fcfa),
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
      <main className="min-h-screen bg-green-50 p-6">
        <div className="mx-auto max-w-xl">
          <p className="text-gray-600">
            Chargement de l'activité...
          </p>
        </div>
      </main>
    );
  }

  if (isError) {
    return (
      <main className="min-h-screen bg-green-50 p-6">
        <div className="mx-auto max-w-xl">
          <div className="rounded-xl bg-red-100 p-4 text-red-700">
            Impossible de récupérer cette activité.
          </div>
        </div>
      </main>
    );
  }

  if (!entry) {
    return (
      <main className="min-h-screen bg-green-50 p-6">
        <div className="mx-auto max-w-xl">
          <div className="rounded-xl bg-red-100 p-4 text-red-700">
            Activité introuvable.
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 p-6">
      <div className="mx-auto max-w-xl">
        <form
          onSubmit={handleSubmit}
          className="rounded-2xl bg-white p-8 shadow"
        >
          <h1 className="mb-2 text-3xl font-bold text-green-800">
            Modifier l'activité ✏️
          </h1>

          <p className="mb-6 text-gray-600">
            Modifiez les informations de cette activité.
          </p>

          {error && (
            <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
              {error}
            </div>
          )}

          <div className="space-y-5">
            <div>
              <label
                htmlFor="action_type"
                className="mb-1 block font-medium text-gray-700"
              >
                Type d'activité
              </label>

              <select
                id="action_type"
                name="action_type"
                value={form.action_type}
                onChange={handleChange}
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-green-600 focus:outline-none"
              >
                {actionTypes.map((actionType) => (
                  <option key={actionType} value={actionType}>
                    {actionType}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label
                htmlFor="title"
                className="mb-1 block font-medium text-gray-700"
              >
                Titre
              </label>

              <input
                id="title"
                name="title"
                type="text"
                value={form.title}
                onChange={handleChange}
                required
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-green-600 focus:outline-none"
              />
            </div>

            <div>
              <label
                htmlFor="description"
                className="mb-1 block font-medium text-gray-700"
              >
                Description
              </label>

              <textarea
                id="description"
                name="description"
                value={form.description}
                onChange={handleChange}
                rows="5"
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-green-600 focus:outline-none"
              />
            </div>

            <div>
              <label
                htmlFor="cout_fcfa"
                className="mb-1 block font-medium text-gray-700"
              >
                Coût (FCFA)
              </label>

              <input
                id="cout_fcfa"
                name="cout_fcfa"
                type="number"
                min="0"
                value={form.cout_fcfa}
                onChange={handleChange}
                required
                className="w-full rounded-lg border border-gray-300 px-4 py-3 focus:border-green-600 focus:outline-none"
              />
            </div>
          </div>

          <div className="mt-8 flex gap-3">
            <button
              type="button"
              onClick={handleCancel}
              className="flex-1 rounded-lg border border-gray-300 px-4 py-3 font-semibold text-gray-700 hover:bg-gray-100"
            >
              Annuler
            </button>

            <button
              type="submit"
              disabled={saving}
              className="flex-1 rounded-lg bg-green-700 px-4 py-3 font-semibold text-white hover:bg-green-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {saving ? "Enregistrement..." : "Enregistrer"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

export default EditJournalEntryPage;