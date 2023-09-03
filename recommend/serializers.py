from rest_framework import serializers
from chat.models import Conversation


class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ['prompt', 'response']
        extra_kwargs = {
            'response': {"read_only": True}
        }
