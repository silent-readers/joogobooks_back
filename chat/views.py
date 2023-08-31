# views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import render
from django.urls import reverse

from book.models import Book
from user.models import User
from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, ChatMessageSerializer


class CreateChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_id = request.data.get('room_id')
        host = request.user
        guest = request.data.get('guest')

        try:
            book_instance = Book.objects.get(id=room_id)
            guest_instance = User.objects.get(id=guest)
        except Book.DoesNotExist:
            return Response({"detail": "Book does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST)

        # host와 guest를 사용하여 채팅방 생성
        chat_room, created = ChatRoom.objects.get_or_create(
            host=host, guest=guest_instance, roomname=book_instance)

        if created:
            serializer = ChatRoomSerializer(chat_room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Chat room already exists."}, status=status.HTTP_200_OK)


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_pk):
        room = ChatRoom.objects.filter(request.user)
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        room_id = request.data.get('room_id')
        message = request.data.get('message')

        try:
            chat_room = ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return Response({"success": False, "error": "Chat room does not exist."}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user
        chat_message = Message.objects.create(
            chat_room=chat_room, sender=sender, message=message)

        serializer = ChatMessageSerializer(chat_message)

        return Response({"success": True, "message": serializer.data}, status=status.HTTP_201_CREATED)
