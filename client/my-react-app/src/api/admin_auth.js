import api from "./axios";

// Admin Login
export async function adminLogin(payload) {
  const res = await api.post("/auth/login/admin", payload);
  return res.data.data;
}