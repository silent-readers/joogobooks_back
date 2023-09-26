from django.urls import path, include
from .views import BookReviewListView, BookReviewDetailView, BookReviewCreateView, BookReviewUpdateView, BookReviewDeleteView, BookReviewHashtagListView, BookReviewHashtagCreateView, BookReviewHashtagDeleteView, BookReviewHashtagSearchView


urlpatterns = [
    path('list/', BookReviewListView.as_view(), name='bookreview-list'),
    path('<int:bookreview_id>/', BookReviewDetailView.as_view(),
         name='bookreview-detail'),
    path('create/', BookReviewCreateView.as_view(), name='bookreview-create'),
    path('<int:bookreview_id>/update/',
         BookReviewUpdateView.as_view(), name='bookreview-update'),
    path('<int:bookreview_id>/delete/',
         BookReviewDeleteView.as_view(), name='bookreview-delete'),

    # 해시태그
    path('<int:bookreview_id>/hashtag/',
         BookReviewHashtagListView.as_view(), name="bookreview-tag-list"),
    path('hashtag/search/', BookReviewHashtagSearchView.as_view(),
         name="bookreview-tag-search"),
    path('<int:bookreview_id>/hashtag/create/',
         BookReviewHashtagCreateView.as_view(), name='bookreview-tag-create'),
    path('hashtag/<int:hashtag_id>/delete/',
         BookReviewHashtagDeleteView.as_view(), name='bookreview-tag-delete'),

]
