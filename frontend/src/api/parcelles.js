import api from "./client.js";

export async function getParcelles() {
  const response = await api.get("/parcelles");
  return response.data;
}

export async function createParcelle(data) {
  const response = await api.post("/parcelles", data);
  return response.data;
}

export async function updateParcelle(id, data) {
  const response = await api.patch(`/parcelles/${id}`, data);
  return response.data;
}

export async function deleteParcelle(id) {
  await api.delete(`/parcelles/${id}`);
}
export async function getParcelle(id) {
  const response = await api.get(`/parcelles/${id}`);
  return response.data;
}