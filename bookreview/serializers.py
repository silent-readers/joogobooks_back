from rest_framework import serializers
from .models import BookReview, BookReviewHashtag
from book.models import Book

### 서평
class BookReviewListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookReview
        exclude = ['review']


class BookReviewEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReview
        exclude =['review_writer']
        read_only_fields = ['view_count']


class BookReviewSerializer(serializers.ModelSerializer):
    purchased_book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = BookReview
        fields = '__all__'
        read_only_fields = ['view_count']
        
### 해시태그
class BookReviewHashtagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookReviewHashtag
        fields = '__all__'
        read_only_fields = ['bookreview','writer']

class BookReviewHashtagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReviewHashtag
        fields = ['tagname']