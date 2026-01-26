"""
Models for seller-owned storefronts.

Defines the Store model, which represents a seller’s storefront within
the marketplace and groups products under a single brand or identity.
"""


from django.db import models
from django.conf import settings


class Store(models.Model):
    """
    Represents a seller-owned storefront within the marketplace.

    A store groups together products under a single brand or identity.
    Each store is owned by a specific user (seller), and deleting the
    owner will remove all associated stores.

    Fields:
        name:
            The public-facing name of the store.

        description:
            Optional text describing the store, its purpose, or branding.

        owner:
            The user who created and manages the store. Only the owner
            may edit or delete the store.

        created_at:
            Timestamp indicating when the store was created. Useful for
            sorting and analytics.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stores",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name