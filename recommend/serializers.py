from rest_framework import serializers
from .models import Conversation


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = '__all__'
        extra_kwargs = {
            'response': {"read_only": True}
        }
