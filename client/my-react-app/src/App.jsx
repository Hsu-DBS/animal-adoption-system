// References:
// https://api.reactrouter.com/v7/functions/react_router.Routes.html
// https://reactrouter.com/6.28.0/start/tutorial#the-root-route

// Import routing components from React Router.
// - Routes: Container that holds all route definitions
// - Route: Represents a single route (URL → Component)
import { Routes, Route } from "react-router-dom";

// Import the Login page component
import LoginPage from "./pages/LoginPage";

// Import the AnimalsList page component
import AnimalsList from "./pages/AnimalsList";

// Import Animal Details page component
import AnimalDetails from "./pages/AnimalDetails";

// Import Animal Details page component
import AdoptionForm from "./pages/AdoptionForm";

// Import the ProtectedRoute wrapper that checks if the user is authenticated
import ProtectedRoute from "./components/ProtectedRoute";

// Import the Navbar component
import Navbar from "./components/Navbar";

// Main App component that defines all application routes
function App() {
  return (
    // Routes container that holds all <Route> elements
    <Routes>
      
      {/* Public Route: /login */}
      <Route path="/login" element={<LoginPage />} />

      {/*
        Protected Route: /
        - Wrapped inside <ProtectedRoute>
        - Only accessible if user has a valid JWT token
        - If not logged in → automatically redirects to /login
      */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            {/* Component rendered only after authentication */}
            <Navbar />
            <AnimalsList />
          </ProtectedRoute>
        }
      />

      {/* Add route for AnimalDetails page */}
      <Route
        path="/animals/:animalId"
        element={
          <ProtectedRoute>
            <Navbar />
            <AnimalDetails />
          </ProtectedRoute>
        }
      />

      <Route 
        path="/adopt/:animalId"
        element={
          <ProtectedRoute>
            <Navbar />
            <AdoptionForm />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

// Export App so it can be used by main.jsx
export default App;
