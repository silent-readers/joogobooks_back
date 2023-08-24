from django.urls import path, include
from .views import BookListView, BookCreateView, BookDetailView, BookUpdateView, BookDeleteView


urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:book_id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:book_id>/delete/', BookDeleteView.as_view(), name='book-delete'),
]
