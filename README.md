# University Course Management System - FastAPI

A RESTful API to manage students, professors, courses, and enrollments for a university, built using **FastAPI** with in-memory data storage. The system includes full CRUD support, business rule validation, data integrity checks, and proper HTTP responses.

---

## Features

### Core Entities

* **Students**: ID, name, email, major, year, GPA
* **Professors**: ID, name, email, department, hire\_date
* **Courses**: ID, name, code, credits, professor\_id, max\_capacity
* **Enrollments**: student\_id, course\_id, enrollment\_date, grade

### API Capabilities

* Full **CRUD** for all entities
* Data validation using **Pydantic** models
* Proper **HTTP status codes** and structured error handling
* Business rule enforcement:

  * Prevent duplicate enrollments
  * Enforce course capacity limits
  * GPA auto-calculation
  * Unique email across entities
* Cascading logic (e.g., delete professor → update courses)

---

## Endpoints

### Students

* `GET /students`
* `POST /students`
* `GET /students/{id}`
* `PUT /students/{id}`
* `DELETE /students/{id}`
* `GET /students/{id}/courses`

### Professors

* `GET /professors`
* `POST /professors`
* `GET /professors/{id}`
* `PUT /professors/{id}`
* `DELETE /professors/{id}`

### Courses

* `GET /courses`
* `POST /courses`
* `GET /courses/{id}`
* `PUT /courses/{id}`
* `DELETE /courses/{id}`
* `GET /courses/{id}/students`

### Enrollments

* `POST /enrollments`
* `GET /enrollments`
* `PUT /enrollments/{student_id}/{course_id}`
* `DELETE /enrollments/{student_id}/{course_id}`

---

## Validation Rules (Pydantic)

* **Student**

  * GPA: 0.0–4.0
  * Year: 1–4
  * Valid email format
* **Course**

  * Credits: 1–6
  * Code format: DEPT###-### (e.g., CS101-001)
* **Professor**

  * Hire date: Not in the future
  * Email: Valid format
* **Enrollment**

  * Grade: Must be A–F or 0.0–4.0
  * Enrollment date: Not in the future

---

## Status Codes

* `200 OK` – Success for GET/PUT
* `201 Created` – Success for POST
* `204 No Content` – Successful DELETE
* `400 Bad Request` – Invalid or missing input
* `404 Not Found` – Resource doesn’t exist
* `409 Conflict` – Business rule violation
* `422 Unprocessable Entity` – Validation error

---

## Error Format

```json
{
  "error": {
    "message": "Detailed error message",
    "type": "ValidationError | BusinessRuleViolation | NotFound"
  }
}
```

---

## Running the App

### 1. Install dependencies

```bash
pip install fastapi uvicorn
```

### 2. Run the server

```bash
uvicorn main:app --reload
```

### 3. Open docs

```
http://localhost:8000/docs
```

---

## Project Structure

```
project/
│
├── main.py         # FastAPI app and route definitions
├── models.py       # Pydantic models
├── logic.py        # Business logic and utilities
└── database.py     # In-memory data store
```
