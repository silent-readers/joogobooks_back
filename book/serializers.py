from rest_framework import serializers
from .models import Post, PostImage

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id',  'title', 'author', 'publisher', 'condition', 'original_price', 'selling_price', 'detail_info', 'sale_condition', 'uploaded_at')


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ('id', 'postID', 'image', 'created_at')