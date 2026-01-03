# ytm-downloader

A robust, full-stack web application and containerized solution for archiving high-fidelity music albums from YouTube Music. Designed to populate self-hosted music streaming servers like **Navidrome**, **Jellyfin**, or **Plex**.

## 🚀 About The Project

This tool automates the process of finding, scraping, and downloading full discographies from YouTube Music. It is now a **Web Application** featuring a modern React frontend and a FastAPI backend, making it easier than ever to manage your downloads.

It solves common scraping challenges (like headless browser detection) and prioritizes audio quality, organizing files into a structure perfectly suited for music servers.

### Key Features

-   **Web Interface**: A beautiful, dark-themed dashboard to manage downloads and library.
-   **High-Fidelity Audio**: Prioritizes **M4A (AAC)** / Opus streams (Best Audio) over legacy MP3 conversion.
-   **Smart Navigation**: Uses Selenium with **Chromium** to navigate dynamic YouTube Music pages.
-   **Anti-Detection**: Built-in `XVFB` (virtual display) integration to bypass "headless browser" blocks.
-   **Rate Limiting**: Intelligent random delays between downloads to prevent IP blocking/throttling.
-   **Smart History**: Tracks downloaded songs in `download_archive.txt` to ensure you never download the same song twice.
-   **Size Filter**: Use `--max-album-length` (or UI setting) to skip massive compilations or playlists.
-   **Navidrome Ready**: Automatically organizes content into `Artist/Album/Song` hierarchy.
-   **Dockerized**: Zero-dependency cleanup. Runs entirely within containers.

## 🛠 Architecture

The project is built on a modern stack:
*   **Backend**: Python (FastAPI) + Selenium/Chromium (Scraping) + yt-dlp (Download Core)
*   **Frontend**: React + TypeScript + Vite (Single Page Application)
*   **Infrastructure**: Docker Compose (Orchestration)

## 📂 Output Structure

Music is saved in the following hierarchy, ready to be mounted by your media server:

```text
music/
├── Metallica/
│   ├── Reload/
│   │   ├── Fuel.m4a
│   │   ├── The Memory Remains.m4a
│   │   └── ...
│   └── ...
└── ...
```

## 🐳 Getting Started (Docker)

This is the recommended way to run the application.

### Prerequisites
*   Docker
*   Docker Compose

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/volkantasci/ytm-downloader.git
    cd ytm-downloader
    ```

2.  Start the application:
    ```bash
    docker-compose up -d --build
    ```

3.  Access the Web Interface:
    Open [http://localhost:5174](http://localhost:5174) in your browser.

    > **Note**: The backend API is available at [http://localhost:8001/docs](http://localhost:8001/docs).

### Usage (Web)

-   **Search**: Enter a song or album name (e.g., "Pink Floyd Comfortably Numb") to download it.
-   **Artist**: Enter an Artist Name or URL to download their entire discography.
-   **Library**: Use the "Scan & Fix" button to organize and tag your existing files.

### Usage (CLI - Legacy)

You can still use the CLI command for one-off tasks or scripting. Note that the service name in `docker-compose` is now `backend`.

**Basic Download:**
```bash
docker-compose run --rm backend --artist-name "Metallica"
```

**Search & Download:**
```bash
docker-compose run --rm backend --search "Beyhude"
```

## 🔧 Local Development

To run the project locally without Docker:

### Backend
1.  Install system dependencies (Chromium, XVFB, FFmpeg).
2.  Install Python dependencies: `pip install -r requirements.txt`
3.  Run the API:
    ```bash
    xvfb-run --auto-servernum --server-args="-screen 0 1280x1024x24" uvicorn src.api.main:app --reload --port 8001
    ```

### Frontend
1.  Navigate to `frontend/`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start dev server:
    ```bash
    npm run dev
    ```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
