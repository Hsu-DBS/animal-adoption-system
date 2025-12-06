// References:
// React Forms: https://www.w3schools.com/react/react_forms.asp
// AXIOS Post Requests: https://axios-http.com/docs/post_example
// React Managing State: https://react.dev/learn/managing-state


// React imports for handling state and context
import { useState, useContext } from "react";

// Axios instance (configured with base URL + token)
import api from "../api/axios";

// Import AuthContext to access login function
import { AuthContext } from "../context/AuthContext";

//  Import CSS module for styling
import styles from "./LoginPage.module.css";

export default function LoginPage() {
  // Extract the login function from AuthContext
  const { login } = useContext(AuthContext);

  // Local states for form input values and error message
  const [email, setEmail] = useState("");       // Store user's email
  const [password, setPassword] = useState(""); // Store user's password
  const [error, setError] = useState("");       // Display login error

  // Handle form submission
  const handleLogin = async (e) => {
    e.preventDefault(); // Prevent page reload

    try {
      // Send POST request to FastAPI backend for authentication
      const res = await api.post("/auth/login/adopter", {
        email,
        password,
      });

      // Save the returned JWT token using AuthContext
      login(res.data.data.access_token);

      // Redirect user to homepage after successful login
      window.location.href = "/";
    } catch (err) {
      // Show error message if login fails
      setError("Invalid email or password");
    }
  };

  return (
    // This  login form logic is referenced and guided by ChatGPT.
    <div className={styles.container}>
      <h2 className={styles.title}>Login</h2>

      {/* Show error message if login failed */}
      {error && <p className={styles.error}>{error}</p>}

      {/* Login form */}
      <form onSubmit={handleLogin}>
        <div className={styles.formGroup}>

          {/* Email Input */}
          <label className={styles.label}>Email</label>
          <input
            type="text"
            className={styles.input}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        {/* Password Input */}
        <div className={styles.formGroup}>
          <label className={styles.label}>Password</label>
          <input
            type="password"
            className={styles.input}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {/* Submit Button */}
        <button className={styles.button}>Login</button>
      </form>
    </div>
  );
}
