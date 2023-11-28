from django.db import models
from Accounts.models import Account
# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    slots_available = models.IntegerField(default=0)
    
class RegistrationForEvent(models.Model):
    user  = models.ForeignKey(Account, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE) 