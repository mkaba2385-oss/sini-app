import api from "./client.js";

export async function getDiagnostics() {
  const response = await api.get("/diagnostics");
  return response.data;
}

export async function getDiagnostic(id) {
  const response = await api.get(`/diagnostics/${id}`);
  return response.data;
}
