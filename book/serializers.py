from rest_framework import serializers
from .models import Book

class BookEditSerializer(serializers.ModelSerializer):
    sale_condition_display = serializers.CharField(source='get_sale_condition_display', read_only=True)
    
    class Meta:
        model = Book
        # fields = '__all__'
        exclude =['writer']
        
class BookSerializer(serializers.ModelSerializer):
    sale_condition_display = serializers.CharField(source='get_sale_condition_display', read_only=True)
    
    class Meta:
        model = Book
        fields = '__all__'