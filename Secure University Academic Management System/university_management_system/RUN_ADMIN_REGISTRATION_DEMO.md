# Admin Registration Demo & Usage

## ✅ What's Working

The admin-only registration system is **fully functional**. Administrators can now register students, faculty, staff, and other roles directly from the admin dashboard.

### Verified Features

1. **Admin Dashboard Enhanced**
   - Role selection dropdown with options: `student`, `faculty`, `staff`, `other`
   - Clearer labels and required fields
   - Form submits to `/admin/create_user` endpoint (protected by `@login_required('staff')`)

2. **User Creation**
   - Creates users in the correct role-specific JSON files (e.g., `students.json`, `faculty.json`)
   - Generates bcrypt-hashed passwords
   - Computes and stores `record_hash` for tamper detection
   - Returns success/failure messages

3. **Audit Logging**
   - Every user creation is logged with timestamp, admin ID, role, action, and target user ID
   - Append-only JSON file ensures audit trail integrity

---

## 🚀 Quick Start

### 1. Start the Server
```powershell
cd "d:\Projects\Secure University Academic Management System"
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Navigate to app directory
cd university_management_system

# Run Flask app
python app.py
```

The server starts on `http://localhost:5000` by default.

### 2. Log In as Admin
- **Email:** `admin@uni.edu`
- **Password:** `password123`
- **Role:** Staff (admin)

### 3. Register Users
Once logged in, you'll see the **"Register User (Admin only)"** form with:
- **Role dropdown** to select: Student, Faculty, Staff, or Other
- **User ID** (e.g., `S2001` for student, `F3001` for faculty)
- **Name** (full name)
- **Email** (unique email)
- **Password** (stored hashed)

Fill in the form and click **"Register"** to create the user.

---

## 📋 Test Users (Pre-Populated)

### Students
- **ID:** `S1001` | **Email:** `ali@uni.edu` | **Name:** Ali Khan
- **ID:** `S1002` | **Email:** `amina@uni.edu` | **Name:** Amina Ahmed

### Faculty
- **ID:** `F2001` | **Email:** `sana@uni.edu` | **Name:** Dr. Sana Ahmad
- **ID:** `F2002` | **Email:** `ahmed@uni.edu` | **Name:** Dr. Ahmed Hassan

### Admin/Staff
- **ID:** `A3001` | **Email:** `admin@uni.edu` | **Name:** Admin User

**All test users use password:** `password123`

---

## 🔒 Security Highlights

- **Password Hashing:** bcrypt with salt (not stored in plain text)
- **Role-Based Access Control (RBAC):** Only `staff` role can create users
- **Audit Trail:** Every action logged with user, timestamp, and details
- **Record Hash:** Tamper detection via SHA-256 hash of user record (computed at creation)
- **Data Integrity:** Atomic writes (temp file + replace) prevent partial writes

---

## 📊 Verifying Registration

### Check Newly Created Users in JSON Files

**Students:**
```bash
cat .\data\students.json | jq '.S9999'
```

**Faculty:**
```bash
cat .\data\faculty.json | jq '.F9999'
```

**Audit Log:**
```bash
cat .\data\audit_logs.json | jq '.[-1]'  # Last entry
```

---

## 📝 Notes

- When a user is created, the response shows `"ok": true` and a success message
- If a user ID already exists, creation fails with `"ok": false` and error message
- Audit logs can be viewed from the admin dashboard: click **"View Audit Logs"**
- The system supports creating unlimited users across all four roles

---

## 🧪 Smoke Test (What Was Verified)

✅ Admin login succeeds  
✅ Create student via admin form → written to `students.json`  
✅ User record includes bcrypt hash and record_hash  
✅ Audit log appended with `create_user` action  
✅ Form reloads on success (redirect to login for new user to sign in)  

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Access denied" on register page | Make sure you're logged in as `admin@uni.edu` (role: `staff`) |
| "User exists" message | That user ID is already in the system; try a different ID |
| Flask crashes on startup | Check `requirements.txt` installed: `pip install -r requirements.txt` |
| Can't reach localhost:5000 | Ensure Flask is running (`python app.py`) and try `http://127.0.0.1:5000` |

