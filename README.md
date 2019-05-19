Spotified
=========

## Auth start - returns the Spotify oAuth URL to open
http GET https://spotified.403.io/api/v1/auth/start/

## Auth finish - returns Authorization:Token 
http POST https://spotified.403.io/api/v1/auth/finish/ code=AQBgVo9ldZHlUVCP-iAZhuj-4cEcVGzyEW8UUNrfAbQr5iWRraV7wcAJUgXgJrhGPUXQ4iZj0F-bkWAD46fyWzTt65Rm-6ZXnQuPgwrw6hsRjw4ReCkG8wKwbz0YqLmP917XJYxkBGXGcpPE7wlMIz1Q3R5fJpvmIYinUpJ5ne1CdJI5Isj7LJMxQBnYbthf6ZC-6c6kZ2cJy-pvHAayiXYM6idT

## Create a playlist
http POST http://localhost:8000/api/v1/playlists/ name='aaaaaaa' 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Add a track to the playlist by URI 
http POST http://localhost:8000/api/v1/playlists/1/tracks/ spotify_id=spotify:track:1csLNQUyuhEPFiP1Qvjk9b 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Add a track to the playlist by URL
http POST https://spotified.403.io/api/v1/playlists/1/tracks/ spotify_id=https://open.spotify.com/track/3Kbriu0vdmCxd6iGDGBENw\?si\=lqHwG7qeSIaMYYXTS9f0Pw 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Vote for a playlist track up
http POST https://spotified.403.io/api/v1/playlists/1/tracks/1/vote/up/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Vote for a playlist track down
http POST https://spotified.403.io/api/v1/playlists/1/tracks/1/vote/down/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Get all playlists
http GET https://spotified.403.io/api/v1/playlists/

## Get a playlist
http GET https://spotified.403.io/api/v1/playlists/1/

## Add a Tag to Playlist
http POST https://spotified.403.io/api/v1/playlists/1/tags/ name="heavymetal" 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Get Tag by "startswith" name
http GET https://spotified.403.io/api/v1/playlists/tags/\?name\=ha 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad'

## Remove a Tag from a Playlist
http DELETE https://spotified.403.io/api/v1/playlists/1/tags/1/ 'Authorization:Token 1368c2a192d699b1a0e6a9dad75e926326d288ad' spotify_id=https://open.spotify.com/track/3Kbriu0vdmCxd6iGDGBENw\?si\=lqHwG7qeSIaMYYXTS9f0Pw 