import yt_dlp

url = "https://music.youtube.com/channel/UCGexzRso_X06F8t3pXwGbfI"
ydl_opts = {'quiet': True, 'extract_flat': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(url, download=False)
    print(f"Artist: {info.get('channel') or info.get('uploader') or info.get('title')}")
