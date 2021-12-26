import spotipy
from spotipy import SpotifyOAuth
from json import loads
from .utils import _form_user, _form_playlist
from .utils import _default_repr


class SpotifyApp:
    def __init__(
        self,
        client_id,
        client_secret,
        redirect_uri,
        scope="playlist-modify-public",
    ):

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.app = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=self.scope,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
            )
        )

        with open(".cache", "r") as cache:
            self.cache = loads(cache.read())

    def current_user(self):
        user_model = self.app.current_user()
        return _form_user(self, user_model)


    def current_user_playlists(self):
        playlists = list()

        for playlist_model in self.app.current_user_playlists().get("items"):
            playlist = _form_playlist(self, playlist_model)            
            playlists.append(playlist)

        return playlists


    def __repr__(self) -> str:
        return _default_repr(self)