#!/bin/bash
set -e

# If the first argument is "api", run the FastAPI server
if [ "$1" = "api" ]; then
    echo "Starting Xvfb..."
    Xvfb :99 -screen 0 1280x1024x24 > /dev/null 2>&1 &
    export DISPLAY=:99
    echo "Starting FastAPI Server..."
    exec uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
else
    # Otherwise assume arguments for the CLI
    echo "Starting CLI..."
    exec xvfb-run --auto-servernum --server-args="-screen 0 1280x1024x24" python -m src.main "$@"
fi
