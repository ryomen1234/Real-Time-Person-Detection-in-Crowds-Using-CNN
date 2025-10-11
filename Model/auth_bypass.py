"""Temporary auth bypass for debugging"""
from database import User, SessionLocal
from fastapi import Depends

# Fake current user - always returns admin
def get_current_user_bypass() -> User:
    db = SessionLocal()
    user = db.query(User).filter(User.email == "admin@university.edu").first()
    db.close()
    return user

def require_role_bypass(allowed_roles: list):
    async def role_checker():
        return get_current_user_bypass()
    return role_checker

