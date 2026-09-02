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
    <main className="flex min-h-screen items-center justify-center bg-green-50 p-6">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-2xl bg-white p-8 shadow"
      >
        <h1 className="mb-2 text-3xl font-bold text-green-800">
          Se connecter
        </h1>

        <p className="mb-6 text-gray-600">
          Entrez votre numéro de téléphone pour recevoir un code OTP.
        </p>

        {error && (
          <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
            {error}
          </div>
        )}

        <input
          type="tel"
          value={phoneNumber}
          onChange={(event) => setPhoneNumber(event.target.value)}
          placeholder="Numéro de téléphone"
          required
          className="mb-4 w-full rounded-lg border p-3"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-green-700 p-3 font-semibold text-white hover:bg-green-800 disabled:opacity-50"
        >
          {loading ? "Envoi..." : "Recevoir le code"}
        </button>

        <button
          type="button"
          onClick={() => navigate("/register")}
          className="mt-4 w-full rounded-lg border border-green-700 p-3 font-semibold text-green-700"
        >
          Créer un compte
        </button>
      </form>
    </main>
  );
}

export default LoginPage;
