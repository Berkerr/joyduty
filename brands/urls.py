# brands/urls.py
from django.urls import path
from . import views  # Aynı klasördeki views.py'ı import et

app_name = 'brands'  # URL'leri namespace ile gruplamak için

urlpatterns = [
    # Marka listesi
    path('', views.brand_list, name='list'),
    # İleride marka detay sayfası için bir path eklenebilir:
    path('brand/<slug:slug>/', views.brand_detail, name='detail'),
    path('new/', views.brand_create, name='create'),
]
