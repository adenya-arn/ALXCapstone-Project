from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'created', 'last_accessed', 'is_superuser')

    list_filter = ( 'username', 'email', 'is_superuser', 'created')



admin.site.register(User, CustomUserAdmin)
