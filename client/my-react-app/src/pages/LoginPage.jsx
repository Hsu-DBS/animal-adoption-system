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
      const res = await api.post("/auth/login/admin", {
        email,
        password,
      });

      // Save the returned JWT token using AuthContext
      login(res.data.access_token);

      // Redirect user to homepage after successful login
      window.location.href = "/";
    } catch (err) {
      // Show error message if login fails
      setError("Invalid email or password");
    }
  };

  return (
    // This  login form logic is referenced and guided by ChatGPT.
    <div style={{ maxWidth: "350px", margin: "80px auto", padding: "20px" }}>
      <h2>Login</h2>

      {/* Show error message if login failed */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* Login form */}
      <form onSubmit={handleLogin}>
        {/* Email input */}
        <div style={{ marginBottom: "10px" }}>
          <label>Email</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)} // Update email state
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>

        {/* Password input */}
        <div style={{ marginBottom: "10px" }}>
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Update password state
            style={{ width: "100%", padding: "8px" }}
            required
          />
        </div>

        {/* Submit button */}
        <button
          type="submit"
          style={{
            padding: "8px",
            width: "100%",
            background: "black",
            color: "white",
            border: "none",
          }}
        >
          Login
        </button>
      </form>
    </div>
  );
}
