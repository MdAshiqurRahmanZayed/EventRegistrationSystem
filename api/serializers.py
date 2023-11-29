from rest_framework import serializers
from Accounts.serializers import UserSerializer
from Accounts.models import *
from Events.models import *


class EventModelSerializer(serializers.ModelSerializer):
     user = UserSerializer(many=False,read_only=True)
     
     class Meta:
          model = Event
          fields = '__all__'
          
class EventCreateSerializer(serializers.ModelSerializer):     
     class Meta:
          model = Event
          fields = ('title','description','date','time'
                    ,'location','slots_available',)

class RegistrationForEventSerializer(serializers.ModelSerializer):
    user =  UserSerializer(many=False,read_only=True)
    event = EventModelSerializer(many=False,read_only=True)
    class Meta:
        model = RegistrationForEvent
        fields = '__all__'