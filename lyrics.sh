#!/bin/sh
# https://gist.github.com/febuiles/1549991

set -e

: ${MPD_HOST=localhost}
: ${MPD_LIBRARY="$HOME/Music"}

mpc_query() {
	mpc -h "$MPD_HOST" -f "$1" current
}

# obtain lyrics from mp3 file
id3_lyrics() {
	local file="$1"
	kid3-cli -c "get Lyrics" "$file"
}

save_id3_lyrics() {
	local file="$1" lyrics="$2" t=$(mktemp)

	echo "$lyrics" > "$t"
	eyeD3-py3 --preserve-file-times --add-lyrics="$t" "$file"
	rm "$t"
}

# fetch lyrics from net
fetch_lyrics() {
	local artist="$1" title="$2"

	curl -s --get "https://makeitpersonal.co/lyrics" --data-urlencode "artist=$artist" --data-urlencode "title=$title"
}

get_lyrics() {
	local file="$1" artist="$2" title="$3" lyrics

	lyrics=$(id3_lyrics "$file")
	if [ -z "$lyrics" ]; then
		lyrics=$(fetch_lyrics "$artist" "$title")
		lyrics=$(echo "$lyrics" | grep -v "Sorry, We don't have lyrics for this song yet.")

		if [ -n "$lyrics" ]; then
			save_id3_lyrics "$file" "$lyrics" >&2
		fi
	fi

	echo "$lyrics"
}

artist=$(mpc_query %artist%)
title=$(mpc_query %title%)
file="$MPD_LIBRARY"/$(mpc_query %file%)

lyrics=$(get_lyrics "$file" "$artist" "$title")

printf "%s - %s\n%s\n" "$artist" "$title" "$lyrics"
