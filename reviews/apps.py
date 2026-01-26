"""
Application configuration for the reviews app.

Defines the ReviewsConfig class used by Django to register and
initialize the reviews application within the project.
"""

from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Configuration class for the reviews application.

    Specifies the app name so Django can correctly identify and load
    the reviews app during project initialization.
    """
    name = 'reviews'