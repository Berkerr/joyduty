from django import forms
from .models import Brand

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'logo', 'country_of_origin', 'description']
