// References:
// <StrictMode>: https://react.dev/reference/react/StrictMode 
// createRoot: https://react.dev/reference/react-dom/client/createRoot
// React Router: https://www.w3schools.com/react/react_router.asp


// Import React core (for JSX and StrictMode)
import React from 'react';

// Import the ReactDOM client for rendering the application
import ReactDOM from 'react-dom/client';

// Import the main App component of frontend
import App from './App.jsx';

import { HashRouter } from "react-router-dom";

// Import global AuthProvider (manages JWT token, login state, logout)
import { AuthProvider } from './context/AuthContext.jsx';

// Import global CSS styles
import "./styles/global.css";

// Render the entire React application into the <div id="root"> element in index.html
ReactDOM.createRoot(document.getElementById('root')).render(

  // StrictMode helps catch errors in development
  <React.StrictMode>

    {/* HashRouter enables routing throughout the app */}
    <HashRouter>

      {/* AuthProvider wraps the entire app and provides authentication state */}
      <AuthProvider>

        {/* App is main component that contains all routes (Login, Home, Animal, etc.) */}
        <App />

      </AuthProvider>
    </HashRouter>
  </React.StrictMode>
);
