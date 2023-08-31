# chat/consumers.py

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import ChatRoom


class ChatConsumer(JsonWebsocketConsumer):

    def __init__(self):
        super().__init__()
        self.room_id = ""

    def connect(self, room_id):
        user = self.scope["user"]

        if not user.is_authenticated:
            self.close()
        else:
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
            self.room_id = ChatRoom.objects.get(room_pk=room_pk)

            async_to_sync(self.channel_layer.group_add)(
                self.room_id,
                self.channel_name
            )
            self.accept()

    def disconnect(self, code):
        if self.room_id:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_id, self.channel_name
            )

    def receive_json(self, content, **kwargs):
        user = self.scope["user"]

        _type = content["type"]

        if _type == "chat.message":
            message = content["message"]
            sender = user.username
            async_to_sync(self.channel_layer.group_send)(
                self.room_id,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender,
                },
            )
        else:
            print(f'Invalid message type : {_type}')

    def chat_message(self, message_dict):
        self.send_json({
            "type": "chat.message",
            "message": message_dict["message"],
            "sender": message_dict["sender"],
        })
