from rest_framework import serializers
from .models import BookReview, BookReviewHashtag
from book.models import Book


# 서평
class BookReviewListSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y.%m.%d")
    writer_nickname = serializers.CharField(
        source='review_writer.nickname', read_only=True)

    class Meta:
        model = BookReview
        exclude = ['review']


class BookReviewEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReview
        exclude = ['review_writer']
        read_only_fields = ['view_count']


class BookReviewSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y년 %m월 %d일")
    writer_nickname = serializers.CharField(
        source='review_writer.nickname', read_only=True)

    class Meta:
        model = BookReview
        fields = '__all__'
        read_only_fields = ['view_count']

# 해시태그


class BookReviewHashtagSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReviewHashtag
        fields = '__all__'


class BookReviewHashtagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReviewHashtag
        fields = '__all__'
        read_only_fields = ['bookreview', 'writer']


class BookReviewHashtagSearchSerializer(serializers.ModelSerializer):

    bookreview = BookReviewSerializer()

    class Meta:
        model = BookReviewHashtag
        fields = '__all__'
