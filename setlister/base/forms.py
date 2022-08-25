from django import forms
from base.models import Artist


# creating a form
class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name"]
