#!/bin/bash

echo "========================================"
echo "Smart Attendance System Starter"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR] Python 3 is not installed${NC}"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${RED}[ERROR] Node.js is not installed${NC}"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}[1/6] Setting up Python environment...${NC}"
cd Model

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo -e "${GREEN}[2/6] Starting Qdrant Vector Database...${NC}"
# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${YELLOW}[WARNING] Docker is not running${NC}"
    echo "Please start Docker and run: docker run -p 6333:6333 qdrant/qdrant"
else
    # Check if Qdrant is already running
    if ! docker ps | grep -q qdrant; then
        docker run -d -p 6333:6333 qdrant/qdrant
        echo "Qdrant started in background"
    else
        echo "Qdrant is already running"
    fi
fi

sleep 3

echo ""
echo -e "${GREEN}[3/6] Initializing Database...${NC}"
python init_admin.py

echo ""
echo -e "${GREEN}[4/6] Seeding Sample Data...${NC}"
python seed_data.py

echo ""
echo -e "${GREEN}[5/6] Starting FastAPI Backend...${NC}"
# Start backend in background
nohup python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

cd ..

echo ""
echo -e "${GREEN}[6/6] Starting React Frontend...${NC}"
if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

echo ""
echo "========================================"
echo -e "${GREEN}✅ All services started successfully!${NC}"
echo "========================================"
echo ""
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🗄️  Qdrant: http://localhost:6333/dashboard"
echo ""
echo "📋 Default Credentials:"
echo "   Admin: admin@university.edu / admin123"
echo "   Teacher: sarah.johnson@university.edu / teacher123"
echo "   Student: alice.w@student.edu / student123"
echo ""
echo -e "${YELLOW}To stop all services, run: ./stop_system.sh${NC}"
echo ""

# Save PIDs for later stopping
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid

# Wait for user input
read -p "Press Enter to open browser..."
xdg-open http://localhost:5173 2>/dev/null || open http://localhost:5173 2>/dev/null || echo "Please open http://localhost:5173 in your browser"

