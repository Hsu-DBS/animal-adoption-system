import axios from "axios";


// Load backend base URL from .env file
const BASE_URL = import.meta.env.VITE_API_BASE_URL;


// This code is the original axios import and instance creation example from axios documentation
// const instance = axios.create({
//   baseURL: 'https://some-domain.com/api/',
//   timeout: 1000,
//   headers: {'X-Custom-Header': 'foobar'}
// });

// My code: Create a reusable Axios instance with a common base URL
// Reference: https://axios-http.com/docs/instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});


// The original code from axios documentation: Add a request interceptor
// axios.interceptors.request.use(function (config) {
//     // Do something before request is sent
//     return config;
//   }, function (error) {
//     // Do something with request error
//     return Promise.reject(error);
//   },
//   { synchronous: true, runWhen: () => /* This function returns true */}
// );

/**
 * My code: Request Interceptor
 *
 * Automatically attaches JWT token to every outgoing request.
 * This avoids manually adding Authorization headers each time.
 *
 * Reference:
 * Axios Interceptors Documentation:
 * https://axios-http.com/docs/interceptors
 */
api.interceptors.request.use(
  (config) => {
    // Read token stored in browser's localStorage
    const token = localStorage.getItem("access_token");

    // If token exists, attach it to Authorization header
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config; // continue request
  },
  (error) => Promise.reject(error)
);



// The original code from axios documentation: Add a response interceptor
// axios.interceptors.response.use(function onFulfilled(response) {
//     // Any status code that lie within the range of 2xx cause this function to trigger
//     // Do something with response data
//     return response;
//   }, function onRejected(error) {
//     // Any status codes that falls outside the range of 2xx cause this function to trigger
//     // Do something with response error
//     return Promise.reject(error);
//   });

/**
 * My code: Response Interceptor
 *
 * Handles responses after they return from the server.
 * If a 401 Unauthorized error occurs, the user's session token
 * is cleared and they are redirected to the login page.
 *
 * This ensures the app automatically logs out users with
 * expired or invalid JWT tokens.
 *
 * Reference:
 * https://axios-http.com/docs/interceptors
 */
api.interceptors.response.use(
  (response) => response, // if success, return normally

  (error) => {
    // If backend says "401 Unauthorized"
    if (error.response?.status === 401) {

      // Remove invalid JWT token
      localStorage.removeItem("access_token");

      // Redirect user to login page
      window.location.href = "/login";
    }

    return Promise.reject(error); // forward error to caller
  }
);


// Export the axios instance to use in API files
export default api;
