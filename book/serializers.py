from rest_framework import serializers
from .models import Book, Comment, ChildComment


class BookSerializer(serializers.ModelSerializer):

    sale_condition_display = serializers.CharField(
        source='get_sale_condition_display', read_only=True)
    writer_nickname = serializers.CharField(
        source='writer.nickname', read_only=True)
    

    class Meta:
        model = Book
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']


class ChildCommentSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ChildComment
        fields = ['id', 'content', 'created_at']


class BookLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['like']
