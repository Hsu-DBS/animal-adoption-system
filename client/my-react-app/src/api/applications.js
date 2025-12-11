// axios instance with token + baseURL
import api from "./axios";


// ------------------------------------
// Common API
// ------------------------------------

// GET application by ID
export async function getApplicationById(id) {
  // Send GET request
  const res = await api.get(`/application-management/applications/${id}`);
  return res.data.data;
}


// ------------------------------------
// Application API calls for adopters
// ------------------------------------

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

// UPDATE application (adopter can update reason or cancel application)
export async function updateApplicationByAdopter(id, payload) {
  // Send PUT request
  return await api.put(`/application-management/applications/${id}/adopter`, payload);
}


// ------------------------------------------
// Application API calls for administrators
// ------------------------------------------

// Get all applications (with filters + pagination)
export async function getApplications(params) {
  const res = await api.get("/application-management/applications", { params });
  return res.data;
}

// Update application status
export async function updateApplicationStatus(applicationId, payload) {
  return await api.patch(
    `/application-management/applications/${applicationId}/status`,
    payload,
    {
      headers: { "Content-Type": "application/json" }
    }
  );
}
