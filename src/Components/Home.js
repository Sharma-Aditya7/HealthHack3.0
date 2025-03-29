import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import { FaBrain, FaChartLine, FaClock, FaUserMd } from 'react-icons/fa';

const Home = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Modal Component (defined inline)
  const Modal = ({ onClose }) => {
    return (
      <div className="modal-overlay" onClick={onClose}>
        <div className="modal-content" onClick={e => e.stopPropagation()}>
          <h2>Understanding Brain Tumors</h2>
          <div className="modal-sections">
            <div className="modal-section">
              <h3>What is a Brain Tumor?</h3>
              <p>
                A brain tumor is an abnormal growth of cells in the brain or central spinal canal, classified as benign (non-cancerous) or malignant (cancerous).
              </p>
            </div>
            <div className="modal-section">
              <h3>Types of Tumors</h3>
              <p>
                Benign tumors, like meningiomas, grow slowly and are often encapsulated but can still cause symptoms such as headaches, seizures, or cognitive issues.
              </p>
            </div>
            <div className="modal-section">
              <h3>Treatment Options</h3>
              <p>
                Treatment involves surgery, radiation, or chemotherapy. Early detection is crucial for better outcomes and improved quality of life.
              </p>
            </div>
          </div>
          <button onClick={onClose}>Close</button>
        </div>
      </div>
    );
  };

  return (
    <div className="home">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Empowering Early Detection</h1>
            <p>Advanced AI-powered tumor detection for better healthcare outcomes</p>
            <div className="hero-buttons">
              <button className="cta-btn primary" onClick={() => setIsModalOpen(true)}>
                Learn More
              </button>
              <Link to="/tools" className="cta-btn secondary">
                Get Started
              </Link>
            </div>
          </div>
          <div className="hero-image">
            <div className="brain-icon">
              <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z" fill="white"/>
                <path d="M12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z" fill="white"/>
              </svg>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <h2>Why Choose Our Platform?</h2>
        <div className="features-grid">
          <div className="feature-card">
            <FaBrain className="feature-icon" />
            <h3>AI-Powered Analysis</h3>
            <p>Advanced machine learning algorithms for accurate tumor detection</p>
          </div>
          <div className="feature-card">
            <FaChartLine className="feature-icon" />
            <h3>Real-time Results</h3>
            <p>Get instant analysis and detailed reports within minutes</p>
          </div>
          <div className="feature-card">
            <FaClock className="feature-icon" />
            <h3>Early Detection</h3>
            <p>Identify potential issues before they become critical</p>
          </div>
          <div className="feature-card">
            <FaUserMd className="feature-icon" />
            <h3>Expert Support</h3>
            <p>Access to medical professionals for consultation</p>
          </div>
        </div>
      </section>

      {/* Facts Section */}
      <section className="news-section">
        <h2>Did You Know?</h2>
        <div className="fact-cards">
          <div className="fact-card">
            <div className="fact-icon">📊</div>
            <h3>Early Detection Saves Lives</h3>
            <p>
              Early detection of tumors can increase survival rates by up to 90% in some cases.
            </p>
          </div>
          <div className="fact-card">
            <div className="fact-icon">🌍</div>
            <h3>Global Impact</h3>
            <p>
              Over 18 million new cancer cases are diagnosed globally each year, according to WHO.
            </p>
          </div>
          <div className="fact-card">
            <div className="fact-icon">🤖</div>
            <h3>AI Revolution</h3>
            <p>
              AI-powered tools are revolutionizing tumor detection, making it faster and more accurate.
            </p>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Get Started?</h2>
          <p>Upload your MRI or CT scan for instant analysis</p>
          <Link to="/tools" className="cta-btn primary">Start Analysis</Link>
        </div>
      </section>

      {/* Conditionally Render the Modal */}
      {isModalOpen && <Modal onClose={() => setIsModalOpen(false)} />}
    </div>
  );
};

export default Home;