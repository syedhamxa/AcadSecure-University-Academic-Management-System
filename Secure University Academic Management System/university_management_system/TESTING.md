# TESTING.md - Complete Test Guide

## Getting Started with Testing

### Generate Test Data
Before testing, run the setup script once:

```bash
python setup.py
```

This creates sample users with password `password123` and courses:

**Test Users:**
- Student: `S1001` (ali@uni.edu), `S1002` (amina@uni.edu)
- Faculty: `F2001` (sana@uni.edu), `F2002` (ahmed@uni.edu)
- Admin: `A3001` (admin@uni.edu)

**Test Courses:**
- CS101 (Intro to CS, 3 cr, no prereq)
- CS201 (Data Structures, 3 cr, requires CS101)
- MATH101 (Calculus I, 4 cr, no prereq)

---

## Test Scenario 1: Student Registration & Grades

**Objective:** Test course registration with prerequisites and GPA calculation.

**Steps:**

1. **Login as Student S1001**
   ```
   Email: ali@uni.edu
   Password: password123
   ```
   ✓ Should see dashboard with CS101 enrolled (2025-Fall)
   ✓ CGPA: 0.0 (no grades yet)

2. **Try to Register for CS201**
   - Input: `CS201`, Semester: `2025-Fall`
   - Click Register
   - ✓ Should FAIL with: "Missing prerequisites: ['CS101']"

3. **Login as Faculty F2001**
   ```
   Email: sana@uni.edu
   Password: password123
   ```
   ✓ Should see CS101 in assigned courses

4. **Upload Grade for S1001**
   - Student ID: `S1001`
   - Course ID: `CS101`
   - Score: `88`
   - Semester: `2025-Fall`
   - Click Upload
   - ✓ Should show "Grade uploaded"

5. **Verify CGPA Updated**
   - Logout
   - Login as S1001 again
   - ✓ CGPA should now be 3.7 (88 score = 3.7 GPA)
   - ✓ Grade should appear: "CS101: 88"

6. **Now S1001 Can Register for CS201**
   - In student dashboard, register: CS201, 2025-Fall
   - ✓ Should succeed (prerequisite now met)

---

## Test Scenario 2: Credit Limit Enforcement

**Objective:** Verify max 18 credits per semester rule.

**Steps:**

1. **Admin Creates Courses**
   - Login as admin (admin@uni.edu)
   - Create courses:
     - `PHYS101`: Physics I, 4 credits
     - `CHEM101`: Chemistry I, 4 credits
   - ✓ Courses created

2. **Assign to Faculty**
   - Assign PHYS101 to F2001
   - Assign CHEM101 to F2001
   - ✓ Both assigned

3. **Register Student S1002 for Courses**
   - Login as S1002 (amina@uni.edu)
   - Register:
     - `CS101` (3 cr) - ✓ OK (total: 3)
     - `MATH101` (4 cr) - ✓ OK (total: 7)
     - `PHYS101` (4 cr) - ✓ OK (total: 11)
     - `CHEM101` (4 cr) - ✓ OK (total: 15)
   - Now register:
     - `CS201` (3 cr) - ✓ Should FAIL (would be 18+3)

4. **Verify Log**
   - Login as admin
   - View audit logs
   - ✓ Should see 4 successful registrations and 1 failed attempt

---

## Test Scenario 3: Access Control (RBAC)

**Objective:** Verify role-based access enforcement.

**Steps:**

1. **Student Cannot Access Faculty Routes**
   - Login as student
   - Try to manually visit `/faculty` URL
   - ✓ Should show "Access denied" (403)

2. **Student Cannot See Other Students' Grades**
   - Login as S1001
   - Try to manually edit URL to access S1002's data
   - ✓ Should show "Access denied"

3. **Faculty Cannot Access Admin Routes**
   - Login as faculty
   - Try to visit `/admin` URL
   - ✓ Should show "Access denied"

4. **Check Audit Logs for Access Denials**
   - Login as admin
   - View audit logs
   - ✓ Should see `access_denied` entries with attempted endpoints

