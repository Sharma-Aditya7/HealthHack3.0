import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaBars, FaTimes, FaHeart } from 'react-icons/fa';
import './Navbar.css';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const closeMenu = () => {
    setIsOpen(false);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className={`navbar ${scrolled ? 'scrolled' : ''}`}>
      <div className="nav-container">
        {/* Logo */}
        <Link to="/" className="logo">
          <span className="logo-text">TumorDetect</span>
        </Link>

        {/* Hamburger Menu Icon */}
        <div className="hamburger" onClick={() => setIsOpen(!isOpen)}>
          {isOpen ? <FaTimes /> : <FaBars />}
        </div>

        {/* Navigation Links */}
        <ul className={`nav-links ${isOpen ? 'active' : ''}`}>
          <li>
            <Link 
              to="/" 
              onClick={closeMenu}
              className={isActive('/') ? 'active' : ''}
            >
              Home
            </Link>
          </li>
          <li>
            <Link 
              to="/about" 
              onClick={closeMenu}
              className={isActive('/about') ? 'active' : ''}
            >
              About Us
            </Link>
          </li>
          <li>
            <Link 
              to="/tools" 
              onClick={closeMenu}
              className={isActive('/tools') ? 'active' : ''}
            >
              Tools
            </Link>
          </li>
          <li>
            <button className="donate-btn" onClick={closeMenu}>
              <FaHeart className="heart-icon" />
              Donate Now
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;