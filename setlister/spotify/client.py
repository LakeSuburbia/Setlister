sfrom datetime import datetime

import spotipy
from base.client import BaseAPI
from base.formatting import compare_strings
from setlister.settings import ApiKeys, ApiURLS
from spotipy.oauth2 import SpotifyOAuth

apikeys = ApiKeys()
apiurls = ApiURLS()


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