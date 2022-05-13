import time
from datetime import datetime

import requests
import spotipy
from requests.structures import CaseInsensitiveDict
from spotipy.oauth2 import SpotifyOAuth

from .formatting import compare_strings
from .settings import ApiKeys, ApiURLS

apikeys = ApiKeys()
apiurls = ApiURLS()


class BaseAPI:
    HEADERS = CaseInsensitiveDict()

    def __init__(self):
        self.HEADERS["Accept"] = "application/json"
        self.HEADERS["Content-Type"] = "application/json"

    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs).json()

    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs).json()


class SetlistAPI(BaseAPI):
    def __init__(self):
        super(SetlistAPI, self).__init__()
        self.HEADERS["x-api-key"] = apikeys.SETLIST_FM

    def get(self, path, *args, **kwargs):
        url = apiurls.SETLIST_FM
        if path[0] != "/":
            url += "/"
        url += path
        time.sleep(0.5)
        return super().get(url, headers=self.HEADERS, *args, **kwargs)


class SpotifyAPI(BaseAPI):
    def __init__(self):
        self.HEADERS["Authorization"] = apikeys.SPOTIFY
        scope = "playlist-modify-public"
        self.user = "21dx3vvgs2hunjbzvezp4dp5q"
        self.api = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=apikeys.SPOTIFY_CLIENT_ID,
                client_secret=apikeys.SPOTIFY_CLIENT_SECRET,
                redirect_uri="http://localhost",
                scope=scope,
            )
        )

    def create_playlist(self, artist: str, songs: list[str]):
        playlist = self.api.user_playlist_create(
            user=self.user,
            name=f"{artist} - setlist {datetime.now().year}",
            public=True,
            description=f"This is an estimation of what a setlist of {artist} would look like.",
        )["id"]
        song_uris = self._get_songs(artist, songs)
        return self.api.user_playlist_add_tracks(
            user=self.user, playlist_id=playlist, tracks=song_uris
        )

    def _get_songs(self, artist: str, songs: list[str]):
        uris = []
        for song in songs:
            print(f"trying to find {song}")
            try:
                tracks = self.api.search(
                    q=f"track:{song}, artist:{artist}", type="track"
                )["tracks"]["items"]
                new_track = None
                for track in tracks:
                    for art in track["artists"]:
                        if compare_strings(art["name"], artist):
                            new_track = track["id"]
                            break
                    if new_track:
                        uris.append(new_track)
                        break
                if new_track:
                    print("Succeeded")
                else:
                    print("Failed")
            except IndexError:
                print("failed")
        return uris


class MusicbrainzAPI(BaseAPI):
    def __init__(self):
        super(MusicbrainzAPI, self).__init__()
        self.HEADERS["User-Agent"] = apikeys.MUSICBRAINZ

    def get(self, path, *args, **kwargs):
        url = apiurls.MUSICBRAINZ
        if path[0] != "/":
            url += "/"
        url += path
        return super().get(url, headers=self.HEADERS, *args, **kwargs)
