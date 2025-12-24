#!/bin/bash
set -e

echo "Starting entrypoint script..."
echo "Arguments: $@"

# Run with xvfb to bypass headless detection
# --auto-servernum: Pick a free server number
# --server-args: Configure screen resolution
# -s "-ac -screen 0 1280x1024x24" might be safer
echo "Launching xvfb-run..."
xvfb-run --auto-servernum --server-args="-screen 0 1280x1024x24" python -m src.main "$@"

