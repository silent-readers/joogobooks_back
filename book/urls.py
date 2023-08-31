from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BookListView, BookCreateView, BookDetailView, BookUpdateView, BookDeleteView, BookSearchView


urlpatterns = [
    path('list/', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:book_id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:book_id>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('search/', BookSearchView.as_view(), name='book-search')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
