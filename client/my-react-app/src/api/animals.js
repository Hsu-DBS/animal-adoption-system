// axios instance with token + baseURL
import api from "./axios";

// Fetch animals with pagination
export async function getAnimals(page = 1, limit = 12) {
  // Send GET request with page + limit as query params to get all animals
  const res = await api.get("/animal-management/animals", {
    params: { page, limit },
  });

  return res.data; // return the response data
}
