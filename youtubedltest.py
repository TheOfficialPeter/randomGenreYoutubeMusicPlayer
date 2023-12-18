import yt_dlp

ydl_opts = {'format': 'bestaudio'}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    song_info = ydl.extract_info("https://www.youtube.com/watch?v=n_l4aUnkX1U", download=False)
    audio_url = song_info['url']

print(audio_url)