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
                📖
              </div>

              <div>
                <h1 className="text-2xl font-bold sm:text-3xl">
                  Nouvelle activité
                </h1>

                <p className="mt-1 text-sm text-green-50 sm:text-base">
                  Ajoutez une activité à votre journal agricole.
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
                  {actionTypes.map((action) => (
                    <option key={action} value={action}>
                      {action}
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
                  Vous pouvez ajouter les détails utiles de
                  l'activité.
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
                    className={`w-full rounded-xl border bg-white px-4 py-3 pr-20 text-base text-gray-800 outline-none transition focus:ring-4 focus:ring-green-100 ${
                      error && form.cout_fcfa
                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                        : "border-gray-300 focus:border-green-600"
                    }`}
                  />

                  <span className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-sm font-semibold text-gray-500">
                    FCFA
                  </span>
                </div>

                <p className="mt-2 text-xs text-gray-500">
                  Le montant doit être un nombre entier et un
                  multiple de 5 FCFA.
                </p>
              </div>

              {/* Séparateur */}
              <div className="border-t border-gray-100 pt-2" />

              {/* Actions */}
              <div className="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
                <button
                  type="button"
                  onClick={handleCancel}
                  disabled={loading}
                  className="w-full rounded-xl border border-gray-300 px-5 py-3.5 font-semibold text-gray-700 transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:min-w-36"
                >
                  Annuler
                </button>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full rounded-xl bg-green-700 px-5 py-3.5 font-semibold text-white shadow-sm transition hover:bg-green-800 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50 sm:w-auto sm:min-w-48"
                >
                  {loading
                    ? "Enregistrement..."
                    : "Ajouter l'activité"}
                </button>
              </div>
            </div>
          </form>
        </div>

        {/* Petit rappel */}
        <p className="mt-4 text-center text-xs text-gray-400">
          Les informations enregistrées pourront être
          consultées depuis le journal de la parcelle.
        </p>
      </div>
    </main>
  );
}

export default AddJournalEntryPage;