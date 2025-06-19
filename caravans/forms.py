from django import forms
from .models import CaravanModel

class CaravanModelForm(forms.ModelForm):
    class Meta:
        model = CaravanModel
        fields = ['brand', 'model_name', 'type', 'year_start', 'year_end', 'description', 'length_mm', 'width_mm', 'height_mm', 'max_weight_kg', 'berths', 'equipments', 'is_approved']
