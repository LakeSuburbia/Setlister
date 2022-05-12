from base.client import MusicbrainzAPI, SetlistAPI, SpotifyAPI
from base.formatting import format_string

setlist_api = SetlistAPI()
musicbrainz_api = MusicbrainzAPI()
spotify_api = SpotifyAPI()

artist = input("Van welke artiest wou je graag de setlist? \n")


class Song:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 0
        self.position = [0] * 30

    def calculate_position(self):
        total = 0
        for i, value in enumerate(self.position):
            total += i * value
        self.final_position = total / self.count
        return self.final_position


print()
print("loading")
m_result = musicbrainz_api.get(f'/artist?query="{artist}"')
print("---------------------------")
result = setlist_api.get(
    f"/1.0/search/setlists?artistMbid={m_result['artists'][0]['id']}"
)
print("---------------------------")
print()
print()
max_length = 0
songs_dict: dict[str, Song] = {}
for setlist in result["setlist"]:
    if len(setlist["sets"]["set"]):
        setlist_length = len(setlist["sets"]["set"][0]["song"])
        max_length = max(max_length, setlist_length)
        if setlist_length > 10:
            for i, song in enumerate(setlist["sets"]["set"][0]["song"]):
                if song["name"] == "":
                    continue
                song_name = format_string(song["name"])
                if song_name in songs_dict.keys():
                    current_song = songs_dict[song_name]
                else:
                    current_song = Song()
                current_song.count += 1
                current_song.position[i] += 1
                songs_dict[song_name] = current_song

length = int((max_length + 25) / 2)
selected_songs: dict[str, Song] = dict(
    sorted(songs_dict.items(), key=lambda x: x[1].count)[:length],
)
print(artist)
print("---------------------------")
print()
sorted_songs = dict(
    sorted(selected_songs.items(), key=lambda x: x[1].calculate_position())
)
for key, value in sorted_songs.items():
    print(key, value.final_position)
print()
print("This playlist:", length)
print()
print("---------------------------")
print()
print("Creating the playlist")
print()
songs = list(sorted_songs.keys())
spotify_api.create_playlist(artist=artist, songs=songs)
print()
print("FINISHED")
