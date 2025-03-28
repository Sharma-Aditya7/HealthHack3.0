import React, { useState } from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false); // State to toggle the hamburger menu

  // Function to close the menu
  const closeMenu = () => {
    setIsOpen(false);
  };

  return (
    <nav className="navbar">
      {/* Logo */}
      <div className="logo">TumorDetect</div>

      {/* Hamburger Menu Icon */}
      <div
        className="hamburger"
        onClick={() => setIsOpen(!isOpen)} // Toggle the menu
      >
        &#9776; {/* Unicode for hamburger icon */}
      </div>

      {/* Navigation Links */}
      <ul className={`nav-links ${isOpen ? 'active' : ''}`}>
        {/* Home */}
        <li>
          <Link to="/" onClick={closeMenu}>Home</Link>
        </li>
        {/* About Us */}
        <li>
          <Link to="/about" onClick={closeMenu}>About Us</Link>
        </li>
        {/* Tools */}
        <li>
          <Link to="/tools" onClick={closeMenu}>Tools</Link>
        </li>
        {/* Donate Now */}
        <li>
          <button className="donate-btn" onClick={closeMenu}>Donate Now</button>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;