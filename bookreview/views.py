from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from .models import BookReview
from .serializers import BookReviewListSerializer, BookReviewSerializer
from book.models import Book

from rest_framework import generics, filters
# Create your views here.

class IsBookReviewAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        bookreview = view.get_object()
        return request.user == bookreview.review_writer
    
    
class BookReviewListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = BookReview.objects.all()
    serializer_class = BookReviewListSerializer
    filter_backends = [filters.OrderingFilter]
    ordering =['view_count', 'created_at']
    

class BookReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = BookReviewSerializer(data=request.data)
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
        serializer = BookReviewSerializer(bookreview)
        return Response(serializer.data)
    
    def put(self, request, bookreview_id):
        bookreview = get_object_or_404(BookReview, id=bookreview_id)
        serializer = BookReviewSerializer(bookreview, data=request.data)
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
        bookreview.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
