# QUICKSTART.md - 5 Minute Setup

## 🚀 In 5 Minutes

### Step 1: Install Dependencies (1 min)
```bash
pip install -r requirements.txt
```

### Step 2: Generate Test Data (1 min)
```bash
python setup.py
```

### Step 3: Start Server (instantly)
```bash
python app.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

### Step 5: Login!

**Test Logins (password: `password123` for all):**

| Role    | Email              |
|---------|-------------------|
| Student | ali@uni.edu       |
| Faculty | sana@uni.edu      |
| Admin   | admin@uni.edu     |

---

## 📚 What You Just Deployed

A **secure, offline university management system** with:

✅ **3 Roles** with access control
- Students: Register courses, view grades, download transcripts
- Faculty: Upload/modify grades, see assigned courses
- Admin: Manage users & courses, view audit logs

✅ **Security Features**
- Bcrypt password hashing
- Role-based access control on every endpoint
- SHA-256 hashing for data integrity
- Comprehensive audit logging

✅ **Data Validation**
- Prerequisite enforcement
- Credit limit (max 18/semester)
- Duplicate course prevention
- GPA auto-calculation

✅ **Zero Dependencies**
- No database (JSON files only)
- No external APIs
- No cloud services
- Pure Python + Flask

---

## 📁 File Structure

```
university_management_system/
├── app.py                  # Flask server
├── setup.py               # Initialize test data
├── /modules/              # Business logic
│   ├── utils.py          # Hashing, JSON I/O, audit
│   ├── authentication.py  # Login
│   ├── student_module.py  # Course registration, GPA
│   ├── faculty_module.py  # Grade management
│   └── admin_module.py    # User/course management
├── /templates/            # HTML pages
├── /static/               # CSS & JavaScript
└── /data/                 # JSON data files
    ├── students.json
    ├── faculty.json
    ├── staff.json
    ├── courses.json
    ├── enrollments.json
    ├── grades.json
    ├── transcripts.json
    └── audit_logs.json
```

---

## 🧪 Try These Features

### As Student (ali@uni.edu):
1. View enrolled courses (already has CS101)
2. Try registering for CS201 (blocked - needs CS101 prerequisite)
3. Generate transcript
4. Logout

### As Admin (admin@uni.edu):
1. Create new student: S1002, "Jane Doe", jane@uni.edu
2. Create new course: CS202, "Web Dev", 3 credits
3. Assign faculty F2001 to course
4. View audit logs (shows all actions)

### As Faculty (sana@uni.edu):
1. See assigned courses (CS101)
2. Upload grade for S1001 in CS101: 95
3. Modify it with reason: "Recalculation"

### Back to Student:
1. Check CGPA (score 95 = 4.0 GPA, so CGPA ≈ 4.0)
2. Verify grade appears in list

---

## 🎯 Key Design Decisions

| Feature              | Implementation          |
|----------------------|-------------------------|
| Database             | JSON files (`/data/`)    |
| Password Security    | bcrypt hashing           |
| Data Integrity       | SHA-256 record hashing   |
| Access Control       | Role-based (3 roles)     |
| Audit Trail          | append-only JSON log     |
| Session Management   | Flask secure sessions    |
| API Framework        | Flask (lightweight)      |
| Frontend             | Plain HTML/CSS/JS        |

---

## ⚠️ Important Notes

🔒 **Security:**
- All passwords hashed with bcrypt
- Every action logged to audit trail
- Role checks on every endpoint
- Session-based authentication

📊 **Data:**
- GPA calculated: (grade_points × credits) / total_credits
- Grades: 90+ = 4.0, 85+ = 3.7, 80+ = 3.3, etc.
- Max 18 credits per semester enforced
- Prerequisites checked on registration

🔧 **Extending:**
- Add new roles: Create module, add route, create template
- Add features: Create function, add route, add UI
- Modify GPA scale: Edit `GRADE_POINTS` in `student_module.py`

---

## 🐛 Troubleshooting

| Issue | Fix |
|-------|-----|
| Port 5000 in use | Change `port=5000` in app.py to different port |
| Can't login | Run `python setup.py` first to generate data |
| 404 on routes | Ensure `/templates/` exists with .html files |
| Permission denied on /data/ | Check file permissions, run as admin if needed |
| Grades not uploading | Faculty must be assigned to course first |

---

## 📖 Next Steps

1. **Read** [README.md](README.md) - Full feature documentation
2. **Test** [TESTING.md](TESTING.md) - Detailed test scenarios
3. **Customize** - Modify templates, add more courses, create users
4. **Deploy** - Use Gunicorn + HTTPS for production
5. **Backup** - Regularly backup `/data/` directory

---

## 🏗️ Architecture

```
Browser (HTML) ──┐
                 │ HTTP
          ┌──────▼──────┐
          │ Flask App   │
          │ (app.py)    │
          └──────┬──────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌────────┐  ┌─────────┐
│Student │  │Faculty │  │ Admin   │
│Module  │  │Module  │  │ Module  │
└────┬───┘  └───┬────┘  └────┬────┘
     └──────────┼────────────┘
              Utils (hashing, JSON I/O, audit)
                    │
              ┌─────▼─────┐
              │ JSON Files│
              │ (in /data)│
              └───────────┘
```

---

**Happy Academic Management! 🎓**
