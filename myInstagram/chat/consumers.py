import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 전역 채팅방 설정
        self.room_group_name = 'global_chat'

        # 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 탈퇴
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info(f"Received data: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        nickname = text_data_json['nickname']

        # 메시지를 같은 그룹의 모든 클라이언트에 브로드캐스트
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'nickname': nickname
            }
        )

    async def chat_message(self, event):
        message = event['message']
        nickname = event['nickname']

        # 웹 소켓을 통해 메시지 전송
        await self.send(text_data=json.dumps({
            'message': message,
            'nickname': nickname
        }))
