from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


from book.models import Book
from user.models import User


class Jjim(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(null=True,
                                                default=1,
                                                validators=[MinValueValidator(1),
                                                            MaxValueValidator(100)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'jjim'

    def __str__(self):
        return f"유저id : {self.user} / 도서id : {self.book} / 번호 : {self.quantity}"
