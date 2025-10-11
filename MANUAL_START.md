# 🚀 Manual Startup Guide (Windows)

## ✅ Dependencies Installed!

Good news - all Python dependencies are now installed correctly!

## 🎯 How to Start the System

### Step 1: Start Docker (Qdrant Database)

1. **Open Docker Desktop**
2. Make sure it's running (check system tray)
3. Open a **new PowerShell** window and run:
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```
4. Leave this window open

### Step 2: Start Backend (FastAPI)

1. Open a **new PowerShell** window
2. Navigate to your project:
   ```bash
   cd "C:\Users\kevin\OneDrive\Desktop\Real-Time-Person-Detection-in-Crowds-Using-CNN"
   cd Model
   .\venv\Scripts\activate
   python main.py
   ```
3. You should see: `Uvicorn running on http://127.0.0.1:8000`
4. Leave this window open

### Step 3: Start Frontend (React)

1. Open a **new PowerShell** window
2. Navigate to your project:
   ```bash
   cd "C:\Users\kevin\OneDrive\Desktop\Real-Time-Person-Detection-in-Crowds-Using-CNN"
   npm install
   npm run dev
   ```
3. You should see: `Local: http://localhost:5173`
4. Leave this window open

### Step 4: (Optional) Seed Sample Data

After the backend is running, open another terminal:
```bash
cd Model
.\venv\Scripts\activate
python seed_data.py
```

This will create:
- 3 teachers
- 10 students  
- 5 subjects
- All enrollments

## 🌐 Access Your System

Open your browser and go to: **http://localhost:5173**

### Login Credentials

**Admin:**
- Email: `admin@university.edu`
- Password: `admin123`

**Teacher:**
- Email: `sarah.johnson@university.edu`
- Password: `teacher123`

**Student:**
- Email: `alice.w@student.edu`
- Password: `student123`

## 📝 Next Steps

1. **Login as Admin**
2. **Go to "User Management"**
3. **Register student faces** - Click "Register Face" for each student and upload a clear photo
4. **Logout and login as Teacher**
5. **Go to "Take Attendance"**
6. **Upload a group photo** with the registered students
7. **Watch the AI detect students!** 🎉

## ❗ Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check if Qdrant (Docker) is running
- Make sure venv is activated

### Frontend won't start
- Make sure port 5173 is not in use
- Try: `npm install` first

### "Cannot connect to Qdrant"
- Make sure Docker Desktop is running
- Make sure you ran: `docker run -p 6333:6333 qdrant/qdrant`

### Docker not installed
Download from: https://www.docker.com/products/docker-desktop/

## 🎯 Quick Test

Once everything is running:
1. Open http://localhost:8000/docs - Should show FastAPI docs
2. Open http://localhost:5173 - Should show your app
3. Open http://localhost:6333/dashboard - Should show Qdrant dashboard

---

**You're all set!** 🚀 Start registering faces and taking attendance!

