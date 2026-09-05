import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { getCurrentUser, verifyOtp } from "../api/auth.js";
import useAuthStore from "../store/authStore.js";

function OtpPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const setTokens = useAuthStore((state) => state.setTokens);
  const setUser = useAuthStore((state) => state.setUser);

  const phoneNumber = location.state?.phoneNumber ?? "";

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const data = await verifyOtp(phoneNumber, code);

      setTokens(data.access_token, data.refresh_token);

      const user = await getCurrentUser();

      setUser(user);

      navigate("/");
    } catch (err) {
      console.error(err);
      setError("Code OTP incorrect ou expiré.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-gradient-to-b from-green-50 via-white to-green-50 p-4 sm:p-6">
      <div className="w-full max-w-md">
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
            <div className="mb-6 text-center">
              <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-green-100 text-xl">
                🔐
              </div>

              <h2 className="text-2xl font-bold text-gray-800 sm:text-3xl">
                Vérification OTP
              </h2>

              <p className="mt-2 text-sm leading-6 text-gray-600 sm:text-base">
                Entrez le code reçu par SMS pour confirmer votre numéro.
              </p>
            </div>

            {phoneNumber && (
              <div className="mb-5 rounded-2xl border border-green-100 bg-green-50 px-4 py-3 text-center">
                <p className="text-xs font-medium uppercase tracking-wide text-green-700">
                  Code envoyé au
                </p>

                <p className="mt-1 font-semibold text-green-900">
                  {phoneNumber}
                </p>
              </div>
            )}

            {error && (
              <div
                role="alert"
                className="mb-5 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700"
              >
                <div className="flex items-start gap-3">
                  <span className="font-bold">!</span>
                  <p className="font-medium">{error}</p>
                </div>
              </div>
            )}

            <div>
              <label
                htmlFor="otp-code"
                className="mb-2 block text-center text-sm font-semibold text-gray-700"
              >
                Code de vérification
              </label>

              <input
                id="otp-code"
                type="text"
                inputMode="numeric"
                autoComplete="one-time-code"
                maxLength={6}
                value={code}
                onChange={(event) => setCode(event.target.value)}
                placeholder="000000"
                required
                className={`w-full rounded-xl border bg-white px-4 py-4 text-center text-2xl font-semibold tracking-[0.5em] text-gray-800 outline-none transition placeholder:tracking-[0.5em] placeholder:text-gray-300 focus:ring-4 ${
                  error
                    ? "border-red-400 focus:border-red-500 focus:ring-red-100"
                    : "border-gray-300 focus:border-green-600 focus:ring-green-100"
                }`}
              />

              <p className="mt-2 text-center text-xs leading-5 text-gray-500">
                Saisissez les 6 chiffres du code reçu.
              </p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="mt-6 w-full rounded-xl bg-green-700 px-4 py-3.5 font-semibold text-white shadow-sm transition hover:bg-green-800 hover:shadow-md focus:outline-none focus:ring-4 focus:ring-green-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Vérification..." : "Vérifier le code"}
            </button>

            <div className="my-6 flex items-center gap-3">
              <div className="h-px flex-1 bg-gray-200" />

              <span className="text-xs text-gray-400">
                Besoin d'aide ?
              </span>

              <div className="h-px flex-1 bg-gray-200" />
            </div>

            <button
              type="button"
              onClick={() => navigate("/register")}
              className="w-full rounded-xl border border-green-600 bg-white px-4 py-3.5 font-semibold text-green-700 transition hover:bg-green-50 focus:outline-none focus:ring-4 focus:ring-green-100"
            >
              Retour à l'inscription
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

export default OtpPage;