import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

class ChatConsumer(AsyncWebsocketConsumer):

    def _get_room_group_name(self, room_name):
        return f'chat_{room_name}'
    async def connect(self):
        url_kwargs = self.scope['url_route']['kwargs']
        self.room_name = url_kwargs['room_name']

        user = self.scope['user']
        # if not user close websocket
        if user.is_anonymous:
            print('websocket close')
            await super().close(close_code = json.dumps({
                "message":"User must be authenticated"}))

        print(user)
        self.room_group_name = self._get_room_group_name(self.room_name)

        print('___________')

        print(dir(self))
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await super().close(close_code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data = json.dumps({
            'message':message
        }))