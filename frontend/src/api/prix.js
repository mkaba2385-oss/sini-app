import api from "./client.js";

export async function getPrix() {
  const response = await api.get("/prix");
  return response.data;
}

export async function getPrixById(id) {
  const response = await api.get(`/prix/${id}`);
  return response.data;
}

export async function getPrixByCulture(culture) {
  const response = await api.get(
    `/prix/culture/${encodeURIComponent(culture)}`,
  );
  return response.data;
}

export async function getPrixByMarche(marche) {
  const response = await api.get(
    `/prix/marche/${encodeURIComponent(marche)}`,
  );
  return response.data;
}