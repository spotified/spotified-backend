Spotified
=========

## Auth start - returns the Spotify oAuth URL to open
http GET http://localhost:8000/api/v1/auth/start/

## Auth finish - returns Authorization:Token 
http POST http://localhost:8000/api/v1/auth/finish/ code=AQBgVo9ldZHlUVCP-iAZhuj-4cEcVGzyEW8UUNrfAbQr5iWRraV7wcAJUgXgJrhGPUXQ4iZj0F-bkWAD46fyWzTt65Rm-6ZXnQuPgwrw6hsRjw4ReCkG8wKwbz0YqLmP917XJYxkBGXGcpPE7wlMIz1Q3R5fJpvmIYinUpJ5ne1CdJI5Isj7LJMxQBnYbthf6ZC-6c6kZ2cJy-pvHAayiXYM6idT

## Refresh Spotify Auth Token
http POST http://localhost:8000/api/v1/auth/token/refresh/ 'Authorization:Token '

## Create a playlist
http POST http://localhost:8000/api/v1/playlists/ name='aaaaaaa' 'Authorization:Token '

## Add a track to the playlist by URI 
http POST http://localhost:8000/api/v1/playlists/1/tracks/ spotify_id=spotify:track:1csLNQUyuhEPFiP1Qvjk9b 'Authorization:Token '

## Add a track to the playlist by URL
http POST http://localhost:8000/api/v1/playlists/1/tracks/ spotify_id=http://open.spotify.com/track/3Kbriu0vdmCxd6iGDGBENw\?si\=lqHwG7qeSIaMYYXTS9f0Pw 'Authorization:Token '

## Vote for a playlist track up
http POST http://localhost:8000/api/v1/playlists/1/tracks/1/vote/up/ 'Authorization:Token '

## Vote for a playlist track down
http POST http://localhost:8000/api/v1/playlists/1/tracks/1/vote/down/ 'Authorization:Token '

## Get all playlists
http GET http://localhost:8000/api/v1/playlists/

## Get a playlist
http GET http://localhost:8000/api/v1/playlists/1/

## Add a Tag to Playlist
http POST http://localhost:8000/api/v1/playlists/1/tags/ name="heavymetal" 'Authorization:Token '

## Get Tag by "startswith" name
http GET http://localhost:8000/api/v1/playlists/tags/\?name\=ha 'Authorization:Token '

## Remove a Tag from a Playlist
http DELETE http://localhost:8000/api/v1/playlists/1/tags/1/ 'Authorization:Token ' spotify_id=http://open.spotify.com/track/3Kbriu0vdmCxd6iGDGBENw\?si\=lqHwG7qeSIaMYYXTS9f0Pw 
