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

// React Router's BrowserRouter handles client-side routing (URLs without page reload)
import { BrowserRouter } from 'react-router-dom';

// Import global AuthProvider (manages JWT token, login state, logout)
import { AuthProvider } from './context/AuthContext.jsx';

// Render the entire React application into the <div id="root"> element in index.html
ReactDOM.createRoot(document.getElementById('root')).render(

  // StrictMode helps catch errors in development
  <React.StrictMode>

    {/* BrowserRouter enables routing throughout the app */}
    <BrowserRouter>

      {/* AuthProvider wraps the entire app and provides authentication state */}
      <AuthProvider>

        {/* App is main component that contains all routes (Login, Home, Animal, etc.) */}
        <App />

      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
