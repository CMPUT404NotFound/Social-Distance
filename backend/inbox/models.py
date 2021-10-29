from django.db import models

# Create your models here.

from author.models import Author

class InboxItem(models.Model):
    
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    # post = models
    