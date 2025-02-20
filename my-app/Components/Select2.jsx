"use client";

import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Col from "react-bootstrap/Col";
import "./Select2.css";

export default function Select2({ props, label, options = [], setFieldValue }) {
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownList, setDropdownList] = useState(options);

  const toggleDropdown = () => setIsOpen(!isOpen);

  function filterOptions(event) {
    const filtered = options.filter((item) =>
      item.toLowerCase().startsWith(event.target.value.toLowerCase())
    );
    setDropdownList(filtered);
  }

  return (
    <div className="container mb-4">
      <Form.Group as={Col} md="12">
        <Form.Label>{label}</Form.Label>
        <div className="d-flex flex-column position-relative">
          <Form.Control
            type="text"
            value={props.values[label] || ""}
            readOnly
            onClick={toggleDropdown}
            name={label}
            className="select2-input"
            isValid={props.touched[label] && !props.errors[label]}
            isInvalid={!!props.errors[label]}
          />
          <Form.Control.Feedback type="invalid">{props.errors[label]}</Form.Control.Feedback>
        </div>

        {isOpen && (
          <div className="select2-dropdown">
            <input className="select2-search" type="text" placeholder={`Search ${label}`} onChange={filterOptions} />
            <ul className="list-group">
              {dropdownList.length > 0 ? (
                dropdownList.map((item, index) => (
                  <li
                    key={index}
                    className="list-group-item list-group-item-action"
                    onClick={() => {
                      setFieldValue(label, item);
                      setIsOpen(false);
                    }}
                  >
                    {item}
                  </li>
                ))
              ) : (
                <li className="list-group-item text-muted">No options available</li>
              )}
            </ul>
          </div>
        )}
      </Form.Group>
    </div>
  );
}
