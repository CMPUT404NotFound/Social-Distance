from django.db import models

# Create your models here.


class Like(models.Model):
    
    author = models.CharField(max_length=100, null= False, blank=False, default="") # author of the like
    parentId = models.CharField(max_length=100, null= False, blank=False, default="") #can be either a local post or a comment
    

    def __str__(self) -> str:
        return f"{str(self.pk)} is liked by {self.author}" 