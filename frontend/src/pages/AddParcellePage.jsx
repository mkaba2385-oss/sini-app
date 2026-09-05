import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { createParcelle } from "../api/parcelles.js";

function AddParcellePage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    superficie_ha: "",
    culture: "Maïs",
    region: "Bamako",
    commune: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      await createParcelle({
        ...form,
        superficie_ha: Number(form.superficie_ha),
      });

      navigate("/parcelles");
    } catch (err) {
      console.error(err);

      setError(
        err.response?.data?.detail ||
          "Impossible de créer la parcelle.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-green-50 p-4 sm:p-6">
      <div className="mx-auto max-w-3xl">
        {/* Retour */}
        <button
          type="button"
          onClick={() => navigate("/parcelles")}
          className="mb-5 text-sm font-medium text-green-700 hover:text-green-800 hover:underline sm:mb-6 sm:text-base"
        >
          ← Retour à mes parcelles
        </button>

        {/* Formulaire */}
        <form
          onSubmit={handleSubmit}
          className="rounded-2xl bg-white p-5 shadow sm:p-8"
        >
          {/* En-tête */}
          <div className="mb-6 sm:mb-8">
            <h1 className="text-2xl font-bold text-green-800 sm:text-3xl">
              Ajouter une parcelle 🌱
            </h1>

            <p className="mt-2 text-sm text-gray-600 sm:text-base">
              Enregistrez les informations de votre parcelle.
            </p>
          </div>

          {/* Message d'erreur */}
          {error && (
            <div
              role="alert"
              className="mb-5 rounded-lg bg-red-100 p-3 text-sm text-red-700 sm:mb-6 sm:p-4 sm:text-base"
            >
              {error}
            </div>
          )}

          <div className="space-y-5 sm:space-y-6">
            {/* Nom */}
            <div>
              <label
                htmlFor="name"
                className="mb-2 block text-sm font-medium text-gray-700 sm:text-base"
              >
                Nom de la parcelle
              </label>

              <input
                id="name"
                name="name"
                type="text"
                value={form.name}
                onChange={handleChange}
                placeholder="Ex : Champ Ségou Nord"
                required
                minLength={2}
                maxLength={100}
                autoComplete="off"
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base text-gray-800 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 sm:p-4"
              />
            </div>

            {/* Superficie */}
            <div>
              <label
                htmlFor="superficie_ha"
                className="mb-2 block text-sm font-medium text-gray-700 sm:text-base"
              >
                Superficie (hectares)
              </label>

              <input
                id="superficie_ha"
                name="superficie_ha"
                type="number"
                value={form.superficie_ha}
                onChange={handleChange}
                placeholder="Ex : 2.5"
                min="0.01"
                step="0.01"
                required
                inputMode="decimal"
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base text-gray-800 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 sm:p-4"
              />
            </div>

            {/* Culture */}
            <div>
              <label
                htmlFor="culture"
                className="mb-2 block text-sm font-medium text-gray-700 sm:text-base"
              >
                Culture
              </label>

              <select
                id="culture"
                name="culture"
                value={form.culture}
                onChange={handleChange}
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base text-gray-800 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 sm:p-4"
              >
                <option value="Coton">Coton</option>
                <option value="Maïs">Maïs</option>
                <option value="Riz">Riz</option>
                <option value="Mil">Mil</option>
                <option value="Sorgho">Sorgho</option>
                <option value="Arachide">Arachide</option>
                <option value="Maraîchage">Maraîchage</option>
                <option value="Niébé">Niébé</option>
                <option value="Fonio">Fonio</option>
                <option value="Autre">Autre</option>
              </select>
            </div>

            {/* Région */}
            <div>
              <label
                htmlFor="region"
                className="mb-2 block text-sm font-medium text-gray-700 sm:text-base"
              >
                Région
              </label>

              <select
                id="region"
                name="region"
                value={form.region}
                onChange={handleChange}
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base text-gray-800 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 sm:p-4"
              >
                <option value="Bamako">Bamako</option>
                <option value="Kayes">Kayes</option>
                <option value="Koulikoro">Koulikoro</option>
                <option value="Sikasso">Sikasso</option>
                <option value="Ségou">Ségou</option>
                <option value="Mopti">Mopti</option>
                <option value="Tombouctou">Tombouctou</option>
                <option value="Gao">Gao</option>
                <option value="Kidal">Kidal</option>
                <option value="Ménaka">Ménaka</option>
                <option value="Taoudénit">Taoudénit</option>
              </select>
            </div>

            {/* Commune */}
            <div>
              <label
                htmlFor="commune"
                className="mb-2 block text-sm font-medium text-gray-700 sm:text-base"
              >
                Commune
              </label>

              <input
                id="commune"
                name="commune"
                type="text"
                value={form.commune}
                onChange={handleChange}
                placeholder="Ex : Pelengana"
                maxLength={100}
                autoComplete="address-level2"
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base text-gray-800 outline-none transition focus:border-green-600 focus:ring-2 focus:ring-green-100 sm:p-4"
              />
            </div>

            {/* Bouton */}
            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-green-700 p-3.5 font-semibold text-white transition hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-600 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 sm:p-4"
            >
              {loading
                ? "Enregistrement..."
                : "Enregistrer la parcelle"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

export default AddParcellePage;