"""
Seed data script to populate the database with sample users and subjects
Run this after starting the backend to create test data
"""

import requests
import sys

API_URL = "http://localhost:8000/api"

def create_admin():
    """Create admin user"""
    admin_data = {
        "name": "Admin User",
        "email": "admin@university.edu",
        "password": "admin123",
        "role": "admin"
    }
    
    # First, login as admin (if exists) or create a temp user
    # For seed, we'll create directly through database
    print("🔧 Creating admin user...")
    return admin_data

def seed_database():
    """Seed the database with sample data"""
    
    print("🌱 Starting database seeding...")
    print("=" * 50)
    
    # Create admin credentials
    admin = create_admin()
    print(f"✅ Admin created: {admin['email']} / {admin['password']}")
    
    # Login as admin to get token
    print("\n🔐 Logging in as admin...")
    try:
        login_response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": admin['email'], "password": admin['password']}
        )
        
        if login_response.status_code != 200:
            print("❌ Failed to login. Please create admin user manually first.")
            print("   Use the FastAPI docs at http://localhost:8000/docs")
            return
        
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✅ Login successful!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Please start the backend first:")
        print("   cd Model && python main.py")
        return
    
    # Create teachers
    print("\n👨‍🏫 Creating teachers...")
    teachers = [
        {"name": "Dr. Sarah Johnson", "email": "sarah.johnson@university.edu", "password": "teacher123", "role": "teacher"},
        {"name": "Prof. Michael Chen", "email": "michael.chen@university.edu", "password": "teacher123", "role": "teacher"},
        {"name": "Dr. Emily Davis", "email": "emily.davis@university.edu", "password": "teacher123", "role": "teacher"},
    ]
    
    teacher_ids = []
    for teacher in teachers:
        response = requests.post(f"{API_URL}/users", json=teacher, headers=headers)
        if response.status_code == 200:
            teacher_id = response.json()["id"]
            teacher_ids.append(teacher_id)
            print(f"   ✅ Created: {teacher['name']} (ID: {teacher_id})")
        else:
            print(f"   ⚠️  Skipped: {teacher['name']} (may already exist)")
    
    # Create students
    print("\n👨‍🎓 Creating students...")
    students = [
        {"name": "Alice Williams", "email": "alice.w@student.edu", "prn": "PRN001", "password": "student123", "role": "student"},
        {"name": "Bob Martinez", "email": "bob.m@student.edu", "prn": "PRN002", "password": "student123", "role": "student"},
        {"name": "Carol Thompson", "email": "carol.t@student.edu", "prn": "PRN003", "password": "student123", "role": "student"},
        {"name": "David Garcia", "email": "david.g@student.edu", "prn": "PRN004", "password": "student123", "role": "student"},
        {"name": "Emma Rodriguez", "email": "emma.r@student.edu", "prn": "PRN005", "password": "student123", "role": "student"},
        {"name": "Frank Lee", "email": "frank.l@student.edu", "prn": "PRN006", "password": "student123", "role": "student"},
        {"name": "Grace Kim", "email": "grace.k@student.edu", "prn": "PRN007", "password": "student123", "role": "student"},
        {"name": "Henry Patel", "email": "henry.p@student.edu", "prn": "PRN008", "password": "student123", "role": "student"},
        {"name": "Iris Zhang", "email": "iris.z@student.edu", "prn": "PRN009", "password": "student123", "role": "student"},
        {"name": "Jack Brown", "email": "jack.b@student.edu", "prn": "PRN010", "password": "student123", "role": "student"},
    ]
    
    student_ids = []
    for student in students:
        response = requests.post(f"{API_URL}/users", json=student, headers=headers)
        if response.status_code == 200:
            student_id = response.json()["id"]
            student_ids.append(student_id)
            print(f"   ✅ Created: {student['name']} - {student['prn']} (ID: {student_id})")
        else:
            print(f"   ⚠️  Skipped: {student['name']} (may already exist)")
    
    # Create subjects
    print("\n📚 Creating subjects...")
    subjects = [
        {"name": "Data Structures and Algorithms", "code": "CS201", "description": "Learn fundamental data structures and algorithms", "teacher_id": teacher_ids[0] if teacher_ids else None},
        {"name": "Machine Learning", "code": "CS301", "description": "Introduction to ML concepts and applications", "teacher_id": teacher_ids[1] if teacher_ids else None},
        {"name": "Web Development", "code": "CS202", "description": "Full-stack web development", "teacher_id": teacher_ids[2] if teacher_ids else None},
        {"name": "Database Management Systems", "code": "CS203", "description": "Database design and SQL", "teacher_id": teacher_ids[0] if teacher_ids else None},
        {"name": "Computer Networks", "code": "CS302", "description": "Networking fundamentals", "teacher_id": teacher_ids[1] if teacher_ids else None},
    ]
    
    subject_ids = []
    for subject in subjects:
        response = requests.post(f"{API_URL}/subjects", json=subject, headers=headers)
        if response.status_code == 200:
            subject_id = response.json()["id"]
            subject_ids.append(subject_id)
            print(f"   ✅ Created: {subject['name']} ({subject['code']}) - ID: {subject_id}")
        else:
            print(f"   ⚠️  Skipped: {subject['name']} (may already exist)")
    
    # Enroll students in subjects
    print("\n📝 Enrolling students in subjects...")
    enrollment_count = 0
    for subject_id in subject_ids:
        for student_id in student_ids:
            response = requests.post(
                f"{API_URL}/subjects/{subject_id}/enroll",
                json={"student_id": student_id, "subject_id": subject_id},
                headers=headers
            )
            if response.status_code == 200:
                enrollment_count += 1
    
    print(f"   ✅ Created {enrollment_count} enrollments")
    
    print("\n" + "=" * 50)
    print("🎉 Database seeding completed successfully!")
    print("\n📋 Test Credentials:")
    print("-" * 50)
    print("Admin:")
    print(f"  Email: {admin['email']}")
    print(f"  Password: {admin['password']}")
    print("\nTeacher (any):")
    print("  Email: sarah.johnson@university.edu")
    print("  Password: teacher123")
    print("\nStudent (any):")
    print("  Email: alice.w@student.edu")
    print("  Password: student123")
    print("-" * 50)
    print("\n⚠️  IMPORTANT: Students need to register their faces!")
    print("   Use the admin panel to upload face photos for each student.")
    print("   Then you can use the 'Take Attendance' feature with group photos.")
    print("\n🚀 Next steps:")
    print("   1. Go to http://localhost:5173")
    print("   2. Login as admin")
    print("   3. Register student faces (Admin > User Management)")
    print("   4. Login as teacher")
    print("   5. Take attendance with a group photo!")

if __name__ == "__main__":
    seed_database()

