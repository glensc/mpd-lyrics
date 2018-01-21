#!/bin/sh
# https://gist.github.com/febuiles/1549991

: ${MPD_HOST=localhost}

artist=$(mpc -h $MPD_HOST -f %artist% current)
title=$(mpc -h $MPD_HOST -f %title% current)
song=$(curl -s --get "https://makeitpersonal.co/lyrics" --data-urlencode "artist=$artist" --data-urlencode "title=$title")

printf "%s - %s\n%s" "$artist" "$title" "$song"
