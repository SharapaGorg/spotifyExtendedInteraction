import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dataclasses import dataclass, field
from json import loads
from accessify import protected
import requests
from inspect import getfullargspec


@dataclass
class UserData:
    app: str  # SpotifyApp
    id: str = field(default_factory=str)
    api_href: str = field(default_factory=str)
    href: str = field(default_factory=str)
    uri: str = field(default_factory=str)


class User(UserData):
    def __init__(self, app, id=str(), api_href=str(), href=str(), uri=str()):
        super().__init__(app, id, api_href, href, uri)

        self.app = app.app

        if not id:  # search User globally
            pass


@dataclass
class PlaylistData:
    app: str  # SpotifyApp
    name: str = field(default_factory=str)
    description: str = field(default_factory=str)
    id: str = field(default_factory=str)
    tracks: list = field(default_factory=list)
    external_urls: dict = field(default_factory=dict)
    api_href: str = field(default_factory=str)
    images: list = field(default_factory=list)
    owner: dict = field(default_factory=dict)
    public: bool = field(default_factory=False)
    snapshot_id: str = field(default_factory=str)
    uri: str = field(default_factory=str)


class Playlist(PlaylistData):
    def __init__(
        self,
        app,
        name=str(),
        description=str(),
        id=str(),
        tracks=list(),
        external_urls=dict(),
        api_href=str(),
        images=list(),
        owner=dict(),
        public=False,
        snapshot_id=str(),
        uri=str(),
    ):
        super().__init__(
            app,
            name,
            description,
            id,
            tracks,
            external_urls,
            api_href,
            images,
            owner,
            public,
            snapshot_id,
            uri,
        )

        self.app = app.app

        if not id:  # search playlist globally
            pass


@dataclass
class ArtistData:
    app: str  # SpotifyApp
    href: field(default_factory=str)
    api_href: field(default_factory=str)
    id: field(default_factory=str)
    name: field(default_factory=str)
    uri: field(default_factory=str)


class Artist(ArtistData):
    def __init__(
        self, app, href=str(), api_href=str(), id=str(), name=str(), uri=str()
    ):
        super().__init__(app, href, api_href, id, name, uri)

        self.app = app.app


@dataclass
class AlbumData:
    app: str  # SpotifyApp
    album_type: str = field(default_factory=str)
    artists: list[Artist] = field(default_factory=list)
    href: str = field(default_factory=str)
    api_href: str = field(default_factory=str)
    id: str = field(default_factory=str)
    images: list = field(default_factory=list)
    name: str = field(default_factory=str)
    release_date: str = field(default_factory=str)
    release_date_precision: str = field(default_factory=str)
    total_tracks: int = field(default_factory=int)
    uri: str = field(default_factory=str)


class Album(AlbumData):
    def __init__(
        self,
        app,
        album_type=str(),
        artists=list(),
        href=str(),
        api_href=str(),
        id=str(),
        images=list(),
        name=str(),
        release_date=str(),
        release_date_precision=str(),
        total_tracks=int,
        uri=str(),
    ):
        super().__init__(
            app,
            album_type,
            artists,
            href,
            api_href,
            id,
            images,
            name,
            release_date,
            release_date_precision,
            total_tracks,
            uri,
        )

        self.app = app.app


@dataclass
class Track:
    def __init__(
        self,
        app,
        added_at=str(),
        added_by: User = None,
        name=str(),
        id=str(),
        api_href=str(),
        duration=0,
        uri=str(),
        href=str(),
        artists: list[Artist] = list(),
        album: Album = None,
    ):
        self.app = app.app
        self.added_at = added_at
        self.added_by = added_by
        self.name = name
        self.id = id
        self.api_href = api_href
        self.duration = duration
        self.uri = uri
        self.href = href
        self.artists = artists
        self.album = album 

        if not id and name:
            searching = self.app.search(q="track:" + self.name, type="track")
            track_model = filter(searching, track_name=self.name)
            track = _form_track(app, track_model)

            for var in vars(track):
                self.__setattr__(var, track.__getattribute__(var))

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

    def current_user_playlists(self) -> list[Playlist]:
        playlists = list()

        for playlist_model in self.app.current_user_playlists().get("items"):
            tracks: list = self._get_tracks_from_playlist(
                tracks_url=playlist_model.get("tracks").get("href")
            )

            playlist = Playlist(
                self,
                name=playlist_model.get("name"),
                description=playlist_model.get("description"),
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


def filter(searching, track_name, artist_name=str()):
    for found_track in searching.get("tracks").get("items"):
        if found_track["name"].lower() == track_name.lower():
            return found_track


def _get_artists_from_field(app, artists_field):
    artists = list()
    for artist_model in artists_field:
        artist = Artist(
            app,
            href=artist_model.get("external_urls").get("spotify"),
            api_href=artist_model.get("href"),
            id=artist_model.get("id"),
            name=artist_model.get("name"),
            uri=artist_model.get("uri"),
        )
        artists.append(artist)

    return artists


def _form_track(app, track_model):
    added_by_field = track_model.get("added_by")
    track_field = track_model

    album_field = track_field.get("album")

    track_artists = _get_artists_from_field(app, track_field.get("artists"))
    album_artists = _get_artists_from_field(
        app, track_field.get("album").get("artists")
    )

    if added_by_field is not None:
        added_by_user = User(
            app,
            id=added_by_field.get("id"),
            api_href=added_by_field.get("href"),
            href=added_by_field.get("external_urls").get("spotify"),
            uri=added_by_field.get("uri"),
        )
    else:
        added_by_user = None

    track_album = Album(
        app,
        album_type=album_field.get("album_type"),
        href=album_field.get("external_urls").get("spotify"),
        api_href=album_field.get("href"),
        id=album_field.get("id"),
        images=album_field.get("images"),
        name=album_field.get("name"),
        release_date=album_field.get("release_date"),
        release_date_precision=album_field.get("release_date_precision"),
        total_tracks=album_field.get("total_tracks"),
        uri=album_field.get("uri"),
        artists=album_artists,
    )

    track = Track(
        app,
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
    return track
