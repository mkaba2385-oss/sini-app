import { useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";

import { createJournalEntry } from "../api/journal.js";

const actionTypes = [
  "Semis",
  "Irrigation",
  "Fertilisation",
  "Traitement phytosanitaire",
  "Désherbage",
  "Récolte",
  "Observation",
];

function AddJournalEntryPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const parcelleId = searchParams.get("parcelle");

  const [form, setForm] = useState({
    action_type: "Observation",
    title: "",
    description: "",
    cout_fcfa: "0",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

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

    setLoading(true);
    setError("");

    try {
      await createJournalEntry({
        parcelle_id: Number(parcelleId),
        action_type: form.action_type,
        title: form.title,
        description: form.description || null,
        cout_fcfa: coutFcfa,
      });

      navigate(`/parcelles/${parcelleId}/journal`);
    } catch (err) {
      console.error(err);
      setError("Impossible d'ajouter cette entrée.");
    } finally {
      setLoading(false);
    }
  }

  function handleCancel() {
    if (parcelleId) {
      navigate(`/parcelles/${parcelleId}/journal`);
    } else {
      navigate("/parcelles");
    }
  }

  return (
    <main className="min-h-screen bg-green-50 p-4 sm:p-6">
      <div className="mx-auto max-w-xl">
        <form
          onSubmit={handleSubmit}
          className="rounded-2xl bg-white p-5 shadow sm:p-8"
        >
          <h1 className="mb-2 text-2xl font-bold text-green-800 sm:text-3xl">
            Ajouter au journal 📖
          </h1>

          <p className="mb-6 text-sm text-gray-600 sm:text-base">
            Ajoutez une nouvelle activité agricole.
          </p>

          {error && (
            <div className="mb-4 rounded-lg bg-red-100 p-3 text-sm text-red-700 sm:text-base">
              {error}
            </div>
          )}

          <div className="space-y-4">
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
                className="w-full rounded-lg border border-gray-300 bg-white p-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              >
                {actionTypes.map((action) => (
                  <option key={action} value={action}>
                    {action}
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
                value={form.title}
                onChange={handleChange}
                placeholder="Ex : Apport d'engrais NPK"
                required
                minLength={3}
                maxLength={150}
                className="w-full rounded-lg border border-gray-300 p-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
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
                placeholder="Décrivez l'activité..."
                maxLength={1000}
                rows={5}
                className="w-full resize-y rounded-lg border border-gray-300 p-3 outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
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
                step="5"
                value={form.cout_fcfa}
                onChange={handleChange}
                className={`w-full rounded-lg border p-3 outline-none focus:ring-2 focus:ring-green-100 ${
                  error && form.cout_fcfa
                    ? "border-red-500 focus:border-red-500"
                    : "border-gray-300 focus:border-green-600"
                }`}
              />

              <p className="mt-1 text-sm text-gray-500">
                Le montant doit être un multiple de 5 FCFA.
              </p>
            </div>

            <div className="flex flex-col gap-3 pt-4 sm:flex-row">
              <button
                type="button"
                onClick={handleCancel}
                className="w-full rounded-lg border border-gray-300 p-3 font-semibold text-gray-700 hover:bg-gray-50 sm:flex-1"
              >
                Annuler
              </button>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-lg bg-green-700 p-3 font-semibold text-white hover:bg-green-800 disabled:opacity-50 sm:flex-1"
              >
                {loading ? "Enregistrement..." : "Ajouter"}
              </button>
            </div>
          </div>
        </form>
      </div>
    </main>
  );
}

export default AddJournalEntryPage;