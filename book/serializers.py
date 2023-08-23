from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id',  'title', 'author', 'publisher', 'condition', 'original_price', 'selling_price', 'detail_info', 'sale_condition', 'uploaded_at')
