# users/forms.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# İleride özelleştirmek için temel sınıfımızı oluşturalım
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model() # Projenin aktif User modelini kullanır
        # İleride buraya ek alanlar ekleyebiliriz:
        # fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name',)
        fields = ('username', 'email') # Şimdilik sadece username ve email isteyelim