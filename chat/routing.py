from django.urls import path
from . import consumers as chat_consumers
from notifications import consumers as notify_consumers

websocket_urlpatterns = [
    path('ws/chat/<int:room_id>/', chat_consumers.ChatConsumer.as_asgi()),
    path('ws/notifications/', notify_consumers.NotificationConsumer.as_asgi()),
]
