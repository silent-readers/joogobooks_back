from django.db import models
from django.contrib.auth import get_user_model
from book.models import Book

User = get_user_model()


# Create your models here.
class ChatRoom(models.Model):
    roomname = models.ForeignKey(
        Book, related_name='book', on_delete=models.CASCADE)
    host = models.ForeignKey(
        User, related_name='host', on_delete=models.CASCADE)
    guest = models.ForeignKey(
        User, related_name='guest', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f'host : {self.host}, guest: {self.guest}'


class Message(models.Model):
    room = models.ForeignKey(
        ChatRoom, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'User : {self.sender}, Message: {self.message}'
