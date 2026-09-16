from .utils import load_json, write_json, compute_hash, append_audit
from datetime import datetime

def faculty_assigned(faculty_id, course_id):
    faculty = load_json('faculty.json').get(faculty_id)
    if not faculty:
        return False
    return course_id in faculty.get('assigned_courses', [])

def upload_grade(faculty_id, student_id, course_id, score, semester, by_user=None):
    if not faculty_assigned(faculty_id, course_id):
        return False, 'Not authorized for this course'
    grades = load_json('grades.json')
    grades.setdefault(student_id, [])
    entry = {'course': course_id, 'score': score, 'semester': semester, 'graded_by': faculty_id, 'timestamp': datetime.utcnow().isoformat()+'Z'}
    grades[student_id].append(entry)
    write_json('grades.json', grades)
    append_audit(by_user or faculty_id, 'faculty', 'upload_grade', {'student': student_id, 'course': course_id, 'score': score})
    # update student cgpa
    from .student_module import compute_gpa
    compute_gpa(student_id)
    return True, 'Grade uploaded'

def modify_grade(faculty_id, student_id, course_id, new_score, reason, by_user=None):
    grades = load_json('grades.json')
    entries = grades.get(student_id, [])
    found = False
    for e in entries:
        if e.get('course') == course_id:
            e['score'] = new_score
            e['modified_by'] = faculty_id
            e['modify_reason'] = reason
            e['modified_at'] = datetime.utcnow().isoformat()+'Z'
            found = True
    if not found:
        return False, 'Grade not found'
    write_json('grades.json', grades)
    append_audit(by_user or faculty_id, 'faculty', 'modify_grade', {'student': student_id, 'course': course_id, 'new_score': new_score, 'reason': reason})
    from .student_module import compute_gpa
    compute_gpa(student_id)
    return True, 'Grade modified'
