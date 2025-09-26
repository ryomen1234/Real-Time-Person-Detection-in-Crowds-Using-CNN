from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class ClassType(str, Enum):
    LECTURE = "lecture"
    LAB = "lab"
    TUTORIAL = "tutorial"

# User schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Subject schemas
class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    teacher_id: Optional[int] = None

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    teacher_id: Optional[int] = None
    is_active: Optional[bool] = None

class Subject(SubjectBase):
    id: int
    teacher_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SubjectWithTeacher(Subject):
    teacher: Optional[User] = None

# Attendance schemas
class AttendanceSessionBase(BaseModel):
    subject_id: int
    session_date: datetime
    class_type: ClassType = ClassType.LECTURE
    notes: Optional[str] = None

class AttendanceSessionCreate(AttendanceSessionBase):
    pass

class AttendanceSession(AttendanceSessionBase):
    id: int
    teacher_id: int
    image_path: Optional[str]
    total_students: int
    present_students: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceRecordBase(BaseModel):
    status: AttendanceStatus
    notes: Optional[str] = None

class AttendanceRecordCreate(AttendanceRecordBase):
    student_id: int

class AttendanceRecord(AttendanceRecordBase):
    id: int
    session_id: int
    student_id: int
    confidence_score: Optional[str]
    manual_override: bool
    marked_at: datetime
    
    class Config:
        from_attributes = True

class AttendanceRecordWithStudent(AttendanceRecord):
    student: User

# Enrollment schemas
class EnrollmentBase(BaseModel):
    student_id: int
    subject_id: int

class EnrollmentCreate(EnrollmentBase):
    pass

class Enrollment(EnrollmentBase):
    id: int
    enrollment_date: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

# Response schemas
class AttendanceStats(BaseModel):
    total_classes: int
    attended_classes: int
    attendance_percentage: float
    subject_name: str
    subject_id: int

class StudentAttendanceResponse(BaseModel):
    student: User
    subjects: List[AttendanceStats]
    overall_percentage: float

# Image processing response
class ImageProcessingResponse(BaseModel):
    session_id: int
    detected_students: List[dict]
    total_detected: int
    processing_status: str
