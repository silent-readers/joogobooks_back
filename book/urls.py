from django.urls import path, include
from .views import BookListView, BookCreateView


urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create')
]
