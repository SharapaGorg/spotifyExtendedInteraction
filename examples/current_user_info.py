from spotifyExtendedInteraction import SpotifyApp, Track
from personal_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

app = SpotifyApp(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI
)


for playlist in app.current_user_playlists():
    print(playlist)