import api from "./axios";

// Fetch current logged-in user info
export async function getCurrentUser() {
  const res = await api.get("/user-management/current-user");
  return res.data.data;
}

// Update adopter profile
export async function updateAdopterProfile(adopterId, payload) {
  return await api.put(`/user-management/adopters/${adopterId}`, payload);
}
