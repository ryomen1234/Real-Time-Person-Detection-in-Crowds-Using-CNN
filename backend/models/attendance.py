from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    session_date = Column(DateTime, nullable=False)
    class_type = Column(String(50), default="lecture")  # lecture, lab, tutorial
    image_path = Column(String(500))  # Path to uploaded image
    total_students = Column(Integer, default=0)
    present_students = Column(Integer, default=0)
    status = Column(String(20), default="active")  # active, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subject = relationship("Subject", back_populates="attendance_sessions")
    teacher = relationship("User", back_populates="attendance_sessions")
    attendance_records = relationship("AttendanceRecord", back_populates="session")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(20), nullable=False)  # present, absent, late
    confidence_score = Column(String(10))  # ML model confidence (if detected automatically)
    manual_override = Column(Boolean, default=False)  # If manually adjusted by teacher
    notes = Column(String(500))
    marked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("AttendanceSession", back_populates="attendance_records")
    student = relationship("User", back_populates="attendance_records")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    student = relationship("User")
    subject = relationship("Subject", back_populates="enrollments")
