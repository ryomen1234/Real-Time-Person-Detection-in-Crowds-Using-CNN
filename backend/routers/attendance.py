from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime, date
import os
import shutil
from PIL import Image
from database.database import get_db
from models.user import User
from models.subject import Subject
from models.attendance import AttendanceSession, AttendanceRecord, Enrollment
from app.schemas import (
    AttendanceSession as AttendanceSessionSchema,
    AttendanceSessionCreate,
    AttendanceRecord as AttendanceRecordSchema,
    AttendanceRecordCreate,
    AttendanceRecordWithStudent,
    AttendanceStats,
    StudentAttendanceResponse,
    ImageProcessingResponse
)
from app.auth import get_teacher_user, get_current_active_user, get_student_user

router = APIRouter()

@router.post("/sessions", response_model=AttendanceSessionSchema)
async def create_attendance_session(
    session_data: AttendanceSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_teacher_user)
):
    """Create a new attendance session (teacher only)."""
    # Check if subject exists and teacher has permission
    subject = db.query(Subject).filter(Subject.id == session_data.subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    if current_user.role == "teacher" and subject.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create sessions for your own subjects"
        )
    
    # Create attendance session
    session = AttendanceSession(
        subject_id=session_data.subject_id,
        teacher_id=current_user.id,
        session_date=session_data.session_date,
        class_type=session_data.class_type,
        notes=session_data.notes
    )
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session

@router.post("/sessions/{session_id}/upload-image")
async def upload_attendance_image(
    session_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_teacher_user)
):
    """Upload image for attendance session and process for face recognition."""
    # Check if session exists and teacher has permission
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance session not found"
        )
    
    if current_user.role == "teacher" and session.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only upload images for your own sessions"
        )
    
    # Validate image file
    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads/attendance", exist_ok=True)
    
    # Save uploaded image
    file_extension = image.filename.split(".")[-1]
    filename = f"session_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_extension}"
    file_path = f"uploads/attendance/{filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Update session with image path
    session.image_path = file_path
    db.commit()
    
    # TODO: Integrate with ML model for face recognition
    # For now, we'll return mock detected students
    enrolled_students = db.query(Enrollment).filter(
        Enrollment.subject_id == session.subject_id,
        Enrollment.is_active == True
    ).all()
    
    detected_students = []
    for enrollment in enrolled_students:
        student = db.query(User).filter(User.id == enrollment.student_id).first()
        if student:
            # Mock detection - randomly mark some as present
            import random
            is_detected = random.choice([True, False, True])  # 66% chance of detection
            detected_students.append({
                "student_id": student.id,
                "name": student.name,
                "email": student.email,
                "detected": is_detected,
                "confidence": f"{random.randint(75, 95)}%" if is_detected else None
            })
    
    # Update session stats
    session.total_students = len(detected_students)
    session.present_students = sum(1 for s in detected_students if s["detected"])
    db.commit()
    
    return ImageProcessingResponse(
        session_id=session_id,
        detected_students=detected_students,
        total_detected=session.present_students,
        processing_status="completed"
    )

@router.post("/sessions/{session_id}/records", response_model=AttendanceRecordSchema)
async def mark_attendance(
    session_id: int,
    attendance_data: AttendanceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_teacher_user)
):
    """Mark attendance for a student in a session."""
    # Check if session exists and teacher has permission
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance session not found"
        )
    
    if current_user.role == "teacher" and session.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only mark attendance for your own sessions"
        )
    
    # Check if student is enrolled in the subject
    enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == attendance_data.student_id,
        Enrollment.subject_id == session.subject_id,
        Enrollment.is_active == True
    ).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is not enrolled in this subject"
        )
    
    # Check if attendance already marked for this student in this session
    existing_record = db.query(AttendanceRecord).filter(
        AttendanceRecord.session_id == session_id,
        AttendanceRecord.student_id == attendance_data.student_id
    ).first()
    
    if existing_record:
        # Update existing record
        existing_record.status = attendance_data.status
        existing_record.notes = attendance_data.notes
        existing_record.manual_override = True
        db.commit()
        db.refresh(existing_record)
        return existing_record
    else:
        # Create new attendance record
        record = AttendanceRecord(
            session_id=session_id,
            student_id=attendance_data.student_id,
            status=attendance_data.status,
            notes=attendance_data.notes,
            manual_override=True
        )
        
        db.add(record)
        db.commit()
        db.refresh(record)
        
        return record

@router.get("/sessions/{session_id}/records", response_model=List[AttendanceRecordWithStudent])
async def get_session_attendance(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get attendance records for a specific session."""
    # Check if session exists
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance session not found"
        )
    
    # Check permissions
    if current_user.role == "teacher" and session.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own session attendance"
        )
    
    records = db.query(AttendanceRecord).filter(
        AttendanceRecord.session_id == session_id
    ).all()
    
    return records

@router.get("/student/{student_id}", response_model=StudentAttendanceResponse)
async def get_student_attendance(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get attendance statistics for a student."""
    # Students can only view their own attendance unless user is admin/teacher
    if (current_user.role == "student" and current_user.id != student_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own attendance"
        )
    
    # Get student
    student = db.query(User).filter(User.id == student_id, User.role == "student").first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Get student's enrolled subjects
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.is_active == True
    ).all()
    
    subject_stats = []
    total_classes = 0
    total_attended = 0
    
    for enrollment in enrollments:
        subject = db.query(Subject).filter(Subject.id == enrollment.subject_id).first()
        if not subject:
            continue
        
        # Count total sessions for this subject
        subject_sessions = db.query(AttendanceSession).filter(
            AttendanceSession.subject_id == subject.id,
            AttendanceSession.status == "completed"
        ).count()
        
        # Count attended sessions
        attended_sessions = db.query(AttendanceRecord).filter(
            AttendanceRecord.student_id == student_id,
            AttendanceRecord.status == "present"
        ).join(AttendanceSession).filter(
            AttendanceSession.subject_id == subject.id
        ).count()
        
        attendance_percentage = (attended_sessions / subject_sessions * 100) if subject_sessions > 0 else 0
        
        subject_stats.append(AttendanceStats(
            total_classes=subject_sessions,
            attended_classes=attended_sessions,
            attendance_percentage=round(attendance_percentage, 2),
            subject_name=subject.name,
            subject_id=subject.id
        ))
        
        total_classes += subject_sessions
        total_attended += attended_sessions
    
    overall_percentage = (total_attended / total_classes * 100) if total_classes > 0 else 0
    
    return StudentAttendanceResponse(
        student=student,
        subjects=subject_stats,
        overall_percentage=round(overall_percentage, 2)
    )

@router.get("/sessions", response_model=List[AttendanceSessionSchema])
async def get_attendance_sessions(
    subject_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get attendance sessions with optional filters."""
    query = db.query(AttendanceSession)
    
    if subject_id:
        query = query.filter(AttendanceSession.subject_id == subject_id)
    
    if teacher_id:
        query = query.filter(AttendanceSession.teacher_id == teacher_id)
    
    if start_date:
        query = query.filter(AttendanceSession.session_date >= start_date)
    
    if end_date:
        query = query.filter(AttendanceSession.session_date <= end_date)
    
    # Teachers can only see their own sessions unless admin
    if current_user.role == "teacher":
        query = query.filter(AttendanceSession.teacher_id == current_user.id)
    
    sessions = query.order_by(desc(AttendanceSession.session_date)).all()
    return sessions
