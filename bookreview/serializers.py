from rest_framework import serializers
from .models import BookReview
from book.models import Book


class BookReviewListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookReview
        exclude = ['review']


    
    
class BookReviewSerializer(serializers.ModelSerializer):
    purchased_book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = BookReview
        fields = '__all__'
        read_only_fields = ['view_count']
