from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.filters import SearchFilter
from rest_framework import viewsets

# from rest_framework.permissions import (
#     IsAuthenticated,
#     IsAuthenticatedOrReadOnly,
#     AllowAny
# )

from .models import Post
from .serializers import PostSerializer

# Create your views here.
class PostListView(APIView):
    
    def get(self, request):
        postlist = Post.objects.all()
        serializer = PostSerializer(postlist, many=True)
        return Response(serializer.data)

    
class PostCreateView(APIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [
    #     IsAuthenticated,
    # ]
    
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

