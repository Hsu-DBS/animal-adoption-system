// Import the CSS module for component styles
import styles from "./Navbar.module.css";

// Navbar component
export default function Navbar() {
  return (
    // Main navigation bar container
    <nav className={styles.navbar}>

      {/* LEFT SECTION: Logo + Project Name */}
      <div className={styles.left}>

        {/* Logo image */}
        <img
          src="/vite.svg"
          alt="Logo"
          className={styles.logo}
        />

        {/* Project title text */}
        <span className={styles.projectName}>Animal Adoption System</span>
      </div>

    </nav>
  );
}
