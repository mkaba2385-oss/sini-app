import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { VitePWA } from "vite-plugin-pwa";

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: "autoUpdate",
      workbox: {
        navigateFallback: "/index.html",
        runtimeCaching: [
          {
            urlPattern:
              /^https?:\/\/(localhost:8000|sini-app-production\.up\.railway\.app)\/prix/,
            handler: "NetworkFirst",
            options: {
              cacheName: "sini-prix-api",
              expiration: {
                maxEntries: 20,
                maxAgeSeconds: 60 * 60 * 24,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern:
              /^https?:\/\/(localhost:8000|sini-app-production\.up\.railway\.app)\/parcelles/,
            handler: "NetworkFirst",
            options: {
              cacheName: "sini-parcelles-api",
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern:
              /^https?:\/\/(localhost:8000|sini-app-production\.up\.railway\.app)\/journal\/parcelle\//,
            handler: "NetworkFirst",
            options: {
              cacheName: "sini-journal-api",
              expiration: {
                maxEntries: 50,
                maxAgeSeconds: 60 * 60 * 24,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
          {
            urlPattern:
              /^https?:\/\/(localhost:8000|sini-app-production\.up\.railway\.app)\/weather/,
            handler: "NetworkFirst",
            options: {
              cacheName: "sini-weather-api",
              expiration: {
                maxEntries: 20,
                maxAgeSeconds: 60 * 60 * 6,
              },
              cacheableResponse: {
                statuses: [0, 200],
              },
            },
          },
        ],
      },
    }),
  ],
});