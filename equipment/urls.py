from django.urls import path
from . import views # Aynı klasördeki views.py'ı import et

app_name = 'equipment' # URL'leri namespace ile gruplamak için (önemli!)

urlpatterns = [
    # /equipment/ -> Ekipman listesi
    path('', views.equipment_list, name='list'),
    # /equipment/category/<slug:category_slug>/ -> Kategoriye göre filtreli liste
    path('category/<slug:category_slug>/', views.equipment_list, name='list_by_category'),
    # /equipment/brand/<slug:brand_slug>/ -> Markaya göre filtreli liste
    path('brand/<slug:brand_slug>/', views.equipment_list, name='list'),
    # /equipment/kategori-slug/marka-slug/ekipman-slug/ -> Ekipman detayı (slug ile)
    path('category/<slug:category_slug>/brand/<slug:brand_slug>/<slug:equipment_slug>/', views.equipment_detail_by_slugs, name='detail_by_slugs'),
    # /equipment/<int:pk>/ -> Ekipman detayı (PK ile)
    path('<int:pk>/', views.equipment_detail_by_pk, name='detail_by_pk'),
    path('new/', views.equipment_create, name='create'),
]
