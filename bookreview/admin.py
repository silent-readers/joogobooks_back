from django.contrib import admin
from .models import BookReview, BookReviewHashtag

admin.site.register(BookReview)
admin.site.register(BookReviewHashtag)