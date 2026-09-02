import axios from "axios";
import useAuthStore from "../store/authStore.js";
import { refreshToken } from "./auth.js";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Ajoute automatiquement le access token
api.interceptors.request.use((config) => {
  const accessToken = useAuthStore.getState().accessToken;

  if (accessToken) {
    config.headers.Authorization = `Bearer ${accessToken}`;
  }

  return config;
});

// Gestion automatique d'un access token expiré
api.interceptors.response.use(
  (response) => response,

  async (error) => {
    const originalRequest = error.config;

    // Seulement pour les erreurs 401
    if (error.response?.status !== 401) {
      return Promise.reject(error);
    }

    // Évite une boucle infinie
    if (originalRequest?._retry) {
      return Promise.reject(error);
    }

    const url = originalRequest?.url || "";

    // Pas de refresh pour les routes d'authentification
    if (
      url.includes("/auth/otp") ||
      url.includes("/auth/verify") ||
      url.includes("/auth/refresh")
    ) {
      return Promise.reject(error);
    }

    const currentRefreshToken =
      useAuthStore.getState().refreshToken;

    // Aucun refresh token disponible
    if (!currentRefreshToken) {
      useAuthStore.getState().logout();

      window.location.href = "/login";

      return Promise.reject(error);
    }

    originalRequest._retry = true;

    try {
      const data = await refreshToken(currentRefreshToken);

      useAuthStore
        .getState()
        .setTokens(
          data.access_token,
          data.refresh_token,
        );

      // Nouveau token pour la requête qui avait échoué
      originalRequest.headers.Authorization =
        `Bearer ${data.access_token}`;

      // Rejoue automatiquement la requête
      return api(originalRequest);
    } catch (refreshError) {
      // Refresh token invalide ou expiré
      useAuthStore.getState().logout();

      window.location.href = "/login";

      return Promise.reject(refreshError);
    }
  },
);

export default api;