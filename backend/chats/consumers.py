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

    def _send_state(self):
        all_method = self.chat.messages.all

        messages = all_method()

        logger.debug(str(messages))

        json_object = MessageSerializer(messages, many = True).data

        send = async_to_sync(self.send)
        send(text_data = json.dumps(json_object))

    def _get_room_group_name(self, room_name):
        return f'chat_{room_name}'

    async def _get_chat_model(self, id:str, *args, **kwargs):
        get_instance = sync_to_async(Chat.objects.get)
        try:
            instance = await get_instance(id = id)
        except Chat.DoesNotExist:
            message = {
                "message":"Chat instance DoesNotExist!"
            }
            await super().close(json.dumps(message))
        else:
            # self.chat = instance
            return instance

    async def connect(self):
        url_kwargs = self.scope['url_route']['kwargs']
        chat_id = url_kwargs['chat_id']

        self.chat = await self._get_chat_model(id = chat_id)

        self.room_group_name = self._get_room_group_name(chat_id)

        self.user = self.scope['user']
        # # if not user close websocket
        # if user.is_anonymous:
        #     logger.info('websocket close')
        #     await super().close(json.dumps({
        #         "message":"User must be authenticated"}))
        #     return

        # logger.debug(user)
        

        logger.debug('Room group name: ' + self.room_group_name)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


        logger.info('Websocket accept')

        self._send_state = sync_to_async(self._send_state)
        await self._send_state()

        

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



        create_method = sync_to_async(Message.objects.create)
        message_instance = await create_method(
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