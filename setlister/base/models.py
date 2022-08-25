from __future__ import annotations

from django.db import models
from django.utils import timezone

from base.formatting import format_string


class SetlistCacheManager(models.Manager):
    def create_from_list(self, artist: Artist, songs: dict[str, Song]) -> SetlistCache:
        setlist = SetlistCache.objects.create()
        artist.setlist = setlist
        print(artist.save())
        print(artist.__dict__)
        for song in songs.values():
            song.setlist = setlist
            song.save()
            print(song.name)
        Song.objects.filter(artist=artist, setlist__isnull=True).delete()
        return setlist

    def generate_average_setlist(self, result, artist: Artist) -> dict[str, Song]:
        print("TEST")
        max_length = 0
        songs_dict: dict[str, Song] = {}
        for setlist in result["setlist"]:
            if len(setlist["sets"]["set"]):
                setlist_length = len(setlist["sets"]["set"][0]["song"])
                if setlist_length > 4:
                    max_length = max(max_length, setlist_length)
                    for i, song in enumerate(setlist["sets"]["set"][0]["song"]):
                        if song["name"] == "":
                            continue
                        song_name = format_string(song["name"])
                        if song_name in songs_dict.keys():
                            current_song = songs_dict[song_name]
                        else:
                            current_song, _ = Song.objects.get_or_create(
                                name=song_name, artist_id=artist.pk
                            )
                            current_song.count = 0
                            current_song.position = [0] * 30
                            current_song.save()
                        current_song.count += 1
                        current_song.position[i] += 1
                        songs_dict[song_name] = current_song

        length = int((max_length + 25) / 2)
        selected_songs: dict[str, Song] = dict(
            sorted(songs_dict.items(), key=lambda x: x[1].count)[:length],
        )
        print(selected_songs)
        sorted_songs = dict(
            sorted(selected_songs.items(), key=lambda x: x[1].calculate_position())
        )
        print(sorted_songs)
        return sorted_songs


class SetlistCache(models.Model):
    objects = SetlistCacheManager()
    time_created = models.DateTimeField(default=timezone.now)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    MBID = models.CharField(max_length=100, blank=True, null=True)
    spotify_uri = models.CharField(max_length=100, blank=True, null=True)
    setlist = models.ForeignKey(SetlistCache, on_delete=models.CASCADE, null=True)


class SongManager(models.Manager):
    def reset_from_artist(self, artist: Artist):
        for song in self.filter(artist=artist):
            song.reset()


class Song(models.Model):
    objects=SongManager()

    name = models.CharField(max_length=100)
    spotify_uri = models.CharField(max_length=100, null=True)
    setlist = models.ForeignKey(SetlistCache, on_delete=models.CASCADE, null=True)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)

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

    def reset(self):
        self.count = 0
        self.position = [0] * 30
        self.save()
