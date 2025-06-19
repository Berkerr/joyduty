from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.location_list, name='list'),
    path('category/<slug:category_slug>/', views.location_list, name='list_by_category'),
    path('detail/<int:pk>/', views.location_detail_by_pk, name='detail_by_pk'),
    path('detail/<int:pk>/review/', views.location_review_create, name='location_review_create'),
    path('new/', views.location_create, name='create'),
]
