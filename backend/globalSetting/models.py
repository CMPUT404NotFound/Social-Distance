from django.db import models

# Create your models here.


class Setting(models.Model):
    '''
    global settings goes here  
    this model can only ever have 1 row, every new option for the admin should be a attribute here.
    '''
    newUserRequireActivation = models.BooleanField("New User Require Activation",default=False)
    
    def settings():
        return Setting.objects.all().first()
    
    def __str__(self) -> str:
        return "Global Site Setting"