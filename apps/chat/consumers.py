
import json
import time

from channels.generic.websocket import AsyncWebsocketConsumer

from utils.functions import Listener
from .utils.consumer_wrapper import heartbeat, chatCreate

class Chatting(AsyncWebsocketConsumer, Listener):

    async def connect(self):

        # self.room_group_name = 'xiaoyuanqujing'
        # 加入聊天室
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )
        await self.accept()

    async def disconnect(self, close_code):
        # 离开聊天室
        # await self.channel_layer.group_discard(
        #     self.room_group_name,
        #     self.channel_name
        # )
        ...

    # 通过WebSocket，接收数据
    @heartbeat()
    @chatCreate()
    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
            chat_id = data["chat_id"]
            # 增加时间字段
            data["chat_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            # Send message to room group
            await self.channel_layer.group_send(
                chat_id,
                {
                    "type": "chat.message",
                    "data": data
                }
            )
            # 给监听者发送消息
            Chatting.trigger(data)
        except Exception as e:
            print(e)
            pass

    # Receive message from room group
    async def chat_message(self, event):
        # 通过WebSocket发送
        await self.send(text_data=json.dumps(event['data']))

