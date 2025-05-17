"""
joyduty URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views # core app'in view'larını import et

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('core.urls')), # Include core app URLs
    path('admin/', admin.site.urls),
    path('messages/', include('messaging.urls')),
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('brands/', include('brands.urls', namespace='brands')),
    path('caravans/', include('caravans.urls', namespace='caravans')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('locations/', include('locations.urls', namespace='locations')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
