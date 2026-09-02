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
      await registerUser(form);
      await requestOtp(form.phone_number);

      navigate("/verify-otp", {
        state: {
          phoneNumber: form.phone_number,
        },
      });
    } catch (err) {
      console.error(err);
      setError("Impossible de créer le compte.");
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

        {error && (
          <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <input
            name="full_name"
            value={form.full_name}
            onChange={handleChange}
            placeholder="Nom complet"
            required
            className="w-full rounded-lg border p-3"
          />

          <input
            name="phone_number"
            value={form.phone_number}
            onChange={handleChange}
            placeholder="Numéro de téléphone"
            type="tel"
            required
            className="w-full rounded-lg border p-3"
          />

          <select
            name="region"
            value={form.region}
            onChange={handleChange}
            className="w-full rounded-lg border p-3"
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
          </select>


          <select
            name="role"
            value={form.role}
            onChange={handleChange}
            className="w-full rounded-lg border p-3"
          >
            <option value="FARMER">Agriculteur</option>
            <option value="AGRONOMIST">Agronome</option>
          </select>

          <input
            name="password"
            value={form.password}
            onChange={handleChange}
            placeholder="Mot de passe"
            type="password"
            required
            className="w-full rounded-lg border p-3"
          />

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