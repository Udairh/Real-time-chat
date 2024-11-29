import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = f'chat_{self.room_name}'

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"WebSocket connected to room: {self.room_name}")
        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"WebSocket disconnected from room: {self.room_name}")
        except Exception as e:
            logger.error(f"Error during WebSocket disconnection: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            message_type = text_data_json.get('messageType', 'user-message')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'messageType': message_type
                }
            )
            logger.info(f"Message received: {message}")
        except Exception as e:
            logger.error(f"Error during message reception: {e}")

    async def chat_message(self, event):
        try:
            message = event['message']
            message_type = event.get('messageType', 'user-message')
            await self.send(text_data=json.dumps({
                'message': message,
                'messageType': message_type
            }))
            logger.info(f"Message sent to WebSocket: {message}")
        except Exception as e:
            logger.error(f"Error during message broadcast: {e}")
