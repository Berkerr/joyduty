# users/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = 'users'

urlpatterns = [
    # /accounts/register/ -> Kayıt sayfası
    path('register/', views.register_view, name='register'),
    # İleride profil sayfası vb. eklenebilir
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('inventory/', views.inventory_list_view, name='inventory_list'),
    path('login/', LoginView.as_view(template_name='accounts/login.html', next_page='accounts:inventory_list'), name='login'),
]
