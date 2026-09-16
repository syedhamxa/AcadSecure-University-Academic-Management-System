# START HERE - University Academic Management System

Welcome! This is your **secure, offline, role-based university management system**.

## 🎯 Quick Navigation

### 🚀 Want to Get Started Immediately?
→ **Read [QUICKSTART.md](QUICKSTART.md)** (5 minutes)

### 📚 Want Full Documentation?
→ **Read [README.md](README.md)** (all features explained)

### 🧪 Want to Test the System?
→ **Read [TESTING.md](TESTING.md)** (8 detailed test scenarios)

### 📊 Want Project Overview?
→ **Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** (complete requirements fulfillment)

---

## 🚀 Quick Setup (Copy & Paste)

### Step 1: Install
```bash
pip install -r requirements.txt
```

### Step 2: Generate Data
```bash
python setup.py
```

### Step 3: Run
```bash
python app.py
```

### Step 4: Open Browser
```
http://localhost:5000
```

### Step 5: Login!
- **Student:** ali@uni.edu / password123
- **Faculty:** sana@uni.edu / password123
- **Admin:** admin@uni.edu / password123

---

## 📁 Project Structure

```
university_management_system/
├── 📖 README.md              ← Full documentation
├── 🚀 QUICKSTART.md          ← 5-minute setup
├── 🧪 TESTING.md             ← Test scenarios
├── 📊 PROJECT_SUMMARY.md     ← Requirements checklist
├── 📄 INDEX.md (this file)
│
├── app.py                    ← Flask server (main entry point)
├── setup.py                  ← Generate sample data
├── requirements.txt          ← Dependencies: Flask, bcrypt
│
├── modules/                  ← Business logic
│   ├── utils.py             ← Hashing, JSON I/O
│   ├── authentication.py    ← Login system
│   ├── student_module.py    ← Student features
│   ├── faculty_module.py    ← Faculty features
│   └── admin_module.py      ← Admin features
│
├── templates/               ← HTML pages
│   ├── login.html
│   ├── student_dashboard.html
│   ├── faculty_dashboard.html
│   └── admin_dashboard.html
│
├── static/                  ← CSS & JavaScript
│   ├── styles.css
│   └── scripts.js
│
└── data/                    ← JSON data files (created by setup.py)
    ├── students.json        ← Student data
    ├── faculty.json         ← Faculty data
    ├── staff.json           ← Admin data
    ├── courses.json         ← Course catalog
    ├── enrollments.json     ← Registrations
    ├── grades.json          ← Grades
    ├── transcripts.json     ← Transcripts
    └── audit_logs.json      ← Audit trail
```

---

## ✨ Key Features

### 👨‍🎓 Student Features
- Register for courses (with prerequisites)
- View enrolled courses and grades
- Track GPA in real-time
- Download transcripts
- View personal audit logs

### 👨‍🏫 Faculty Features
- View assigned courses
- Upload student grades
- Modify grades with audit trail
- See grade statistics

### 🔐 Admin Features
- Manage users (create/delete)
- Create courses and prerequisites
- Assign faculty to courses
- View system-wide audit logs

---

## 🔒 Security Features

✅ **Bcrypt Password Hashing** - Industry standard password security  
✅ **SHA-256 Data Hashing** - Detect any unauthorized changes  
✅ **Role-Based Access Control** - Students, Faculty, Admin  
✅ **Complete Audit Logging** - Every action tracked  
✅ **Offline Only** - No external APIs or cloud services  
✅ **JSON File Storage** - No database required  

---

## 📖 Documentation Guide

| Document | Purpose | Read Time |
|----------|---------|-----------|
| [QUICKSTART.md](QUICKSTART.md) | Get running in 5 minutes | 5 min |
| [README.md](README.md) | Complete feature reference | 20 min |
| [TESTING.md](TESTING.md) | Test scenarios & verification | 30 min |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Requirements fulfillment | 15 min |
| [INDEX.md](INDEX.md) | This navigation guide | 5 min |

---

## 🎯 Common Tasks

### I Want to...

**Start the application**
```bash
python app.py
# Then visit http://localhost:5000
```

**Generate test data with sample users**
```bash
python setup.py
# Creates 2 students, 2 faculty, 1 admin with password "password123"
```

**Create a new student**
1. Login as admin (admin@uni.edu)
2. Fill "Create User" form
3. Role: `student`, ID: `S1003`, etc.

**Register a course**
1. Login as student
2. Enter course ID (e.g., CS101)
3. Enter semester (e.g., 2025-Fall)
4. Click Register

**Upload a grade**
1. Login as faculty
2. Enter student ID (e.g., S1001)
3. Enter course ID (e.g., CS101)
4. Enter score (0-100)
5. Click Upload

**View audit logs**
1. Login as admin
2. Click "View Audit Logs"
3. See JSON viewer with all actions

