from django.urls import path
from . import views

urlpatterns = [
    path('start/<int:user_id>/', views.start_chat, name='start_chat'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('inbox/', views.chat_list, name='chat_list'),
]
