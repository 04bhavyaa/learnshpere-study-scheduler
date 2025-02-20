import React from "react";
import "./StudyPlan.css"; // Import the updated CSS

const StudyPlan = ({ data }) => {
  if (!data || !data.study_plan) {
    return <p>Loading study plan...</p>;
  }

  // Handle cases where study_plan might be nested
  const studyPlan = data.study_plan.studyPlan || data.study_plan.study_plan || {};

  return (
    <div className="study-plan-container">
      <h1 className="title">Study Plan</h1>
      <div className="plan_grid">
        {Object.entries(studyPlan).map(([key, value], index) => (
          <div className="glass-card" key={index}>
            <h2>{formatKey(key)}</h2>
            <div className="card-content">{renderContent(value)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Function to format keys into readable titles
const formatKey = (key) => {
  return key.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase());
};

// Function to render dynamic content
const renderContent = (content) => {
  if (Array.isArray(content)) {
    return (
      <ul className="subject-list">
        {content.map((item, idx) =>
          typeof item === "object" ? (
            <li key={idx}>
              {Object.entries(item).map(([subKey, subValue]) => (
                <div key={subKey}>
                  <strong>{formatKey(subKey)}:</strong> {subValue}
                </div>
              ))}
            </li>
          ) : (
            <li key={idx}>{item}</li>
          )
        )}
      </ul>
    );
  } else if (typeof content === "object") {
    return (
      <>
        {Object.entries(content).map(([subKey, subValue]) => (
          <div key={subKey}>
            <strong>{formatKey(subKey)}:</strong>{" "}
            {typeof subValue === "object" ? renderContent(subValue) : subValue}
            {subKey === "completion_bar" &&
              Array.isArray(subValue) &&
              subValue.map((progress, i) => (
                <div className="progress" key={i}>
                  <div
                    className="progress-bar"
                    style={{ width: `${progress.progress}%` }}
                  >
                    {progress.progress}%
                  </div>
                </div>
              ))}
          </div>
        ))}
      </>
    );
  } else {
    return <span>{content}</span>;
  }
};

export default StudyPlan;
