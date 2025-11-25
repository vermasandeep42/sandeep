from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model
from profiles.models import Connection
from .models import Message

User = get_user_model()

@login_required
def send_interest(request, user_id):
    receiver = get_object_or_404(User, pk=user_id)
    if request.user != receiver:
        Connection.objects.get_or_create(sender=request.user, receiver=receiver)
    return redirect('dashboard')

@login_required
def matches_list(request):
    connections = Connection.objects.filter(
        (Q(sender=request.user) | Q(receiver=request.user)),
        status='accepted'
    )
    matches = []
    for conn in connections:
        if conn.sender == request.user:
            matches.append(conn.receiver)
        else:
            matches.append(conn.sender)
            
    # Also show pending requests received
    pending_requests = Connection.objects.filter(receiver=request.user, status='pending')
    
    return render(request, 'communication/matches.html', {'matches': matches, 'pending_requests': pending_requests})

@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user))
    )
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('chat_view', user_id=user_id)
            
    return render(request, 'communication/chat.html', {'other_user': other_user, 'messages': messages})
