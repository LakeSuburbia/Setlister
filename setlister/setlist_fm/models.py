from django.db import models
from django.utils import timezone


# Create your models here.
class SetlistCache(models.Model):
    time_created = models.DateTimeField(default=timezone.now())
    artist = models.CharField(max_length=100)
