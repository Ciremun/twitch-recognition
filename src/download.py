import sys

from youtube_dl import YoutubeDL

channel = sys.argv[1]
filename = sys.argv[2]

print(filename)

ydl_opts = {
    'outtmpl': f'audio/{filename}.%(ext)s',
    'cookiefile': 'cookies.txt',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
    'quiet': True
}

ydl = YoutubeDL(ydl_opts)

ydl.download([f'https://twitch.tv/{channel}'])
