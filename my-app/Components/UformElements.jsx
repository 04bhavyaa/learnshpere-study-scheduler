"use client";

import Col from "react-bootstrap/Col";
import Form from "react-bootstrap/Form";
import * as formik from "formik";

const UFormText = ({ props, label, id }) => {
    return (
        <Form.Group as={Col} md="4" controlId={id}>
            <Form.Label>{label}</Form.Label>
            <Form.Control
                type="text"
                name={id}
                value={formik.getIn(props.values, id)}
                onChange={props.handleChange}
                isValid={formik.getIn(props.touched, id) && !formik.getIn(props.errors, id)}
                isInvalid={!!formik.getIn(props.errors, id)}
            />
            <Form.Control.Feedback>Looks good!</Form.Control.Feedback>
            <Form.Control.Feedback type="invalid">{formik.getIn(props.errors, id)}</Form.Control.Feedback>
        </Form.Group>);
}

const UFormCheck = ({ props, label, id }) => {
    return (
        <Form.Group className="mb-3">
            <Form.Check
                required
                name={id}
                label={label}
                onChange={props.handleChange}
                isValid={formik.getIn(props.touched, id) && !formik.getIn(props.errors, id)}
                isInvalid={!!formik.getIn(props.errors, id)}
                feedback={formik.getIn(props.errors, id)}
                feedbackType="invalid"
                id={id}
            />
        </Form.Group>);
}

export {UFormText, UFormCheck}