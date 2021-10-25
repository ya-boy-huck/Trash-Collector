from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.


class EmployeeAdmin(UserAdmin):
    """Overrides default Admin model to allow for custom user creation in Admin interface"""
    pass


# Registering our custom user in the admin interface
admin.site.register(User, UserAdmin)
