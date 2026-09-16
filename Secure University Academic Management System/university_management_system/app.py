from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from modules.authentication import authenticate, find_user_by_email
from modules.utils import load_json, write_json, append_audit, compute_hash
from modules.student_module import register_course, compute_gpa, generate_transcript
from modules.faculty_module import upload_grade, modify_grade
from modules.admin_module import create_user, delete_user, create_course, assign_faculty
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = os.urandom(24)

def login_required(role=None):
    def decorator(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login'))
            if role and session['user']['role'] != role:
                append_audit(session['user']['id'], session['user']['role'], 'access_denied', {'endpoint': request.path})
                return "Access denied", 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

@app.route('/')
def index():
    if 'user' in session:
        role = session['user']['role']
        if role == 'student':
            return redirect(url_for('student_dashboard'))
        if role == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = authenticate(email, password)
        if user:
            session['user'] = {'id': user['id'], 'role': user['role'], 'name': user.get('name')}
            return redirect(url_for('index'))
        return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        append_audit(session['user']['id'], session['user']['role'], 'logout')
    session.clear()
    return redirect(url_for('login'))

@app.route('/student')
@login_required('student')
def student_dashboard():
    sid = session['user']['id']
    students = load_json('students.json')
    enrollments = load_json('enrollments.json').get(sid, [])
    grades = load_json('grades.json').get(sid, [])
    cgpa = students.get(sid, {}).get('cgpa', 0.0)
    return render_template('student_dashboard.html', enrollments=enrollments, grades=grades, cgpa=cgpa)

@app.route('/student/register', methods=['POST'])
@login_required('student')
def student_register():
    sid = session['user']['id']
    course = request.form.get('course')
    semester = request.form.get('semester')
    ok, msg = register_course(sid, course, semester, by_user=sid)
    return jsonify({'ok': ok, 'message': msg})

@app.route('/student/transcript')
@login_required('student')
def student_transcript():
    sid = session['user']['id']
    t = generate_transcript(sid, by_user=sid)
    return jsonify(t)

@app.route('/faculty')
@login_required('faculty')
def faculty_dashboard():
    fid = session['user']['id']
    faculty = load_json('faculty.json').get(fid, {})
    assigned = faculty.get('assigned_courses', [])
    return render_template('faculty_dashboard.html', assigned=assigned)

@app.route('/faculty/upload_grade', methods=['POST'])
@login_required('faculty')
def faculty_upload_grade():
    fid = session['user']['id']
    student = request.form.get('student')
    course = request.form.get('course')
    score = int(request.form.get('score'))
    semester = request.form.get('semester')
    ok, msg = upload_grade(fid, student, course, score, semester, by_user=fid)
    return jsonify({'ok': ok, 'message': msg})

@app.route('/admin')
@login_required('staff')
def admin_dashboard():
    return render_template('admin_dashboard.html')

@app.route('/admin/create_user', methods=['POST'])
@login_required('staff')
def admin_create_user():
    role = request.form.get('role')
    uid = request.form.get('id')
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    ok, msg = create_user(role, uid, name, email, password)
    return jsonify({'ok': ok, 'message': msg})

@app.route('/admin/create_course', methods=['POST'])
@login_required('staff')
def admin_create_course():
    cid = request.form.get('id')
    title = request.form.get('title')
    credits = int(request.form.get('credits'))
    ok, msg = create_course(cid, title, credits)
    return jsonify({'ok': ok, 'message': msg})

@app.route('/admin/assign_faculty', methods=['POST'])
@login_required('staff')
def admin_assign_faculty():
    cid = request.form.get('course')
    fid = request.form.get('faculty')
    ok, msg = assign_faculty(cid, fid)
    return jsonify({'ok': ok, 'message': msg})

@app.route('/audit_logs')
@login_required('staff')
def view_audit():
    logs = load_json('audit_logs.json')
    return jsonify(logs)

if __name__ == '__main__':
    app.run(debug=True)
