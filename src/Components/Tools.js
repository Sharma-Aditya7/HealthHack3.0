import React, { useState } from 'react';
import './Tools.css';
import { FaUpload, FaSpinner, FaChartBar, FaExclamationTriangle, FaFileAlt, FaCheckCircle, FaTimes } from 'react-icons/fa';

const Tools = () => {
  const [files, setFiles] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [selectedImage, setSelectedImage] = useState(null);

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (files.length === 0) {
      setError("Please select at least one file.");
      return;
    }
    setIsLoading(true);
    setResult(null);
    setError(null);

    try {
      const formData = new FormData();
      files.forEach((file, index) => {
        formData.append('file', file);
      });

      // Get the API URL from environment variables or use a default
      const apiUrl = process.env.REACT_APP_API_URL || 'https://tumor-detect.onrender.com';
      console.log('Using API URL:', apiUrl); // Debug log

      const response = await fetch(`${apiUrl}/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server response:', errorText); // Debug log
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error.message);
      setError(error.message || "An error occurred while processing the files.");
    } finally {
      setIsLoading(false);
    }
  };

  const ImageModal = ({ image, onClose }) => {
    return (
      <div className="image-modal-overlay" onClick={onClose}>
        <div className="image-modal-content" onClick={e => e.stopPropagation()}>
          <button className="close-modal-btn" onClick={onClose}>
            <FaTimes />
          </button>
          <img src={image} alt="Full size analysis result" />
        </div>
      </div>
    );
  };

  return (
    <div className="tools">
      {/* Hero Section */}
      <section className="tools-hero">
        <div className="hero-content">
          <h1>Tumor Analysis Tool</h1>
          <p>Upload your MRI or CT scan reports for instant AI-powered analysis</p>
        </div>
      </section>

      {/* Upload Section */}
      <section className="upload-section">
        <div className="container">
          <div className="upload-container">
            <div className="upload-box">
              <FaUpload className="upload-icon" />
              <h2>Upload Your Images</h2>
              <p>Drag and drop your files here or click to browse</p>
              <form onSubmit={handleSubmit} className="upload-form">
                <input
                  type="file"
                  onChange={handleFileChange}
                  multiple
                  accept="image/*"
                  className="file-input"
                  id="file-input"
                />
                <label htmlFor="file-input" className="file-label">
                  Choose Files
                </label>
                {files.length > 0 && (
                  <div className="selected-files">
                    <h3>Selected Files:</h3>
                    <ul>
                      {files.map((file, index) => (
                        <li key={index}>
                          <FaFileAlt className="file-icon" />
                          <span>{file.name}</span>
                          <FaCheckCircle className="check-icon" />
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                <button type="submit" className="analyze-btn" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <FaSpinner className="spinner" />
                      Processing...
                    </>
                  ) : (
                    'Analyze Images'
                  )}
                </button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Results Section */}
      {result && (
        <section className="results-section">
          <div className="container">
            <div className="results-container">
              <h2>Analysis Results</h2>
              <div className="results-grid">
                <div className="result-card">
                  <FaChartBar className="result-icon" />
                  <h3>Tumor Type</h3>
                  <p>{result.tumor_type}</p>
                </div>
                <div className="result-card">
                  <FaExclamationTriangle className="result-icon" />
                  <h3>Risk Level</h3>
                  <p className={`risk-${result.risk_level.toLowerCase()}`}>
                    {result.risk_level}
                  </p>
                </div>
                <div className="result-card">
                  <FaChartBar className="result-icon" />
                  <h3>Probability</h3>
                  <p>{result.probability}%</p>
                </div>
              </div>

              {result.processed_images && result.processed_images.length > 0 && (
                <div className="processed-images">
                  <h3>Processed Images</h3>
                  <div className="images-grid">
                    {result.processed_images.map((imagePath, index) => (
                      <div 
                        key={index} 
                        className="image-card"
                        onClick={() => setSelectedImage(`${process.env.REACT_APP_API_URL}/processed_images/${imagePath}`)}
                      >
                        <img
                          src={`${process.env.REACT_APP_API_URL}/processed_images/${imagePath}`}
                          alt={`Processed Image ${index + 1}`}
                        />
                        <div className="image-overlay">
                          <span>Click to View Full Size</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </section>
      )}

      {/* Image Modal */}
      {selectedImage && (
        <ImageModal 
          image={selectedImage} 
          onClose={() => setSelectedImage(null)} 
        />
      )}

      {/* Error Message */}
      {error && (
        <div className="error-message">
          <div className="container">
            <div className="error-content">
              <FaExclamationTriangle className="error-icon" />
              <p>{error}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Tools;