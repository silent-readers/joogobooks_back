from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin

from .models import Book
from .serializers import BookSerializer, BookEditSerializer

# Create your views here.
class BookPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class IsBookAuthor(permissions.BasePermission):
    
    def has_object_permission(self, request, view, book):
        if request.method in permissions.SAFE_METHODS:
            return True
        # 요청자(request.user)가 객체의 user와 동일한지 확인
        return book.writer == request.user

class BookListView(APIView, PaginationHandlerMixin):
    permission_classes = [permissions.AllowAny]
    pagination_class = BookPagination
    serializer_class = BookSerializer
    
    def get(self, request, *args, **kwargs):
        booklist = Book.objects.all()
        page = self.paginate_queryset(booklist)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(booklist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class BookCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookEditSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = BookEditSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(writer = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)


class BookUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookAuthor]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if request.user == book.writer:
            serializer = BookEditSerializer(book)
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookEditSerializer(book, data=request.data)
        if serializer.is_valid():
            if request.user == book.writer:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsBookAuthor]

    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        if request.user == book.writer:
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)
    

class BookSearchFilter(FilterSet):

    class Meta:
        model = Book
        fields = {
            'title':['icontains'],
            'sale_condition':['exact'],            
        }


class BookSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookSearchFilter
    ordering = ['uploaded_at', 'selling_price']