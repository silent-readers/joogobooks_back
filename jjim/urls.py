from django.contrib import admin
from django.urls import path, include

from jjim import views

urlpatterns = [
    path('create/', views.JjimAddView.as_view()),
    path('delete/<int:book_id>/<int:user_id>/', views.JjimDeleteView.as_view()),
]