from django.contrib import admin
from Accounts.models import *
from django.contrib.auth.admin import UserAdmin


# Include Admin in models

class CustomAccountAdmin(UserAdmin):
    model = Account
    
    list_display =('email','username','last_login','is_active','is_staff')
    list_display_links =('email',)
    ordering = ('-id',)
    
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    
    search_fields = ("username", "first_name", "last_name", "email")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")  
    
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
        ('Important dates', {'fields': ("last_login", "date_joined")}),
    )
admin.site.register(Account,CustomAccountAdmin) 