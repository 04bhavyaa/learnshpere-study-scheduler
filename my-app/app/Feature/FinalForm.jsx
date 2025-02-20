"use client";

import React from "react";
import { Formik } from "formik";
import { useRouter } from "next/navigation";
import * as yup from "yup";
import Form from "react-bootstrap/Form";
import { Button, Row, Container, Col, Card } from "react-bootstrap";
import Select2 from "@/Components/Select2";
import Select2Multi from "@/Components/Select2Multi";
import InputGroup from 'react-bootstrap/InputGroup';

export default function FinalForm() {
    const router = useRouter();
    const subjectMapping = {
        IT: 0, French: 1, Arabic: 2, Science: 3, English: 4, Biology: 5,
        Spanish: 6, Chemistry: 7, Geology: 8, Math: 10, History: 11,
    };

    const absenceMapping = { low: "low", high: "high" };

    const validationSchema = yup.object().shape({
        education: yup.string().required("Education must be selected"),
        gender: yup.string().required("Gender is required"),
        absence: yup.string().oneOf(Object.keys(absenceMapping)).required("Absence level must be selected"),
        mother_job: yup.string().required("Mother's job must be selected"),
        father_job: yup.string().required("Father's job must be selected"),
        freetime: yup.string().oneOf(["1", "2", "3", "4", "5"]).required("Free time must be selected"),
        school_support: yup.string().oneOf(["yes", "no"]).required("School support must be selected"),
        family_support: yup.string().oneOf(["yes", "no"]).required("Family support must be selected"),
        extra_paid_class: yup.string().oneOf(["yes", "no"]).required("Extra paid class must be selected"),
        extracurricular: yup.string().oneOf(["yes", "no"]).required("Extracurricular must be selected"),
        romantic_rel: yup.string().oneOf(["yes", "no"]).required("Romantic relationship must be selected"),
        higher_education: yup.string().oneOf(["yes", "no"]).required("Higher education must be selected"),
        grade1: yup.number().min(0).max(20).required("Grade1 must be between 0 and 20"),
        grade2: yup.number().min(0).max(20).required("Grade2 must be between 0 and 20"),
        subject: yup.array().of(yup.string().oneOf(Object.keys(subjectMapping))).min(1, "At least one subject must be selected"),
        goal: yup.string().required("Goal is required")
    });

    const initialValues = {
        education: "", gender: "", subject: [], absence: "", mother_job: "", father_job: "",
        freetime: "", school_support: "", family_support: "", extra_paid_class: "",
        extracurricular: "", romantic_rel: "", higher_education: "", grade1: "", grade2: "", goal: ""
    };

    const options = {
        education: ["Middle School", "Lower Level", "High School"],
        subjects: Object.keys(subjectMapping),
        gender: ["Male", "Female", "Other"],
        absence: Object.keys(absenceMapping),
        motherJob: ["other", "services", "teacher", "at_home", "health"],
        fatherJob: ["other", "services", "teacher", "health", "at_home"],
        freetime: ["1", "2", "3", "4", "5"],
        yesNo: ["yes", "no"],
        grades: Array.from({ length: 21 }, (_, i) => i.toString()), // 0 to 20
    };

    const handleSubmit = async (values) => {
        const jsonData = {
            ...values,
            subject_mapping: values.subject.reduce((acc, sub) => {
                acc[sub] = 1;
                return acc;
            }, {}),
            absence_mapping: {
                low: values.absence === "low" ? "yes" : "no",
                high: values.absence === "high" ? "yes" : "no",
            },
        };
    
        fetch("http://127.0.0.1:5000/studyplan", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(jsonData),
        })
            .then(async (response) => {
                if (!response.ok) {
                    throw new Error(`HTTP Error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                localStorage.setItem("predictionData", JSON.stringify(data)); // Store the prediction result
                window.location.href = "/Dashboard"; // Redirect to result page
            })
            .catch((error) => console.error("Error in API request:", error));
    };
    
    return (
        <Container className="d-flex justify-content-center align-items-center min-vh-100">
            <Card className="glass-form p-5 w-100 shadow-lg rounded-5 border-0" style={{ backdropFilter: "blur(20px)", background: "rgba(255, 255, 255, 0.3)" }}>
                <h3 className="text-center mb-3 text-primary">Let's Get Started!</h3>
                <Formik validationSchema={validationSchema} initialValues={initialValues} onSubmit={handleSubmit}>
                    {(props) => (
                        <Form noValidate onSubmit={props.handleSubmit}>
                            <Row className="g-4">
                                <Col md={6}><Select2 props={props} label="education" options={options.education} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="gender" options={options.gender} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="absence" options={options.absence} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="freetime" options={options.freetime} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="mother_job" options={options.motherJob} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="father_job" options={options.fatherJob} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="school_support" options={options.yesNo} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="family_support" options={options.yesNo} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="extra_paid_class" options={options.yesNo} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="extracurricular" options={options.yesNo} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="romantic_rel" options={options.yesNo} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="higher_education" options={options.yesNo} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="grade1" options={options.grades} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}><Select2 props={props} label="grade2" options={options.grades} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={12}><Select2Multi props={props} label="subject" options={options.subjects} setFieldValue={props.setFieldValue} /></Col>
                                <Col md={6}>
                                    <InputGroup className="mb-3 rounded">
                                        <InputGroup.Text id="inputGroup-sizing-default rounded">Goal:</InputGroup.Text>
                                        <Form.Control
                                            aria-label="Large"
                                            aria-describedby="inputGroup-sizing-default"
                                            name="goal"
                                            value={props.values.goal}
                                            onChange={props.handleChange}
                                            onBlur={props.handleBlur}
                                            isInvalid={props.touched.goal && !!props.errors.goal}
                                        />
                                        <Form.Control.Feedback type="invalid">{props.errors.goal}</Form.Control.Feedback>
                                    </InputGroup>
                                </Col>
                                <Col md={12} className="text-center"><Button type="submit" className="w-100">Generate Dashboard</Button></Col>
                            </Row>
                        </Form>
                    )}
                </Formik>
            </Card>
        </Container>
    );
}
