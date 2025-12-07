// axios instance with token + baseURL
import api from "./axios";

// Submit an adoption application
export async function submitApplication(payload) {
  // Send POST request
  const res = await api.post("/application-management/applications", payload);
  return res.data;
}