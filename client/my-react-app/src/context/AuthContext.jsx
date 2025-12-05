// Purpose: Authentication Context for JWT handling
// Reference: https://www.w3schools.com/react/react_usecontext.asp

// Import React functions used for creating context and managing state
import { createContext, useState, useEffect } from "react";

// Create a global context that can be used by any component
export const AuthContext = createContext();

// AuthProvider wraps the whole app and provides authentication data (token, login, logout)
export function AuthProvider({ children }) {

  // Store JWT token in state. Load initial value from localStorage if available.
  const [token, setToken] = useState(localStorage.getItem("access_token") || null);

  // Function to handle login - save token to localStorage and React state
  const login = (accessToken) => {
    localStorage.setItem("access_token", accessToken); // save token to browser storage
    setToken(accessToken); // update React state
  };

  // Function to handle logout - remove token from storage and state
  const logout = () => {
    localStorage.removeItem("access_token"); // remove token from browser storage
    setToken(null); // clear token from state
  };

  // Provide token, login, and logout to all children components
  return (
    <AuthContext.Provider value={{ token, login, logout }}>
      {children} {/* Render the rest of the app inside provider */}
    </AuthContext.Provider>
  );
}
