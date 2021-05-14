from django.shortcuts import render
from django.http import Http404

from chats.models import Chat, Message
# Create your views here.
def index(request):
    return render(request, 'chats/index.html')

def chat(request, id):
    try:
        instance = Chat.objects.get(id = id)
    except Chat.DoesNotExist:
        raise Http404

    else:
        return render(request, 'chats/room.html', {
            'chat_id': str(instance.id)
        })