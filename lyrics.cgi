#!/usr/bin/env python2

import os
import mpd
from mutagen.id3 import ID3

client = mpd.MPDClient()
client.connect("/run/mpd/socket", 6600)
status = client.status()
song = client.currentsong()

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

music_directory = '/var/lib/mpd/music'
song_path = os.path.join(music_directory, song['file'])
print(song_path)
print(ID3(song_path).getall("USLT")[0])
