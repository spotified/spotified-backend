Spotified
=========

# Auth start - returns the Spotify oAuth URL to open
http GET https://spotified.403.io/api/v1/auth/start/

# Auth finish - returns Authorization:Token 
http POST https://spotified.403.io/api/v1/auth/finish/ code=AQBgVo9ldZHlUVCP-iAZhuj-4cEcVGzyEW8UUNrfAbQr5iWRraV7wcAJUgXgJrhGPUXQ4iZj0F-bkWAD46fyWzTt65Rm-6ZXnQuPgwrw6hsRjw4ReCkG8wKwbz0YqLmP917XJYxkBGXGcpPE7wlMIz1Q3R5fJpvmIYinUpJ5ne1CdJI5Isj7LJMxQBnYbthf6ZC-6c6kZ2cJy-pvHAayiXYM6idT

# Create a playlist
http POST https://spotified.403.io/api/v1/playlists/ 'Authorization:Token 24993d9a20433816c5bdaeb86a3f0c8b650b6c32' name='aaaaaaa'

# Add a track to the playlist by URI 
http POST https://spotified.403.io/api/v1/playlists/1/tracks/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad' spotify_id=spotify:track:1csLNQUyuhEPFiP1Qvjk9b

# Add a track to the playlist by URL
http POST https://spotified.403.io/api/v1/playlists/1/tracks/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad' spotify_id=https://open.spotify.com/track/3Kbriu0vdmCxd6iGDGBENw\?si\=lqHwG7qeSIaMYYXTS9f0Pw

# Vote for a playlist track up
http POST https://spotified.403.io/api/v1/playlists/1/tracks/1/vote/up/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

# Vote for a playlist track down
http POST https://spotified.403.io/api/v1/playlists/1/tracks/1/vote/down/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

# Get all playlists
http GET https://spotified.403.io/api/v1/playlists/

# Get a playlist
http GET https://spotified.403.io/api/v1/playlists/1/