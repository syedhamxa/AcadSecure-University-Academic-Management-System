# AcadSecure-University-Academic-Management-System
A secure academic management platform that handles course registration, GPA tracking, and transcript generation for students and faculty. Includes role-based access control and data integrity validation.
# University Academic Management System - README

## Overview

A **secure, offline, role-based university academic management system** built entirely in Python & Flask with JSON file storage. Perfect for educational institutions seeking a lightweight alternative to heavy ERP systems.

### Key Features
✅ **3 Roles** - Students, Faculty, Admin  
✅ **Secure** - Bcrypt passwords, SHA-256 hashing, audit logs  
✅ **Offline** - Zero database, zero external APIs  
✅ **RBAC** - Role-based access control on every endpoint  
✅ **GPA Calculation** - Automatic CGPA computation  
✅ **Prerequisite Enforcement** - Course prerequisites validated  
✅ **Transcripts** - Secure, hash-verified transcripts  
✅ **Audit Trail** - Complete action log for compliance  

---

## Quick Start (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Sample Data
```bash
python setup.py
```

**Output:**
```
✓ Created students.json
✓ Created faculty.json
✓ Created staff.json
✓ Created courses.json
✓ Created enrollments.json
✓ Created grades.json
✓ Created transcripts.json
✓ Created audit_logs.json

✅ SETUP COMPLETE!

Test Credentials (password: 'password123'):
👨‍🎓 Student: ali@uni.edu
👨‍🏫 Faculty: sana@uni.edu
🔐 Admin: admin@uni.edu
```

### 3. Start Flask Server
```bash
python app.py
```

### 4. Open Browser
```
http://localhost:5000
```

---

##Features by Role

### 👨‍🎓 Student Dashboard
- **View Enrollments** - See all registered courses per semester
- **Check Grades** - View scores for all courses
- **Track CGPA** - Real-time GPA calculation
- **Download Transcript** - Secure, hash-verified transcript as JSON
- **Register Courses** - With prerequisite and credit limit validation
- **View Audit Log** - Personal action history

### 👨‍🏫 Faculty Dashboard
- **View Assigned Courses** - See all courses assigned
- **Upload Grades** - Enter student scores (100% audit logged)
- **Modify Grades** - Update scores with reason logging
- **View Analytics** - Class performance statistics
- **Access Logs** - See grading audit trail

### 🔐 Admin/Staff Dashboard
- **User Management** - Create/delete students, faculty, staff
- **Course Management** - Create courses with credits & prerequisites
- **Assign Faculty** - Assign instructors to courses
- **View Audit Logs** - System-wide action history
- **Lock Semesters** - Prevent course registration (optional)
- **Data Integrity** - Verify record hashes, detect tampering

---

## Project Structure

```
university_management_system/
├── app.py                    # Flask web server
├── setup.py                  # Sample data generator
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── TESTING.md               # Test scenarios
├── QUICKSTART.md            # 5-min quickstart
│
├── /modules/
│   ├── __init__.py
│   ├── utils.py             # Hashing, JSON I/O, audit logging
│   ├── authentication.py    # Login & credential verification
│   ├── student_module.py    # Registration, GPA, transcripts
│   ├── faculty_module.py    # Grade upload & modification
│   └── admin_module.py      # User & course management
│
├── /templates/
│   ├── login.html
│   ├── student_dashboard.html
│   ├── faculty_dashboard.html
│   └── admin_dashboard.html
│
├── /static/
│   ├── styles.css
│   └── scripts.js
│
└── /data/                   # JSON data files (created by setup.py)
    ├── students.json        # Student profiles, enrollments, CGPA
    ├── faculty.json         # Faculty profiles, assigned courses
    ├── staff.json           # Admin/staff profiles
    ├── courses.json         # Course catalog
    ├── enrollments.json     # Course registrations
    ├── grades.json          # Student grades
    ├── transcripts.json     # Generated transcripts (immutable)
    └── audit_logs.json      # Full action audit trail
```

