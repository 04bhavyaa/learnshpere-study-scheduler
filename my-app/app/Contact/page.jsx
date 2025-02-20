import React from "react";
import "./page.css";

export default function Contact() {
  return (
    <div className="contact-container">
      <h1 className="contact-header">Contact Us</h1>

      <div className="contact-section">
        <p>
          Have questions or need support? Reach out to us, and we’ll be happy to
          assist you!
        </p>
      </div>

      <div className="contact-info">
        <div className="contact-box">
          <h2>Email Us</h2>
          <p>support@learnsphere.ai</p>
        </div>

        <div className="contact-box">
          <h2>Call Us</h2>
          <p>+91 98765 43210</p>
        </div>

        <div className="contact-box">
          <h2>Visit Us</h2>
          <p>123 AI Street, Tech City, India</p>
        </div>
      </div>

      <div className="contact-form">
        <h2>Send Us a Message</h2>
        <form>
          <input type="text" placeholder="Your Name" required />
          <input type="email" placeholder="Your Email" required />
          <textarea placeholder="Your Message" rows="5" required></textarea>
          <button type="submit">Send Message</button>
        </form>
      </div>
    </div>
  );
}



