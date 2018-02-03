#!/bin/sh

set -e

: ${MPD_LIBRARY="$HOME/Music"}

mpc_query() {
	mpc -f "$1" current
}

# obtain lyrics from mp3 file
id3_lyrics() {
	local file="$1"

	python -c '

import sys
from mutagen.id3 import ID3

try:
	print ID3(sys.argv[1]).getall("USLT")[0]
except IndexError:
	print "Lyrics not embedded into mp3 file"
	pass

' "$file"
}

artist=$(mpc_query %artist%)
title=$(mpc_query %title%)
file="$MPD_LIBRARY"/$(mpc_query %file%)

lyrics=$(id3_lyrics "$file")

printf "Content-Type: text/plain; charset=utf-8\r\n"
printf "Refresh: 60"
printf "\r\n"
printf "%s - %s\n%s\n" "$artist" "$title" "$lyrics"
