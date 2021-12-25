from spotifyExtendedInteraction import SpotifyApp
from personal_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

app = SpotifyApp(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI)

""" .current_user_playlists() """
for playlist in app.current_user_playlists():
    print(playlist['id'])
    print(playlist['name'])
    print(playlist['description'])

