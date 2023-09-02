from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import BookListView, BookCreateView, BookDetailView, BookUpdateView, BookDeleteView, BookSearchView, CommentWriteView, CommentDeleteView, ChildCommentCreateView, ChildCommentDeleteView

urlpatterns = [
    # 책 CRUD 관련 url
    path('list/', BookListView.as_view(), name='book-list'),
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('<int:book_id>/', BookDetailView.as_view(), name='book-detail'),
    path('<int:book_id>/update/', BookUpdateView.as_view(), name='book-update'),
    path('<int:book_id>/delete/', BookDeleteView.as_view(), name='book-delete'),

    # 검색기능 url
    path('search/', BookSearchView.as_view(), name='book-search'),

    # 댓글기능 url
    path('<int:book_id>/comment/create/', CommentWriteView.as_view()),
    path('<int:book_id>/comment/delete/', CommentDeleteView.as_view()),
    path('comment/<int:parent_comment_id>/childcomment/create/',
         ChildCommentCreateView.as_view()),
    path('comment/<int:parent_comment_id>/childcomment/delete/',
         ChildCommentDeleteView.as_view()),
]
