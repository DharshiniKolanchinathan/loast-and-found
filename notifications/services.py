from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Notification

def create_notification(user, title, message):
    """
    Creates a notification in DB and sends it via WebSocket if user is online.
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notify_{user.id}",
        {
            "type": "send_notification",
            "title": title,
            "message": message
        }
    )
    return notification
