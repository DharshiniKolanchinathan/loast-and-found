from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage

@login_required
def start_chat(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    if other_user == request.user:
        return redirect('dashboard')
    
    # Ensure participant1 is the user with smaller ID for uniqueness
    u1, u2 = sorted([request.user, other_user], key=lambda x: x.id)
    
    room, created = ChatRoom.objects.get_or_create(participant1=u1, participant2=u2)
    return redirect('chat_room', room_id=room.id)

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in [room.participant1, room.participant2]:
        return redirect('dashboard')
    
    messages = room.messages.all()
    return render(request, 'chat/room.html', {
        'room': room,
        'chat_messages': messages,
    })

@login_required
def chat_list(request):
    rooms = ChatRoom.objects.filter(Q(participant1=request.user) | Q(participant2=request.user))
    return render(request, 'chat/chat_list.html', {
        'rooms': rooms
    })
