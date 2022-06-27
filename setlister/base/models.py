from django.db import models


# Create your models here.
class Song(models.Model):
    name = models.CharField(max_length=100)
    spotify_uri = models.CharField(max_length=100)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    spotify_uri = models.CharField(max_length=100)
