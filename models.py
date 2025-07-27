from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, EmailStr, validator

class Student(BaseModel):
    id: int
    name: str
    email: EmailStr
    major: str
    year: int = Field(..., ge=1, le=4)
    gpa: float = Field(..., ge=0.0, le=4.0)

class Course(BaseModel):
    id: int
    name: str
    code: str = Field(..., regex=r"^[A-Z]{2,4}\d{3}-\d{3}$")
    credits: int = Field(..., ge=1, le=6)
    professor_id: int
    max_capacity: int

class Professor(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    hire_date: date

    @validator("hire_date")
    def validate_hire_date(cls, value):
        if value > date.today() or value < date(1950, 1, 1):
            raise ValueError("Hire date must be between 1950 and today")
        return value

class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[float] = Field(None, ge=0.0, le=4.0)