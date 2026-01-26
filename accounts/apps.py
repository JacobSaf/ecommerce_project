"""
Application configuration for the accounts app.

Defines the AccountsConfig class used by Django to register
and initialize the accounts application within the project.
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration class for the accounts application.

    Sets the app name so Django can correctly identify and load
    the accounts app during project initialization.
    """
    name = 'accounts'