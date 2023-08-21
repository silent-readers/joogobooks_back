from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Post(models.Model): 
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, required=True)
    author = models.CharField(max_length=100, required=True)
    publisher = models.CharField(max_length=100, required=True)
    condition = models.CharField(max_length=10, required=True)
    original_price = models.IntegerField(required=True, min_value=0)
    selling_price = models.IntegerField(required=True, min_value=0)
    detail_info = models.TextField(max_length=1000, required=True)
    sale_condition = models.CharField(max_length=10, default="판매중")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
class PostImage(models.Model):
    postID = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    image = models.ImageField(upload_to=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)