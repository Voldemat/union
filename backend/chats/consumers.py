import json
import logging

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

        # convert send method from async to sync
        self.sync_send = async_to_sync(self.send)

        # convert "send initial state" method
        self.async_send_state = sync_to_async(self._send_state)


    def _get_chat(self):
        return self.chat

    def _send_state(self) -> None:
        # check self.chat instance
        assert self.chat, 'self.chat is not defined!'
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

        # add user to self object to use it in other functions
        self.user = self.scope['user']

        # if user not logged in close websocket
        # if user.is_anonymous:
        #     logger.info('User isn`t logged in')
        #     await super().close(json.dumps({
        #         "message":"User must be authenticated"}))

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

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data['message']

        message_instance = await self.async_message_create(
            writer = self.user,
            text = text,
            chat = self.chat
        )

        message_json = MessageSerializer(message_instance).data
        logger.debug(message_json)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message_json
            }
        )

    async def chat_message(self, event):
        message = event['message']

        logger.debug(message)

        await self.send(text_data = json.dumps(message))