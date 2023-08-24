from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    sale_condition_display = serializers.CharField(source='get_sale_condition_display', read_only=True)
    class Meta:
        model = Book
        fields = ('id', 'writer', 'title', 'author', 'publisher', 'condition', 'original_price', 'selling_price', 'detail_info', 'uploaded_at', 'image', 'sale_condition', 'sale_condition_display')