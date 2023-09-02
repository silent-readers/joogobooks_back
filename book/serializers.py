from rest_framework import serializers
from .models import Book, Comment, ChildComment


class BookSerializer(serializers.ModelSerializer):

    sale_condition_display = serializers.CharField(
        source='get_sale_condition_display', read_only=True)

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
