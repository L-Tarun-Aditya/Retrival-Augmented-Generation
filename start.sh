#!/bin/bash

echo "Starting RAG Application..."

# Check if vector store exists
if [ ! -d "src/rag/chroma_db" ]; then
    echo "Building vector store..."
    cd src/rag
    python vector_store.py
    cd ../..
fi

# Start API server in background
echo "Starting API server..."
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/api
python3 server.py &
API_PID=$!
cd ../..

# Wait for API to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "Application started!"
echo "API: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "kill $API_PID $FRONTEND_PID; exit" INT
wait
