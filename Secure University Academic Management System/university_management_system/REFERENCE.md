# REFERENCE.md - Quick Command & API Reference

## 🚀 Quick Commands

### Setup & Run
```bash
# Install dependencies
pip install -r requirements.txt

# Generate sample data (creates test users)
python setup.py

# Run the application
python app.py

# Run on custom port
python app.py  # Then modify app.run(port=5001)

# Production with Gunicorn
gunicorn -w 4 app:app
```

### Data Management
```bash
# View student data
cat data/students.json

# View audit logs
cat data/audit_logs.json

# Check file integrity
sha256sum data/*.json

# Backup all data
cp -r data/ data_backup_$(date +%s)/

# Restore from backup
cp -r data_backup_xxx/* data/
```

---

## 🔐 Test Logins

| Role    | Email              | Password      |
|---------|-------------------|----------------|
| Student | ali@uni.edu       | password123   |
| Student | amina@uni.edu     | password123   |
| Faculty | sana@uni.edu      | password123   |
| Faculty | ahmed@uni.edu     | password123   |
| Admin   | admin@uni.edu     | password123   |

---

## 📡 API Endpoints

### Authentication
```
GET/POST  /login              → Login page & process
GET       /logout             → LogOut
```

### Student Routes
```
GET       /student            → View dashboard
POST      /student/register   → Register for course
GET       /student/transcript → Get transcript JSON
```

**Student Register Example:**
```bash
curl -X POST http://localhost:5000/student/register \
  -d "course=CS101&semester=2025-Fall"
```

### Faculty Routes
```
GET       /faculty            → View dashboard
POST      /faculty/upload_grade → Upload grade
```

**Faculty Upload Grade Example:**
```bash
curl -X POST http://localhost:5000/faculty/upload_grade \
  -d "student=S1001&course=CS101&score=92&semester=2025-Fall"
```

### Admin Routes
```
GET       /admin              → Admin dashboard
POST      /admin/create_user  → Create user
POST      /admin/create_course → Create course
POST      /admin/assign_faculty → Assign faculty to course
GET       /audit_logs         → View audit logs (JSON)
```

**Admin Create User Example:**
```bash
curl -X POST http://localhost:5000/admin/create_user \
  -d "role=student&id=S1003&name=Hassan&email=hassan@uni.edu&password=test123"
```

---

## 📊 JSON File Schemas

### students.json
```json
{
  "S1001": {
    "name": "Ali Khan",
    "email": "ali@uni.edu",
    "program": "BSCS",
    "password_hash": "$2b$12$...",  // bcrypt hash
    "enrolled_courses": ["CS101"],
    "cgpa": 3.45,
    "record_hash": "abc123..."     // SHA-256 hash
  }
}
```

### courses.json
```json
{
  "CS101": {
    "title": "Intro to Computer Science",
    "credits": 3,
    "prerequisites": [],
    "record_hash": "def456..."
  }
}
```

### enrollments.json
```json
{
  "S1001": [
    {
      "course": "CS101",
      "semester": "2025-Fall",
      "timestamp": "2025-09-01T00:00:00Z"
    }
  ]
}
```

### grades.json
```json
{
  "S1001": [
    {
      "course": "CS101",
      "score": 92,
      "semester": "2025-Fall",
      "graded_by": "F2001",
      "timestamp": "2025-09-15T14:30:00Z"
    }
  ]
}
```

### audit_logs.json
```json
[
  {
    "timestamp": "2025-09-15T14:30:00Z",
    "user": "S1001",
    "role": "student",
    "action": "register_course",
    "target": {
      "student": "S1001",
      "course": "CS101",
      "semester": "2025-Fall"
    }
  }
]
```

---

## 🔧 Python API Reference

### Authentication Module
```python
from modules.authentication import authenticate, find_user_by_email

# Authenticate user
user = authenticate("ali@uni.edu", "password123")
# Returns: {'role': 'student', 'id': 'S1001', 'name': 'Ali Khan'}

# Find user by email
role, uid, record = find_user_by_email("ali@uni.edu")
# Returns: ('student', 'S1001', {...user data...})
```

### Student Module
```python
from modules.student_module import (
    register_course, 
    compute_gpa, 
    generate_transcript
)

# Register for course
ok, msg = register_course("S1001", "CS101", "2025-Fall")
# Returns: (True, "Registered") or (False, "Error message")

# Recalculate GPA
cgpa = compute_gpa("S1001")
# Returns: 3.45

# Generate transcript
transcript = generate_transcript("S1001")
# Returns: transcript JSON object with hash
```

### Faculty Module
```python
from modules.faculty_module import upload_grade, modify_grade

# Upload grade
ok, msg = upload_grade("F2001", "S1001", "CS101", 92, "2025-Fall")
# Returns: (True, "Grade uploaded") or (False, "Error message")

# Modify grade
ok, msg = modify_grade("F2001", "S1001", "CS101", 95, "Arithmetic error")
# Returns: (True, "Grade modified") or (False, "Error message")
```

### Admin Module
```python
from modules.admin_module import (
    create_user,
    delete_user,
    create_course,
    assign_faculty
)

# Create user
ok, msg = create_user("student", "S1003", "Hassan", "hassan@uni.edu", "pwd")
# Returns: (True, "Created") or (False, "User exists")

# Delete user
ok, msg = delete_user("student", "S1003")
# Returns: (True, "Deleted") or (False, "Not found")

# Create course
ok, msg = create_course("CS201", "Data Structures", 3, ["CS101"])
# Returns: (True, "Course created") or (False, "Exists")

# Assign faculty
ok, msg = assign_faculty("CS101", "F2001")
# Returns: (True, "Assigned") or (False, "Faculty not found")
```

