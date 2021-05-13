from django.shortcuts import render
from django.http import Http404

from chats.models import Chat, Message
# Create your views here.
def index(request):
    return render(request, 'chats/index.html')

def chat(request, id):
    if not request.user.is_authenticated:
        raise Http404
    instance = Chat.objects.get_or_create(id = id, users = request.user.id)[0]
    return render(request, 'chats/room.html', {
        'chat_id': str(instance.id)
    })