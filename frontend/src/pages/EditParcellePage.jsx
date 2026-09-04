import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import {
  getParcelle,
  updateParcelle,
} from "../api/parcelles.js";

function EditParcellePage() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    superficie_ha: "",
    culture: "Maïs",
    region: "Bamako",
    commune: "",
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadParcelle() {
      try {
        const parcelle = await getParcelle(id);

        setForm({
          name: parcelle.name,
          superficie_ha: parcelle.superficie_ha,
          culture: parcelle.culture,
          region: parcelle.region,
          commune: parcelle.commune || "",
        });
      } catch (err) {
        console.error(err);
        setError(
          err.response?.data?.detail ||
            "Impossible de récupérer la parcelle.",
        );
      } finally {
        setLoading(false);
      }
    }

    loadParcelle();
  }, [id]);

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setSaving(true);
    setError("");

    try {
      await updateParcelle(id, {
        ...form,
        superficie_ha: Number(form.superficie_ha),
      });

      navigate("/parcelles");
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail ||
          "Impossible de modifier la parcelle.",
      );
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <main className="min-h-screen bg-green-50 p-4 sm:p-6">
        <div className="mx-auto max-w-2xl">
          <div className="rounded-2xl bg-white p-5 shadow sm:p-6">
            <p className="text-gray-600">
              Chargement de la parcelle...
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 p-4 sm:p-6">
      <div className="mx-auto max-w-2xl">
        <button
          type="button"
          onClick={() => navigate("/parcelles")}
          className="mb-5 text-sm font-medium text-green-700 hover:underline sm:mb-6 sm:text-base"
        >
          ← Retour à mes parcelles
        </button>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl bg-white p-5 shadow sm:p-8"
        >
          <h1 className="text-2xl font-bold text-green-800 sm:text-3xl">
            Modifier la parcelle 🌱
          </h1>

          <p className="mt-2 mb-6 text-sm text-gray-600 sm:text-base">
            Modifiez les informations de votre parcelle.
          </p>

          {error && (
            <div className="mb-4 rounded-lg bg-red-100 p-3 text-sm text-red-700 sm:text-base">
              {error}
            </div>
          )}

          <div className="space-y-5">
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
                value={form.name}
                onChange={handleChange}
                required
                minLength={2}
                maxLength={100}
                className="w-full rounded-lg border border-gray-300 p-3 text-base outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              />
            </div>

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
                value={form.superficie_ha}
                onChange={handleChange}
                type="number"
                min="0.01"
                step="0.01"
                required
                className="w-full rounded-lg border border-gray-300 p-3 text-base outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              />
            </div>

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
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              >
                <option value="Coton">Coton</option>
                <option value="Maïs">Maïs</option>
                <option value="Riz">Riz</option>
                <option value="Mil">Mil</option>
                <option value="Sorgho">Sorgho</option>
                <option value="Arachide">Arachide</option>
                <option value="Maraîchage">Maraîchage</option>
                <option value="Autre">Autre</option>
              </select>
            </div>

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
                className="w-full rounded-lg border border-gray-300 bg-white p-3 text-base outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
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
                value={form.commune}
                onChange={handleChange}
                maxLength={100}
                className="w-full rounded-lg border border-gray-300 p-3 text-base outline-none focus:border-green-600 focus:ring-2 focus:ring-green-100"
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="w-full rounded-lg bg-green-700 p-3.5 font-semibold text-white transition hover:bg-green-800 disabled:opacity-50"
            >
              {saving
                ? "Modification..."
                : "Enregistrer les modifications"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

export default EditParcellePage;