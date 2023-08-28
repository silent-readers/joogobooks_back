from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
# Create your models here.
class BookReview(models.Model):
    book_title = models.CharField("도서명", max_length=100)
    book_author = models.CharField("저자", max_length=100)
    review_writer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField("평점", validators=[ MaxValueValidator(10, "평점은 최대 10점입니다."), MinValueValidator(1, "평점은 최소 1점입니다.")]) #1~10점
    review_title = models.CharField("서평 제목", max_length=100)
    review = models.TextField("서평", max_length=1000)
    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    view_count = models.IntegerField("조회수", default=0)

    def __str__(self):
        return f"책 제목 : {self.book_title} / 책 저자 : {self.book_author} / 작성자 : {self.review_writer} / 서평 제목 : {self.review_title} / 평점 : {self.rating}/10"