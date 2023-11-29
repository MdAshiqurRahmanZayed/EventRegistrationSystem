from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'events-all-crud', EventViewSet, basename='event')

urlpatterns = [
     
     path("",EventListCreateAPIView.as_view(),name='EventListCreateAPIView'),
     path("<int:pk>/",EventRetrieveUpdateDestroyAPIView.as_view(),name='EventRetrieveUpdateDestroyAPIView'),
     path("registration-or-unregistration/<int:pk>/",registration_or_unregistration_for_events,
          name='registration_or_unregistration_for_events'),
     path('', include(router.urls)),
     
     path('registered-events/', RegisteredEventsAPIView.as_view(), name='registered-events'),
     path('created-events/', created_events, name='created_events'),
    
]
