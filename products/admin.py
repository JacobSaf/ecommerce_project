"""
Admin configuration for product-related models.

Registers Product and Category models with the Django admin site.
"""
from django.contrib import admin
from .models import Product, Category

admin.site.register(Product)
admin.site.register(Category)