from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Post(models.Model):
    # writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("도서명", max_length=100)
    author = models.CharField("저자", max_length=100)
    publisher = models.CharField("출판사", max_length=100)
    condition = models.CharField("도서상태", max_length=10)
    original_price = models.IntegerField("정가")
    selling_price = models.IntegerField("판매가")
    detail_info = models.TextField("상세내용", max_length=1000)
    sale_condition = models.CharField("판매상태", max_length=10, default="판매중")
    uploaded_at = models.DateTimeField("작성시간",auto_now_add=True)
    
    
class PostImage(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField("이미지",upload_to=None, blank=True)
    created_at = models.DateTimeField("업로드시간",auto_now_add=True)