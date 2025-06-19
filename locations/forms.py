from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'category', 'description', 'latitude', 'longitude', 'is_approved']
