from django.contrib import admin
from .models import * 
class CustomEventAdmin(admin.ModelAdmin):
     models = Event
     list_display = ('title','date','time','slots_available',)

admin.site.register(Event,CustomEventAdmin)