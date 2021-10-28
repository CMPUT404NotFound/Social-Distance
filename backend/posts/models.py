from django.db import models
import uuid
from author.models import Author
# Create your models here.
class postsManager(models.Model):
    pass


class posts(models.Model):
    visibility_choice = [("PUBLIC", "PRIVATE")]
    post_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField("title", max_length= 100, unique= False, null = False, blank  = False)
    visibility = models.CharField(choices=visibility_choice,max_length=6 ,blank = False, default = "PUBLIC")
    
