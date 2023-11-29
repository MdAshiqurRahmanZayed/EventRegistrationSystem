
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/",include('Accounts.urls')),
    path("", include('Events.urls')),
    path("api/", include('api.urls')),
]