### Utilities Module
```python
from modules.utils import (
    load_json,
    write_json,
    compute_hash,
    hash_password,
    check_password,
    append_audit
)

# Load JSON file
data = load_json("students.json")  # Returns dict

# Write JSON file
write_json("students.json", data)  # Atomic write

# Compute hash
hash_val = compute_hash({"name": "Ali", "email": "ali@uni.edu"})
# Returns: "abc123def456..."

# Hash password
pwd_hash = hash_password("mypassword")
# Returns: "$2b$12$..." (bcrypt hash)

# Check password
is_valid = check_password("mypassword", pwd_hash)
# Returns: True or False

# Log audit entry
append_audit("S1001", "student", "login", None)
# Appends to audit_logs.json
```

---

## 🎯 GPA Scale

| Score Range | GPA  |
|-------------|------|
| 90-100      | 4.0  |
| 85-89       | 3.7  |
| 80-84       | 3.3  |
| 75-79       | 3.0  |
| 70-74       | 2.7  |
| 65-69       | 2.3  |
| 60-64       | 2.0  |
| 0-59        | 0.0  |

**Formula:** CGPA = Σ(GPA × credits) / Σ(credits)

---

## 📝 Useful SQL-like Operations (Manual JSON)

### Get all students
```bash
cat data/students.json | python -m json.tool
```

### Get specific student
```bash
python -c "import json; print(json.load(open('data/students.json'))['S1001'])"
```

### Add student manually
```bash
python << 'EOF'
import json
from modules.utils import hash_password, compute_hash, write_json

students = json.load(open('data/students.json'))
new_student = {
    "name": "New Student",
    "email": "new@uni.edu",
    "program": "BSCS",
    "password_hash": hash_password("password"),
    "enrolled_courses": [],
    "cgpa": 0.0
}
new_student['record_hash'] = compute_hash(new_student)
students['S9999'] = new_student
write_json('students.json', students)
print("Student added!")
EOF
```

---

## 🐛 Common Issues & Quick Fixes

| Issue | Command/Fix |
|-------|-----------|
| Port in use | `sudo lsof -i :5000` then `kill -9 <PID>` |
| Module error | `pip install -r requirements.txt` |
| Can't login | `python setup.py` |
| Invalid JSON | `python -m json.tool data/students.json` |
| Permission denied | `chmod 700 data/` |

---

## 🔍 Debugging Commands

### Check Flask app syntax
```bash
python -m py_compile app.py
```

### Test module imports
```bash
python -c "from modules import authentication; print('OK')"
```

### Validate all JSON files
```bash
for f in data/*.json; do python -m json.tool "$f" > /dev/null && echo "$f: OK" || echo "$f: ERROR"; done
```

### Monitor audit logs
```bash
tail -f data/audit_logs.json
```

### Check system resources
```bash
free -h
df -h
top
```

---

## 🚀 Performance Tips

### Optimize GPA Calculation
- Cache CGPA values in students.json
- Add indexed lookup by program/semester
- Pre-compute class averages

### Speed Up Audit Searches
- Split audit_logs.json by month: `audit_logs_2025_09.json`
- Add index file with offsets
- Implement pagination

### Database Migration Path
When data grows:
1. Start with PostgreSQL + SQLAlchemy ORM
2. Import JSON → SQL
3. Update Flask models
4. Redirect reads/writes to database
5. Keep audit trail in PostgreSQL JSON columns

---

## 📊 Reporting Commands

### List all active students
```bash
python -c "import json; s=json.load(open('data/students.json')); print(f'Total: {len(s)}'); [print(f\"{k}: {v['name']}\") for k,v in s.items()]"
```

### Average GPA
```bash
python -c "import json; s=json.load(open('data/students.json')); gpas=[v.get('cgpa',0) for v in s.values()]; print(f'Avg GPA: {sum(gpas)/len(gpas):.2f}')"
```

### Total enrollments
```bash
python -c "import json; e=json.load(open('data/enrollments.json')); print(f'Total: {sum(len(v) for v in e.values())}')"
```

### Audit log statistics
```bash
python -c "import json; logs=json.load(open('data/audit_logs.json')); actions={l['action']:logs.count(l) for l in logs}; [print(f\"{a}: {actions[a]}\") for a,c in actions.items()]"
```

---

## 🔒 Security Checklist

### Before Production
- [ ] `app.secret_key` changed
- [ ] `debug=False`
- [ ] HTTPS enabled
- [ ] File permissions: `chmod 700 data/`
- [ ] Backups enabled
- [ ] Monitoring setup
- [ ] All test data removed
- [ ] Admin credentials changed

### Ongoing
- [ ] Review audit logs daily
- [ ] Monitor error logs
- [ ] Verify backups
- [ ] Update dependencies monthly
- [ ] Run security scans quarterly

---

## 📚 Documentation Map

| Document | Purpose |
|----------|---------|
| INDEX.md | Navigation guide |
| QUICKSTART.md | 5-minute setup |
| README.md | Full documentation |
| TESTING.md | Test scenarios |
| DEPLOYMENT.md | Production deployment |
| PROJECT_SUMMARY.md | Requirements checklist |
| REFERENCE.md | This quick reference |

---

**Bookmark this page for quick access to commands and APIs!** 📌
