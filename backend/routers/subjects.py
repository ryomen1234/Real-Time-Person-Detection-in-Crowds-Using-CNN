from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.database import get_db
from models.user import User
from models.subject import Subject
from models.attendance import Enrollment
from app.schemas import (
    Subject as SubjectSchema, 
    SubjectCreate, 
    SubjectUpdate, 
    SubjectWithTeacher,
    EnrollmentCreate,
    Enrollment as EnrollmentSchema
)
from app.auth import get_admin_user, get_teacher_user, get_current_active_user

router = APIRouter()

@router.get("/", response_model=List[SubjectWithTeacher])
async def get_subjects(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=100),
    teacher_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all subjects."""
    query = db.query(Subject).filter(Subject.is_active == True)
    
    if teacher_id:
        query = query.filter(Subject.teacher_id == teacher_id)
    
    if search:
        query = query.filter(
            (Subject.name.contains(search)) | 
            (Subject.code.contains(search))
        )
    
    subjects = query.offset(skip).limit(limit).all()
    return subjects

@router.get("/{subject_id}", response_model=SubjectWithTeacher)
async def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get subject by ID."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    return subject

@router.post("/", response_model=SubjectSchema)
async def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Create new subject (admin only)."""
    # Check if subject code already exists
    existing_subject = db.query(Subject).filter(Subject.code == subject_data.code).first()
    if existing_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subject code already exists"
        )
    
    # Verify teacher exists if provided
    if subject_data.teacher_id:
        teacher = db.query(User).filter(
            User.id == subject_data.teacher_id,
            User.role == "teacher",
            User.is_active == True
        ).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Teacher not found or inactive"
            )
    
    # Create new subject
    db_subject = Subject(
        name=subject_data.name,
        code=subject_data.code,
        description=subject_data.description,
        teacher_id=subject_data.teacher_id
    )
    
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    
    return db_subject

@router.put("/{subject_id}", response_model=SubjectSchema)
async def update_subject(
    subject_id: int,
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Update subject information (admin only)."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Check if new code conflicts with existing subject
    if subject_data.code and subject_data.code != subject.code:
        existing_subject = db.query(Subject).filter(Subject.code == subject_data.code).first()
        if existing_subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject code already exists"
            )
    
    # Verify teacher exists if provided
    if subject_data.teacher_id:
        teacher = db.query(User).filter(
            User.id == subject_data.teacher_id,
            User.role == "teacher",
            User.is_active == True
        ).first()
        if not teacher:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Teacher not found or inactive"
            )
    
    # Update subject fields
    update_data = subject_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subject, field, value)
    
    db.commit()
    db.refresh(subject)
    
    return subject

@router.delete("/{subject_id}")
async def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Delete subject (admin only)."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Soft delete by setting is_active to False
    subject.is_active = False
    db.commit()
    
    return {"message": "Subject deleted successfully"}

@router.get("/teacher/{teacher_id}", response_model=List[SubjectSchema])
async def get_teacher_subjects(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get subjects taught by a specific teacher."""
    # Teachers can only see their own subjects unless user is admin
    if current_user.role != "admin" and current_user.id != teacher_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    subjects = db.query(Subject).filter(
        Subject.teacher_id == teacher_id,
        Subject.is_active == True
    ).all()
    
    return subjects

@router.post("/{subject_id}/enroll", response_model=EnrollmentSchema)
async def enroll_student(
    subject_id: int,
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_admin_user)
):
    """Enroll a student in a subject (admin only)."""
    # Check if subject exists
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Check if student exists
    student = db.query(User).filter(
        User.id == enrollment_data.student_id,
        User.role == "student",
        User.is_active == True
    ).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student not found or inactive"
        )
    
    # Check if already enrolled
    existing_enrollment = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment_data.student_id,
        Enrollment.subject_id == subject_id,
        Enrollment.is_active == True
    ).first()
    if existing_enrollment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student is already enrolled in this subject"
        )
    
    # Create enrollment
    enrollment = Enrollment(
        student_id=enrollment_data.student_id,
        subject_id=subject_id
    )
    
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    
    return enrollment

@router.get("/{subject_id}/students", response_model=List[dict])
async def get_subject_students(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_teacher_user)
):
    """Get all students enrolled in a subject."""
    # Check if subject exists
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    # Teachers can only see their own subject students unless user is admin
    if current_user.role == "teacher" and subject.teacher_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Get enrolled students
    enrollments = db.query(Enrollment).filter(
        Enrollment.subject_id == subject_id,
        Enrollment.is_active == True
    ).all()
    
    students = []
    for enrollment in enrollments:
        student = db.query(User).filter(User.id == enrollment.student_id).first()
        if student:
            students.append({
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "enrollment_date": enrollment.enrollment_date
            })
    
    return students
