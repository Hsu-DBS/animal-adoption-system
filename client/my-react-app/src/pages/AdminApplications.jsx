// References:
// useState: https://react.dev/reference/react/useState
// useEffect: https://react.dev/reference/react/useEffect
// Debouncing input in React: https://dev.to/manishkc104/debounce-input-in-react-3726


import { useEffect, useState } from "react";
import { getApplications } from "../api/applications";
import styles from "./AdminApplications.module.css";

export default function AdminApplications() {

  // Store the list of applications returned from API
  const [applications, setApplications] = useState([]);

  // Pagination controls
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [totalPages, setTotalPages] = useState(1);

  // Search field states
  const [searchInput, setSearchInput] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  // Filter for application status
  const [status, setStatus] = useState("");

  // Debouncing animal search
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(searchInput);
      setPage(1);
    }, 500);
    return () => clearTimeout(timer);
  }, [searchInput]);

  // Load applications whenever filters or page change
  useEffect(() => {
    loadApplications();
  }, [page, debouncedSearch, status]);

  // Fetch application list
  async function loadApplications() {
    try {
      const params = {
        page,
        limit,
        search_by_name: debouncedSearch || undefined,
        application_status: status || undefined,
      };

      const res = await getApplications(params);
      const data = res.data;

      setApplications(data.applications || []);
      setTotalPages(data.total_pages || 1);

    } catch (err) {
      console.error("Failed to load applications", err);
    }
  }

  // Map status with CSS badge color
  const statusClass = (s) => {
    const k = (s || "").toLowerCase();
    if (k === "submitted") return styles.submitted;
    if (k === "approved") return styles.approved;
    if (k === "rejected") return styles.rejected;
    if (k === "cancelled") return styles.cancelled;
    return styles.unknown;
  };

  // Clear all filters at once
  const clearFilters = () => {
    setSearchInput("");
    setDebouncedSearch("");
    setStatus("");
    setPage(1);
  };

  return (
    <div className={styles.container}>
      <h2>Applications Management</h2>

      {/* Filters Section */}
      <div className={styles.filters}>

        {/* search input */}
        <input
          type="text"
          placeholder="Search by animal or adopter name"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
        />

        {/* Status dropdown */}
        <select
          value={status}
          onChange={(e) => {
            setStatus(e.target.value);
            setPage(1); // reset pagination
          }}
        >
          <option value="">All Status</option>
          <option value="Submitted">Submitted</option>
          <option value="Approved">Approved</option>
          <option value="Rejected">Rejected</option>
          <option value="Cancelled">Cancelled</option>
        </select>

        {/* Clear filters */}
        <button className={styles.clearBtn} onClick={clearFilters}>
          Clear Filters
        </button>
      </div>

      {/* Table Section */}
      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Animal</th>
              <th>Adopter</th>
              <th>Reason</th>
              <th>Status</th>
              <th>Submitted At</th>
              <th>Updated At</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {applications.map((app) => (
              <tr key={app.id}>

                {/* Animal name */}
                <td>{app.animal_name}</td>

                {/* Adopter name */}
                <td>{app.adopter_name}</td>

                {/* Reason message */}
                <td>{app.reason}</td>

                {/* Status badge */}
                <td>
                  <span
                    className={`${styles.statusBadge} ${statusClass(app.status)}`}
                  >
                    {app.status}
                  </span>
                </td>

                {/* Created date */}
                <td>{new Date(app.created_at).toLocaleDateString()}</td>

                {/* Updated date */}
                <td>{new Date(app.updated_at).toLocaleDateString()}</td>

                {/* Action buttons */}
                <td className={styles.actions}>
                  <button className={styles.updateBtn}>Update</button>
                  <button className={styles.deleteBtn}>Delete</button>
                </td>

              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination Section */}
      <div className={styles.pagination}>
        <button
          disabled={page === 1}
          onClick={() => setPage(page - 1)}
        >
          Prev
        </button>

        <span>
          Page {page} of {totalPages}
        </span>

        <button
          disabled={page === totalPages}
          onClick={() => setPage(page + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
}
