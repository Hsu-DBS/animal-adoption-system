// axios instance with token + baseURL
import api from "./axios";

// Submit an adoption application
export async function submitApplication(payload) {
  // Send POST request
  const res = await api.post("/application-management/applications", payload);
  return res.data;
}


// GET applications for the current logged-in adopter
export async function getMyApplications() {
  // Send GET request
  const res = await api.get("/application-management/applications/current-adopter");
  return res.data.data.applications;
}
