from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

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

