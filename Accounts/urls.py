
from django.urls import path
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
    
    # API 
    path('api/register/',register_view,name='register'),
    path("api/token/", MyTokenObtainPairView.as_view(),name='MyTokenObtainPairView'),
    path("token/refresh/", TokenRefreshView.as_view(),name='TokenRefreshView'),
]