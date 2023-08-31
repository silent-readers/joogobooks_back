from django.urls import path, include
from .views import BookReviewListView, BookReviewDetailView, BookReviewCreateView, BookReviewUpdateView, BookReviewDeleteView


urlpatterns = [
    path('list/', BookReviewListView.as_view(), name='bookreview-list'),
    path('<int:bookreview_id>/', BookReviewDetailView.as_view(), name='bookreview-detail'),
    path('create/', BookReviewCreateView.as_view(), name='bookreview-create'),
    path('<int:bookreview_id>/update/', BookReviewUpdateView.as_view(), name='bookreview-update'),
    path('<int:bookreview_id>/delete/', BookReviewDeleteView.as_view(), name='bookreview-delete'),
]
