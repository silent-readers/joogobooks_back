# yourapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.CreateChatRoomView.as_view()),
    path('<str:room_pk>/chat/', views.ChatView.as_view()),
    path('send_message/', views.SendMessageView.as_view()),
    path('<int:room_id>/', views.ChatView.as_view()),
]
