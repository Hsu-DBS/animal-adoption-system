import { useContext } from "react";
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
      <div className={styles.left}>
        <img
          src="/vite.svg"
          alt="Logo"
          className={styles.logo}
        />
        <span className={styles.projectName}>Digital Animal Adoption System</span>
      </div>

      {/* RIGHT SIDE - LOGOUT BUTTON */}
      <button className={styles.logoutButton} onClick={handleLogout}>
        Logout
      </button>
    </nav>
  );
}
