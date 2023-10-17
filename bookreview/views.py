from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .models import BookReview, BookReviewHashtag
from .serializers import BookReviewListSerializer, BookReviewSerializer, BookReviewEditSerializer, BookReviewHashtagSerializer, BookReviewHashtagCreateSerializer, BookReviewHashtagSearchSerializer

from book.models import Book

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
# Create your views here.

# 서평


class IsBookReviewAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, bookreview):
        if request.method in permissions.SAFE_METHODS:
            return True
        # 요청자(request.user)가 객체의 user와 동일한지 확인
        return bookreview.review_writer == request.user


class BookReviewSearchFilter(FilterSet):

    class Meta:
        model = BookReview
        fields = {
            'book_title': ['icontains'],
        }


class BookReviewHashtagFilter(FilterSet):

    class Meta:
        model = BookReviewHashtag
        fields = {
            'tagname': ['exact'],
        }


class BookReviewListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BookReview.objects.all()
    serializer_class = BookReviewListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookReviewSearchFilter


class BookReviewHashtagSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BookReviewHashtag.objects.all()
    serializer_class = BookReviewHashtagSearchSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookReviewHashtagFilter


class BookReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookReview.objects.all()
    serializer_class = BookReviewEditSerializer

    def post(self, request, *args, **kwargs):
        serializer = BookReviewEditSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(review_writer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        serializer = BookReviewSerializer(bookreview)
        bookreview.view_count += 1
        bookreview.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookReviewUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookReviewAuthor]

    def get(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        if request.user == bookreview.review_writer:
            serializer = BookReviewEditSerializer(bookreview)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        serializer = BookReviewEditSerializer(bookreview, data=request.data)
        if serializer.is_valid():
            if request.user == bookreview.review_writer:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookReviewAuthor]

    def delete(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        if request.user == bookreview.review_writer:
            bookreview.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

# 해시태그


class BookReviewHashtagListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        hashtags = BookReviewHashtag.objects.filter(bookreview=bookreview)
        serializer = BookReviewHashtagSerializer(hashtags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookReviewHashtagCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookReviewAuthor]
    queryset = BookReviewHashtag.objects.all()
    serializer_class = BookReviewHashtagCreateSerializer

    def post(self, request, bookreview_id):
        serializer = BookReviewHashtagCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            bookreview = get_object_or_404(BookReview, id=bookreview_id)
            if not bookreview:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if bookreview.review_writer != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer.save(writer=request.user, bookreview=bookreview)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)


class BookReviewHashtagDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookReviewAuthor]

    def delete(self, request, hashtag_id):
        hashtag = get_object_or_404(BookReviewHashtag, id=hashtag_id)
        if request.user == hashtag.writer:
            hashtag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
