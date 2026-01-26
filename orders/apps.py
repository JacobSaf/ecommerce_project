"""
Application configuration for the orders app.

Defines the OrdersConfig class used by Django to register and initialize
the orders application within the project.
"""

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration class for the orders application.

    Specifies the app name so Django can correctly identify and load
    the orders app during project initialization.
    """
    name = 'orders'