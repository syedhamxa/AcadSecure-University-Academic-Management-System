#!/usr/bin/env python3
"""
Setup script to initialize sample data with real bcrypt hashes for testing.
Run once to generate test credentials.
"""
import os
import sys
import json
sys.path.insert(0, os.path.dirname(__file__))

from modules.utils import hash_password, compute_hash, write_json, DATA_DIR

def setup_sample_data():
    """Initialize all sample JSON files with real bcrypt hashes."""
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Sample password for all test users: "password123"
    test_pwd_hash = hash_password("password123")
    
    # Students
    students = {
        "S1001": {
            "name": "Ali Khan",
            "email": "ali@uni.edu",
            "program": "BSCS",
            "password_hash": test_pwd_hash,
            "enrolled_courses": ["CS101"],
            "cgpa": 0.0
        },
        "S1002": {
            "name": "Amina Ahmed",
            "email": "amina@uni.edu",
            "program": "BSSE",
            "password_hash": test_pwd_hash,
            "enrolled_courses": [],
            "cgpa": 0.0
        }
    }
    for s in students.values():
        s['record_hash'] = compute_hash(s)
    write_json('students.json', students)
    print("✓ Created students.json")
    
    # Faculty
    faculty = {
        "F2001": {
            "name": "Dr. Sana Ahmad",
            "email": "sana@uni.edu",
            "password_hash": test_pwd_hash,
            "assigned_courses": ["CS101"]
        },
        "F2002": {
            "name": "Dr. Ahmed Hassan",
            "email": "ahmed@uni.edu",
            "password_hash": test_pwd_hash,
            "assigned_courses": []
        }
    }
    for f in faculty.values():
        f['record_hash'] = compute_hash(f)
    write_json('faculty.json', faculty)
    print("✓ Created faculty.json")
    
    # Staff/Admin
    staff = {
        "A3001": {
            "name": "Admin User",
            "email": "admin@uni.edu",
            "password_hash": test_pwd_hash
        }
    }
    for s in staff.values():
        s['record_hash'] = compute_hash(s)
    write_json('staff.json', staff)
    print("✓ Created staff.json")
    
    # Courses
    courses = {
        "CS101": {
            "title": "Intro to Computer Science",
            "credits": 3,
            "prerequisites": []
        },
        "CS201": {
            "title": "Data Structures",
            "credits": 3,
            "prerequisites": ["CS101"]
        },
        "MATH101": {
            "title": "Calculus I",
            "credits": 4,
            "prerequisites": []
        }
    }
    for c in courses.values():
        c['record_hash'] = compute_hash(c)
    write_json('courses.json', courses)
    print("✓ Created courses.json")
    
    # Enrollments
    enrollments = {
        "S1001": [
            {
                "course": "CS101",
                "semester": "2025-Fall",
                "timestamp": "2025-09-01T00:00:00Z"
            }
        ],
        "S1002": []
    }
    write_json('enrollments.json', enrollments)
    print("✓ Created enrollments.json")
    
    # Grades (empty initially)
    grades = {}
    write_json('grades.json', grades)
    print("✓ Created grades.json")
    
    # Transcripts (empty initially)
    transcripts = {}
    write_json('transcripts.json', transcripts)
    print("✓ Created transcripts.json")
    
    # Audit logs
    audit_logs = []
    write_json('audit_logs.json', audit_logs)
    print("✓ Created audit_logs.json")
    
    print("\n" + "="*50)
    print("✅ SETUP COMPLETE!")
    print("="*50)
    print("\nTest Credentials (password: 'password123'):")
    print("\n👨‍🎓 Student:")
    print("  Email: ali@uni.edu")
    print("\n👨‍🏫 Faculty:")
    print("  Email: sana@uni.edu")
    print("\n🔐 Admin:")
    print("  Email: admin@uni.edu")
    print("\nTo start the app, run: python app.py")
    print("Then visit: http://localhost:5000")

if __name__ == '__main__':
    setup_sample_data()
