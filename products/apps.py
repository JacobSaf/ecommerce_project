"""
Application configuration for the products app.

Defines the ProductsConfig class used by Django to register and
initialize the products application within the project.
"""

from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration class for the products application.

    Specifies the app name so Django can correctly identify and load
    the products app during project initialization.
    """
    name = 'products'