---

## Test Scenario 4: Unauthorized Grade Upload

**Objective:** Verify faculty can only grade assigned courses.

**Steps:**

1. **F2001 Assigned to CS101 Only**
   - Login as admin
   - Verify F2001 only assigned to CS101
   - ✓ Confirmed

2. **F2001 Tries to Grade CS201**
   - Login as F2001
   - Try to upload grade:
     - Student: S1001
     - Course: CS201
     - Score: 95
   - ✓ Should FAIL: "Not authorized for this course"

3. **F2001 Can Grade CS101**
   - Upload grade for CS101 (assigned course)
   - ✓ Should succeed

---

## Test Scenario 5: User Management

**Objective:** Test admin user creation and management.

**Steps:**

1. **Create New Student**
   - Login as admin
   - Create User form:
     - Role: `student`
     - ID: `S1003`
     - Name: Hassan Ali
     - Email: hassan@uni.edu
     - Password: test_password
   - ✓ Should show "Created"

2. **Login as New Student**
   - Logout
   - Email: `hassan@uni.edu`, Password: `test_password`
   - ✓ Should login successfully
   - ✓ Dashboard empty (no enrollments/grades)

3. **Create New Faculty**
   - Login as admin
   - Create User:
     - Role: `faculty`
     - ID: `F2003`
     - Name: Dr. Sarah
     - Email: sarah@uni.edu
     - Password: prof_pwd
   - ✓ Should show "Created"

4. **Assign Faculty to Course**
   - Use Assign Faculty form
   - Course: `MATH101`
   - Faculty: `F2003`
   - ✓ Should show "Assigned"

5. **Verify New Faculty Dashboard**
   - Logout
   - Email: `sarah@uni.edu`, Password: `prof_pwd`
   - ✓ Should see MATH101 in assigned courses

---

## Test Scenario 6: Transcript Generation

**Objective:** Test secure transcript generation with hash verification.

**Steps:**

1. **Student with Grades**
   - Ensure S1001 has at least one grade
   - (Already uploaded 88 in CS101)

2. **Generate Transcript**
   - Login as S1001
   - Click "Generate Transcript"
   - ✓ New window opens with JSON data
   - ✓ Should include:
     - `student_id`: S1001
     - `name`: Ali Khan
     - `program`: BSCS
     - `grades`: [CS101 grade]
     - `generated_at`: timestamp
     - `record_hash`: SHA-256 hash

3. **Verify Hash in Root Data**
   - Open `/data/transcripts.json`
   - ✓ Should contain generated transcript
   - ✓ `record_hash` present and non-empty

---

## Test Scenario 7: Audit Log Viewing

**Objective:** Verify audit trail completeness.

**Steps:**

1. **Access Audit Logs**
   - Login as admin
   - Click "View Audit Logs"
   - ✓ Should open JSON viewer in new window

2. **Verify Log Entries Include:**
   - ✓ `timestamp` - ISO 8601 format
   - ✓ `user` - User ID
   - ✓ `role` - student/faculty/staff
   - ✓ `action` - login, register_course, upload_grade, create_user, etc.
   - ✓ `target` - JSON object with affected data

3. **Actions to Verify in Log:**
   - All logins
   - Course registrations
   - Grade uploads
   - User creates
   - Failed registrations
   - Access denied attempts

---

## Test Scenario 8: Grade Modification

**Objective:** Test grade updates with reason logging.

**Steps:**

1. **Upload Initial Grade**
   - Login as F2001
   - Upload grade: S1001, CS101, Score: 88

2. **Modify Grade (Optional Feature)**
   - If modify endpoint implemented:
   - Input: S1001, CS101, New Score: 92
   - Reason: "Recalculation - arithmetic error"

3. **Verify in Audit**
   - ✓ Should see `modify_grade` action in audit log
   - ✓ Should include old/new scores and reason

---

## Data Integrity Tests

### Hash Verification

