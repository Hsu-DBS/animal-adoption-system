// References:
// https://api.reactrouter.com/v7/functions/react_router.Routes.html
// https://reactrouter.com/6.28.0/start/tutorial#the-root-route

// Import routing components from React Router.
// - Routes: Container that holds all route definitions
// - Route: Represents a single route
import { Routes, Route } from "react-router-dom";

// ---------------------
// Adopter Routes
// ---------------------

// Import the ProtectedRoute wrapper that checks if the user is authenticated
import ProtectedRoute from "./components/ProtectedRoute";

// Import the Navbar component
import Navbar from "./components/Navbar";

// Import the Login page component
import LoginPage from "./pages/LoginPage";

// Import Adopter Registration page component
import AdopterRegister from "./pages/AdopterRegister";

// Import the AnimalsList page component
import AnimalsList from "./pages/AnimalsList";

// Import Animal Details page component
import AnimalDetails from "./pages/AnimalDetails";

// Import Adoption Form page component
import AdoptionForm from "./pages/AdoptionForm";

// Import Applications List page component
import ApplicationsList from "./pages/ApplicationsList";

// Import Application Details page component
import ApplicationDetails from "./pages/ApplicationDetails";

// Import Adopter Profile page component
import AdopterProfile from "./pages/AdopterProfile";


// ---------------------
// Admin Routes
// ---------------------

import AdminLogin from "./pages/AdminLogin";

// Main App component that defines all application routes
function App() {
  return (
    // Routes container that holds all <Route> elements
    <Routes>
      
      {/* Adopter Public Routes */}

      {/* Public Route: /login */}
      <Route path="/login" element={<LoginPage />} />

      {/* Public Route: Register */}
      <Route path="/register" element={<AdopterRegister />} />

      {/* Admin Public Routes */}
      {/* Public Route: /admin/login */}
      <Route path="/admin/login" element={<AdminLogin />} />

      {/*
        Protected Route: /
        - Wrapped inside <ProtectedRoute>
        - Only accessible if user has a valid JWT token
        - If not logged in, automatically redirects to /login
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

      {/* AnimalDetails page */}
      <Route
        path="/animals/:animalId"
        element={
          <ProtectedRoute>
            <Navbar />
            <AnimalDetails />
          </ProtectedRoute>
        }
      />

      {/* AdoptionForm page */}
      <Route 
        path="/adopt/:animalId"
        element={
          <ProtectedRoute>
            <Navbar />
            <AdoptionForm />
          </ProtectedRoute>
        }
      />

      {/* ApplicationsList page */}
      <Route
        path="/applications"
        element={
          <ProtectedRoute>
            <Navbar />
            <ApplicationsList />
          </ProtectedRoute>
        }
      />

      {/* ApplicationDetails page */}
       <Route
        path="/applications/:applicationId"
        element={
          <ProtectedRoute>
            <Navbar />
            <ApplicationDetails />
          </ProtectedRoute>
        }
      />

      {/* AdopterProfile page */}
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Navbar />
            <AdopterProfile />
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

// Export App so it can be used by main.jsx
export default App;
