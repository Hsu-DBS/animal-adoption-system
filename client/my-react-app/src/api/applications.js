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


// GET application by ID
export async function getApplicationById(id) {
  // Send GET request
  const res = await api.get(`/application-management/applications/${id}`);
  return res.data.data;
}

// UPDATE application (adopter can update reason or cancel application)
export async function updateApplicationByAdopter(id, payload) {
  // Send PUT request
  return await api.put(`/application-management/applications/${id}/adopter`, payload);
}
