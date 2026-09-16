from .utils import load_json, write_json, compute_hash, hash_password, append_audit
from datetime import datetime

def _role_filename(role):
    mapping = {
        'student': 'students.json',
        'faculty': 'faculty.json',
        'staff': 'staff.json',
        'other': 'other.json'
    }
    return mapping.get(role, f'{role}.json')


def create_user(role, uid, name, email, password):
    filename = _role_filename(role)
    data = load_json(filename)
    if uid in data:
        return False, 'User exists'
    rec = {'name': name, 'email': email, 'password_hash': hash_password(password)}
    rec['record_hash'] = compute_hash(rec)
    data[uid] = rec
    write_json(filename, data)
    append_audit('system', 'staff', 'create_user', {'role': role, 'id': uid})
    return True, 'Created'

def delete_user(role, uid):
    filename = _role_filename(role)
    data = load_json(filename)
    if uid not in data:
        return False, 'Not found'
    del data[uid]
    write_json(filename, data)
    append_audit('system', 'staff', 'delete_user', {'role': role, 'id': uid})
    return True, 'Deleted'

def create_course(course_id, title, credits, prerequisites=None):
    courses = load_json('courses.json')
    if course_id in courses:
        return False, 'Exists'
    courses[course_id] = {'title': title, 'credits': credits, 'prerequisites': prerequisites or [], 'record_hash': ''}
    courses[course_id]['record_hash'] = compute_hash(courses[course_id])
    write_json('courses.json', courses)
    append_audit('system', 'staff', 'create_course', {'course': course_id})
    return True, 'Course created'

def assign_faculty(course_id, faculty_id):
    faculty = load_json('faculty.json')
    if faculty_id not in faculty:
        return False, 'Faculty not found'
    faculty[faculty_id].setdefault('assigned_courses', [])
    if course_id not in faculty[faculty_id]['assigned_courses']:
        faculty[faculty_id]['assigned_courses'].append(course_id)
    write_json('faculty.json', faculty)
    append_audit('system', 'staff', 'assign_faculty', {'course': course_id, 'faculty': faculty_id})
    return True, 'Assigned'
