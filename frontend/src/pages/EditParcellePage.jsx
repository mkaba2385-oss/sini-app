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
      <main className="min-h-screen bg-green-50 p-6">
        <div className="mx-auto max-w-2xl">
          <p className="text-gray-600">
            Chargement de la parcelle...
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-green-50 p-6">
      <div className="mx-auto max-w-2xl">
        <button
          type="button"
          onClick={() => navigate("/parcelles")}
          className="mb-6 text-green-700 hover:underline"
        >
          ← Retour à mes parcelles
        </button>

        <form
          onSubmit={handleSubmit}
          className="rounded-2xl bg-white p-8 shadow"
        >
          <h1 className="mb-2 text-3xl font-bold text-green-800">
            Modifier la parcelle 🌱
          </h1>

          <p className="mb-6 text-gray-600">
            Modifiez les informations de votre parcelle.
          </p>

          {error && (
            <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label
                htmlFor="name"
                className="mb-1 block font-medium text-gray-700"
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
                className="w-full rounded-lg border p-3"
              />
            </div>

            <div>
              <label
                htmlFor="superficie_ha"
                className="mb-1 block font-medium text-gray-700"
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
                className="w-full rounded-lg border p-3"
              />
            </div>

            <div>
              <label
                htmlFor="culture"
                className="mb-1 block font-medium text-gray-700"
              >
                Culture
              </label>

              <select
                id="culture"
                name="culture"
                value={form.culture}
                onChange={handleChange}
                className="w-full rounded-lg border p-3"
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
                className="mb-1 block font-medium text-gray-700"
              >
                Région
              </label>

              <select
                id="region"
                name="region"
                value={form.region}
                onChange={handleChange}
                className="w-full rounded-lg border p-3"
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
                className="mb-1 block font-medium text-gray-700"
              >
                Commune
              </label>

              <input
                id="commune"
                name="commune"
                value={form.commune}
                onChange={handleChange}
                maxLength={100}
                className="w-full rounded-lg border p-3"
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="w-full rounded-lg bg-green-700 p-3 font-semibold text-white hover:bg-green-800 disabled:opacity-50"
            >
              {saving ? "Modification..." : "Enregistrer les modifications"}
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}

export default EditParcellePage;