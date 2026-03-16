from django.urls import re_path
from . import consumers as chat_consumers
from notifications import consumers as notify_consumers

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_id>\d+)/$', chat_consumers.ChatConsumer.as_asgi()),
    re_path(r'^ws/notifications/$', notify_consumers.NotificationConsumer.as_asgi()),
]
