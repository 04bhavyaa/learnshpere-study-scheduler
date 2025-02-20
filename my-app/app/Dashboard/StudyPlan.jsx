import React from "react";
import "./StudyPlan.css";
import "bootstrap/dist/css/bootstrap.min.css";

const StudyPlan = ({ data }) => {
  if (!data || !data.study_plan || !data.study_plan.studyPlan)
    return <p className="text-center">Loading...</p>;

  const { aiLearningTips, dailySchedule, progressTrackingSystem, studyResources } =
    data.study_plan.studyPlan;

  return (
    <div className="study-plan container">
      <h1 className="text-center my-4">Study Plan Overview</h1>

      {/* AI Learning Tips */}
      <div className="card mb-3">
        <div className="card-body">
          <h2 className="card-title">AI Learning Tips</h2>
          <ul className="list-group">
            {aiLearningTips.map((tip, index) => (
              <li key={index} className="list-group-item">
                {tip}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Daily Schedule */}
      <div className="card mb-3">
        <div className="card-body">
          <h2 className="card-title">Daily Schedule</h2>
          {Object.entries(dailySchedule).map(([day, subjects]) => (
            <div key={day} className="day-schedule">
              <h3>{day.charAt(0).toUpperCase() + day.slice(1)}</h3>
              <ul className="list-group">
                {Object.entries(subjects).map(([subject, time]) => (
                  <li key={subject} className="list-group-item">
                    <strong>{subject}:</strong> {time}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>

      {/* Progress Tracking */}
      <div className="card mb-3">
        <div className="card-body">
          <h2 className="card-title">Progress Tracking</h2>
          <div className="progress-container">
            {progressTrackingSystem.completionBar.map((task, index) => (
              <div key={index} className="progress-item">
                <strong>{task.taskName}:</strong>
                <div className="progress mb-2">
                  <div
                    className="progress-bar bg-success"
                    role="progressbar"
                    style={{ width: `${task.progress}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* To-Do List */}
      <div className="card mb-3">
        <div className="card-body">
          <h2 className="card-title">To-Do List</h2>
          <ul className="list-group">
            {progressTrackingSystem.todoList.map((item, index) => (
              <li key={index} className="list-group-item">
                <strong>{item.taskName}:</strong> Due {item.dueDate}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Study Resources */}
      <div className="card mb-3">
        <div className="card-body">
          <h2 className="card-title">Study Resources</h2>
          <ul className="list-group">
            {studyResources.map((resource, index) => (
              <li key={index} className="list-group-item">
                <strong>{resource.resourceName}:</strong> {resource.description} (
                <a href={resource.url} target="_blank" rel="noopener noreferrer">
                  Link
                </a>
                )
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default StudyPlan;
