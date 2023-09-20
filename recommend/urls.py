from django.urls import path
from .views import ChatbotView, ConversationsView

urlpatterns = [
    path('chatbot/', ChatbotView.as_view(), name="chatbot"),
    path('chatbot/<int:user_id>/conversations/',
         ConversationsView.as_view(), name="conversations"),
]
