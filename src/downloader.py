import os
import yt_dlp
import random
import time
import subprocess
from multiprocessing import Pool, cpu_count
from mutagen.mp4 import MP4, MP4Tags
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, ID3NoHeaderError
from mutagen import File as MutagenFile

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
            print(f"Error downloading album {album_url}: {e}")

def fix_metadata(filepath, main_artist):
    """
    Cleans up metadata using mutagen.
    1. Deduplicates Artist tag (e.g. 'Artist, Artist' -> 'Artist')
    2. Sets Album Artist to main_artist to group albums correctly.
    """
    try:
        audio = MutagenFile(filepath, easy=True)
        if audio is None:
            # Try manual MP4 check if auto detection failed for m4a
            if filepath.lower().endswith('.m4a'):
                audio = MP4(filepath)
            else:
                print(f"Warning: Could not open {filepath} for metadata fixing.")
                return
        
        saved = False
        
        # 1. Fix Artist Name
        # EasyID3/EasyMP4 keys are usually 'artist', 'albumartist', 'title', 'album'
        
        # Check 'artist'
        if 'artist' in audio:
            artists = audio['artist']
            # It might be a list of strings or a single string
            if isinstance(artists, list):
                # Flatten comma separated values inside list items if any
                raw_artists = []
                for a in artists:
                    raw_artists.extend([x.strip() for x in a.split(',')])
            else:
                raw_artists = [x.strip() for x in str(artists).split(',')]
            
            # Deduplicate preserving order
            clean_artists = list(dict.fromkeys(raw_artists))
            
            # Update if changed
            # Note: For MP4/mutagen, we usually expect a list of strings for multiple artists, 
            # or a single string. Youtube Music often puts "Artist A, Artist B" as one string.
            # We will join them back with ", " or keeping them as list depending on format.
            # For compatibility, a single string separated by comma is often safest for players 
            # that don't support multi-value tags well, OR we just keep the first one?
            # User wants to deduplicate "Oğuz Aksaç, Oğuz Aksaç".
            
            new_artist_val = clean_artists
            
            # If it was a list and now it's the same list, don't save. 
            # But compare carefully.
            
            if new_artist_val != artists:
                audio['artist'] = new_artist_val
                saved = True
                print(f"Fixed Artist: {artists} -> {new_artist_val}")

        # 1.5 Fix Album Name (Trim whitespace)
        if 'album' in audio:
            albums = audio['album']
            if isinstance(albums, list):
                clean_albums = [x.strip() for x in albums]
            else:
                clean_albums = str(albums).strip()
            
            if clean_albums != albums:
                audio['album'] = clean_albums
                saved = True
                print(f"Fixed Album Name: '{albums}' -> '{clean_albums}'")

        # 2. Fix Album Artist
        # If we have a main_artist context, force it as Album Artist.
        if main_artist:
            current_aa = audio.get('albumartist')
            # If missing or different, update it
            # Note: current_aa might be a list
            if not current_aa or (isinstance(current_aa, list) and current_aa[0] != main_artist) or (isinstance(current_aa, str) and current_aa != main_artist):
                audio['albumartist'] = main_artist
                saved = True
                print(f"Fixed Album Artist: '{current_aa}' -> '{main_artist}'")

        if saved:
            audio.save()
            print(f"Metadata saved for {os.path.basename(filepath)}")
            
    except Exception as e:
        print(f"Error fixing metadata for {filepath}: {e}")

from .scraper import MusicScraper

# get_artist_albums is deprecated/removed in favor of scraper

def download_artist_albums(artist_url, artist_name=None, limit=None, song_limit=None, max_album_length=None, dry_run=False):
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
    # Pass song_limit and max_album_length as well
    items = [(url, artist_name, song_limit, max_album_length) for url in album_urls]

    with Pool(processes=cpu_count()) as pool:
        pool.map(download_item_wrapper, items)

    with Pool(processes=cpu_count()) as pool:
        pool.map(download_item_wrapper, items)