**Check transcript**
1. Login as student
2. Click "Generate Transcript"
3. Opens JSON in new window

---

## ⚙️ Configuration

### Change Server Port
Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Change Password
Edit `setup.py`:
```python
test_pwd_hash = hash_password("YOUR_NEW_PASSWORD")
```

### Modify GPA Scale
Edit `modules/student_module.py`:
```python
GRADE_POINTS = [(90,4.0), (85,3.7), ...]  # Edit this
```

---

## 🧪 Testing

### Quick Test
1. Run `python setup.py` to generate data
2. Run `python app.py` to start server
3. Login as ali@uni.edu / password123
4. Try all features

### Full Testing
See [TESTING.md](TESTING.md) for:
- 8 detailed test scenarios
- Data integrity tests
- Performance tests
- Negative tests (expected failures)

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **ImportError: Flask** | Run `pip install -r requirements.txt` |
| **Port 5000 in use** | Change port in app.py or kill process |
| **Can't login** | Run `python setup.py` to generate data |
| **404 on routes** | Ensure `/templates/` and `/static/` exist |
| **Grades not showing** | Faculty must be assigned to course first |

See [README.md#Troubleshooting](README.md) for more solutions.

---

## 🚀 Production Deployment

### Before Going Live
1. [ ] Change `app.secret_key` to random value
2. [ ] Set `debug=False` in app.py
3. [ ] Use production WSGI server (Gunicorn)
4. [ ] Enable HTTPS/SSL
5. [ ] Set up automated backups of `/data/`
6. [ ] Review security checklist in PROJECT_SUMMARY.md

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

---

## 📊 What's Included

✅ **Complete Python/Flask Backend** - All business logic  
✅ **Responsive HTML/CSS/JS Frontend** - Modern UI  
✅ **Sample Data Generator** - Ready-to-test credentials  
✅ **Comprehensive Documentation** - 4 detailed guides  
✅ **Security Implementation** - Production-grade crypto  
✅ **Audit System** - Full compliance logging  
✅ **Test Scenarios** - 8 complete test plans  

---

## ❓ FAQ

**Q: Do I need a database?**  
A: No! Everything is stored in JSON files. No database setup required.

**Q: Do I need to install anything besides Python?**  
A: Just Flask and bcrypt - run `pip install -r requirements.txt`

**Q: Is this secure?**  
A: Yes! Uses bcrypt for passwords and SHA-256 for data integrity. See [README.md](README.md) for details.

**Q: Can I use this in production?**  
A: Yes, but read the Production Deployment section first and follow the checklist.

**Q: How many users can it handle?**  
A: Recommended for up to 10,000 students. For larger deployments, migrate to a database.

**Q: Can I modify the code?**  
A: Absolutely! All code is well-documented and modular. See each .py file for comments.

---

## 📞 Support

- **Setup Issues?** → Check [QUICKSTART.md](QUICKSTART.md)
- **Feature Questions?** → Check [README.md](README.md)
- **Testing Questions?** → Check [TESTING.md](TESTING.md)
- **Requirements Met?** → Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)

---

## 📋 Next Steps

### For Immediate Use
1. Run `python setup.py`
2. Run `python app.py`
3. Visit http://localhost:5000
4. Login with test credentials

### For Learning
1. Read [README.md](README.md) to understand features
2. Review [modules/](modules/) code structure
3. Run test scenarios from [TESTING.md](TESTING.md)
4. Customize as needed

### For Production
1. Review [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) security checklist
2. Configure `/data/` backup strategy
3. Set up production HTTPS
4. Deploy with Gunicorn

---

## 🎓 Educational Resources

This system demonstrates:
- ✓ Python web development (Flask)
- ✓ RESTful API design
- ✓ Role-based access control (RBAC)
- ✓ Data persistence (JSON)
- ✓ Cryptography (bcrypt, SHA-256)
- ✓ Session management
- ✓ Audit logging
- ✓ Frontend/backend integration
- ✓ Security best practices

---

## 📄 License & Attribution

Built as an educational and production-ready system for university academic management.

**Principles:**
- No database required
- Completely offline
- Security-first design
- Easy to extend

---

## ✅ Verification Checklist

Before deployment, verify:

- [ ] All 3 roles (student, faculty, admin) login successfully
- [ ] Course registration validates prerequisites
- [ ] Credit limit enforced (max 18)
- [ ] CGPA calculated correctly
- [ ] Transcript generated with hash
- [ ] Role-based access control working
- [ ] All actions logged in audit trail
- [ ] Faculty can only grade assigned courses
- [ ] Students see only own data
- [ ] File permissions correct on `/data/`

---

**Ready to manage your university?** 🚀

→ **Start with [QUICKSTART.md](QUICKSTART.md) for instant setup!**
