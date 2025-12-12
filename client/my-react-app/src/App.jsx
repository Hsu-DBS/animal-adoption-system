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

// Import Admin Login page component
import AdminLogin from "./pages/AdminLogin";

// Import AdminNavbar component
import AdminNavbar from "./components/AdminNavbar";

// Import Admin Dashboard page component
import AdminDashboard from "./pages/AdminDashboard";

// Import the AdminProtectedRoute wrapper that checks if the admin is authenticated
import AdminProtectedRoute from "./components/AdminProtectedRoute";

// Import Admin Animals Management page component
import AdminAnimals from "./pages/AdminAnimals";

// Import Animal Create page component
import AdminAnimalCreate from "./pages/AdminAnimalCreate";

// Import Animal Update page component
import AdminAnimalUpdate from "./pages/AdminAnimalUpdate";

// Import Admin Applications Management page component
import AdminApplications from "./pages/AdminApplications";

// Import Application Update page component
import AdminApplicationUpdate from "./pages/AdminApplicationUpdate";

// Import Admin Adopters Management page component
import AdminAdopters from "./pages/AdminAdopters";

// Import Admin Profile page component
import AdminProfile from "./pages/AdminProfile";

// Import Admin Management page component
import AdminUsers from "./pages/AdminUsers";

// Import Admin Create page component
import AdminUserCreate from "./pages/AdminUserCreate";

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
        Adopter Protected Route: /
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

      {/* -------------------- */}
      {/*      Admin Routes    */}
      {/* -------------------- */}

      {/* Admin dashboard */}
      <Route
        path="/admin/dashboard"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminDashboard />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/animals"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminAnimals />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/animals/create"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminAnimalCreate />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/animals/update/:animalId"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminAnimalUpdate />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/applications"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminApplications />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/applications/update/:applicationId"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminApplicationUpdate />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/adopters"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminAdopters />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/profile"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminProfile />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/users"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminUsers />
          </AdminProtectedRoute>
        }
      />

      <Route
        path="/admin/users/create"
        element={
          <AdminProtectedRoute>
            <AdminNavbar />
            <AdminUserCreate />
          </AdminProtectedRoute>
        }
      />

    </Routes>
  );
}

// Export App so it can be used by main.jsx
export default App;
