
from django.urls import path
from .views import *
urlpatterns = [
    path("",home,name='home'),
    path("create-event/",createEvent,name='createEvent'),
    path("all-events/",event_list,name='event_list'),
    path("event-detail/<int:pk>/",event_detail,name='event_detail'),
    path("event-update/<int:pk>/",update_event,name='update_event'),
    path("event-delete/<int:pk>/",delete_event,name='delete_event'),
    path("event-registration/<int:pk>/",registrationOrUnregistrationForEvents,name='registration_event'),
    path('search/', searchEvent, name="searchEvent"),
]
