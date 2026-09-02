import axios from "axios";
import api from "./client.js";

export async function registerUser(userData) {
  const response = await api.post("/users", userData);

  return response.data;
}

export async function requestOtp(phoneNumber) {
  const response = await api.post("/auth/otp", {
    phone_number: phoneNumber,
  });

  return response.data;
}

export async function verifyOtp(phoneNumber, code) {
  const response = await api.post("/auth/verify", {
    phone_number: phoneNumber,
    code,
  });

  return response.data;
}

export async function refreshToken(refreshTokenValue) {
  const response = await axios.post(
    `${import.meta.env.VITE_API_URL}/auth/refresh`,
    {
      refresh_token: refreshTokenValue,
    },
    {
      headers: {
        "Content-Type": "application/json",
      },
    },
  );

  return response.data;
}

export async function getCurrentUser() {
  const response = await api.get("/users/me");

  return response.data;
}