from .utils import load_json, hash_password, check_password, append_audit

def find_user_by_email(email):
    for filename, role in [('students.json', 'student'), ('faculty.json', 'faculty'), ('staff.json', 'staff')]:
        data = load_json(filename)
        for uid, rec in data.items():
            if rec.get('email') == email:
                return role, uid, rec
    return None, None, None

def authenticate(email, password):
    role, uid, rec = find_user_by_email(email)
    if not role:
        return None
    if check_password(password, rec.get('password_hash', '')):
        append_audit(uid, role, 'login', None)
        return {'role': role, 'id': uid, 'name': rec.get('name')}
    return None
