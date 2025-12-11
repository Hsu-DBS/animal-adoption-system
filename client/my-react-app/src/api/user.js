import api from "./axios";


// ------------------------------------------
//       Common API
// ------------------------------------------

// Fetch current logged-in user info
export async function getCurrentUser() {
  const res = await api.get("/user-management/current-user");
  return res.data.data;
}


// ------------------------------------------
//       APIs for adopter portal
// ------------------------------------------

// Update adopter profile
export async function updateAdopterProfile(adopterId, payload) {
  return await api.put(`/user-management/adopters/${adopterId}`, payload);
}

// Register a new adopter account
export async function registerAdopter(payload) {
  const res = await api.post("/user-management/adopters", payload);
  return res.data;
}
