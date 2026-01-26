from .models import Cart

def get_user_cart(user):
    try:
        return user.cart  # always the correct cart
    except Cart.DoesNotExist:
        return Cart.objects.create(user=user)
