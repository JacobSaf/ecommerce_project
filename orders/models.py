from django.db import models
from django.conf import settings
from products.models import Product


class Cart(models.Model):
    """
    Represents a shopping cart belonging to a logged-in user.

    Each authenticated user has exactly one Cart, created automatically
    when needed. The cart stores CartItem entries, each representing a
    product and quantity. Guest users use a session-based cart instead.

    Fields:
        user:
            One-to-one relationship with the authenticated user.
            Deleting the user removes the cart.

        created_at:
            Timestamp indicating when the cart was created.

    Properties:
        total_price:
            Computes the total cost of all items in the cart.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart ({self.user.username})"

    @property
    def total_price(self):
        return sum(item.total for item in self.items.all())


class CartItem(models.Model):
    """
    Represents a single product entry inside a user's cart.

    Each CartItem links a product to a cart with a specific quantity.
    A product may appear only once per cart (enforced by unique_together).

    Fields:
        cart:
            The cart this item belongs to.

        product:
            The product being purchased.

        quantity:
            Number of units of the product.

    Properties:
        total:
            Returns the subtotal price for this item (price × quantity).
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity} × {self.product.name}"

    @property
    def total(self):
        return self.product.price * self.quantity


class Order(models.Model):
    """
    Represents a completed checkout, either by a logged-in user or a guest.

    Orders store billing information, total price, status, and optional
    guest checkout details. Logged-in users have an associated user record,
    while guest orders store name, email, and address fields directly.

    Fields:
        user:
            Optional FK to the authenticated user who placed the order.
            Null for guest checkouts.

        billing_email:
            Email used for sending invoices.

        total_price:
            Total cost of all items at the time of purchase.

        status:
            Current order status (Pending, Paid, Shipped, Delivered, Cancelled).

        created_at:
            Timestamp when the order was created.

        guest_* fields:
            Populated only for guest checkouts. Store name, email, address,
            city, state, ZIP code, and phone number.
    """
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    billing_email = models.EmailField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    # Guest checkout fields
    guest_name = models.CharField(max_length=255, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    guest_address = models.CharField(max_length=255, null=True, blank=True)
    guest_city = models.CharField(max_length=100, null=True, blank=True)
    guest_state = models.CharField(max_length=100, null=True, blank=True)
    guest_zip = models.CharField(max_length=20, null=True, blank=True)
    guest_phone = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """
    Represents a single product purchased within an order.

    OrderItems store a snapshot of the product at the time of purchase,
    including its name and price. This ensures order history remains
    accurate even if the product is later updated or deleted.

    Fields:
        order:
            The order this item belongs to.

        product:
            FK to the product, kept nullable to preserve order history
            even if the product is removed.

        product_name:
            Stored name of the product at purchase time.

        quantity:
            Number of units purchased.

        price_at_purchase:
            The price of the product at the moment of checkout.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"


class ShippingAddress(models.Model):
    """
    Represents the shipping address associated with an order.

    Each order has exactly one shipping address, and each address is tied
    to the user who placed the order (for logged-in users).

    Fields:
        user:
            The user who owns this address.

        order:
            The order this address belongs to.

        address_line1 / address_line2:
            Street address fields.

        city / state / postal_code / country:
            Location details for delivery.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shipping_addresses'
    )
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='shipping_address'
    )
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')

    def __str__(self):
        return f"{self.address_line1}, {self.city}"