from database import students, enrollments, courses

def calculate_gpa(student_id):
    grades = [e['grade'] for e in enrollments if e['student_id'] == student_id and e['grade'] is not None]
    if not grades:
        return 0.0
    return round(sum(grades) / len(grades), 2)

def is_course_full(course_id):
    enrolled = len([e for e in enrollments if e['course_id'] == course_id])
    return enrolled >= courses[course_id]['max_capacity']

def already_enrolled(student_id, course_id):
    return any(e for e in enrollments if e['student_id'] == student_id and e['course_id'] == course_id)
