from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()
# Create your models here.


class BookReview(models.Model):
    category_choices = (('사회 정치', '사회 정치'), ('소설/시/희곡', '소설/시/희곡'), ('어린이', '어린이'), ('여행', '여행'),
                        ('역사', '역사'), ('예술', '예술'), ('인문',
                                                     '인문'), ('인물', '인물'), ('자기계발', '자기계발'),
                        ('자연과학', '자연과학'), ('잡지', '잡지'), ('종교', '종교'), ('청소년', '청소년'))
    category = models.CharField(
        max_length=20, choices=category_choices, null=True)

    book_title = models.CharField("도서명", max_length=100)
    book_author = models.CharField("저자", max_length=100)
    book_publisher = models.CharField("출판사", max_length=100)
    review_writer = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField("평점", validators=[MaxValueValidator(
        10, "평점은 최대 10점입니다."), MinValueValidator(1, "평점은 최소 1점입니다.")])  # 1~10점
    review_title = models.CharField("서평 제목", max_length=100)
    review = models.TextField("서평", max_length=1000)
    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    view_count = models.IntegerField("조회수", default=0)

    def __str__(self):
        return f"책 제목 : {self.book_title} / 책 저자 : {self.book_author} / 작성자 : {self.review_writer} / 서평 제목 : {self.review_title} / 평점 : {self.rating}/10"


class BookReviewHashtag(models.Model):
    bookreview = models.ForeignKey("BookReview", on_delete=models.CASCADE)
    tagname = models.CharField("해시태그", max_length=10)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tagname
