#!/usr/bin/env python2

import os
import mpd
from mutagen.id3 import ID3

client = mpd.MPDClient()
client.connect("/run/mpd/socket", 6600)
music_directory = '/var/lib/mpd/music'

song = client.currentsong()

# get lyrics first, it may take time on slow RPI1 so the Refresh gets out of sync
song_path = os.path.join(music_directory, song['file'])
lyrics = ID3(song_path).getall("USLT")[0]

status = client.status()
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
    "%(lyrics)s"
    % {
        'artist': song['artist'],
        'title' : song['title'],
        'refresh': refresh,
        'lyrics': lyrics,
    }
)
