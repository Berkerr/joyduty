# reviews/urls.py
from django.urls import path
from . import views

app_name = 'reviews' # Namespace for the reviews app URLs

urlpatterns = [
    path('add/<int:content_type_id>/<int:object_id>/', views.add_review, name='add_review'),
    # Add other review-related URLs here if needed in the future
]
