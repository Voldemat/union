import json
import logging

from rest_framework.authtoken.models import Token
from asgiref.sync import sync_to_async, async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

from chats.models import Chat, Message
from chats.serializers import MessageSerializer

# logging flow
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.setLevel(logging.DEBUG)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

class ChatConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """Converting async and sync functions"""
        # define chat get_instance methods
        self.sync_chat_get = Chat.objects.get
        self.async_chat_get = sync_to_async(self.sync_chat_get)

        # define messages create method 
        self.sync_message_create = Message.objects.create
        self.async_message_create = sync_to_async(self.sync_message_create)


        self.async_get_user:callable = sync_to_async(self.sync_get_user)
        # convert send method from async to sync
        self.sync_send = async_to_sync(self.send)

        # convert "send initial state" method
        self.async_send_state = sync_to_async(self._send_state)


    def _send_state(self) -> None:
        # get all messages in current chat
        messages:list[Message] = self.chat.messages.all()

        logger.debug(str(messages))

        # parse messages throw serializer into json
        json_object:list[dict] = MessageSerializer(messages, many = True).data

        # send serialized messages - initial state
        self.sync_send(text_data = json.dumps(json_object))

        return None


    async def _get_chat_model(self, id:str, *args:list, **kwargs:dict):
        try:
            instance = await self.async_chat_get(id = id)
        except Chat.DoesNotExist:
            message = {
                "message":"Chat instance DoesNotExist!"
            }
            await super().close(json.dumps(message))
        else:
            # self.chat = instance
            return instance

    async def connect(self):
        # get chat id from url
        chat_id = self.scope['url_route']['kwargs']['chat_id']

        # get chat instance 
        self.chat = await self._get_chat_model(id = chat_id)

        # generate room group name from chat id
        self.room_group_name = f'chat_{chat_id}'



        # add chat to channel layer
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # accepting websocket connection && switching protocol HTTP 101
        await self.accept()


        # send initial state (later messages)
        await self.async_send_state()

        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().close(close_code)


    def sync_get_user(self, token:str):
        try:
            user:object = Token.objects.get(key = token).user
            
        except Token.DoesNotExist:
            self.send(json.dumps({
                "error":"wrong user token"
            }))
        return user
    async def receive(self, text_data:str):
        data:dict = json.loads(text_data)

        user = await self.async_get_user(token = data['token'])
        
        try:
            message_instance = await self.async_message_create(
                writer = user,
                text = data['message'],
                chat = self.chat
            )
        except:
            self.send(json.dumps({
                "error":"Message text must be not blank"
                }))
            return

        
        def get_message_data():
            return MessageSerializer(message_instance, many = False).data


        message_json = await sync_to_async(get_message_data)()

    
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message_json
            }
        )

    async def chat_message(self, event):
        message = event['message']

        logger.debug(f'Message: {message}')

        await self.send(text_data = json.dumps(message))

