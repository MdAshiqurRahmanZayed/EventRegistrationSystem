from django.contrib.auth.models import AbstractUser
from django.db import models

#  
class Account(AbstractUser):
    username = models.CharField(verbose_name='Username', max_length=150,unique=True)
    email = models.EmailField(verbose_name='Email address',unique=True,null=False,blank=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username',]
    
    def save(self, *args, **kwargs):
     #    print(self.email,self.username) 
        if not self.username:
            username = self.email.split('@')[0] + '_' + self.email.split('@')[1].split('.')[0]
            self.username = username
        super().save(*args, **kwargs)
    