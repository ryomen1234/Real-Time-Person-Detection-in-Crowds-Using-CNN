# 🤖 ML Integration Guide - SUPER SIMPLE

## 📁 Project Structure (DON'T CHANGE THIS!)
```
role-attende/
├── src/                    ← React Frontend (DON'T TOUCH)
├── backend/                ← FastAPI Backend (YOUR WORK HERE)
│   ├── routers/
│   │   └── attendance.py   ← EDIT THIS FILE ONLY
│   └── your_ml_model.py    ← CREATE THIS FILE
└── package.json            ← Frontend stuff (DON'T TOUCH)
```

## 🎯 EXACTLY What You Need to Do:

### Step 1: Create Your ML File
**File**: `backend/your_ml_model.py`

```python
# your_ml_model.py
import cv2
import face_recognition
# Add your ML imports here

def detect_faces_in_image(image_path: str, known_students: list) -> list:
    """
    YOUR ML FUNCTION GOES HERE
    
    Input:
    - image_path: "uploads/attendance/session_1_20241126.jpg"
    - known_students: [{"student_id": 1, "name": "John", "email": "john@school.com"}, ...]
    
    Output:
    [
        {"student_id": 1, "name": "John", "email": "john@school.com", "detected": True, "confidence": "85%"},
        {"student_id": 2, "name": "Jane", "email": "jane@school.com", "detected": False, "confidence": None}
    ]
    """
    
    # YOUR ML CODE HERE
    # Process the image_path
    # Detect faces
    # Match with known_students
    # Return results in the format above
    
    # Example (replace with your real ML code):
    detected_students = []
    for student in known_students:
        # Your face detection logic here
        is_present = True  # Replace with your detection result
        detected_students.append({
            "student_id": student["student_id"],
            "name": student["name"],
            "email": student["email"],
            "detected": is_present,
            "confidence": "87%" if is_present else None
        })
    
    return detected_students
```

### Step 2: Edit ONE File Only
**File**: `backend/routers/attendance.py`  
**Lines**: 107-127

**FIND THIS CODE:**
```python
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
        is_detected = random.choice([True, False, True])
        detected_students.append({
            "student_id": student.id,
            "name": student.name,
            "email": student.email,
            "detected": is_detected,
            "confidence": f"{random.randint(75, 95)}%" if is_detected else None
        })
```

**REPLACE WITH:**
```python
# ML MODEL INTEGRATION
from your_ml_model import detect_faces_in_image

# Get enrolled students
enrolled_students = db.query(Enrollment).filter(
    Enrollment.subject_id == session.subject_id,
    Enrollment.is_active == True
).all()

# Prepare student data for ML model
student_data = []
for enrollment in enrolled_students:
    student = db.query(User).filter(User.id == enrollment.student_id).first()
    if student:
        student_data.append({
            "student_id": student.id,
            "name": student.name,
            "email": student.email
        })

# Use ML model to detect faces
detected_students = detect_faces_in_image(file_path, student_data)
```

## 🚀 That's It! Only 2 Things to Do:

1. **Create** `backend/your_ml_model.py` with your ML function
2. **Edit** `backend/routers/attendance.py` lines 107-127

**DON'T TOUCH ANYTHING ELSE!**

## 🧪 How to Test:

1. Start backend: `cd backend && python main.py`
2. Start frontend: `npm run dev`  
3. Login as teacher
4. Upload a class photo
5. Your ML model will process it!

## 📞 Need Help?

Just focus on these 2 files:
- `backend/your_ml_model.py` ← Your ML code
- `backend/routers/attendance.py` ← Replace 20 lines

Everything else is already working perfectly!
