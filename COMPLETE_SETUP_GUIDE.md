# 🎓 Smart Attendance System - Complete Setup Guide

A real-time facial recognition attendance system using CNN (FaceNet) to detect students in group photos and automatically mark attendance.

## 🌟 Features

- 📸 **Group Photo Detection**: Upload a class photo and automatically detect all students
- 🧠 **AI-Powered Recognition**: Uses FaceNet (InceptionResnetV1) for accurate face recognition
- 👥 **Multi-Role System**: Admin, Teacher, and Student accounts
- 📊 **Attendance Analytics**: Track attendance rates and statistics
- 🎨 **Beautiful Modern UI**: Built with React, TypeScript, and Tailwind CSS
- 🔒 **Secure Authentication**: JWT-based authentication system
- 🗄️ **Vector Database**: Qdrant for efficient face embedding storage

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Docker Desktop** - [Download](https://www.docker.com/products/docker-desktop/) (for Qdrant vector database)
- **Git** - [Download](https://git-scm.com/downloads)

## 🚀 Quick Start (Automated)

### Windows

1. Open PowerShell or Command Prompt in the project directory
2. Run the automated setup script:
```bash
./start_system.bat
```

### Linux/macOS

1. Open Terminal in the project directory
2. Make the script executable:
```bash
chmod +x start_system.sh
```
3. Run the automated setup script:
```bash
./start_system.sh
```

The automated script will:
- ✅ Install all dependencies
- ✅ Start Qdrant database (Docker)
- ✅ Initialize the database
- ✅ Create sample users and data
- ✅ Start the backend API (FastAPI)
- ✅ Start the frontend (React)

## 📖 Manual Setup

If you prefer manual setup or the automated script doesn't work:

### Step 1: Install Backend Dependencies

```bash
cd Model
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### Step 2: Start Qdrant (Vector Database)

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Keep this terminal open.

### Step 3: Initialize Database & Seed Data

Open a new terminal:

```bash
cd Model
# Activate venv (see Step 1)

# Create admin user
python init_admin.py

# Add sample data (teachers, students, subjects)
python seed_data.py
```

### Step 4: Start Backend API

```bash
cd Model
# Activate venv (see Step 1)

python main.py
```

Backend will run at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Step 5: Start Frontend

Open a new terminal:

```bash
# From project root
npm install
npm run dev
```

Frontend will run at: `http://localhost:5173`

## 🔑 Default Login Credentials

### Admin Account
- Email: `admin@university.edu`
- Password: `admin123`
- Can manage users, subjects, and view all data

### Teacher Account
- Email: `sarah.johnson@university.edu`
- Password: `teacher123`
- Can take attendance and manage their classes

### Student Account
- Email: `alice.w@student.edu`
- Password: `student123`
- Can view their own attendance

## 📚 How to Use

### 1. Register Student Faces (Admin)

1. Login as **Admin**
2. Go to **User Management**
3. Find a student in the table
4. Click **"Register Face"** button
5. Upload a clear photo of the student's face
6. Wait for confirmation ✅

**Tips for best results:**
- Use well-lit photos
- Face should be clearly visible
- One person per photo
- Front-facing photos work best

### 2. Create Subjects & Enroll Students (Admin)

1. Login as **Admin**
2. Go to **Subject Management**
3. Click **"Add New Subject"**
4. Fill in subject details and assign a teacher
5. Click on a subject to enroll students

### 3. Take Attendance (Teacher)

1. Login as **Teacher**
2. Go to **Take Attendance**
3. Select the subject
4. Upload a group photo or use webcam
5. Click **"Process Attendance"**
6. Review detected students (green = present, red = absent)
7. Click cards to manually adjust if needed
8. Click **"Save Attendance"**

### 4. View Attendance (Student)

1. Login as **Student**
2. Go to **My Attendance**
3. View attendance statistics for all subjects
4. See overall attendance percentage

## 🏗️ Architecture

### Backend Stack
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database management
- **SQLite**: Lightweight database
- **FaceNet (facenet-pytorch)**: Face recognition model
- **MTCNN**: Face detection
- **Qdrant**: Vector database for face embeddings
- **JWT**: Authentication

### Frontend Stack
- **React 18**: UI library
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool
- **Tailwind CSS**: Utility-first CSS
- **shadcn/ui**: Beautiful UI components

### AI/ML Components
- **InceptionResnetV1**: Pre-trained face recognition model
- **MTCNN**: Multi-task Cascaded Convolutional Networks for face detection
- **Qdrant**: Vector similarity search for face matching

## 🛠️ Project Structure

```
Real-Time-Person-Detection-in-Crowds-Using-CNN/
├── Model/                      # Backend (Python/FastAPI)
│   ├── main.py                # Main FastAPI application
│   ├── database.py            # Database models & setup
│   ├── auth.py                # Authentication logic
│   ├── schemas.py             # Pydantic schemas
│   ├── init_admin.py          # Create initial admin
│   ├── seed_data.py           # Populate sample data
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Uploaded images
├── src/                       # Frontend (React/TypeScript)
│   ├── pages/                 # Page components
│   │   ├── admin/            # Admin pages
│   │   ├── teacher/          # Teacher pages
│   │   └── student/          # Student pages
│   ├── components/           # Reusable components
│   ├── services/             # API service layer
│   └── contexts/             # React contexts
├── public/                    # Static assets
├── start_system.bat          # Windows startup script
├── start_system.sh           # Linux/macOS startup script
└── stop_system.sh            # Stop all services
```

## 🔧 Configuration

### Backend Configuration

Edit `Model/auth.py` to change:
- JWT secret key
- Token expiration time

Edit `Model/database.py` to change:
- Database connection string

### Frontend Configuration

Edit `src/services/api.ts` to change:
- API base URL (default: `http://localhost:8000/api`)

## 🐛 Troubleshooting

### "No faces detected in the image"
- Ensure the image is clear and well-lit
- Face should be visible and not too small
- Try with a different photo

### "Docker not running"
- Start Docker Desktop
- Run: `docker run -p 6333:6333 qdrant/qdrant`

### "Failed to connect to backend"
- Ensure backend is running at `http://localhost:8000`
- Check if port 8000 is not in use by another application

### "Module not found" (Python)
- Ensure virtual environment is activated
- Run: `pip install -r Model/requirements.txt`

### "Port already in use"
Backend (8000):
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8000
kill -9 <PID>
```

Frontend (5173):
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :5173
kill -9 <PID>
```

## 📊 Database Schema

### Users Table
- id, prn (student ID), name, email, password_hash, role, face_registered

### Subjects Table
- id, name, code, description, teacher_id

### Enrollments Table
- id, student_id, subject_id, enrollment_date

### Attendance Sessions Table
- id, subject_id, teacher_id, session_date, class_type, image_path, status

### Attendance Records Table
- id, session_id, student_id, status, confidence_score, manual_override

## 🎯 Real-World Use Cases

This system is perfect for:

1. **Universities & Schools**: Automate attendance in large lecture halls
2. **Corporate Training**: Track attendance in training sessions
3. **Events**: Monitor attendee presence
4. **Conferences**: Automated check-in systems
5. **Security**: Access control and monitoring

## 🤝 Contributing

This project was built for educational purposes. Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Use it for your own projects

## 📄 License

This project is open-source for educational purposes.

## 👨‍💻 Credits

Built with ❤️ using modern AI/ML technologies:
- FaceNet by Google
- Qdrant for vector search
- FastAPI for backend
- React for frontend

## 🆘 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review the error logs in terminal
3. Ensure all prerequisites are installed
4. Check if all services are running

## 🎓 For Your Teacher

**Key Features That Demonstrate Real-Life Use:**

1. **Scalability**: Can handle large class photos with multiple students
2. **Accuracy**: Uses state-of-the-art FaceNet model for recognition
3. **Practical UI**: Beautiful, intuitive interface for all user roles
4. **Complete System**: Not just a model - full-stack application with auth, database, and analytics
5. **Real Data**: Uses actual database with students, subjects, and attendance records
6. **Production-Ready**: Proper error handling, validation, and security

---

**🎉 You're all set! Enjoy your Smart Attendance System!**

