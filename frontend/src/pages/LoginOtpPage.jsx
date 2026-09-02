import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { getCurrentUser, verifyOtp } from "../api/auth.js";
import useAuthStore from "../store/authStore.js";

function LoginOtpPage() {
  const navigate = useNavigate();
  const location = useLocation();

  const setTokens = useAuthStore((state) => state.setTokens);
  const setUser = useAuthStore((state) => state.setUser);

  const phoneNumber = location.state?.phoneNumber;

  const [code, setCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();

    if (!phoneNumber) {
      setError("Numéro de téléphone introuvable.");
      return;
    }

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
      setError("Code OTP invalide ou expiré.");
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
          Vérification OTP
        </h1>

        <p className="mb-6 text-gray-600">
          Un code a été envoyé à votre numéro de téléphone.
        </p>

        <p className="mb-4 text-center font-semibold">
          {phoneNumber}
        </p>

        {error && (
          <div className="mb-4 rounded-lg bg-red-100 p-3 text-red-700">
            {error}
          </div>
        )}

        <input
          type="text"
          inputMode="numeric"
          value={code}
          onChange={(event) => setCode(event.target.value)}
          placeholder="Code OTP"
          required
          className="mb-4 w-full rounded-lg border p-3 text-center text-xl tracking-widest"
        />

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-green-700 p-3 font-semibold text-white hover:bg-green-800 disabled:opacity-50"
        >
          {loading ? "Vérification..." : "Se connecter"}
        </button>
      </form>
    </main>
  );
}

export default LoginOtpPage;
