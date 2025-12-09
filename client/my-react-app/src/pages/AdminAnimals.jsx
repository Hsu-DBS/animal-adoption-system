// References:
// https://www.w3schools.com/jsref/met_win_settimeout.asp
// https://www.w3schools.com/react/react_useeffect.asp
// https://www.w3schools.com/jsref/jsref_filter.asp
// https://www.telerik.com/blogs/how-to-create-custom-debounce-hook-react
// https://medium.com/swlh/simple-pagination-in-react-1f5100a070a3


import { useEffect, useState } from "react";
import { getAnimals } from "../api/animals";
import styles from "./AdminAnimals.module.css";
import { useNavigate } from "react-router-dom";

export default function AdminAnimals() {
  const navigate = useNavigate();

  // Data states
  const [animals, setAnimals] = useState([]);

  // Pagination states
  const [page, setPage] = useState(1);
  const [limit] = useState(10);
  const [totalPages, setTotalPages] = useState(1);

  // Filters
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [gender, setGender] = useState("");
  const [status, setStatus] = useState("");

  // Load API base URL from .env
  const BASE_URL = import.meta.env.VITE_API_BASE_URL;

  // Debounce for search input
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search);
      setPage(1); // reset to page 1 when typing new search
    }, 500);

    return () => clearTimeout(timer);
  }, [search]);

  // Fetch animals whenever filters / page change
  useEffect(() => {
    async function loadAnimals() {
      try {
        const res = await getAnimals(page, limit, debouncedSearch, gender, status);

        const payload = res.data ?? res;
        const data = payload.data ?? payload;

        setAnimals(data.animals || []);
        setTotalPages(data.total_pages || 1);
      } catch (err) {
        console.error("Failed to load animals", err);
        setAnimals([]);
        setTotalPages(1);
      }
    }

    loadAnimals();
  }, [page, debouncedSearch, gender, status]);

  // Clear all filters
  const clearFilters = () => {
    setSearch("");
    setDebouncedSearch("");
    setGender("");
    setStatus("");
    setPage(1);
  };

  // Status color badge
  const statusClass = (s) => {
    if (!s) return styles.statusUnknown;
    const key = String(s).toLowerCase();
    if (key === "available") return styles.statusAvailable;
    if (key === "adopted") return styles.statusAdopted;
    return styles.statusUnknown;
  };

  return (
    <div className={styles.container}>
      <h2>Animals Management</h2>

      {/* Search + Filters */}
      <div className={styles.filters}>
        {/* Search box */}
        <input
          type="text"
          placeholder="Search name, species, breed..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />

        {/* Gender filter */}
        <select value={gender} onChange={(e) => {
          setGender(e.target.value);
          setPage(1);
        }}>
          <option value="">All Genders</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>

        {/* Status filter */}
        <select value={status} onChange={(e) => {
          setStatus(e.target.value);
          setPage(1);
        }}>
          <option value="">All Status</option>
          <option value="Available">Available</option>
          <option value="Adopted">Adopted</option>
        </select>

        {/* Clear Filters */}
        <button className={styles.clearBtn} onClick={clearFilters}>
          Clear Filters
        </button>

        {/* Add New Animal */}
        <button
          type="button"
          className={styles.addBtn}
          onClick={() => navigate("")}
        >
          + Add New Animal
        </button>
      </div>

      {/* Animals Table */}
      <table className={styles.table}>
        <thead>
          <tr>
            <th>Photo</th>
            <th>Name</th>
            <th>Species</th>
            <th>Breed</th>
            <th>Age</th>
            <th>Gender</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Updated At</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {animals.map((a) => (
            <tr key={a.id}>
              {/* Photo */}
              <td>
                {a.photo_url ? (
                  <img src={`${BASE_URL}${a.photo_url}`} alt={a.name} className={styles.photo} />
                ) : (
                  <div className={styles.noImage}>No Image</div>
                )}
              </td>

              <td>{a.name}</td>
              <td>{a.species}</td>
              <td>{a.breed}</td>
              <td>{a.age}</td>
              <td>{a.gender}</td>

              <td>
                <span
                  className={`${styles.statusBadge} ${statusClass(a.adoption_status)}`}
                >
                  {a.adoption_status}
                </span>
              </td>

              <td>{a.created_at ? new Date(a.created_at).toLocaleDateString() : ""}</td>
              <td>{a.updated_at ? new Date(a.updated_at).toLocaleDateString() : ""}</td>

              <td className={styles.actions}>
                <button
                  className={styles.updateBtn}
                  onClick={() => navigate("")}
                >
                  Update
                </button>

                <button className={styles.deleteBtn}>
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Pagination  */}
      <div className={styles.pagination}>
        <button disabled={page === 1} onClick={() => setPage(page - 1)}>
          Prev
        </button>

        <span>Page {page} of {totalPages}</span>

        <button disabled={page === totalPages} onClick={() => setPage(page + 1)}>
          Next
        </button>
      </div>
    </div>
  );
}
