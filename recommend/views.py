from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from .models import Conversation as ConversationModel
from .serializers import ConversationSerializer

from dotenv import load_dotenv
import openai
import os


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class ChatbotView(APIView):
    throttle_scope = 'contacts'
    permission_classes = [IsAuthenticated]

    def get(self, request):
        conversations = request.session.get('conversations', [])
        return Response({'conversations': conversations})

    def post(self, request):
        user = request.user

        prompt = request.data.get('prompt')

        if prompt:
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join(
                [f"prompt: {c['prompt']}\nresponse: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nresponse: {prompt}\nresponse:"

        completions = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_with_previous,
            max_tokens=1024,
            n=5,
            stop=None,
            temperature=0.5,
        )

        response = completions.choices[0].text.strip()

        conversation = ConversationModel(
            user=user, prompt=prompt, response=response)
        conversation.save()

        # 대화 기록에 새로운 응답 추가
        session_conversations.append({'prompt': prompt, 'response': response})
        request.session['conversations'] = session_conversations
        request.session.modified = True

        return self.get(request)


class ConversationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        conversations = ConversationModel.objects.filter(user_id=user_id)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
