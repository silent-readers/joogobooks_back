from rest_framework import serializers
from .models import Book, Comment, ChildComment


class BookSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format="%Y년 %m월 %d일")

    sale_condition_display = serializers.CharField(
        source='get_sale_condition_display', read_only=True)
    writer_nickname = serializers.CharField(
        source='writer.nickname', read_only=True)

    class Meta:
        model = Book
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = Comment
        fields = '__all__'


class ChildCommentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = ChildComment
        fields = '__all__'


class BookLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['like']
