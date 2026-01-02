import click
from .downloader import download_artist_albums, download_search_query, scan_and_fix_library

@click.command()
@click.option('--artist-url', required=False, help='URL of the artist on music.youtube.com')
@click.option('--artist-name', required=False, help='Name of the artist to search for')
@click.option('--limit', default=None, type=int, help='Limit the number of albums to download')
@click.option('--song-limit', default=None, type=int, help='Limit the number of songs to download per album')
@click.option('--max-album-length', default=None, type=int, help='Skip albums with more than this number of tracks')
@click.option('--search', required=False, help='Search and download an album or song')
@click.option('--fix-library', is_flag=True, help='Scan music folder and fix metadata for all files')
@click.option('--dry-run', is_flag=True, help='List albums without downloading')
def main(artist_url, artist_name, limit, song_limit, max_album_length, dry_run, search, fix_library):
    """
    Download all albums from a YouTube Music artist URL or Name, or search for a specific album/song.
    """
    if fix_library:
        scan_and_fix_library()
        return

    if search:
        click.echo(f"Searching for: {search}")
        download_search_query(search, song_limit=song_limit)
        return

    if not artist_url and not artist_name:
        click.echo("Error: Excatly one of --artist-url or --artist-name must be provided.")
        return

    click.echo(f"Processing artist: {artist_name or artist_url}")
    download_artist_albums(artist_url, artist_name, limit=limit, song_limit=song_limit, max_album_length=max_album_length, dry_run=dry_run)

if __name__ == '__main__':
    main()
