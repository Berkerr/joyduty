"""
joyduty URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views # core app'in view'larını import et
from django.shortcuts import redirect # Import redirect

def home_redirect_view(request):
    if request.user.is_authenticated:
        return core_views.home(request)
    else:
        return core_views.landing_page(request=request)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('', home_redirect_view, name='home'), # Use the custom redirect view for the root URL
    path('admin/', admin.site.urls),
    path('messages/', include('messaging.urls')),
    path('equipment/', include('equipment.urls', namespace='equipment')),
    path('brands/', include('brands.urls', namespace='brands')),
    path('caravans/', include('caravans.urls', namespace='caravans')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('locations/', include('locations.urls', namespace='locations')),
]

# Static pages URLs
urlpatterns += [
    path('about/', core_views.about_view, name='about'),
    path('contact/', core_views.contact_view, name='contact'),
    path('privacy-policy/', core_views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', core_views.terms_of_service_view, name='terms_of_service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add a separate URL pattern for the timeline page for logged-in users
urlpatterns += [
    path('timeline/', core_views.home, name='timeline'),
]
