"use client";

import React, { useState, useEffect } from "react";
import "./page.css";
import StudyPlan from "./StudyPlan";

export default function Dashboard() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [predictionData, setPredictionData] = useState(null);

  useEffect(() => {
    const data = localStorage.getItem("predictionData");
    if (data) {
      const parsedData = JSON.parse(data);
      console.log("Loaded predictionData:", parsedData);
      setPredictionData(parsedData);
    }
  }, []);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");
    setLoading(true);
    setError("");

    const requestBody = JSON.stringify({ query: input });
    console.log("Sending JSON:", requestBody);

    try {
      const response = await fetch("http://localhost:5000/chatbot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: requestBody
      });

      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }

      const data = await response.json();
      setMessages((prevMessages) => [
        ...prevMessages,
        { sender: "bot", text: data.response }
      ]);
    } catch (err) {
      setError("Failed to get a response. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard">

      {/* Render StudyPlan only if predictionData is not null */}
      {predictionData && <StudyPlan data={predictionData} />}

      {/* Chat Button */}
      <div className="chat-icon" onClick={() => setIsChatOpen(!isChatOpen)}>💬</div>

      {/* Chat Window */}
      {isChatOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <span>Chat</span>
            <button onClick={() => setIsChatOpen(false)}>✖</button>
          </div>

          <div className="chat-body">
            {messages.map((msg, index) => (
              <p key={index} className={msg.sender === "user" ? "user-message" : "bot-message"}>
                {msg.text}
              </p>
            ))}
            {loading && <p className="loading-message">Thinking...</p>}
            {error && <p className="error-message">{error}</p>}
          </div>

          <div className="chat-footer">
            <input
              type="text"
              placeholder="Type a message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
            />
            <button onClick={handleSendMessage} disabled={loading}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
