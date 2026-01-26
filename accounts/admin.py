from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_staff', 'is_active', 'is_seller', 'is_buyer']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_seller', 'is_buyer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_seller', 'is_buyer')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
