from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list, name='conversation_list'),
    path('<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('create/<int:user_id>/', views.create_conversation, name='create_conversation'),
    path('<int:pk>/send/', views.send_message, name='send_message'),
    path('<int:pk>/read/', views.mark_conversation_as_read, name='mark_conversation_as_read'),
]
