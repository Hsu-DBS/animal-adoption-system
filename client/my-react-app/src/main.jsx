import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";

// Import global AuthProvider (manages JWT token & login state)
import { AuthProvider } from "./context/AuthContext.jsx";

// Render the React application and wrap everything inside AuthProvider
ReactDOM.createRoot(document.getElementById("root")).render(
  <AuthProvider>
    <App />
  </AuthProvider>
);
