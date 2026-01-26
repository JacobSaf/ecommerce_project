from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    """
    Registration form for creating a new user account with role selection.

    Extends Django's built-in UserCreationForm and adds two optional
    boolean fields that allow the user to register as a seller, a buyer,
    or both. These fields map directly to the CustomUser model's
    is_seller and is_buyer attributes.

    Fields:
        is_seller:
            Optional checkbox allowing the user to register as a seller.
            Sellers can create stores and list products.

        is_buyer:
            Optional checkbox allowing the user to register as a buyer.
            Buyers can browse products, add items to their cart, and place orders.

    The form also includes standard UserCreationForm fields:
        - username
        - email
        - password1
        - password2
    """
    is_seller = forms.BooleanField(required=False, label="Register as Seller")
    is_buyer = forms.BooleanField(required=False, label="Register as Buyer")

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'is_seller',
            'is_buyer',
            'password1',
            'password2'
        ]