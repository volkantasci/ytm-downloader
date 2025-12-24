import os
import yt_dlp
from multiprocessing import Pool, cpu_count

def download_album(album_url):
    """
    Downloads a single album.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'},
            {'key': 'FFmpegMetadata','add_metadata': True},
            {'key': 'EmbedThumbnail'},
        ],
        'outtmpl': 'music/%(album)s/%(title)s.%(ext)s',
        'quiet': False,
        'ignoreerrors': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([album_url])
        except Exception as e:
            print(f"Error downloading album {album_url}: {e}")

from .scraper import MusicScraper

# get_artist_albums is deprecated/removed in favor of scraper

def download_artist_albums(artist_url, artist_name=None, limit=None, song_limit=None, dry_run=False):
    """
    Main orchestrator for downloading artist albums.
    """
    # Use headless=False because running with xvfb (virtual display)
    # This avoids bot detection that blocks headless browsers.
    scraper = MusicScraper(headless=False)
    try:
        album_urls = scraper.get_artist_albums(artist_url, artist_name)
    finally:
        scraper.close()
    
    print(f"Found {len(album_urls)} albums.")
    
    # Sort for consistency? Or just take first N found? 
    # YTM order is usually chronological or by popularity. 
    # Since we use a set, order is lost. Let's convert to list and sort? 
    # But we don't have metadata to sort by efficiently without scraping more.
    # Let's just convert to list.
    album_urls = list(album_urls)
    
    if limit and limit > 0:
        print(f"Limiting to first {limit} albums.")
        album_urls = album_urls[:limit]

    print(f"Processing {len(album_urls)} albums...")
    
    if dry_run:
        print("[DRY RUN] Albums to be processed:")
        for url in album_urls:
            print(f" - {url}")
        return

    if not album_urls:
        print("No albums found.")
        return

    # Prepare items for download wrapper
    # Pass artist_name to enforce correct directory structure
    # Pass song_limit as well
    items = [(url, artist_name, song_limit) for url in album_urls]

    with Pool(processes=cpu_count()) as pool:
        pool.map(download_item_wrapper, items)

def download_item_wrapper(args):
    """
    Wrapper to unpack arguments for pool map.
    args: (url, artist_name, song_limit)
    """
    url, artist_name, song_limit = args
    
    # Construct output template
    # If artist_name is known, hardcode it to avoid 'NA' or channel ID being used
    if artist_name:
        out_template = f"music/{artist_name}/%(album,playlist_title,playlist)s/%(title)s.%(ext)s"
    else:
        out_template = 'music/%(artist,uploader,channel)s/%(album,playlist_title,playlist)s/%(title)s.%(ext)s'

     # Re-instantiate yt-dlp options here because they can't be pickled easily if we passed the object.
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [
            {'key': 'FFmpegExtractAudio','preferredcodec': 'm4a','preferredquality': '0'},
            {'key': 'FFmpegMetadata','add_metadata': True},
            {'key': 'EmbedThumbnail'},
        ],
        'outtmpl': out_template,
        'quiet': False,
        'ignoreerrors': True,
        'writethumbnail': True,
    }
    
    if song_limit and song_limit > 0:
        ydl_opts['max_downloads'] = song_limit
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
        except Exception as e:
            print(f"Error downloading {url}: {e}")
