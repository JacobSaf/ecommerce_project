"""
Utility functions for working with shopping carts.

Provides helpers for retrieving or creating a user's cart, ensuring that
every authenticated user always has an associated Cart instance.
"""

from .models import Cart


def get_user_cart(user):
    """
    Retrieve the cart associated with the given user.

    If the user already has a cart, it is returned. If no cart exists,
    a new one is created and returned. This ensures that all authenticated
    users always have a valid cart available for adding items.

    Args:
        user (CustomUser): The user whose cart should be retrieved.

    Returns:
        Cart: The existing or newly created cart for the user.
    """
    try:
        return user.cart
    except Cart.DoesNotExist:
        return Cart.objects.create(user=user)