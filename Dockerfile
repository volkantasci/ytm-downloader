FROM python:3.11-slim

# Install system dependencies
# chromium, chromium-driver: Browser logic
# xvfb: Virtual display for headful mode
# ffmpeg: For audio post-processing
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    xvfb \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/

# Copy entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Create volume mount point for output
RUN mkdir -p /app/music

# Default entrypoint
ENTRYPOINT ["./entrypoint.sh"]
