import React from "react";
import "./page.css"

export default function About() {
    return (
        <div className="about-container">
            <header className="about-header">
                <h1>About LearnSphere</h1>
                <p>Welcome to LearnSphere, your ultimate AI-powered study planner and scheduler. We are dedicated to transforming the way students and professionals manage their learning journeys with cutting-edge artificial intelligence technology.</p>
            </header>

            <section className="about-section">
                <h2>Our Mission</h2>
                <p>
                At LearnSphere, we aim to empower learners with personalized, efficient, and adaptive study plans. We believe that everyone deserves a structured yet flexible approach to education, and our AI-driven platform ensures that users can optimize their time, boost productivity, and achieve their academic and professional goals seamlessly.
                </p>
            </section>
            <section className="about-section">
                <h2>Our Vision</h2>
                <p>
                We envision a future where learning is not just effective but also engaging and stress-free. By leveraging AI technology, LearnSphere strives to create a smart learning environment that adapts to each user’s unique needs, fostering a culture of continuous learning and success.

                </p>
            </section>

            <section className="about-section">
                <h2>What we offer?</h2>
                <ul>
                    <li>AI-Powered Scheduling: Our intelligent algorithm curates the most effective study schedules based on your goals, deadlines, and learning pace</li>
                    <li>Personalized Study Plans: Tailored study sessions that adapt to your progress and preferences.</li>
                    <li>Smart Reminders & Notifications: Never miss a study session with our AI-driven alerts and reminders.</li>
                    <li>Performance Tracking: Monitor your progress with in-depth analytics and insights.</li>
                    <li>Seamless Integration: Sync your schedules across multiple devices and platforms.</li>

                </ul>
            </section>

            <section className="about-section">
                <h2>Why Choose LearnSphere?</h2>
                <ul>
                    <li>AI-based personalized study plans</li>
                    <li>Task scheduling with reminders</li>
                    <li>Progress tracking and analytics</li>
                    <li>Smart recommendations for better learning</li>
                </ul>
            </section>

        </div>
    );

}