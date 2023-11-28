from django.contrib import admin
from .models import * 
class CustomEventAdmin(admin.ModelAdmin):
     models = Event
     list_display = ('title','date','time','slots_available',)
class CustomRegistrationForEvent(admin.ModelAdmin):
     models = Event
     list_display = ('event','user','created_at',)

admin.site.register(Event,CustomEventAdmin)
admin.site.register(RegistrationForEvent,CustomRegistrationForEvent)