
from django.urls import path,include
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# Features/Functionalities
urlpatterns = [
    path("register/",register,name='register'),
    path("login/",login,name='login'),
    path('logout/',logout,name='logout'),
    path("dashboard/",dashboard,name="dashboard"),
    path("created-events/",created_events,name="created_events_user"),
    path("registered-events/",registered_events,name="registered_events"),
    
    # API 
    path('api/register/',register_view,name='register-api'),
    path("api/token/", MyTokenObtainPairView.as_view(),name='MyTokenObtainPairView'),
    path("token/refresh/", TokenRefreshView.as_view(),name='TokenRefreshView'),
    path("user-profile/<int:pk>/", UserProfileAPI.as_view(),name='UserProfileAPI'),
]