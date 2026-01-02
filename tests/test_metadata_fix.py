import os
import shutil
import unittest
import subprocess
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError
from src.downloader import fix_metadata

class TestMetadataFix(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_audio.mp3"
        # Generate dummy mp3
        subprocess.run([
            "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", 
            "-t", "1", "-q:a", "9", "-acodec", "libmp3lame", self.test_file
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_fix_metadata_artist_dedup(self):
        # Setup bad metadata
        try:
            audio = EasyID3(self.test_file)
        except ID3NoHeaderError:
            audio = EasyID3()
            audio.save(self.test_file)
            audio = EasyID3(self.test_file)
            
        audio['artist'] = ["Oğuz Aksaç, Oğuz Aksaç"]
        audio['album'] = ["Test Album"]
        audio.save()
        
        # Run fix
        fix_metadata(self.test_file, main_artist="Oğuz Aksaç")
        
        # Verify
        audio = EasyID3(self.test_file)
        # Mutagen returns lists for EasyID3
        self.assertEqual(audio['artist'], ['Oğuz Aksaç'])
        self.assertEqual(audio['albumartist'], ['Oğuz Aksaç'])

    def test_fix_metadata_album_artist_grouping(self):
        # Setup metadata without album artist
        try:
            audio = EasyID3(self.test_file)
        except ID3NoHeaderError:
            audio = EasyID3()
            audio.save(self.test_file)
            
        audio['artist'] = ["Different Artist"]
        audio.save()
        
        # Run fix using a main artist (e.g. from the folder structure)
        fix_metadata(self.test_file, main_artist="Main Artist")
        
        # Verify
        audio = EasyID3(self.test_file)
        self.assertEqual(audio['albumartist'], ['Main Artist'])
        # Artist should remain unchanged if it wasn't duplicate
        self.assertEqual(audio['artist'], ['Different Artist'])

if __name__ == '__main__':
    unittest.main()
