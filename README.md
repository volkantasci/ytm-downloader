# YTM Downloader v2.0.0 (Agentic)

A powerful, self-hosted YouTube Music downloader and library manager, **designed specifically for Navidrome**.

![Dashboard](gallery/dashboard.png)

## Why This?

This project isn't just a downloader; it's a **library builder**. It is built to populate self-hosted music text servers like **Navidrome**, **Jellyfin**, or **Plex** with high-quality, properly tagged music.

-   **Navidrome Ready**: Files are organized exactly how Navidrome expects them (`Artist/Album/Track.m4a`).
-   **Automatic Metadata**: Every song is automatically tagged with correct Title, Artist, Album, and Year.
-   **Album Art**: High-resolution cover art is embedded directly into every file.

## Features

-   **Modern Web UI**: Built with React, Tailwind CSS, and a cyberpunk-inspired dark theme.
-   **Job System**: Background processing for downloads and scans, managed via `multiprocessing`.
-   **Real-time Updates**: WebSocket-based activity feed for zero-latency status tracking.
-   **Live Logs**: View real-time logs for any active job directly in the browser.
-   **Library Management**: Scan your library to fix folder structures and missing tags automatically.
-   **File Browser**: Built-in file explorer to browse your library within the app.
-   **Dockerized**: Easy deployment with Docker and Docker Compose.

## Gallery

### Dashboard & Activity Feed
![Dashboard with Action List](gallery/dashboard-with-action-list.png)

### Live Logs
![Action Logs](gallery/action-logs.png)

### Library Management
![Library](gallery/library.png)

### File Browser
![File Browser](gallery/file-browser.png)

## Installation

### Prerequisites
-   Docker
-   Docker Compose

### Quick Start

1.  Clone the repository:
    ```bash
    git clone https://github.com/volkantasci/ytm-downloader.git
    cd ytm-downloader
    ```

2.  Start the application:
    ```bash
    docker compose up -d --build
    ```

3.  Access the UI:
    Open your browser and navigate to `http://localhost:3000`.

## Usage

### Downloading Music
-   **Search Download**: Enter a search query (e.g., "Chill Lofi") and set a limit. The system will find the top results and download them.
-   **Artist Discography**: Enter an artist's name (or URL) to download their albums. You can limit the number of albums and songs per album.

### Managing Library
-   Go to the **Library** page.
-   **Scan & Fix Metadata**: Run this job to scan your `/app/music` directory. It will organize files into `Artist/Album` folders and apply correct tagging.
-   **Browse Files**: Use the file browser to verify your downloads.

## Architecture

-   **Frontend**: React, Vite, TSX, Tailwind CSS, Zustand (State)
-   **Backend**: Python, FastAPI, Mutagen (Metadata), yt-dlp (Download)
-   **Infrastructure**: Docker Compose (Frontend + Backend services)
