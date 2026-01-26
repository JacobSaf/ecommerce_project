"""
Application configuration for the stores app.

Defines the StoresConfig class used by Django to register and
initialize the stores application within the project.
"""

from django.apps import AppConfig


class StoresConfig(AppConfig):
    """
    Configuration class for the stores application.

    Specifies the app name so Django can correctly identify and load
    the stores app during project initialization.
    """
    name = 'stores'