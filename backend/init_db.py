"""
Initialize database with sample data for testing
"""
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine
from models.user import User
from models.subject import Subject
from models.attendance import Enrollment
from app.auth import get_password_hash

def create_sample_data():
    """Create sample users, subjects, and enrollments"""
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@school.com",
            hashed_password=get_password_hash("password"[:72]),  # Truncate password
            role="admin"
        )
        db.add(admin)
        
        # Create teachers
        teacher1 = User(
            name="John Teacher",
            email="teacher@school.com",
            hashed_password=get_password_hash("password"[:72]),
            role="teacher"
        )
        db.add(teacher1)
        
        teacher2 = User(
            name="Sarah Johnson",
            email="sarah.teacher@school.com",
            hashed_password=get_password_hash("password"[:72]),
            role="teacher"
        )
        db.add(teacher2)
        
        # Create students
        students = [
            User(name="Alice Johnson", email="alice@school.com", hashed_password=get_password_hash("password"[:72]), role="student"),
            User(name="Bob Smith", email="bob@school.com", hashed_password=get_password_hash("password"[:72]), role="student"),
            User(name="Carol Davis", email="carol@school.com", hashed_password=get_password_hash("password"[:72]), role="student"),
            User(name="David Wilson", email="david@school.com", hashed_password=get_password_hash("password"[:72]), role="student"),
            User(name="Eva Brown", email="eva@school.com", hashed_password=get_password_hash("password"[:72]), role="student"),
            User(name="Jane Student", email="student@school.com", hashed_password=get_password_hash("password"[:72]), role="student"),
        ]
        
        for student in students:
            db.add(student)
        
        db.commit()
        
        # Get teacher IDs
        teacher1_id = db.query(User).filter(User.email == "teacher@school.com").first().id
        teacher2_id = db.query(User).filter(User.email == "sarah.teacher@school.com").first().id
        
        # Create subjects
        subjects = [
            Subject(name="Mathematics", code="MATH101", description="Basic Mathematics", teacher_id=teacher1_id),
            Subject(name="Physics", code="PHYS101", description="Introduction to Physics", teacher_id=teacher1_id),
            Subject(name="Computer Science", code="CS101", description="Programming Fundamentals", teacher_id=teacher2_id),
            Subject(name="Chemistry", code="CHEM101", description="General Chemistry", teacher_id=teacher2_id),
            Subject(name="English Literature", code="ENG101", description="English Literature", teacher_id=teacher1_id),
        ]
        
        for subject in subjects:
            db.add(subject)
        
        db.commit()
        
        # Enroll students in subjects
        student_ids = [s.id for s in db.query(User).filter(User.role == "student").all()]
        subject_ids = [s.id for s in db.query(Subject).all()]
        
        # Enroll each student in 3-4 subjects
        import random
        for student_id in student_ids:
            enrolled_subjects = random.sample(subject_ids, random.randint(3, 4))
            for subject_id in enrolled_subjects:
                enrollment = Enrollment(student_id=student_id, subject_id=subject_id)
                db.add(enrollment)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Create tables
    from models import user, subject, attendance
    from database.database import Base
    Base.metadata.create_all(bind=engine)
    
    # Create sample data
    create_sample_data()
