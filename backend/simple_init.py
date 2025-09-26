"""
Simple database initialization
"""
from sqlalchemy.orm import Session
from database.database import SessionLocal, engine, Base
from models.user import User

# Simple password hash function for testing
def simple_hash(password: str) -> str:
    """Simple hash for testing - NOT for production"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def create_basic_users():
    """Create basic users for testing"""
    
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_admin = db.query(User).filter(User.email == "admin@school.com").first()
        if existing_admin:
            print("Users already exist!")
            return
        
        # Create admin user
        admin = User(
            name="Admin User",
            email="admin@school.com",
            hashed_password=simple_hash("password"),
            role="admin"
        )
        db.add(admin)
        
        # Create teacher
        teacher = User(
            name="John Teacher",
            email="teacher@school.com",
            hashed_password=simple_hash("password"),
            role="teacher"
        )
        db.add(teacher)
        
        # Create student
        student = User(
            name="Jane Student",
            email="student@school.com",
            hashed_password=simple_hash("password"),
            role="student"
        )
        db.add(student)
        
        db.commit()
        print("Basic users created successfully!")
        print("Admin: admin@school.com / password")
        print("Teacher: teacher@school.com / password") 
        print("Student: student@school.com / password")
        
    except Exception as e:
        print(f"Error creating users: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_basic_users()
