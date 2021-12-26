from json import loads
import requests

from .contants import TRACK_PREFIX


class User:
    def __init__(
        self,
        app,
        display_name=str(),
        id=str(),
        api_href=str(),
        href=str(),
        uri=str(),
        followers=int,
    ):
        self.app = app.app
        self.display_name = display_name
        self.id = id
        self.api_href = api_href
        self.href = href
        self.uri = uri
        self.followers = followers

    def __repr__(self):
        return _default_repr(self)


class Playlist:
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
        self.app = app.app
        self.name = name
        self.description = description
        self.id = id
        self.tracks = tracks
        self.external_urls = external_urls
        self.api_href = api_href
        self.images = images
        self.owner = owner
        self.public = public
        self.snapshot_id = snapshot_id
        self.uri = uri

        if not id and name:
            """
            searching playlist globally
            """

    def __repr__(self) -> str:
        return _default_repr(self)

    def __str__(self) -> str:
        return self.name


class Artist:
    def __init__(
        self, app, href=str(), api_href=str(), id=str(), name=str(), uri=str()
    ):
        self.app = app.app
        self.href = href
        self.api_href = api_href
        self.id = id
        self.name = name
        self.uri = uri

        if not id and name:
            """
            searching artist globally
            """
            pass

    def __repr__(self) -> str:
        return _default_repr(self)


class Album:
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

        self.app = app
        self.album_type = album_type
        self.artists = artists
        self.href = href
        self.api_href = api_href
        self.id = id
        self.images = images
        self.name = name
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.total_tracks = total_tracks
        self.uri = uri

        if not id and name:
            """
            searching album globally
            """
            pass

    def __repr__(self) -> str:
        return _default_repr(self)

    def __str__(self) -> str:
        return self.name


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

        ignore_vars = ["added_by", "added_at"]
        if not self.id and self.name:
            """
            searching track globally
            """

            searching = self.app.search(q="track:" + self.name, type="track")
            track_model = filter(searching, track_name=self.name)
            track = _form_track(app, track_model)

            _copy_all_vars(track, self)

        all_exist = True
        for var in vars(self):
            if (
                self.__getattribute__(var) is None
                and var != "id"
                and var not in ignore_vars
            ):
                all_exist = False
                break

        if self.id and not all_exist:
            track = _form_track(app, self.app.track(self.id))

            _copy_all_vars(track, self)

        if self.href and not all_exist:
            track_id = self.href.lstrip(TRACK_PREFIX)[:22]
            track = _form_track(app, self.app.track(track_id))

            _copy_all_vars(track, self)

    def __repr__(self) -> str:
        return _default_repr(self)

    def __str__(self) -> str:
        return self.name


def _form_track(app, track_model):
    added_by_field = track_model.get("added_by")
    if "track" in track_model:
        track_field = track_model.get("track")
    else:
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


def _form_playlist(app, playlist_model) -> Playlist:
    tracks = _get_tracks_from_playlist(
        app, tracks_url=playlist_model.get("tracks").get("href")
    )

    playlist = Playlist(
        app,
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

    return playlist


def _form_user(app, user_model):
    user = User(
        app,
        display_name=user_model.get("display_name"),
        href=user_model.get("external_urls").get("spotify"),
        followers=user_model.get('followers').get('total'),
        api_href=user_model.get('href'),
        id=user_model.get('id'),
        uri=user_model.get('uri')
    )

    return user


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


def _get_tracks_from_playlist(app, tracks_url: str):
    tracks_request_link = tracks_url + "?access_token=" + app.cache.get("access_token")
    tracks_source: list = loads(requests.get(tracks_request_link).text).get("items")
    tracks = list()

    for track_model in tracks_source:
        track = _form_track(app, track_model)
        tracks.append(track)

    return tracks


def _type_filter(var_value):
    result_var = str()

    if isinstance(var_value, str):
        result_var = f'"{var_value}"'
    elif isinstance(var_value, int):
        result_var = var_value
    elif isinstance(var_value, bool):
        result_var = var_value
    elif isinstance(var_value, list):
        result_var = (
            var_value.__class__.__name__ + "[" + _type_filter(var_value[0]) + "]"
        )
    elif var_value is None:
        result_var = var_value
    else:
        result_var = var_value.__class__.__name__

    return result_var


def _default_repr(object):
    result = str()
    for var in vars(object):
        var_value = object.__getattribute__(var)
        result_var = _type_filter(var_value)

        result += f"{var}={result_var}, "
    result = result.rstrip(", ")

    return f"{object.__class__.__name__}({result})"


def _copy_all_vars(from_object, to_object):
    for var in vars(from_object):
        to_object.__setattr__(var, from_object.__getattribute__(var))
