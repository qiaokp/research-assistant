#!/bin/bash

# Research Assistant Startup Script
# This will start both backend and frontend servers

echo "🚀 Starting Research Assistant..."
echo ""

# Kill any existing servers
pkill -f "python main.py"
pkill -f "next dev"
sleep 2

# Check if .env exists in backend
if [ ! -f "backend/.env" ]; then
    echo "⚠️  backend/.env not found. Creating from example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env with your API keys and settings"
    echo "   Then run this script again."
    exit 1
fi

# Check if .env.local exists in frontend
if [ ! -f "frontend/.env.local" ]; then
    echo "📝 Creating frontend/.env.local..."
    cp frontend/.env.local.example frontend/.env.local
fi

# Check if Python venv exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Start backend
echo "🔧 Starting backend server..."
cd backend
source venv/bin/activate
pip install -q -r requirements.txt
python main.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "✅ Backend started (PID: $BACKEND_PID) on http://localhost:8000"
sleep 3

# Start frontend on port 4000
echo "🎨 Starting frontend..."
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

PORT=4000 npm run dev > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "✅ Frontend started (PID: $FRONTEND_PID) on http://localhost:4000"
echo ""
echo "🎉 Research Assistant is running!"
echo ""
echo "   Frontend: http://localhost:4000  ← Open this!"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
