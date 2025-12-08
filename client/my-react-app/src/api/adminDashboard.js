import api from "./axios";

// Fetch dashboard summary
export async function getDashboardSummary() {
  const res = await api.get("/dashboard-management/dashboard/summary");
  return res.data.data; // returns summary data
}