---

## JSON Data Schema

### students.json
```json
{
  "S1001": {
    "name": "Ali Khan",
    "email": "ali@uni.edu",
    "program": "BSCS",
    "password_hash": "$2b$12$bcrypt_hash",
    "enrolled_courses": ["CS101"],
    "cgpa": 3.45,
    "record_hash": "sha256_hex_string"
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
    "record_hash": "sha256_hex_string"
  }
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
    "target": {"student": "S1001", "course": "CS101", "semester": "2025-Fall"}
  }
]
```

---

## Security Architecture

### 🔒 Password Security
- **Algorithm:** bcrypt with auto-generated salt
- **Storage:** Hashed only, never plain text
- **Verification:** `bcrypt.checkpw()` on login

### 🔐 Data Integrity
- **Method:** SHA-256 record hashing
- **Coverage:** All student, faculty, staff, and course records
- **Validation:** Hashes verified on data load
- **Immutability:** Transcripts & grade history immutable

### 📋 Audit Logging
Every action records:
- **Timestamp** - ISO 8601 UTC timestamp
- **User** - User ID performing action
- **Role** - Student/Faculty/Staff
- **Action** - What was done (login, register, upload_grade, etc.)
- **Target** - Affected data as JSON object

Examples:
```json
{"timestamp":"2025-09-15T14:30:00Z","user":"S1001","role":"student","action":"login","target":null}
{"timestamp":"2025-09-15T14:31:00Z","user":"S1001","role":"student","action":"register_course","target":{"student":"S1001","course":"CS101"}}
{"timestamp":"2025-09-15T14:31:05Z","user":"F2001","role":"faculty","action":"upload_grade","target":{"student":"S1001","course":"CS101","score":92}}
```

### 🛡️ RBAC Enforcement
1. Check session: is user logged in?
2. Check role: does user have permission?
3. Check ownership: can user access this data?
4. Log action: record in audit trail
5. Execute: perform operation

Every endpoint implements this pattern.

---

## Business Logic

### Course Registration Validation
Student must satisfy **all** conditions:
- [ ] Student exists
- [ ] Course exists
- [ ] Not already enrolled in course/semester
- [ ] Completed prerequisite courses (60+ score)
- [ ] Total credits ≤ 18 per semester

### GPA Calculation
```
CGPA = Σ(grade_points × credits) / Σ(credits)
```

Grade scale:
- 90-100 → 4.0
- 85-89 → 3.7
- 80-84 → 3.3
- 75-79 → 3.0
- 70-74 → 2.7
- 65-69 → 2.3
- 60-64 → 2.0
- 0-59 → 0.0

### Faculty Authorization
- Faculty can only upload grades for **assigned courses**
- Can only see **enrolled students**
- All modifications logged with old/new values

---

## API Endpoints

### Authentication
```
GET/POST  /login          Login page & credentials check
GET       /logout         Clear session
```

### Student Routes
```
GET       /student        Student dashboard (enrollments, grades, CGPA)
POST      /student/register         Register for course
GET       /student/transcript       Generate & download transcript
```

### Faculty Routes
```
GET       /faculty        Faculty dashboard (assigned courses)
POST      /faculty/upload_grade     Upload student grade
POST      /faculty/modify_grade     Update existing grade (optional)
```

### Admin Routes
```
GET       /admin          Admin dashboard
POST      /admin/create_user        Create new user (any role)
POST      /admin/create_course      Create new course
POST      /admin/assign_faculty     Assign faculty to course
GET       /audit_logs     View system audit log
```

---

## Running Tests

Detailed test scenarios available in [TESTING.md](TESTING.md).

