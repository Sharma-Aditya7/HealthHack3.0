import React from 'react';
import './AboutUs.css';

const AboutUs = () => {
  return (
    <div className="about-us">
      {/* Hero Section */}
      <section className="hero">
        <h1>About CancerDetect</h1>
        <p>Empowering early detection and saving lives through innovative technology.</p>
      </section>
      {/* Who We Are Section */}
      <section className="section">
        <h2>Who We Are</h2>
        <p>
          At CancerDetect, we are dedicated to revolutionizing cancer diagnosis and treatment through advanced AI-powered tools. Our mission is to provide accessible, accurate, and timely cancer detection solutions to individuals worldwide.
        </p>
      </section>
      {/* Our Mission Section */}
      <section className="section">
        <h2>Our Mission</h2>
        <p>
          Our mission is simple: to save lives by enabling early detection of cancer. We believe that early diagnosis is the key to successful treatment, and our cutting-edge tools are designed to make this process faster, easier, and more reliable.
        </p>
      </section>
      {/* Team Members Section */}
      <section className="section team-section">
        <h2>Meet Our Team</h2>
        <div className="team-members">
          <div className="team-member">
            <img src="/Memberpics/Coder1.jpg" alt="Team Member 1" />
            <h3>Aditya Sharma</h3>
            <p>Coder1</p>
          </div>
          <div className="team-member">
            <img src="/Memberpics/Coder2.jpg" alt="Team Member 2" />
            <h3>Archita</h3>
            <p>Coder2</p>
          </div>
          <div className="team-member">
            <img src="/Memberpics/Coder3.jpg" alt="Team Member 3" />
            <h3>Shashwat</h3>
            <p>Coder3</p>
          </div>
          <div className="team-member">
            <img src="/Memberpics/Coder4.jpg" alt="Team Member 4" />
            <h3>Adithya V Holla</h3>
            <p>Coder4</p>
          </div>
        </div>
      </section>
      {/* Testimonials Section */}
      <section className="section testimonials-section">
        <h2>What People Say</h2>
        <div className="testimonials">
          <div className="testimonial">
            <p>
              "CancerDetect saved my life! Their AI tool detected early signs of cancer that I wouldn't have noticed otherwise."
            </p>
            <h4>- Gutkesh., Patient</h4>
          </div>
          <div className="testimonial">
            <p>
              "The platform is easy to use and provides accurate results. Highly recommend it to anyone concerned about their health."
            </p>
            <h4>- Mukesh, User</h4>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutUs;