from fastapi import FastAPI, HTTPException
from models import Student, Course, Professor, Enrollment
from database import db
from logic import calculate_gpa, is_course_full, already_enrolled
from datetime import date
from typing import Optional

app = FastAPI()

def get_student(student_id: int):
    student = db["students"].get(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

def get_course(course_id: int):
    course = db["courses"].get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

def get_professor(prof_id: int):
    prof = db["professors"].get(prof_id)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return prof

@app.get("/")
def read_root():
    return {"message": "Welcome to the University Management System API"}

# --- Students ---
@app.post("/students", status_code=201)
def create_student(student: Student):
    if student.id in db["students"]:
        raise HTTPException(status_code=409, detail="Student already exists")
    db["students"][student.id] = student
    return student

@app.get("/students")
def list_students(major: Optional[str] = None, year: Optional[int] = None):
    students = list(db["students"].values())
    if major:
        students = [s for s in students if s.major == major]
    if year:
        students = [s for s in students if s.year == year]
    return students

@app.get("/students/{student_id}")
def get_student_by_id(student_id: int):
    return get_student(student_id)

@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    get_student(student_id)
    db["students"][student_id] = student
    return student

@app.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: int):
    get_student(student_id)
    del db["students"][student_id]

# ====== Courses ======
@app.post("/courses", status_code=201)
def create_course(course: Course):
    if course.id in db["courses"]:
        raise HTTPException(status_code=409, detail="Course already exists")
    if course.professor_id not in db["professors"]:
        raise HTTPException(status_code=404, detail="Professor not found")
    db["courses"][course.id] = course
    return course

@app.get("/courses")
def list_courses():
    return list(db["courses"].values())

@app.get("/courses/{course_id}")
def get_course_by_id(course_id: int):
    return get_course(course_id)

@app.put("/courses/{course_id}")
def update_course(course_id: int, course: Course):
    get_course(course_id)
    db["courses"][course_id] = course
    return course

@app.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int):
    get_course(course_id)
    del db["courses"][course_id]

# ====== Professors ======
@app.post("/professors", status_code=201)
def create_professor(prof: Professor):
    if prof.id in db["professors"]:
        raise HTTPException(status_code=409, detail="Professor already exists")
    db["professors"][prof.id] = prof
    return prof

@app.get("/professors")
def list_professors():
    return list(db["professors"].values())

@app.get("/professors/{prof_id}")
def get_professor_by_id(prof_id: int):
    return get_professor(prof_id)

@app.put("/professors/{prof_id}")
def update_professor(prof_id: int, prof: Professor):
    get_professor(prof_id)
    db["professors"][prof_id] = prof
    return prof

@app.delete("/professors/{prof_id}", status_code=204)
def delete_professor(prof_id: int):
    get_professor(prof_id)
    del db["professors"][prof_id]

# ====== Enrollments ======
@app.post("/enrollments", status_code=201)
def enroll_student(enrollment: Enrollment):
    student = get_student(enrollment.student_id)
    course = get_course(enrollment.course_id)
    if enrollment.grade and (enrollment.grade < 0.0 or enrollment.grade > 4.0):
        raise HTTPException(status_code=400, detail="Invalid grade")
    existing = [e for e in db["enrollments"] if e.student_id == enrollment.student_id and e.course_id == enrollment.course_id]
    if existing:
        raise HTTPException(status_code=409, detail="Student already enrolled")
    enrolled_count = len([e for e in db["enrollments"] if e.course_id == enrollment.course_id])
    if enrolled_count >= course.max_capacity:
        raise HTTPException(status_code=409, detail="Course capacity reached")
    db["enrollments"].append(enrollment)
    return enrollment

@app.get("/enrollments")
def list_enrollments():
    return db["enrollments"]

@app.put("/enrollments/{student_id}/{course_id}")
def update_grade(student_id: int, course_id: int, grade: float):
    for e in db["enrollments"]:
        if e.student_id == student_id and e.course_id == course_id:
            e.grade = grade
            return e
    raise HTTPException(status_code=404, detail="Enrollment not found")

@app.delete("/enrollments/{student_id}/{course_id}", status_code=204)
def drop_course(student_id: int, course_id: int):
    for i, e in enumerate(db["enrollments"]):
        if e.student_id == student_id and e.course_id == course_id:
            del db["enrollments"][i]
            return
    raise HTTPException(status_code=404, detail="Enrollment not found")
