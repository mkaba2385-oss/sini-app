import api from "./client.js";

export async function getWeather(region) {
  const response = await api.get("/weather", {
    params: {
      region,
    },
  });

  return response.data;
}
