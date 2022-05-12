import json
import time
from datetime import datetime
from urllib.parse import urlencode

import requests
from requests.structures import CaseInsensitiveDict

from .formatting import compare_strings, format_string
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

    def create_playlist(self, artist: str, songs: list[str]):
        data = json.dumps(
            {
                "name": f"{artist} - setlist {datetime.now().year}",
                "description": f"This is an estimation of what a setlist of {artist} would look like.",
                "public": True,
            }
        )
        playlist = self.post(
            f"{apiurls.SPOTIFY}/users/21dx3vvgs2hunjbzvezp4dp5q/playlists",
            headers=self.HEADERS,
            data=data,
        )["id"]
        song_uris = self._get_songs(artist, songs)
        new_songs = list(map(lambda x: "spotify%3Atrack%3A" + x, song_uris))
        add_to_playlist_url = (
            f"{apiurls.SPOTIFY}/playlists/{playlist}/tracks?uris={','.join(new_songs)}"
        )
        return requests.post(add_to_playlist_url, headers=self.HEADERS)

    def _get_songs(self, artist: str, songs: list[str]):
        uris = []
        for song in songs:
            print(f"trying to find {song}")
            params = urlencode({"q": f"track:{song}, artist:{artist}", "type": "track"})
            try:
                tracks = self.get(
                    f"{apiurls.SPOTIFY}/search?{params}", headers=self.HEADERS
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
