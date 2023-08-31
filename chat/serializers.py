from rest_framework import serializers
from .models import ChatRoom, Message


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    timestamp = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Message
        fields = ('id', 'sender', 'message', 'timestamp')


class ChatRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatRoom
        fields = '__all__'
