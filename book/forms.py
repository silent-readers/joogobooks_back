from django import forms
from .models import Book

class PostForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['sale_condition', 'title', 'author', 'publisher', 'condition', 'original_price', 'selling_price', 'detail_info','image']
