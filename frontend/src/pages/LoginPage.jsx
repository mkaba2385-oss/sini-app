import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { requestOtp } from "../api/auth.js";

function LoginPage() {
  const navigate = useNavigate();

  const [phoneNumber, setPhoneNumber] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      await requestOtp(phoneNumber);

      navigate("/verify-login-otp", {
        state: {
          phoneNumber,
        },
      });
    } catch (err) {
      console.error(err);
      setError("Impossible d'envoyer le code OTP.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-b from-green-50 via-white to-green-50 p-4 sm:p-6">
      <div className="w-full max-w-md">
        {/* Identité Sini */}
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

        {/* Carte de connexion */}
        <div className="overflow-hidden rounded-3xl border border-green-100 bg-white shadow-lg shadow-green-900/5">
          <form
            onSubmit={handleSubmit}
            className="p-5 sm:p-8"
          >
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-800 sm:text-3xl">
                Se connecter
              </h2>

              <p className="mt-2 text-sm leading-6 text-gray-600 sm:text-base">
                Entrez votre numéro de téléphone pour
                recevoir un code de connexion.
              </p>
            </div>

            {error && (
              <div
                role="alert"
                className="mb-5 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
              >
                <div className="flex items-start gap-3">
                  <span className="font-bold">!</span>

                  <p className="font-medium">
                    {error}
                  </p>
                </div>
              </div>
            )}

            {/* Téléphone */}
            <div>
              <label
                htmlFor="phoneNumber"
                className="mb-2 block text-sm font-semibold text-gray-700"
              >
                Numéro de téléphone
              </label>

              <div className="relative">
                <span className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-lg">
                  📱
                </span>

                <input
                  id="phoneNumber"
                  type="tel"
                  value={phoneNumber}
                  onChange={(event) =>
                    setPhoneNumber(event.target.value)
                  }
                  placeholder="Ex : 76 12 34 56"
                  required
                  autoComplete="tel"
                  inputMode="tel"
                  className="w-full rounded-xl border border-gray-300 bg-white py-3.5 pl-12 pr-4 text-base text-gray-800 outline-none transition placeholder:text-gray-400 focus:border-green-600 focus:ring-4 focus:ring-green-100"
                />
              </div>

              <p className="mt-2 text-xs leading-5 text-gray-500">
                Un code à usage unique vous sera envoyé
                pour vérifier votre numéro.
              </p>
            </div>

            {/* Bouton principal */}
            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full rounded-xl bg-green-700 px-4 py-3.5 font-semibold text-white shadow-sm transition hover:bg-green-800 hover:shadow-md focus:outline-none focus:ring-4 focus:ring-green-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Envoi du code..." : "Recevoir le code"}
            </button>

            {/* Séparateur */}
            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-gray-200" />

              <span className="text-xs text-gray-400">
                Nouveau sur Sini ?
              </span>

              <div className="h-px flex-1 bg-gray-200" />
            </div>

            {/* Inscription */}
            <button
              type="button"
              onClick={() => navigate("/register")}
              className="w-full rounded-xl border border-green-600 bg-white px-4 py-3.5 font-semibold text-green-700 transition hover:bg-green-50 focus:outline-none focus:ring-4 focus:ring-green-100"
            >
              Créer un compte
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

export default LoginPage;