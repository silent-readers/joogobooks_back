from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .models import BookReview
from .serializers import BookReviewListSerializer, BookReviewSerializer, BookEditSerializer

from book.models import Book

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
# Create your views here.

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
            'book_title': ['icontains']
        }

class BookReviewListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BookReview.objects.all()
    serializer_class = BookReviewListSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookReviewSearchFilter
    ordering =['view_count', 'created_at']
    

class BookReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookReview.objects.all()
    serializer_class = BookEditSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = BookEditSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            purchased_book_id = request.data.get('purchased_book')
            purchased_book = get_object_or_404(Book, id=purchased_book_id)
            purchased_book_writer = purchased_book.writer
            serializer.save(review_writer = request.user, purchased_book=purchased_book_writer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookReviewDetailView(APIView):
    permission_classes = [permissions.AllowAny]
    
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
            serializer = BookEditSerializer(bookreview)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)
    
    def put(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        serializer = BookEditSerializer(bookreview, data=request.data)
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
