import React, { useState } from 'react';
import './Home.css';

const Home = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Modal Component (defined inline)
  const Modal = ({ onClose }) => {
    return (
      <div className="modal-overlay">
        <div className="modal-content">
          <h2>Understanding Tumors</h2>
          <p>
          A brain tumor is an abnormal growth of cells in the brain or central spinal canal, classified as benign (non-cancerous) or malignant (cancerous). Benign tumors, like meningiomas, grow slowly and are often encapsulated but can still cause symptoms such as headaches, seizures, or cognitive issues if they press on critical areas. Malignant tumors, such as glioblastomas, are aggressive and invasive, requiring intensive treatments like surgery, radiation, or chemotherapy.
          The exact cause of brain tumors is unclear, but risk factors include genetic conditions, radiation exposure, and possibly environmental toxins. Diagnosis involves imaging (MRI or CT scans) and biopsies to determine tumor type and grade, guiding treatment decisions. While surgery is often the first step, complete removal isn’t always possible, especially near vital brain regions, necessitating additional therapies.
          </p>
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
          <h1>Empowering Early Detection</h1>
          <p>Tumors are complex, but early detection saves lives.</p>
          <button className="cta-btn" onClick={() => setIsModalOpen(true)}>
            Learn More
          </button>
        </div>
      </section>

      {/* Conditionally Render the Modal */}
      {isModalOpen && <Modal onClose={() => setIsModalOpen(false)} />}
      <section className="news-section">
        <h2>Did You Know?</h2>
        <div className="fact-cards">
          <div className="fact-card">
            <h3>Fact #1</h3>
            <p>
              Early detection of tumors can increase survival rates by up to 90% in some cases.
            </p>
          </div>
          <div className="fact-card">
            <h3>Fact #2</h3>
            <p>
              Over 18 million new cancer cases are diagnosed globally each year, according to WHO.
            </p>
          </div>
          <div className="fact-card">
            <h3>Fact #3</h3>
            <p>
              AI-powered tools are revolutionizing tumor detection, making it faster and more accurate.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;