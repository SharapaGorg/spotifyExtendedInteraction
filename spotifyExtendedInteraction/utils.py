import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dataclasses import dataclass
from json import loads
from accessify import protected
import requests


@dataclass
class User:
    id: str
    api_href: str
    href: str
    uri: str


@dataclass
class Playlist:
    name: str
    descripton: str
    id: str
    tracks: list
    external_urls: dict
    api_href: str
    images: list
    owner: dict
    public: bool
    snapshot_id: str
    uri: str


@dataclass
class Artist:
    href : str
    api_href : str
    id : str
    name : str
    uri : str

@dataclass
class Album:
    album_type : str
    artists : list[Artist]
    href : str
    api_href : str
    id : str
    images : list
    name : str
    release_date : str
    release_date_precision : str
    total_tracks : int
    uri : str

@dataclass
class Track:
    added_at: str
    added_by: User
    name: str
    id: str
    api_href: str
    duration: int  # milliseconds
    uri: str
    href: str
    artists: list[Artist]
    album: Album


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

    @protected
    def _get_artists_from_field(self, artists_field) -> list[Artist]:
        artists = list()
        for artist_model in artists_field:
            artist = Artist(
                href = artist_model.get('external_urls').get('spotify'),
                api_href=artist_model.get('href'),
                id=artist_model.get('id'),
                name=artist_model.get('name'),
                uri=artist_model.get('uri')
            )
            artists.append(artist)

        return artists

    @protected
    def _get_tracks_from_playlist(self, tracks_url) -> list[Track]:
        tracks_request_link = (
            tracks_url + "?access_token=" + self.cache.get("access_token")
        )
        tracks_source: list = loads(requests.get(tracks_request_link).text).get("items")
        tracks = list()

        for track_model in tracks_source:
            added_by_field = track_model.get('added_by')
            track_field = track_model.get("track")
            album_field = track_field.get('album')

            track_artists = self._get_artists_from_field(track_field.get('artists'))
            album_artists = self._get_artists_from_field(track_field.get('album').get('artists'))

            added_by_user = User(id=added_by_field.get('id'),
                                api_href=added_by_field.get('href'),
                                href=added_by_field.get('external_urls').get('spotify'),
                                uri=added_by_field.get('uri'))

            track_album = Album(
                album_type=album_field.get('album_type'),
                href = album_field.get('external_urls').get('spotify'),
                api_href=album_field.get('href'),
                id = album_field.get('id'),
                images=album_field.get('images'),
                name=album_field.get('name'),
                release_date=album_field.get('release_date'),
                release_date_precision=album_field.get('release_date_precision'),
                total_tracks=album_field.get('total_tracks'),
                uri=album_field.get('uri'),
                artists = album_artists
            )

            track = Track(
                added_at=track_model.get("added_at"),
                added_by=added_by_user,
                name=track_field.get("name"),
                id=track_field.get("id"),
                api_href=track_field.get("href"),
                duration=track_field.get("duration_ms"),
                uri=track_field.get("uri"),
                href=track_field.get("external_urls").get("spotify"),
                artists=track_artists,
                album=track_album,
            )
            tracks.append(track)

        return tracks

    def current_user_playlists(self) -> list[Playlist]:
        playlists = list()

        for playlist_model in self.app.current_user_playlists().get("items"):
            tracks: list = self._get_tracks_from_playlist(
                tracks_url=playlist_model.get("tracks").get("href")
            )

            playlist = Playlist(
                name=playlist_model.get("name"),
                descripton=playlist_model.get("description"),
                id=playlist_model.get("id"),
                external_urls=playlist_model.get("external_urls"),
                api_href=playlist_model.get("href"),
                images=playlist_model.get("images"),
                owner=playlist_model.get("owner"),
                public=playlist_model.get("public"),
                snapshot_id=playlist_model.get("snapshot_id"),
                uri=playlist_model.get("uri"),
                tracks=tracks,
            )

            playlists.append(playlist)

        return playlists
        # return self.app.current_user_playlists().get('items')[0]['tracks']['href'] + '?access_token=' + self.cache.get('access_token')
