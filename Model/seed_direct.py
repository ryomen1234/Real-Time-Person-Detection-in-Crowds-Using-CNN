"""
Direct database seeding - bypasses API
"""
from database import SessionLocal, User, Subject, Enrollment, init_db
from auth import get_password_hash
from datetime import datetime

def seed_database():
    init_db()
    db = SessionLocal()
    
    print("=" * 60)
    print("DIRECT DATABASE SEEDING")
    print("=" * 60)
    
    try:
        # Check if already seeded
        existing_users = db.query(User).count()
        if existing_users > 1:
            print(f"\n[INFO] Database already has {existing_users} users")
            print("[INFO] Delete attendance_system.db and restart if you want fresh data")
            return
        
        print("\n[1/4] Creating Teachers...")
        teachers_data = [
            {"name": "Dr. Sarah Johnson", "email": "sarah.johnson@university.edu"},
            {"name": "Prof. Michael Chen", "email": "michael.chen@university.edu"},
            {"name": "Dr. Emily Davis", "email": "emily.davis@university.edu"},
        ]
        
        teacher_ids = []
        for t_data in teachers_data:
            teacher = User(
                name=t_data["name"],
                email=t_data["email"],
                password_hash=get_password_hash("teacher123"),
                role="teacher",
                is_active=True,
                face_registered=False
            )
            db.add(teacher)
            db.flush()
            teacher_ids.append(teacher.id)
            print(f"  ✓ Created: {t_data['name']}")
        
        db.commit()
        
        print("\n[2/4] Creating Students...")
        students_data = [
            {"name": "Alice Williams", "prn": "PRN001"},
            {"name": "Bob Martinez", "prn": "PRN002"},
            {"name": "Carol Thompson", "prn": "PRN003"},
            {"name": "David Garcia", "prn": "PRN004"},
            {"name": "Emma Rodriguez", "prn": "PRN005"},
            {"name": "Frank Lee", "prn": "PRN006"},
            {"name": "Grace Kim", "prn": "PRN007"},
            {"name": "Henry Patel", "prn": "PRN008"},
            {"name": "Iris Zhang", "prn": "PRN009"},
            {"name": "Jack Brown", "prn": "PRN010"},
        ]
        
        student_ids = []
        for s_data in students_data:
            email = f"{s_data['name'].lower().replace(' ', '.')}@student.edu"
            student = User(
                name=s_data["name"],
                email=email,
                prn=s_data["prn"],
                password_hash=get_password_hash("student123"),
                role="student",
                is_active=True,
                face_registered=False
            )
            db.add(student)
            db.flush()
            student_ids.append(student.id)
            print(f"  ✓ Created: {s_data['name']} ({s_data['prn']})")
        
        db.commit()
        
        print("\n[3/4] Creating Subjects...")
        subjects_data = [
            {"name": "Data Structures and Algorithms", "code": "CS201", "teacher_id": teacher_ids[0]},
            {"name": "Machine Learning", "code": "CS301", "teacher_id": teacher_ids[1]},
            {"name": "Web Development", "code": "CS202", "teacher_id": teacher_ids[2]},
            {"name": "Database Management Systems", "code": "CS203", "teacher_id": teacher_ids[0]},
            {"name": "Computer Networks", "code": "CS302", "teacher_id": teacher_ids[1]},
        ]
        
        subject_ids = []
        for subj_data in subjects_data:
            subject = Subject(
                name=subj_data["name"],
                code=subj_data["code"],
                description=f"Learn {subj_data['name']}",
                teacher_id=subj_data["teacher_id"],
                is_active=True
            )
            db.add(subject)
            db.flush()
            subject_ids.append(subject.id)
            print(f"  ✓ Created: {subj_data['name']} ({subj_data['code']})")
        
        db.commit()
        
        print("\n[4/4] Enrolling Students...")
        enrollment_count = 0
        for subject_id in subject_ids:
            for student_id in student_ids:
                enrollment = Enrollment(
                    student_id=student_id,
                    subject_id=subject_id,
                    enrollment_date=datetime.utcnow()
                )
                db.add(enrollment)
                enrollment_count += 1
        
        db.commit()
        print(f"  ✓ Created {enrollment_count} enrollments")
        
        print("\n" + "=" * 60)
        print("✓ DATABASE SEEDED SUCCESSFULLY!")
        print("=" * 60)
        print("\n📋 Login Credentials:")
        print("-" * 60)
        print("Admin:")
        print("  Email: admin@university.edu")
        print("  Password: admin123")
        print("\nTeacher:")
        print("  Email: sarah.johnson@university.edu")
        print("  Password: teacher123")
        print("\nStudent:")
        print("  Email: alice.williams@student.edu")
        print("  Password: student123")
        print("-" * 60)
        print("\n🎯 Next Steps:")
        print("1. Refresh your browser (F5)")
        print("2. Login as admin")
        print("3. Go to User Management - you'll see all users!")
        print("4. Register student faces")
        print("5. Login as teacher and take attendance!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

