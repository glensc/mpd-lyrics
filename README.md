# mpd-lyrics

Display Lyrics for current MPD song.

Fetches from https://makeitpersonal.co, caches result in .mp3 file itself.

## Configuration

- **MPD_HOST** Specifies the hostname of the mpd server. This can be a hostname, IP
  address or an absolute path. If it is an absolute path, mpc will use Unix
  Domain Sockets instead of TCP/IP. If the server requires a password, it can
  be specified using password@host in the MPD_HOST variable.
- **MPD_LIBRARY** Path to `music_directory`
