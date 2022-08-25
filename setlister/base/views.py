from django.http import HttpResponse
from django.shortcuts import render
from setlist_fm.client import MusicbrainzAPI, SetlistAPI
from spotify.client import SpotifyAPI

from base.formatting import format_string
from base.forms import ArtistForm
from base.models import Artist, SetlistCache, Song

setlist_api = SetlistAPI()
music_brainz_api = MusicbrainzAPI()
spotify_api = SpotifyAPI()


# Create your views here.
def index(request):
    form = ArtistForm()
    return render(request, "index.html", {"form": form})


def artist_view(request):
    if request.method == "POST":
        form = ArtistForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            print(name)
            artist, _ = Artist.objects.get_or_create(name=name)
            print(artist)
            if not artist.MBID:
                m_result = music_brainz_api.get(f'/artist?query="{name}"')
                artist.MBID = m_result["artists"][0]["id"]
                artist.save()
            print(artist.MBID)
            if not artist.setlist:
                result = setlist_api.get(
                    f"/1.0/search/setlists?artistMbid={artist.MBID}"
                )
                max_length = 0
                songs_dict: dict[str, Song] = {}
                Song.objects.reset_from_artist(artist)
                for setlist in result["setlist"]:
                    if len(setlist["sets"]["set"]):
                        setlist_length = len(setlist["sets"]["set"][0]["song"])
                        if setlist_length > 4:
                            max_length = max(max_length, setlist_length)
                            for i, song in enumerate(setlist["sets"]["set"][0]["song"]):
                                if song["name"] == "":
                                    continue
                                song_name = format_string(song["name"])
                                current_song, _ = Song.objects.get_or_create(name=song_name, artist=artist)
                                current_song.count += 1
                                current_song.position[i] += 1
                                current_song.save()
                                songs_dict[song_name] = current_song
                length = int((max_length + 25) / 2)
                selected_songs: dict[str, Song] = dict(
                    sorted(songs_dict.items(), key=lambda x: x[1].count)[:length],
                )
                sorted_songs = dict(
                    sorted(
                        selected_songs.items(), key=lambda x: x[1].calculate_position()
                    )
                )
                print(sorted_songs)
                setlist_obj = SetlistCache.objects.create_from_list(
                    artist, sorted_songs
                )
                print(setlist_obj)
                artist.setlist = setlist_obj
                artist.save()
            print(artist.setlist)
            return render(
                request,
                "artist.html",
                {"songs": list(sorted_songs.items()), "artist": artist.name, "MBID": artist.MBID},
            )
    # if a GET (or any other method) we'll create a blank form
    else:
        form = ArtistForm()
    return render(request, "index.html", {"form": form})
