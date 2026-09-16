from .utils import load_json, write_json, compute_hash, append_audit
from datetime import datetime

GRADE_POINTS = [(90,4.0),(85,3.7),(80,3.3),(75,3.0),(70,2.7),(65,2.3),(60,2.0),(0,0.0)]

def grade_to_gpa(score):
    for cutoff, pts in GRADE_POINTS:
        if score >= cutoff:
            return pts
    return 0.0

def student_can_register(student_id, course_id, semester):
    students = load_json('students.json')
    courses = load_json('courses.json')
    enrollments = load_json('enrollments.json')
    student = students.get(student_id)
    course = courses.get(course_id)
    if not student or not course:
        return False, 'Invalid student or course'
    # duplicate
    for e in enrollments.get(student_id, []):
        if e.get('course') == course_id and e.get('semester') == semester:
            return False, 'Already enrolled'
    # prerequisites
    prereqs = course.get('prerequisites', [])
    completed = [g.get('course') for g in load_json('grades.json').get(student_id, []) if g.get('score',0)>=60]
    missing = [p for p in prereqs if p not in completed]
    if missing:
        return False, f'Missing prerequisites: {missing}'
    # credit limit (max 18)
    current_credits = 0
    for e in enrollments.get(student_id, []):
        if e.get('semester') == semester:
            c = courses.get(e.get('course'))
            if c:
                current_credits += c.get('credits',0)
    if current_credits + course.get('credits',0) > 18:
        return False, 'Exceeds max credits for semester (18)'
    return True, 'OK'

def register_course(student_id, course_id, semester, by_user=None):
    ok, msg = student_can_register(student_id, course_id, semester)
    if not ok:
        return False, msg
    enrollments = load_json('enrollments.json')
    enrollments.setdefault(student_id, [])
    enrollments[student_id].append({'course': course_id, 'semester': semester, 'timestamp': datetime.utcnow().isoformat()+'Z'})
    write_json('enrollments.json', enrollments)
    append_audit(by_user or student_id, 'student', 'register_course', {'student': student_id, 'course': course_id, 'semester': semester})
    return True, 'Registered'

def compute_gpa(student_id):
    grades_all = load_json('grades.json').get(student_id, [])
    courses = load_json('courses.json')
    total_points = 0.0
    total_credits = 0
    for g in grades_all:
        course = courses.get(g.get('course'))
        if not course:
            continue
        credits = course.get('credits',0)
        pts = grade_to_gpa(g.get('score',0))
        total_points += pts * credits
        total_credits += credits
    cgpa = round(total_points/total_credits,2) if total_credits>0 else 0.0
    students = load_json('students.json')
    if student_id in students:
        students[student_id]['cgpa'] = cgpa
        students[student_id]['record_hash'] = compute_hash(students[student_id])
        write_json('students.json', students)
    return cgpa

def generate_transcript(student_id, by_user=None):
    students = load_json('students.json')
    grades = load_json('grades.json').get(student_id, [])
    courses = load_json('courses.json')
    student = students.get(student_id)
    if not student:
        return None
    transcript = {
        'student_id': student_id,
        'name': student.get('name'),
        'program': student.get('program'),
        'grades': grades,
        'generated_at': datetime.utcnow().isoformat()+'Z'
    }
    import json
    transcript['record_hash'] = compute_hash(transcript)
    trans = load_json('transcripts.json')
    trans.setdefault(student_id, [])
    trans[student_id].append(transcript)
    write_json('transcripts.json', trans)
    append_audit(by_user or student_id, 'student', 'generate_transcript', {'student': student_id})
    return transcript
