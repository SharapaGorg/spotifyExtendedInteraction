from spotifyExtendedInteraction import SpotifyApp, Track
from personal_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

app = SpotifyApp(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI
)


track_name = 'Nuovi orizzonti'
track = Track(app=app, name=track_name)
print(track.name, track.id)