"use client";

import Form from "react-bootstrap/Form";
import React, { useState } from "react";
import Col from "react-bootstrap/Col";
import * as Icon from "react-bootstrap-icons";

export default function Select2Multi({ props, label, options = [], setFieldValue }) {
  const [isOpen, setIsOpen] = useState(false);
  const [dropdownList, setDropdownList] = useState(options);

  const toggleDropdown = () => setIsOpen(!isOpen);

  function filterOptions(event) {
    const filtered = options.filter((item) =>
      item.toLowerCase().includes(event.target.value.toLowerCase())
    );
    setDropdownList(filtered);
  }

  function handleSelect(item) {
    let newValues = [...props.values[label]];
    if (!newValues.includes(item)) {
      newValues.push(item);
      setFieldValue(label, newValues);
    }
  }

  function handleRemove(item) {
    let newValues = props.values[label].filter((value) => value !== item);
    if (newValues.length > 0) {
      setFieldValue(label, newValues);
    }
  }

  return (
    <div className="container mb-4">
      <Form.Group as={Col} md="4">
        <Form.Label>{label}</Form.Label>
        <div className="d-flex flex-wrap border p-3 rounded bg-white" onClick={toggleDropdown}>
          {props.values[label].map((item, index) => (
            <span key={index} className="badge bg-primary m-1">
              {item} <Icon.X onClick={() => handleRemove(item)} style={{ cursor: "pointer" }} />
            </span>
          ))}
        </div>
        <Form.Control.Feedback type="invalid">{props.errors[label]}</Form.Control.Feedback>

        {isOpen && (
          <div className="border p-2 mt-2 rounded" style={{ maxHeight: "200px", overflowY: "auto" }}>
            <input className="form-control mb-2" type="text" placeholder={`Search ${label}`} onChange={filterOptions} />
            <ul className="list-group">
              {dropdownList.length > 0 ? (
                dropdownList.map((item, index) => (
                  <li
                    key={index}
                    className="list-group-item list-group-item-action"
                    onClick={() => handleSelect(item)}
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
