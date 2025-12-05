// Import React hook for consuming context values
import { useContext } from "react";

// Import Navigate for redirecting users to another route
import { Navigate } from "react-router-dom";

// Import AuthContext to access authentication state (token)
import { AuthContext } from "../context/AuthContext";

// ProtectedRoute ensures that only authenticated users
// can access specific pages (such as dashboard, home, admin pages)
export default function ProtectedRoute({ children }) {

  // Get the stored token from AuthContext.
  // If token exists → user is logged in.
  const { token } = useContext(AuthContext);

  // If there is NO token, that means the user is NOT logged in.
  // So redirect them to the login page.
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // If authenticated, allow the requested page to render.
  return children;
}
