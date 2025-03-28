import React, { useState } from 'react';
import './Tools.css';

const Tools = () => {
  const [files, setFiles] = useState([]); // State to store multiple selected files
  const [isLoading, setIsLoading] = useState(false); // Loading state
  const [result, setResult] = useState(null); // Single result state

  const handleFileChange = (e) => {
    setFiles(Array.from(e.target.files)); // Store the selected files as an array
  };

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form submission behavior
    if (files.length === 0) {
      alert("Please select at least one file.");
      return;
    }
    setIsLoading(true); // Start loading
    setResult(null); // Clear previous result
    try {
      const formData = new FormData();

      // Append each file to the form data
      files.forEach((file, index) => {
        formData.append(`file${index}`, file);
      });

      // Send the files to the backend
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });
      console.log("API Response:", response); // Log the response
      if (!response.ok) {
        const errorData = await response.json(); // Try to parse error details
        throw new Error(errorData.error || "Failed to process the files.");
      }
      const data = await response.json(); // Get the aggregated result from the backend
      setResult(data); // Store the single result
    } catch (error) {
      console.error("Error:", error.message);
      alert(error.message || "An error occurred while processing the files.");
    } finally {
      setIsLoading(false); // Stop loading
    }
  };

  return (
    <div className="tools">
      <h1>Tumor Awareness</h1>
      <p>Upload your MRI or CT scan reports for analysis.</p>
      {/* File Upload Section */}
      <form onSubmit={handleSubmit} className="upload-section">
        <input type="file" onChange={handleFileChange} multiple /> {/* Allow multiple file selection */}
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Processing..." : "Upload and Analyze"}
        </button>
      </form>
      {/* Loading Screen */}
      {isLoading && (
        <div className="loading-screen">
          <p>Processing your files...</p>
        </div>
      )}
      {/* Results Section */}
      {result && (
        <div className="results-section">
          <h2>Analysis Results</h2>
          <p><strong>Tumor Type:</strong> {result.tumor_type}</p>
          <p><strong>Risk Level:</strong> {result.risk_level}</p>
          <p><strong>Probability:</strong> {result.probability}%</p>
          <h3>Processed Images</h3>
          {result.processed_images && result.processed_images.length > 0 ? (
            <div className="processed-images">
              {result.processed_images.map((imagePath, index) => (
                <img
                  key={index}
                  src={`http://localhost:5000/processed_images/${imagePath.split('\\').pop()}`}
                  alt={`Processed Image ${index + 1}`}
                  style={{ maxWidth: '450px', margin: '10px' }}
                />
              ))}
            </div>
          ) : (
            <p>No processed images available.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default Tools;