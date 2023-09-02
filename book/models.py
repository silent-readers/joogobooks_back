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
    category_choices = (('사회 정치', '사회 정치'), ('소설/시/희곡', '소설/시/희곡'), ('어린이', '어린이'), ('여행', '여행'),
                        ('역사', '역사'), ('예술', '예술'), ('인문',
                                                     '인문'), ('인물', '인물'), ('자기계발', '자기계발'),
                        ('자연과학', '자연과학'), ('잡지', '잡지'), ('종교', '종교'), ('청소년', '청소년'))
    category = models.CharField(
        max_length=20, choices=category_choices, null=True)

    class Meta:
        ordering = ["-id"]

    SALE_CONDITION_CHOICES = [
        ("판매중", "판매중"),
        ("예약중", "예약중"),
        ("판매완료", "판매완료"),
    ]

    uploaded_at = models.DateTimeField("작성시간", auto_now_add=True)

    sale_condition = models.CharField(
        "판매 상태", max_length=10, choices=SALE_CONDITION_CHOICES)

    def __str__(self):
        return f"책 제목 : {self.title} / 책 저자 : {self.author} / 책 상태 : {self.condition} / 판매자: {self.writer} / 판매가격 {self.selling_price}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True)

    def __str__(self):
        return f'{self.user.nickname} - {self.book.title} - {self.content}'


class ChildComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.parent_comment} - {self.user.nickname} - {self.content}'
