#!/usr/bin/env python

import mpd, os

client = mpd.MPDClient()
client.connect("/run/mpd/socket", 6600)
status = client.status()
song = client.currentsong()
from pprint import pprint
pprint(status)

if 'time' in status:
    current, total = status['time'].split(':')
    refresh = int(total) - int(current)
else:
    # no song is playing
    refresh = 60

print(
    "Content-Type: text/plain\r\n"
    "Refresh: %(refresh)s\r\n"
    "\r\n"
    "%(artist)s - %(title)s\n"
    % {
        'artist': song['artist'],
        'title' : song['title'],
        'refresh': refresh,
    }
)

try:
    from mutagen.id3 import ID3
    music_directory = client.config()
    song_path = os.path.join(music_directory, song['file'])
    print(ID3(song_path).getall("USLT")[0])
except:
    print("Lyrics not embedded into mp3 file")

