from django.db import models

# Create your models here.

from author.models import Author
from posts.models import Post

class Like(models.Model):
    
    author = models.CharField(max_length=100, null= False, blank=False, default="") # author of the like
    parentId = models.CharField(max_length=100, null= False, blank=False, default="") #can be either a local post or a comment
    
