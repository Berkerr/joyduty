# reviews/forms.py
from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    # Rating için seçenekleri (1-5) ve boş seçeneği biz tanımlayalım
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)] # [(1, '1'), (2, '2'), ..., (5, '5')]

    rating = forms.ChoiceField(
        choices=[('', 'Rate this... (Optional)')] + RATING_CHOICES, # Başlangıçta boş seçenek
        required=False, # Puanlama zorunlu değil
        widget=forms.Select(attrs={'class': 'form-select form-select-sm w-auto'}) # Bootstrap stili ve küçük boyut
    )

    class Meta:
        model = Review
        # Formda sadece kullanıcıdan alınacak alanları belirtiyoruz:
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4, # Metin alanının yüksekliği
                'placeholder': 'Share your thoughts and experiences...',
                'class': 'form-control' # Bootstrap stili
            }),
            # 'rating' widget'ını yukarıda ayrıca tanımladık, burada tekrar belirtmeye gerek yok
            # ama belirtseydik: 'rating': forms.Select(attrs={'class': 'form-select'})
        }
        labels = {
            'text': 'Your Review', # Alan etiketini özelleştir
            'rating': 'Your Rating',
        }
        help_texts = {
            'text': 'Please be respectful and provide constructive feedback.',
            'rating': 'Select a rating from 1 (worst) to 5 (best).',
        }