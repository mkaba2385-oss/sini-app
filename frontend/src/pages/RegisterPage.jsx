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
            fieldErrors[field] = "Le mot de passe est trop long.";
          } else if (field === "region") {
            fieldErrors[field] =
              "La région sélectionnée n'est pas valide.";
          } else if (field === "role") {
            fieldErrors[field] = "Le rôle sélectionné n'est pas valide.";
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
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-b from-green-50 via-white to-green-50 p-4 sm:p-6">
      <div className="w-full max-w-xl">
        <div className="mb-6 text-center">
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-green-100 text-3xl shadow-sm">
            🌱
          </div>

          <h1 className="mt-4 text-2xl font-bold text-green-800">
            Sini
          </h1>

          <p className="mt-1 text-sm text-gray-500">
            Votre agriculture, simplement.
          </p>
        </div>

        <div className="overflow-hidden rounded-3xl border border-green-100 bg-white shadow-lg shadow-green-900/5">
          <form onSubmit={handleSubmit} className="p-5 sm:p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 sm:text-3xl">
                Créer un compte
              </h2>

              <p className="mt-2 text-sm leading-6 text-gray-600 sm:text-base">
                Rejoignez Sini pour gérer et suivre votre activité agricole.
              </p>
            </div>

            {errors.general && (
              <div
                role="alert"
                className="mb-5 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
              >
                <div className="flex items-start gap-3">
                  <span className="font-bold">!</span>
                  <p className="font-medium">{errors.general}</p>
                </div>
              </div>
            )}

            <div className="space-y-5">
              <div>
                <label
                  htmlFor="full_name"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Nom complet
                </label>

                <input
                  id="full_name"
                  name="full_name"
                  value={form.full_name}
                  onChange={handleChange}
                  placeholder="Ex : Amadou Traoré"
                  required
                  autoComplete="name"
                  className={`w-full rounded-xl border bg-white px-4 py-3.5 text-base text-gray-800 outline-none transition placeholder:text-gray-400 focus:ring-4 ${
                    errors.full_name
                      ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                      : "border-gray-300 focus:border-green-600 focus:ring-green-100"
                  }`}
                />

                {errors.full_name && (
                  <p className="mt-2 text-sm text-red-600">
                    {errors.full_name}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="phone_number"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Numéro de téléphone
                </label>

                <div className="relative">
                  <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-lg">
                    📱
                  </span>

                  <input
                    id="phone_number"
                    name="phone_number"
                    value={form.phone_number}
                    onChange={handleChange}
                    placeholder="+223XXXXXXXX"
                    type="tel"
                    required
                    autoComplete="tel"
                    inputMode="tel"
                    className={`w-full rounded-xl border bg-white py-3.5 pl-12 pr-4 text-base text-gray-800 outline-none transition placeholder:text-gray-400 focus:ring-4 ${
                      errors.phone_number
                        ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                        : "border-gray-300 focus:border-green-600 focus:ring-green-100"
                    }`}
                  />
                </div>

                {errors.phone_number ? (
                  <p className="mt-2 text-sm text-red-600">
                    {errors.phone_number}
                  </p>
                ) : (
                  <p className="mt-2 text-xs leading-5 text-gray-500">
                    Utilisez le format +223XXXXXXXX.
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="region"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Région
                </label>

                <select
                  id="region"
                  name="region"
                  value={form.region}
                  onChange={handleChange}
                  className={`w-full rounded-xl border bg-white px-4 py-3.5 text-base text-gray-800 outline-none transition focus:ring-4 ${
                    errors.region
                      ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                      : "border-gray-300 focus:border-green-600 focus:ring-green-100"
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
                  <p className="mt-2 text-sm text-red-600">
                    {errors.region}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="role"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Profil
                </label>

                <select
                  id="role"
                  name="role"
                  value={form.role}
                  onChange={handleChange}
                  className={`w-full rounded-xl border bg-white px-4 py-3.5 text-base text-gray-800 outline-none transition focus:ring-4 ${
                    errors.role
                      ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                      : "border-gray-300 focus:border-green-600 focus:ring-green-100"
                  }`}
                >
                  <option value="FARMER">Agriculteur</option>
                  <option value="AGRONOMIST">Agronome</option>
                </select>

                {errors.role && (
                  <p className="mt-2 text-sm text-red-600">
                    {errors.role}
                  </p>
                )}
              </div>

              <div>
                <label
                  htmlFor="password"
                  className="mb-2 block text-sm font-semibold text-gray-700"
                >
                  Mot de passe
                </label>

                <input
                  id="password"
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Au moins 8 caractères"
                  type="password"
                  required
                  autoComplete="new-password"
                  className={`w-full rounded-xl border bg-white px-4 py-3.5 text-base text-gray-800 outline-none transition placeholder:text-gray-400 focus:ring-4 ${
                    errors.password
                      ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                      : "border-gray-300 focus:border-green-600 focus:ring-green-100"
                  }`}
                />

                {errors.password ? (
                  <p className="mt-2 text-sm text-red-600">
                    {errors.password}
                  </p>
                ) : (
                  <p className="mt-2 text-xs leading-5 text-gray-500">
                    Votre mot de passe doit contenir au moins 8 caractères.
                  </p>
                )}
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full rounded-xl bg-green-700 px-4 py-3.5 font-semibold text-white shadow-sm transition hover:bg-green-800 hover:shadow-md focus:outline-none focus:ring-4 focus:ring-green-200 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Création du compte..." : "Créer mon compte"}
              </button>
            </div>

            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-gray-200" />

              <span className="text-xs text-gray-400">
                Déjà un compte ?
              </span>

              <div className="h-px flex-1 bg-gray-200" />
            </div>

            <button
              type="button"
              onClick={() => navigate("/login")}
              className="w-full rounded-xl border border-green-600 bg-white px-4 py-3.5 font-semibold text-green-700 transition hover:bg-green-50 focus:outline-none focus:ring-4 focus:ring-green-100"
            >
              Se connecter
            </button>
          </form>
        </div>

        <p className="mt-5 text-center text-xs text-gray-400">
          Sini — Gestion et suivi de votre activité agricole
        </p>
      </div>
    </main>
  );
}

export default RegisterPage;