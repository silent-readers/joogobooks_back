from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Book(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("도서명", max_length=100)
    author = models.CharField("저자", max_length=100)
    publisher = models.CharField("출판사", max_length=100)
    condition = models.CharField("도서상태", max_length=10)
    original_price = models.IntegerField("정가")
    selling_price = models.IntegerField("판매가")
    detail_info = models.TextField("상세내용", max_length=1000)
    sale_condition = models.CharField("판매상태", max_length=10, default="판매중")
    image = models.ImageField("이미지", upload_to='book_image/', blank=True)
    SALE_CONDITION_CHOICES = [
        ("판매중", "판매중"),
        ("예약중", "예약중"),
        ("판매완료", "판매완료"),
    ]
    uploaded_at = models.DateTimeField("작성시간",auto_now_add=True)

    sale_condition = models.CharField("판매 상태", max_length=10, choices=SALE_CONDITION_CHOICES)

    def __str__(self):
        return self.title
