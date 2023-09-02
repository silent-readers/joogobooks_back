from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from rest_framework.pagination import PageNumberPagination
from .pagination import PaginationHandlerMixin

from .models import Book, Comment, ChildComment
from .serializers import BookSerializer, CommentSerializer, ChildCommentSerializer

# Create your views here.


class BookPagination(PageNumberPagination):
    page_size_query_param = 'limit'


class IsBookAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        book = view.get_object()
        return request.user == book.user


class BookListView(APIView, PaginationHandlerMixin):
    permission_classes = [permissions.AllowAny]
    pagination_class = BookPagination
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        booklist = Book.objects.all()
        page = self.paginate_queryset(booklist)
        if page is not None:
            serializer = self.get_paginated_response(
                self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(booklist, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(writer=request.user)
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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            if request.user == book.writer:
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookSearchFilter(FilterSet):

    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'sale_condition': ['exact'],
        }


class BookSearchView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = BookSearchFilter
    ordering = ['uploaded_at', 'selling_price']


class CommentWriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    serielizer_class = CommentSerializer

    def get(self, request, book_id):
        comments = Comment.objects.filter(book_id=book_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        book_id = self.kwargs.get('book_id')
        book = get_object_or_404(Book, id=book_id)
        serializer.save(user=self.request.user, book=book)

    def post(self, request, book_id):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            comment = serializer.save(user=request.user, book_id=book_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class CommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        comment = Comment.objects.get(pk=book_id)
        comment.delete()
        return Response({'message': 'Comment Delete!'}, status=status.HTTP_204_NO_CONTENT)


class ChildCommentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, parent_comment_id):
        serializer = ChildCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user,
                            parent_comment_id=parent_comment_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildCommentDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, parent_commnet_id):
        childcomment = ChildComment.objects.get(pk=parent_commnet_id)
        childcomment.delete()
        return Response({'message': 'Comment Delete!'}, status=status.HTTP_204_NO_CONTENT)
