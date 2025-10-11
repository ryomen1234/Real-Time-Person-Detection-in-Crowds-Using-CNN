"""Quick script to check database contents"""
from database import SessionLocal, User, Subject, Enrollment
from auth import verify_password

db = SessionLocal()

print("=== DATABASE CHECK ===\n")

# Check users
users = db.query(User).all()
print(f"Total Users: {len(users)}")
for user in users:
    print(f"  - {user.name} ({user.email}) - Role: {user.role}, Face: {user.face_registered}")

print(f"\nTotal Subjects: {db.query(Subject).count()}")
subjects = db.query(Subject).all()
for subj in subjects:
    print(f"  - {subj.name} ({subj.code})")

print(f"\nTotal Enrollments: {db.query(Enrollment).count()}")

# Test password
print("\n=== PASSWORD TEST ===")
admin = db.query(User).filter(User.email == "admin@university.edu").first()
if admin:
    test_passwords = ["admin123", "Admin123", "password"]
    for pwd in test_passwords:
        result = verify_password(pwd, admin.password_hash)
        print(f"  Password '{pwd}': {'✓ WORKS' if result else '✗ FAIL'}")
else:
    print("  Admin user not found!")

db.close()

