from django.db import models

# Create your models here.

from author.models import Author
from posts.models import Post

class Like(models.Model):
    
    context = models.URLField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.CharField(max_length=100)
    
    