1. **Check Student Record Hash**
   - Open `/data/students.json`
   - Pick any student, note the `record_hash`
   - Manually compute hash using Python:
   ```python
   import json, hashlib
   # Remove record_hash from student object
   s = {... student data without record_hash ...}
   calculated = hashlib.sha256(json.dumps(s, sort_keys=True).encode()).hexdigest()
   # Compare with record_hash - should match
   ```

2. **Detect Tampering**
   - Manually modify a student's CGPA in JSON
   - Save file
   - Restart Flask app
   - ✓ System should detect hash mismatch (optional warning)

---

## Performance Tests

### Bulk Operations
1. **Create 10 Students via Admin**
   - Create S1010 through S1019
   - ✓ All created successfully
   - ✓ Performance acceptable

2. **Mass Registration (10 students, 5 courses each)**
   - Register students for courses
   - ✓ No noticeable slowdown

3. **Audit Log Growth**
   - After ~100 actions
   - Check audit_logs.json size
   - ✓ Should be < 100KB

---

## Negative Tests (Expected Failures)

### Invalid Credentials
- Login with wrong email → ✓ "Invalid credentials"
- Login with wrong password → ✓ "Invalid credentials"
- Login with empty fields → ✓ Form validation error

### Data Conflicts
- Register same course twice → ✓ "Already enrolled"
- Register with no prereq → ✓ "Missing prerequisites"
- Exceed credits → ✓ "Exceeds max credits"
- Faculty grade unauthorized course → ✓ "Not authorized"

### Invalid Operations
- Student access faculty URL → ✓ Access denied (403)
- Faculty delete user → ✓ Access denied (403)
- Non-existent student register → ✓ Invalid student/course
- Non-existent course → ✓ Invalid student/course

---

## Verification Checklist

After all tests, verify:

- [ ] All 3 roles (student, faculty, admin) work
- [ ] Course registration validates prerequisites
- [ ] Credit limit enforced (max 18)
- [ ] Duplicate registration prevented
- [ ] CGPA calculated correctly after grade upload
- [ ] Transcript generated with hash
- [ ] Role-based access control enforced
- [ ] All actions logged in audit trail
- [ ] Faculty cannot grade unassigned courses
- [ ] Students see only own data
- [ ] Admin can create/assign users
- [ ] Grades appear in student dashboard
- [ ] File permissions correct on `/data/`

---

## Command Cheat Sheet

```bash
# Setup
pip install -r requirements.txt
python setup.py

# Run
python app.py

# View data files
cat data/students.json
cat data/audit_logs.json
cat data/grades.json

# Check specific user
grep -A 5 "S1001" data/students.json

# Count audit log entries
grep -c "\"action\"" data/audit_logs.json
```

---

## Browser DevTools Tips

### Check Network Requests
1. Open DevTools (F12)
2. Go to Network tab
3. Perform action (register, upload grade)
4. Review request/response
5. Verify POST data and JSON response

### Check Local Storage
1. DevTools → Application
2. Check Session Storage
3. Verify `user` session object exists
4. Check user role and ID

### Console Errors
1. Any errors should be logged in audit_logs.json
2. Check browser console for JS errors
3. Check server console output

---

## Known Limitations

1. **Session Persistence** - Sessions lost on server restart (Flask default)
2. **Scale** - JSON storage adequate for ~10K students, then consider database
3. **Concurrent Access** - No locking, assume single server
4. **Transcript Export** - Currently JSON only (PDF optional enhancement)
5. **Search** - No search feature (GPA, courses, students)

---

## Production Testing Checklist

- [ ] Test with HTTPS enabled
- [ ] Test with `debug=False`
- [ ] Test with production WSGI server (Gunicorn)
- [ ] Load test with 100+ concurrent users
- [ ] Test backup/restore procedure
- [ ] Test disaster recovery
- [ ] Verify audit logs don't grow unbounded
- [ ] Monitor memory usage over time
- [ ] Test with actual institutional data
- [ ] Security audit by third party

---

**All tests completed successfully? You're ready to deploy!** 🚀
