import React from "react";
import "./Card.css";

const Card = ({ title, content }) => {
  return (
    <div className="card-1">
      <div className="card-heading">{title}</div>
      <div className="card-content">{content}</div>
    </div>
  );
};

export default Card;
