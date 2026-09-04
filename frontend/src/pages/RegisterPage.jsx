import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { registerUser, requestOtp } from "../api/auth.js";

function RegisterPage() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    full_name: "",
    phone_number: "",
    region: "Bamako",
    role: "FARMER",
    language: "fr",
    password: "",
  });

  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  function handleChange(event) {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));

    setErrors((current) => ({
      ...current,
      [name]: undefined,
      general: undefined,
    }));
  }

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setErrors({});

    try {
      await registerUser(form);
      await requestOtp(form.phone_number);

      navigate("/verify-otp", {
        state: {
          phoneNumber: form.phone_number,
        },
      });
    } catch (err) {
      console.error(err);

      const details = err.response?.data?.detail;

      if (Array.isArray(details)) {
        const fieldErrors = {};

        details.forEach((detail) => {
          const field = detail.loc?.[1];

          if (!field) {
            return;
          }

          if (field === "full_name" && detail.type === "string_too_short") {
            fieldErrors[field] =
              "Le nom complet doit contenir au moins 2 caractères.";
          } else if (
            field === "full_name" &&
            detail.type === "string_too_long"
          ) {
            fieldErrors[field] =
              "Le nom complet ne doit pas dépasser 100 caractères.";
          } else if (field === "phone_number") {
            fieldErrors[field] =
              "Le numéro de téléphone est invalide. Format attendu : +223XXXXXXXX.";
          } else if (
            field === "password" &&
            detail.type === "string_too_short"
          ) {
            fieldErrors[field] =
              "Le mot de passe doit contenir au moins 8 caractères.";
          } else if (field === "password" && detail.type === "string_too_long") {
            fieldErrors[field] =
              "Le mot de passe est trop long.";
          } else if (field === "region") {
            fieldErrors[field] =
              "La région sélectionnée n'est pas valide.";
          } else if (field === "role") {
            fieldErrors[field] =
              "Le rôle sélectionné n'est pas valide.";
          } else if (field === "language") {
            fieldErrors[field] =
              "La langue sélectionnée n'est pas valide.";
          } else {
            fieldErrors[field] =
              "Ce champ contient une valeur invalide.";
          }
        });

        setErrors(fieldErrors);
      } else {
        setErrors({
          general: details || "Impossible de créer le compte.",
        });
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-green-50 p-6">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-2xl bg-white p-8 shadow"
      >
        <h1 className="mb-2 text-3xl font-bold text-green-800">
          Créer un compte
        </h1>

        <p className="mb-6 text-gray-600">
          Bienvenue sur Sini 🌱
        </p>

        {errors.general && (
          <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
            {errors.general}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <input
              name="full_name"
              value={form.full_name}
              onChange={handleChange}
              placeholder="Nom complet"
              required
              className={`w-full rounded-lg border p-3 ${
                errors.full_name ? "border-red-500" : ""
              }`}
            />

            {errors.full_name && (
              <p className="mt-1 text-sm text-red-600">
                {errors.full_name}
              </p>
            )}
          </div>

          <div>
            <input
              name="phone_number"
              value={form.phone_number}
              onChange={handleChange}
              placeholder="Numéro de téléphone"
              type="tel"
              required
              className={`w-full rounded-lg border p-3 ${
                errors.phone_number ? "border-red-500" : ""
              }`}
            />

            {errors.phone_number && (
              <p className="mt-1 text-sm text-red-600">
                {errors.phone_number}
              </p>
            )}
          </div>

          <div>
            <select
              name="region"
              value={form.region}
              onChange={handleChange}
              className={`w-full rounded-lg border p-3 ${
                errors.region ? "border-red-500" : ""
              }`}
            >
              <option value="Bamako">Bamako</option>
              <option value="Ségou">Ségou</option>
              <option value="Sikasso">Sikasso</option>
              <option value="Kayes">Kayes</option>
              <option value="Mopti">Mopti</option>
              <option value="Koulikoro">Koulikoro</option>
              <option value="Gao">Gao</option>
              <option value="Tombouctou">Tombouctou</option>
              <option value="Kidal">Kidal</option>
              <option value="Ménaka">Ménaka</option>
              <option value="Taoudénit">Taoudénit</option>
            </select>

            {errors.region && (
              <p className="mt-1 text-sm text-red-600">
                {errors.region}
              </p>
            )}
          </div>

          <div>
            <select
              name="role"
              value={form.role}
              onChange={handleChange}
              className={`w-full rounded-lg border p-3 ${
                errors.role ? "border-red-500" : ""
              }`}
            >
              <option value="FARMER">Agriculteur</option>
              <option value="AGRONOMIST">Agronome</option>
            </select>

            {errors.role && (
              <p className="mt-1 text-sm text-red-600">
                {errors.role}
              </p>
            )}
          </div>

          <div>
            <input
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Mot de passe"
              type="password"
              required
              className={`w-full rounded-lg border p-3 ${
                errors.password ? "border-red-500" : ""
              }`}
            />

            {errors.password && (
              <p className="mt-1 text-sm text-red-600">
                {errors.password}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-green-700 p-3 font-semibold text-white hover:bg-green-800 disabled:opacity-50"
          >
            {loading ? "Création..." : "Créer mon compte"}
          </button>
        </div>
      </form>
    </main>
  );
}

export default RegisterPage;