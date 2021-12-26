from spotifyExtendedInteraction import SpotifyApp, Track
from personal_config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

app = SpotifyApp(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI
)

"""

Track forming

The user can create a full-fledged object of an existing track in three ways:

1. With only href (track link)

2. With only track id

3. With only track title


"""

def print_track_info(track_model):
    for elem in (track_model.name, track_model.id, track_model.href):
        print(elem)

# form track with only link
track = Track(app, href='https://open.spotify.com/track/0HhczLdgzfgQUZtkomHF69?si=6373460faf1d4929')

print_track_info(track)
# Profondo blu
# 0HhczLdgzfgQUZtkomHF69
# https://open.spotify.com/track/0HhczLdgzfgQUZtkomHF69

# form track with only id
track = Track(app=app, id='0HhczLdgzfgQUZtkomHF69')

print_track_info(track)
# Profondo blu
# 0HhczLdgzfgQUZtkomHF69
# https://open.spotify.com/track/0HhczLdgzfgQUZtkomHF69

# form track with only name
track = Track(app, name='Profondo blu')

print_track_info(track)
# Profondo blu
# 0HhczLdgzfgQUZtkomHF69
# https://open.spotify.com/track/0HhczLdgzfgQUZtkomHF69