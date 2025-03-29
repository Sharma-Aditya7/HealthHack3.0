import React from 'react';
import './AboutUs.css';
import { FaUsers, FaHeart, FaLightbulb, FaHandshake } from 'react-icons/fa';

const AboutUs = () => {
  return (
    <div className="about-us">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>About CancerDetect</h1>
          <p>Empowering early detection and saving lives through innovative technology.</p>
        </div>
      </section>

      {/* Mission Section */}
      <section className="mission-section">
        <div className="container">
          <div className="mission-content">
            <div className="mission-text">
              <h2>Our Mission</h2>
              <p>
                At CancerDetect, we are dedicated to revolutionizing cancer diagnosis and treatment through advanced AI-powered tools. Our mission is to provide accessible, accurate, and timely cancer detection solutions to individuals worldwide.
              </p>
              <div className="mission-stats">
                <div className="stat">
                  <span className="stat-number">90%</span>
                  <span className="stat-label">Early Detection Rate</span>
                </div>
                <div className="stat">
                  <span className="stat-number">24/7</span>
                  <span className="stat-label">Availability</span>
                </div>
                <div className="stat">
                  <span className="stat-number">1000+</span>
                  <span className="stat-label">Lives Impacted</span>
                </div>
              </div>
            </div>
            <div className="mission-image">
              <div className="image-container">
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="values-section">
        <div className="container">
          <h2>Our Core Values</h2>
          <div className="values-grid">
            <div className="value-card">
              <FaUsers className="value-icon" />
              <h3>Community First</h3>
              <p>We believe in making healthcare accessible to everyone, regardless of their background or location.</p>
            </div>
            <div className="value-card">
              <FaHeart className="value-icon" />
              <h3>Patient Care</h3>
              <p>Every decision we make is guided by our commitment to patient well-being and care.</p>
            </div>
            <div className="value-card">
              <FaLightbulb className="value-icon" />
              <h3>Innovation</h3>
              <p>We continuously push the boundaries of what's possible in medical technology.</p>
            </div>
            <div className="value-card">
              <FaHandshake className="value-icon" />
              <h3>Trust</h3>
              <p>We build trust through transparency, accuracy, and reliable results.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="team-section">
        <div className="container">
          <h2>Meet Our Team</h2>
          <div className="team-grid">
            <div className="team-member">
              <div className="member-image">
                <img src="/Memberpics/Coder1.jpg" alt="Aditya Sharma" />
                <div className="member-overlay">
                  <div className="social-links">
                    <a href="#" className="social-link">LinkedIn</a>
                    <a href="#" className="social-link">GitHub</a>
                    <a href="#" className="social-link">Twitter</a>
                  </div>
                </div>
              </div>
              <h3>Aditya Sharma</h3>
              <p>Lead Developer</p>
            </div>
            <div className="team-member">
              <div className="member-image">
                <img src="/Memberpics/Coder2.jpg" alt="Archita" />
                <div className="member-overlay">
                  <div className="social-links">
                    <a href="#" className="social-link">LinkedIn</a>
                    <a href="#" className="social-link">GitHub</a>
                    <a href="#" className="social-link">Twitter</a>
                  </div>
                </div>
              </div>
              <h3>Archita</h3>
              <p>AI Specialist</p>
            </div>
            <div className="team-member">
              <div className="member-image">
                <img src="/Memberpics/Coder3.jpg" alt="Shashwat" />
                <div className="member-overlay">
                  <div className="social-links">
                    <a href="#" className="social-link">LinkedIn</a>
                    <a href="#" className="social-link">GitHub</a>
                    <a href="#" className="social-link">Twitter</a>
                  </div>
                </div>
              </div>
              <h3>Shashwat</h3>
              <p>Backend Developer</p>
            </div>
            <div className="team-member">
              <div className="member-image">
                <img src="/Memberpics/Coder4.jpg" alt="Adithya V Holla" />
                <div className="member-overlay">
                  <div className="social-links">
                    <a href="#" className="social-link">LinkedIn</a>
                    <a href="#" className="social-link">GitHub</a>
                    <a href="#" className="social-link">Twitter</a>
                  </div>
                </div>
              </div>
              <h3>Adithya V Holla</h3>
              <p>Frontend Developer</p>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="container">
          <h2>What People Say</h2>
          <div className="testimonials-grid">
            <div className="testimonial-card">
              <div className="quote-icon">"</div>
              <p>
                "CancerDetect saved my life! Their AI tool detected early signs of cancer that I wouldn't have noticed otherwise."
              </p>
              <div className="testimonial-author">
                <h4>Gutkesh</h4>
                <span>Patient</span>
              </div>
            </div>
            <div className="testimonial-card">
              <div className="quote-icon">"</div>
              <p>
                "The platform is easy to use and provides accurate results. Highly recommend it to anyone concerned about their health."
              </p>
              <div className="testimonial-author">
                <h4>Mukesh</h4>
                <span>User</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutUs;