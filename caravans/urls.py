
# caravans/urls.py
from django.urls import path
from . import views # Aynı klasördeki views.py'ı import et

app_name = 'caravans' # URL'leri namespace ile gruplamak için

urlpatterns = [
    # /caravans/ -> Karavan listesi (tümü)
    path('', views.caravan_list, name='list'),
    # /caravans/type/<slug:type_slug>/ -> Tipe göre filtreli liste
    path('type/<slug:type_slug>/', views.caravan_list, name='list_by_type'),
    # /caravans/brand/<slug:brand_slug>/ -> Markaya göre filtreli liste
    path('brand/<slug:brand_slug>/', views.caravan_list, name='list'),

    # --- Detay Sayfası URL'leri (Şimdilik sadece PK bazlıyı ekleyelim) ---
    # /caravans/detail/<int:pk>/
    path('detail/<int:pk>/', views.caravan_detail_by_pk, name='detail_by_pk'),
    # İleride slug tabanlı detay URL'si:
    path('<slug:brand_slug>/<slug:model_slug>/', views.caravan_detail_by_slugs, name='detail_by_slugs'),
    path('new/', views.caravan_create, name='create'),
]
