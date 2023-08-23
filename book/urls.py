from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostListView, PostCreateView, PostSearchView


urlpatterns = [
    path('list/', PostListView.as_view(), name='book-list'),
    path('create/', PostCreateView.as_view(), name='book-create')
]
