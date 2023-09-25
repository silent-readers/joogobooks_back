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
from .serializers import BookSerializer, CommentSerializer, ChildCommentSerializer, BookLikeSerializer
from rest_framework.generics import UpdateAPIView

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
        booklist = Book.objects.all().select_related('writer')
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
    pagination_class = BookPagination
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

class BookLikeAPIVIew(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookLikeSerializer

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 사용자가 이미 좋아요를 눌렀는지 확인
        if request.user in instance.liked_by.all():
            return Response({'detail': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 좋아요 증가
        instance.like += 1
        instance.liked_by.add(request.user)
        instance.save()

        # 변경된 데이터 serializer에 반영
        data = {'like': instance.like}

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 객체 최적화 및 메모리 관리
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(data['like'])

class BookDisLikeAPIVIew(UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookLikeSerializer

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # 이미 좋아요했던 확인 여부를 리스트에서 삭제(다시 좋아요를 누를 수 있게끔)
        if request.user in instance.liked_by.all():
            instance.liked_by.remove(request.user)
            instance.save()

        # 좋아요 -1 이후 serializer에 반영
        data = {'like' : instance.like - 1}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(data['like'])
