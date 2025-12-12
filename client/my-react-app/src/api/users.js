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


// ------------------------------------------
//       APIs for admin dashboard
// ------------------------------------------

// Fetch adopters with pagination + filters
export async function getAdopters(params) {
  const res = await api.get("/user-management/adopters", { params });
  return res.data.data;
}

// Delete adopter by ID
export async function deleteAdopter(adopterId) {
  return await api.delete(`/user-management/adopters/${adopterId}`);
}

// Update admin profile
export async function updateAdminProfile(userId, payload) {
  return await api.put(`/user-management/users/${userId}`, payload);
}

// Get admin users
export async function getAdminUsers(params) {
  const res = await api.get("/user-management/users", { params });
  return res.data.data;
}

// Delete admin by ID
export async function deleteAdminUser(userId) {
  return await api.delete(`/user-management/users/${userId}`);
}