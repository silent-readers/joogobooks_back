from rest_framework import serializers
from .models import BookReview


class BookReviewListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookReview
        exclude = ['review']


    
    
class BookReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookReview
        fields = '__all__'
        read_only_fields = ['view_count']
