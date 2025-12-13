// References:
// useState: https://react.dev/reference/react/useState
// useEffect: https://react.dev/reference/react/useEffect
// Debouncing input in React: https://dev.to/manishkc104/debounce-input-in-react-3726
// Implementing CSV Data Export in React: https://dev.to/graciesharma/implementing-csv-data-export-in-react-without-external-libraries-3030
// Creating & Downloading Files Using Blob: https://developer.mozilla.org/en-US/docs/Web/API/Blob
// Creating Downloadable URLs: https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static
// Triggering File Download: https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/a#attr-download,https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/click


import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getApplications, deleteApplication } from "../api/applications";
import styles from "../styles/AdminApplications.module.css";

export default function AdminApplications() {
  const navigate = useNavigate();

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

  // Export current application list to CSV
  const handleExportApplications = () => {
    if (!applications || applications.length === 0) {
      alert("No applications to export.");
      return;
    }

    // CSV headers
    const headers = [
      "ID",
      "Animal Name",
      "Applicant Name",
      "Reason",
      "Status",
      "Created At",
      "Updated At"
    ];

    // Build rows from applications array
    const rows = applications.map((app) => [
      app.id,
      app.animal_name,
      app.adopter_name,
      app.reason,
      app.status,
      new Date(app.created_at).toLocaleString(),
      new Date(app.updated_at).toLocaleString()
    ]);

    // Convert data into CSV
    const csvContent =
      [headers, ...rows]
        .map((row) =>
          row
            .map((cell) => {
              if (cell == null) return "";
              return `"${String(cell).replaceAll('"', "'")}"`;
            })
            .join(",")
        )
        .join("\r\n");

    // Convert CSV to downloadable file
    const blob = new Blob([csvContent], {
      type: "text/csv;charset=utf-8;"
    });

    const ts = new Date().toISOString().slice(0, 10);
    const filename = `applications-export-${ts}.csv`;

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Handle deleting an application
  const handleDelete = async (applicationId) => {

    const yes = confirm("Are you sure you want to delete this application?");
    if (!yes) return;

    try {
      // Call backend API
      await deleteApplication(applicationId);
      alert("Application deleted successfully.");

      // Refresh the current list without resetting pagination
      await loadApplications();

    } catch (err) {
      console.error("Failed to delete application:", err);
      alert(err.response?.data?.detail || "Failed to delete application.");
    }
  };
 
  return (
    // The UI layout & form structure below is generated by ChatGPT
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

        {/* Export Button */}
          <button
              type="button"
              className={styles.exportBtn}
              onClick={handleExportApplications}
          >
              Export
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
                  <button
                    className={styles.updateBtn}
                    onClick={() => navigate(`/admin/applications/update/${app.id}`)}
                  >
                    Update
                  </button>
                  <button className={styles.deleteBtn} onClick={() => handleDelete(app.id)}>
                    Delete
                  </button>
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
