// References:
// https://api.reactrouter.com/v7/functions/react_router.useParams.html
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function
// https://react.dev/learn/synchronizing-with-effects
// https://react.dev/learn/conditional-rendering


// React imports for state management and lifecycle effects
// useState: to store animal data and loading state
// useEffect: to run code when component mounts or when dependency changes
import { useEffect, useState } from "react";

// useParams allows reading route parameters like :animalId from URL
import { useParams } from "react-router-dom";

// API function to fetch one animal by ID
import { getAnimalById } from "../api/animals";

// Import CSS styles using CSS Modules
import styles from "./AnimalDetails.module.css";

export default function AnimalDetails() {
  // Extract dynamic route parameter from URL
  const { animalId } = useParams();

  // Store fetched animal data
  const [animal, setAnimal] = useState(null);

  const [loading, setLoading] = useState(true);

  // Load API base URL from .env
  const BASE_URL = import.meta.env.VITE_API_BASE_URL;

  // Fetch animal details when the page loads
  // useEffect runs only when animalId changes
  useEffect(() => {
    const fetchData = async () => {
      try {
        // Call API function to fetch data by ID
        const data = await getAnimalById(animalId);

        // Save data to state
        setAnimal(data);
      } catch (err) {
        console.error("Error fetching animal:", err);
      } finally {
        // Whether success or error, stop loading indicator
        setLoading(false);
      }
    };

    fetchData();
  }, [animalId]); // re-run if route param changes

  // Show loading message while waiting for backend response
  if (loading) return <p className={styles.loading}>Loading...</p>;

  // If API returned null or backend return 404
  if (!animal) return <p className={styles.notFound}>Animal not found.</p>;

  return (
    <div className={styles.container}>
      {/* animal img */}
      <img
        src={`${BASE_URL}${animal.photo_url}`}
        alt={animal.name}
        className={styles.image}
      />

      {/* animal info */}
      <div className={styles.info}>
        {/* Animal Name */}
        <h2 className={styles.name}>{animal.name}</h2>

        {/* Key attributes */}
        <p className={styles.detail}><strong>Species:</strong> {animal.species}</p>
        <p className={styles.detail}><strong>Breed:</strong> {animal.breed}</p>
        <p className={styles.detail}><strong>Age:</strong> {animal.age}</p>
        <p className={styles.detail}><strong>Gender:</strong> {animal.gender}</p>
        <p className={styles.detail}>
          <strong>Status:</strong> {animal.adoption_status}
        </p>

        {/* Description / Bio */}
        <p className={styles.description}>{animal.description}</p>

        {/* Adopt Button only show if available */}
        {animal.adoption_status === "Available" && (
          <button
            className={styles.adoptButton}
            // React Router alternative: useNavigate()
            onClick={() => window.location.href = `/adopt/${animal.id}`}
          >
            Adopt
          </button>
        )}
      </div>
    </div>
  );
}
