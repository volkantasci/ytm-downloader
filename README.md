# ytm-downloader

A robust, containerized solution for archiving high-fidelity music albums from YouTube Music. Designed to populate self-hosted music streaming servers like **Navidrome**, **Jellyfin**, or **Plex**.

## 🚀 About The Project

This tool automates the process of finding, scraping, and downloading full discographies from YouTube Music. Unlike simple playlist downloaders, it intelligently navigates artist pages to identify albums, singles, and EPs, ensuring a complete collection.

It solves common scraping challenges (like headless browser detection) and prioritizes audio quality, organizing files into a structure perfectly suited for music servers.

### Key Features

-   **High-Fidelity Audio**: Prioritizes **M4A (AAC)** / Opus streams (Best Audio) over legacy MP3 conversion for superior sound quality.
-   **Smart Navigation**: Uses Selenium with **Chromium** to navigate dynamic YouTube Music pages.
-   **Anti-Detection**: Built-in `XVFB` (virtual display) integration to bypass "headless browser" blocks and Cloudflare checks.
-   **Search-Based Discovery**: Robustly finds artist pages via search queries, avoiding broken direct link issues.
-   **Granular Control**: Limit downloads by number of albums (`--limit`) or songs per album (`--song-limit`) for testing or partial archiving.
-   **Navidrome Ready**: Automatically organizes content into `Artist/Album/Song` hierarchy and embeds correct metadata/thumbnails.
-   **Dockerized**: Zero-dependency cleanup. Runs entirely within a container.

## 🛠 Architecture

The project combines several powerful tools:
*   **Selenium & Chromium**: For rendering the JS-heavy YouTube Music interface.
*   **XVFB**: To simulate a physical display buffer, preventing bot detection.
*   **yt-dlp**: For extracting the raw audio streams and metadata.
*   **FFmpeg**: For post-processing, format conversion, and tagging.

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

2.  Build the container image:
    ```bash
    docker-compose build
    ```

### Usage

**Basic Download:**
Download all albums for a specific artist.
```bash
docker-compose run --rm downloader --artist-name "Metallica"
```

**Dry Run (Simulation):**
List found albums without downloading anything. Useful for checking what will be fetched.
```bash
docker-compose run --rm downloader --artist-name "Metallica" --dry-run
```

**Partial Download (Testing):**
Download only the first album, and limited to just 1 song from it.
```bash
docker-compose run --rm downloader --artist-name "Metallica" --limit 1 --song-limit 1
```

## 🔧 Local Development (Linux)

If you prefer to run this without Docker, you will need to install system dependencies manually.

**Requirements:**
*   Python 3.11+
*   Chromium & Chromium Driver
*   Xvfb (X Virtual Framebuffer)
*   FFmpeg

**Setup:**
```bash
# Install system deps (Arch Linux example)
sudo pacman -S chromium chromium-driver xvfb ffmpeg

# Install python deps
pip install -r requirements.txt
```

**Running:**
You **must** use `xvfb-run` to execute the script, otherwise YouTube Music will detect the headless session and return an empty page.

```bash
xvfb-run --auto-servernum --server-args="-screen 0 1280x1024x24" python -m src.main --artist-name "Metallica" --dry-run
```

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
