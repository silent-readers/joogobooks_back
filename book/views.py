from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from .models import Book
from .serializers import BookSerializer
from .forms import PostForm

from .models import Book
from .serializers import BookSerializer

# Create your views here.
class BookListView(APIView):
    
    def get(self, request):
        booklist = Book.objects.all()
        serializer = BookSerializer(booklist, many=True)
        return Response(serializer.data)

    
class BookCreateView(APIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user = request.user)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookSerializer(book)
        return render(request, 'book/book_detail.html', {'book': serializer.data})


class BookUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = PostForm(instance=book)
        return render(request, 'book/book_edit.html', {'form': form, 'book': book})

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        form = PostForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            new_book = form.save(commit=False)
            new_book.writer = request.user
            new_book.save()
            return redirect('book_detail', book_id=new_book.id)
        return render(request, 'book/book_edit.html', {'form': form, 'book': book, 'errors': form.errors})


class BookDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        book.delete()
        return redirect('book_list')