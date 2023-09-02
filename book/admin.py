from django.contrib import admin
from .models import Book, Comment, ChildComment

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(ChildComment)
