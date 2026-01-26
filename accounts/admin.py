"""
Admin configuration for the CustomUser model.

Extends Django's built-in UserAdmin to include marketplace-specific
fields such as is_seller and is_buyer. This ensures that these fields
are visible and editable within the Django admin interface.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.

    Adds seller and buyer role fields to the default UserAdmin
    configuration so administrators can manage user roles directly
    from the Django admin panel.

    Attributes:
        model:
            The model associated with this admin configuration.
        list_display:
            Fields displayed in the user list view.
        fieldsets:
            Field groupings shown when editing an existing user.
        add_fieldsets:
            Field groupings shown when creating a new user.
    """
    model = CustomUser
    list_display = [
        'username',
        'email',
        'is_staff',
        'is_active',
        'is_seller',
        'is_buyer',
    ]

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_seller', 'is_buyer')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_seller', 'is_buyer')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)