from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    prompt = models.CharField(max_length=512)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prompt}: {self.response}"

    def get_nickname(self):
        return self.user.nickname
