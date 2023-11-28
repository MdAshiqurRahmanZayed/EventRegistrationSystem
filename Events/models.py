from django.db import models
from Accounts.models import Account
# Create your models here.
class Event(models.Model):
    user  = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    slots_available = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    def __str__(self):
        return self.title
class RegistrationForEvent(models.Model):
    user  = models.OneToOneField(Account, on_delete=models.CASCADE)
    event = models.OneToOneField(Event, on_delete=models.CASCADE) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True,null=True, blank=True)