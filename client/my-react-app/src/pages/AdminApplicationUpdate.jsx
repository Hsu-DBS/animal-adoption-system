// References:
// React useState/useEffect: https://react.dev/reference/react
// React Router useParams/useNavigate: https://reactrouter.com/en/main/hooks/use-params
// HTML form submission in React: https://react.dev/learn/sharing-state-between-components


import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { getApplicationById, updateApplicationStatus} from "../api/applications";
import styles from "./AdminApplicationUpdate.module.css";

export default function AdminApplicationUpdate() {
  // Get application ID from the URL
  const { applicationId } = useParams();
  // For navigation after update
  const navigate = useNavigate();

  // Local state to store form data
  const [form, setForm] = useState({
    animal_name: "",
    adopter_name: "",
    reason: "",
    status: "",
    created_at: "",
    updated_at: ""
  });

    // Local state to store error messages
  const [error, setError] = useState("");

  // Load application details when component mounts
  useEffect(() => {
    async function load() {
      const app = await getApplicationById(applicationId); // Fetch full application details

      // Populate form state with loaded application data
      setForm({
        animal_name: app.animal_name,
        adopter_name: app.adopter_name,
        reason: app.reason,
        status: app.status,
        created_at: app.created_at,
        updated_at: app.updated_at
      });
    }
    load();
  }, [applicationId]);  // Runs again only if URL param changes

  // Handle form submission for updating application status
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default browser form submit
    setError("");       // Clear previous errors

    try {
      // Send PATCH request to backend to update status
      await updateApplicationStatus(applicationId, {
        application_status: form.status
      });

      alert("Application status updated!");
      navigate("/admin/applications");    // Navigate back to list page

    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to update status.");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.innerBox}>
        <h2 className={styles.title}>Update Application</h2>

        {/* Status Update Form */}
        <form className={styles.form} onSubmit={handleSubmit}>

          {/* Read-only field: animal name */}
          <label>Animal Name</label>
          <input type="text" value={form.animal_name} disabled />

          {/* Read-only field: adopter name */}
          <label>Adopter Name</label>
          <input type="text" value={form.adopter_name} disabled />

          {/* Read-only field: application reason */}
          <label>Reason</label>
          <textarea value={form.reason} disabled />

          {/* Editable field: application status */}
          <label>Status</label>
          <select
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}  // Update state when user selects option
          >
            <option value="Submitted">Submitted</option>
            <option value="Approved">Approved</option>
            <option value="Rejected">Rejected</option>
            <option value="Cancelled">Cancelled</option>
          </select>

          {/* Display error message if exists */}
          {error && <p className={styles.error}>
            {typeof error === "string" ? error : JSON.stringify(error)}
          </p>}

          {/* Action buttons */}
          <div className={styles.actionsRow}>
            
            {/* Cancel */}
            <button
              type="button"
              className={styles.cancelBtn}
              onClick={() => navigate("/admin/applications")}
            >
                Cancel
            </button>

            {/* Submit button */}
            <button type="submit" className={styles.saveBtn}>
                Update
            </button>

          </div>

        </form>
      </div>
    </div>
  );
}
