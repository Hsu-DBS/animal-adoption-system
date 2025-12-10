// axios instance with token + baseURL
import api from "./axios";

// Fetch animals with pagination + filters
export async function getAnimals(page = 1, limit = 12, search = "", gender = "", adoptionStatus = "") {
  // Send GET request + filters as query parameters
  const res = await api.get("/animal-management/animals", {
    params: {
      page,
      limit,
      search: search || undefined, // only send if not empty
      gender: gender || undefined,
      adoption_status: adoptionStatus || undefined,
    },
  });

  return res.data;
}


// Fetch a single animal by ID
export async function getAnimalById(animalId) {
  // Send GET request
  const res = await api.get(`/animal-management/animals/${animalId}`);
  // response data
  return res.data.data; 
}


// Create a new animal
export async function createAnimal(payload) {
  const res = await api.post("/animal-management/animals", payload, {
    headers: { "Content-Type": "multipart/form-data" }
  });
  return res.data.data;
}