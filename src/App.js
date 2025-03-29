import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './Components/Navbar';
import Home from './Components/Home';
import AboutUs from './Components/AboutUs';
import Footer from './Components/Footer';
import Tools from './Components/Tools';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        {/* Navbar is always visible */}
        <Navbar />

        {/* Define routes for Home and AboutUs */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<AboutUs />} />
          <Route path="/tools" element={<Tools />} />
        </Routes>

        {/* Footer is always visible */}
        <Footer />
      </div>
    </Router>
  );
}

export default App;