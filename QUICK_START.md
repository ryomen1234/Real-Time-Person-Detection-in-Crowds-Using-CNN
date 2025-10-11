# 🚀 Quick Start Guide

Get your Smart Attendance System running in 5 minutes!

## ⚡ Prerequisites

Install these first:
- **Python 3.8+**: https://www.python.org/downloads/
- **Node.js 16+**: https://nodejs.org/
- **Docker Desktop**: https://www.docker.com/products/docker-desktop/

## 🎯 One-Command Setup

### Windows
```bash
./start_system.bat
```

### Linux/macOS
```bash
chmod +x start_system.sh
./start_system.sh
```

That's it! The script will:
1. ✅ Install all dependencies
2. ✅ Start Qdrant database
3. ✅ Create database & sample data
4. ✅ Start backend API
5. ✅ Start frontend

## 🌐 Access the System

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔑 Login Credentials

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@university.edu | admin123 |
| Teacher | sarah.johnson@university.edu | teacher123 |
| Student | alice.w@student.edu | student123 |

## 📝 First Steps

### 1. Register Student Faces (5 minutes)
1. Login as **Admin** (admin@university.edu / admin123)
2. Go to **User Management**
3. For each student, click **"Register Face"**
4. Upload a clear face photo
5. Wait for confirmation ✅

### 2. Take Attendance (2 minutes)
1. Login as **Teacher** (sarah.johnson@university.edu / teacher123)
2. Go to **Take Attendance**
3. Select a subject
4. Upload a group photo
5. Click **"Process Attendance"**
6. Review and save!

## 🎨 What You'll See

### Beautiful Detection UI
- **Green cards** = Student detected (with confidence %)
- **Red cards** = Student not detected
- **Click cards** to manually adjust
- **Animated progress bars** showing detection confidence

### Live Stats
- Present count 🟢
- Absent count 🔴
- Attendance rate % 📊

## 🛑 Stop Services

### Linux/macOS
```bash
./stop_system.sh
```

### Windows
Just close the terminal windows or press `Ctrl+C`

## ❓ Issues?

### "Docker not running"
→ Start Docker Desktop first

### "Port already in use"
→ Another app is using port 8000 or 5173. Close it or change ports.

### "No faces detected"
→ Use a clear, well-lit photo with visible faces

## 📚 Need More Help?

See `COMPLETE_SETUP_GUIDE.md` for:
- Detailed setup instructions
- Troubleshooting guide
- Architecture overview
- API documentation

## 🎉 You're Ready!

Your system is now ready to detect students in group photos and mark attendance automatically. Show your teacher how awesome this is! 🚀

