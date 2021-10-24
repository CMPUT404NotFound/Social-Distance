from django.db import models

# Create your models here.



class Author(models.Model):
    
    
    id = models.CharField('id', primary_key=True, max_length=32)
    displayName = models.CharField("displayName", max_length=40) #max 40 chars should be more than enough
    github = models.URLField('github', max_length=60) #len('https://github.com/'), and max user name length on github is 39 chars
    profileImage = models.URLField('profileImage') 
    
    def __str__(self):
        return f"author: {self.displayName}, id: {self.id}"
    
