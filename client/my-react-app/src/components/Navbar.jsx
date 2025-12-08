// References:
// React useContext: https://react.dev/reference/react/useContext
// React Router Link: https://api.reactrouter.com/v7/functions/react_router.Link.html


import { useContext } from "react";
import { Link } from "react-router-dom"; // import Link for navigation
import { AuthContext } from "../context/AuthContext";
import styles from "./Navbar.module.css"; // import CSS module

export default function Navbar() {
  const { logout } = useContext(AuthContext);

  // Handler for logout button click
  const handleLogout = () => {
    logout();              // clear token from AuthContext + localStorage             
    window.location.href = "/login"; // redirect to login page
  };

  return (
    <nav className={styles.navbar}>
      {/* LEFT SIDE - LOGO + PROJECT NAME */}
      {/* Wrap entire left section inside a Link */}
      <Link to="/" className={styles.left}>
        <img
          src="/logo.png"
          alt="Logo"
          className={styles.logo}
        />
        <span className={styles.projectName}>
          Digital Animal Adoption System
        </span>
      </Link>

      {/* Applications List */}
      <Link className={styles.navLink} to="/applications">
        My Applications
      </Link>

      {/* My Profile */}
      <Link className={styles.navLink} to="/profile">
        My Profile
      </Link>

      {/* RIGHT SIDE - LOGOUT BUTTON */}
      <button className={styles.logoutButton} onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
}
