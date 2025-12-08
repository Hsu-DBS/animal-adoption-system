// References:
// https://reactrouter.com/en/main/components/navigate
// https://api.reactrouter.com/v7/functions/react_router.useNavigate.html
// https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage


// Import Navigate to redirect users who are not authenticated.
import { Navigate } from "react-router-dom";

export default function AdminProtectedRoute({ children }) {
  // Retrieve admin JWT token stored in browser.
  // If the token does not exist, user is NOT logged in.
  const token = localStorage.getItem("adminToken");

  // 'replace' prevents user from going back to protected page with back button.
  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }

  return children;
}