def download_search_query(query, song_limit=None):
    """
    Searches for a query and downloads the result.
    """
    scraper = MusicScraper(headless=False)
    try:
        url, result_type = scraper.get_search_results(query)
    finally:
        scraper.close()
    
    if not url:
        print(f"No results found for query: '{query}'")
        return

    print(f"Found {result_type}: {url}")
    
    if result_type == 'album':
        # Download album
        # We can reuse download_album or download_item_wrapper logic
        # But we need artist name for folder grouping... 
        # Scraper didn't extract artist name from search result yet.
        # Let's hope yt-dlp gets it right or we pass None to let extractor handle it.
        # Or we could improve scraper to get artist name.
        
        # For uniformity, let's use the wrapper but we need to fake params
        # (url, artist_name, song_limit, max_album_length)
        download_item_wrapper((url, None, song_limit, None))

    elif result_type == 'song':
        # Download song
        # yt-dlp can handle song URLs same as albums usually
        download_item_wrapper((url, None, song_limit, None))

    url, artist_name, song_limit, max_album_length = args
    
    # Add a random initial delay to spread out requests when using multiprocessing
    delay = random.uniform(2, 10)
    print(f"Waiting {delay:.2f}s before processing {url}...")
    time.sleep(delay)
    
    # Pre-check album size if max_album_length is set
    if max_album_length:
        print(f"Checking track count for {url} with limit {max_album_length}...")
        try:
            # Use subprocess to call yt-dlp CLI directly as it proved more reliable for getting playlist_count
            # for 'browse' type URLs than the Python library in some contexts.
            cmd = [
                'yt-dlp',
                '--flat-playlist',
                '--print', '%(playlist_count)s',
                url
            ]
            
            # Run command and capture output
            result = subprocess.run(cmd, capture_output=True, text=True)
            output = result.stdout.strip().split('\n')[0] # Take first line
            
            if output and output.isdigit():
                track_count = int(output)
                print(f"DEBUG: CLI reported track count: {track_count}")
                
                if track_count > max_album_length:
                    print(f"Skipping {url}: Album has {track_count} tracks (Limit: {max_album_length})")
                    return # Skip this album
                else:
                    print(f"Album validated: {track_count} tracks. Proceeding.")
            else:
                 print(f"Warning: Could not determine track count from CLI output: '{output}'. Proceeding CAUTIOUSLY.")

        except Exception as e:
            print(f"Warning: Could not check album length for {url}: {e}. Proceeding.")

    # Construct output template
    # If artist_name is known, hardcode it to avoid 'NA' or channel ID being used
    if artist_name:
        out_template = f"music/{artist_name}/%(album,playlist_title,playlist)s/%(title)s.%(ext)s"
    else:
        out_template = 'music/%(artist,uploader,channel)s/%(album,playlist_title,playlist)s/%(title)s.%(ext)s'

     # Re-instantiate yt-dlp options here because they can't be pickled easily if we passed the object.
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
        'sleep_interval': 10,       # Minimum sleep time (seconds)
        'max_sleep_interval': 30,   # Maximum sleep time (seconds)
        'download_archive': '/app/music/download_archive.txt', # Track downloaded files
        'nooverwrites': True,       # Don't overwrite existing files (secondary check)
    }
    
    if song_limit and song_limit > 0:
        ydl_opts['max_downloads'] = song_limit
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
             # Use extract_info to get metadata and filenames
            info = ydl.extract_info(url, download=True)
            
            # Process downloaded files
            if 'entries' in info:
                entries = info['entries']
            else:
                entries = [info]

            for entry in entries:
                if not entry: continue
                
                # Get the final filename
                # yt-dlp stores it in 'requested_downloads' inside entry if successful
                if 'requested_downloads' in entry:
                    for downloaded in entry['requested_downloads']:
                        filepath = downloaded.get('filepath')
                        if filepath and os.path.exists(filepath):
                             fix_metadata(filepath, artist_name)
                else:
                    # Fallback: try to guess filename or check if entry has filename
                    # This is harder reliably. 
                    # If 'filepath' is in entry directly (sometimes happens)
                    filepath = entry.get('filepath')
                    if filepath and os.path.exists(filepath):
                        fix_metadata(filepath, artist_name)
                    
        except Exception as e:
            print(f"Error downloading {url}: {e}")

def download_search_query(query, song_limit=None):
    """
    Searches for a query and downloads the result.
    """
    scraper = MusicScraper(headless=False)
    try:
        url, result_type = scraper.get_search_results(query)
    finally:
        scraper.close()
    
    if not url:
        print(f"No results found for query: '{query}'")
        return

    print(f"Found {result_type}: {url}")
    
    if result_type == 'album':
        # Download album
        # We can reuse download_album or download_item_wrapper logic
        # But we need artist name for folder grouping... 
        # Scraper didn't extract artist name from search result yet.
        # Let's hope yt-dlp gets it right or we pass None to let extractor handle it.
        # Or we could improve scraper to get artist name.
        
        # For uniformity, let's use the wrapper but we need to fake params
        # (url, artist_name, song_limit, max_album_length)
        download_item_wrapper((url, None, song_limit, None))

    elif result_type == 'song':
        # Download song
        # yt-dlp can handle song URLs same as albums usually
        download_item_wrapper((url, None, song_limit, None))
