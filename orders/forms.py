# orders/forms.py

from django import forms


class GuestCheckoutForm(forms.Form):
    """
    Form used to collect billing and shipping information from guest users.

    This form is displayed during the guest checkout process and captures
    all required customer details needed to create an Order, including:

        - full_name: The guest's full legal name.
        - email: Used for sending the order confirmation and invoice.
        - address, city, state, zip_code:
            The shipping address where the order will be delivered.
        - phone:
            Optional contact number for delivery updates or issues.

    Logged-in users do not use this form, as their information is pulled
    from their account profile and associated models.
    """
    full_name = forms.CharField(max_length=255, label="Full name")
    email = forms.EmailField(label="Email")
    address = forms.CharField(max_length=255, label="Address")
    city = forms.CharField(max_length=100, label="City")
    state = forms.CharField(max_length=100, label="State")
    zip_code = forms.CharField(max_length=20, label="ZIP / Postal code")
    phone = forms.CharField(
        max_length=20,
        required=False,
        label="Phone (optional)",
    )
