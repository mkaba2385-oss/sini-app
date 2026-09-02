import api from "./client.js";

export async function getJournalByParcelle(parcelleId) {
  const response = await api.get(`/journal/parcelle/${parcelleId}`);
  return response.data;
}

export async function createJournalEntry(data) {
  const response = await api.post("/journal", data);
  return response.data;
}

export async function updateJournalEntry(entryId, data) {
  const response = await api.patch(`/journal/${entryId}`, data);
  return response.data;
}

export async function deleteJournalEntry(entryId) {
  await api.delete(`/journal/${entryId}`);
}

export async function getJournalStats(parcelleId) {
  const response = await api.get(`/journal/parcelle/${parcelleId}/stats`);
  return response.data;
}