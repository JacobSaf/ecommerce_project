from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Extends Django's built-in user model with marketplace-specific roles.

    This custom user model introduces two boolean flags that determine
    how the user interacts with the platform:

        is_seller:
            Indicates whether the user can create stores and list products
            for sale. Sellers have access to seller dashboards and product
            management features.

        is_buyer:
            Indicates whether the user can browse products, add items to
            their cart, and place orders. Most users are buyers by default.

    The model inherits all standard authentication fields such as username,
    password, email, first_name, last_name, and permissions.
    """
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)