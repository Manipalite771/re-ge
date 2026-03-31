#!/bin/bash
# Launch both the background worker and Streamlit app.
# Works locally and on Railway (uses $PORT env var).

PORT=${PORT:-8501}
DIR="$(cd "$(dirname "$0")" && pwd)"

# Use venv if it exists (local), otherwise system Python (Docker/Railway)
if [ -d "$DIR/venv/bin" ]; then
    PYTHON="$DIR/venv/bin/python"
    STREAMLIT="$DIR/venv/bin/streamlit"
else
    PYTHON="python"
    STREAMLIT="streamlit"
fi

echo "Starting Resume Generator..."
echo "  Worker:    background process"
echo "  Streamlit: port $PORT"

# Start worker in background
$PYTHON "$DIR/worker.py" &
WORKER_PID=$!
echo "Worker started (PID: $WORKER_PID)"

# Trap to kill worker on exit
cleanup() {
    echo "Shutting down..."
    kill $WORKER_PID 2>/dev/null
    exit 0
}
trap cleanup SIGTERM SIGINT

# Start Streamlit in foreground (keeps container alive)
$STREAMLIT run "$DIR/app.py" \
    --server.headless true \
    --server.port $PORT \
    --server.address 0.0.0.0 \
    --server.enableCORS false \
    --server.enableXsrfProtection false
