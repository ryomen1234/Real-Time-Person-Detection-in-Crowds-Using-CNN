#!/bin/bash

echo "Stopping Smart Attendance System..."

# Stop backend
if [ -f ".backend.pid" ]; then
    BACKEND_PID=$(cat .backend.pid)
    kill $BACKEND_PID 2>/dev/null && echo "✅ Backend stopped"
    rm .backend.pid
fi

# Stop frontend
if [ -f ".frontend.pid" ]; then
    FRONTEND_PID=$(cat .frontend.pid)
    kill $FRONTEND_PID 2>/dev/null && echo "✅ Frontend stopped"
    rm .frontend.pid
fi

# Stop Qdrant (optional)
read -p "Do you want to stop Qdrant Docker container? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker stop $(docker ps -q --filter ancestor=qdrant/qdrant) 2>/dev/null && echo "✅ Qdrant stopped"
fi

echo "All services stopped."

