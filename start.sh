#!/bin/bash
# Launch both the background worker and Streamlit app.
# Usage: ./start.sh [port]

PORT=${1:-8501}
DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$DIR/venv/bin"

echo "Starting Resume Generator..."
echo "  Worker:    background process"
echo "  Streamlit: http://localhost:$PORT"
echo ""

# Kill any existing instances
pkill -f "python.*worker.py" 2>/dev/null
kill $(lsof -ti:$PORT) 2>/dev/null
sleep 1

# Start worker in background
nohup "$VENV/python" "$DIR/worker.py" > "$DIR/worker.log" 2>&1 &
WORKER_PID=$!
echo "Worker started (PID: $WORKER_PID)"

# Start Streamlit
"$VENV/streamlit" run "$DIR/app.py" \
    --server.headless true \
    --server.port $PORT \
    --server.address 0.0.0.0

# Cleanup on exit
kill $WORKER_PID 2>/dev/null
echo "Stopped."
