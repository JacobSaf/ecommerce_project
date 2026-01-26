# URLS pertaining to order/cart creation

from django.urls import path
from . import views

urlpatterns = [
    # Cart
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),

    # Logged-in cart item operations
    path("cart/update/<int:item_id>/", views.update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),

    # Guest cart item operations
    path("cart/guest/update/<int:product_id>/", views.update_guest_cart_item, name="update_guest_cart_item"),
    path("cart/guest/remove/<int:product_id>/", views.remove_guest_cart_item, name="remove_guest_cart_item"),

    # Checkout
    path("checkout/", views.checkout, name="checkout"),  # logged-in
    path("guest-checkout/", views.guest_checkout, name="guest_checkout"),  # guest

    # Orders
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
]





