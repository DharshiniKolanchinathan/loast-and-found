from django.db import models
from django.contrib.auth.models import User

class ChatRoom(models.Model):
    participant1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_p1')
    participant2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatroom_p2')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('participant1', 'participant2')

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
