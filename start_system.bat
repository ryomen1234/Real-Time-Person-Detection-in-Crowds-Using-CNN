@echo off
echo ========================================
echo Smart Attendance System Starter
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/6] Checking Python dependencies...
cd Model
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt --quiet

echo.
echo [2/6] Starting Qdrant Vector Database...
start cmd /k "docker run -p 6333:6333 qdrant/qdrant || echo [WARNING] Docker not running. Please start Docker Desktop and run: docker run -p 6333:6333 qdrant/qdrant"

timeout /t 5 /nobreak >nul

echo.
echo [3/6] Initializing Database...
python init_admin.py

echo.
echo [4/6] Seeding Sample Data...
python seed_data.py

echo.
echo [5/6] Starting FastAPI Backend...
start cmd /k "cd /d %CD% && venv\Scripts\activate.bat && python main.py"

cd ..

echo.
echo [6/6] Starting React Frontend...
if not exist "node_modules" (
    echo Installing Node dependencies...
    npm install
)

start cmd /k "npm run dev"

echo.
echo ========================================
echo ✅ All services started successfully!
echo ========================================
echo.
echo 🌐 Frontend: http://localhost:5173
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo 🗄️  Qdrant: http://localhost:6333/dashboard
echo.
echo 📋 Default Credentials:
echo    Admin: admin@university.edu / admin123
echo    Teacher: sarah.johnson@university.edu / teacher123
echo    Student: alice.w@student.edu / student123
echo.
echo Press any key to open the browser...
pause >nul
start http://localhost:5173