### Quick Test Flow
1. **Login as student** - ali@uni.edu / password123
2. **Register course** - Try CS201 (should fail - prerequisite)
3. **Login as faculty** - sana@uni.edu / password123
4. **Upload grade** - S1001 in CS101: 95
5. **Back to student** - CGPA updated, grade visible
6. **Login as admin** - admin@uni.edu / password123
7. **View audit logs** - See all actions recorded

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **ImportError: Flask** | Run `pip install -r requirements.txt` |
| **Port 5000 in use** | Change `port=5000` in app.py or kill process |
| **Can't login** | Run `python setup.py` to generate test data |
| **404 on /student** | Ensure `/templates/` exists with .html files |
| **Data not saving** | Check `/data/` folder permissions |
| **Grades not visible** | Faculty must be assigned to course first |

---

## Extending the System

### Add New Role
1. Create JSON file: `/data/newrole.json`
2. Add module: `/modules/newrole_module.py`
3. Update `authentication.py` - add to find_user_by_email()
4. Add route in `app.py` - create `@app.route('/newrole')`
5. Create template: `/templates/newrole_dashboard.html`

### Add New Feature
1. Create function in appropriate module
2. Add route in `app.py`
3. Add form in template
4. Add event handler in `scripts.js`
5. Test & verify in audit logs

### Modify GPA Scale
Edit `GRADE_POINTS` in `/modules/student_module.py`:
```python
GRADE_POINTS = [(90,4.0), (85,3.7), (80,3.3), ...]
```

---

## Production Checklist

- [ ] Change `app.secret_key` to fixed value
- [ ] Set `debug=False` in `app.py`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Enable HTTPS/SSL
- [ ] Backup `/data/` directory regularly
- [ ] Restrict file permissions: `chmod 700 data/`
- [ ] Monitor audit logs for anomalies
- [ ] Document disaster recovery procedure
- [ ] Review password policies
- [ ] Set up automated backups

---

## Performance Notes

**Scalability Limits (JSON storage):**
- ~10,000 students: Excellent performance
- ~50,000 students: Good performance
- ~100,000+ students: Consider migration to database

**Optimization Tips:**
- Implement pagination for large audit logs
- Cache CGPA calculations
- Consider Redis for session management
- Add search indexing for large datasets

---

## Support & Issues

For questions or issues:
1. Check [TESTING.md](TESTING.md) for test scenarios
2. Review audit logs for error context
3. Verify JSON file format and permissions
4. Test with sample credentials from setup.py

---

## License & Compliance

- **GDPR Ready:** Minimal PII, role-based visibility
- **Audit Trail:** Complete action history for compliance
- **Data Integrity:** Hash verification detects tampering
- **No Data Transmission:** Everything stays local

---

## Architecture Diagram

```
┌─────────────────────────────────┐
│      Browser (HTML/CSS/JS)      │
│                                 │
│  Login  │  Student  │ Faculty   │
│         │ Dashboard │ Dashboard │
└────────────────┬────────────────┘
                 │ HTTP
         ┌───────▼────────┐
         │  Flask App     │
         │  (routes,      │
         │   auth,        │
         │   RBAC)        │
         └───────┬────────┘
                 │ Import
    ┌────────────┼─────────────────┐
    │            │                 │
    ▼            ▼                 ▼
┌─────────┐ ┌──────────┐ ┌──────────────┐
│ Student │ │ Faculty  │ │ Admin Module │
│ Module  │ │ Module   │ │              │
└────┬────┘ └────┬─────┘ └──────┬───────┘
     │            │              │
     └────────────┼──────────────┘
                  │ Read/Write
          ┌───────▼────────┐
          │  Utils Module  │
          │  - Hashing     │
          │  - JSON I/O    │
          │  - Audit Log   │
          └───────┬────────┘
                  │
          ┌───────▼────────┐
          │  JSON Files    │
          │  /data/        │
          │  - students.   │
          │  - grades.     │
          │  - audit_logs. │
          └────────────────┘
```

---

**Made with ❤️ for secure, offline academic management.**
