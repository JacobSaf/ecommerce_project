from django.db import models
from django.conf import settings
from stores.models import Store


class Category(models.Model):
    """
    Represents a product category used to organize and group products.

    Each category has:
        - name: Human-readable category name.
        - slug: URL‑friendly identifier used for filtering or SEO.

    Categories are used to classify products and improve navigation
    across the storefront.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a product listed for sale by a seller.

    Fields:
        seller:
            The user who owns and manages this product.
            Deleting the seller removes all associated products.

        name:
            The product's display name.

        description:
            Optional detailed text describing the product.

        price:
            The current selling price.

        stock:
            The available inventory count. Stock is reduced when orders
            are placed and validated during checkout.

        store:
            The store this product belongs to. Deleting the store removes
            all associated products.

        sku:
            A unique stock‑keeping unit identifier generated when the
            product is created.

        category:
            Optional category used for filtering and organization.

        image:
            Optional product image uploaded by the seller.

        is_active:
            Indicates whether the product is visible and purchasable.

        created_at / updated_at:
            Timestamps for auditing and sorting, with newest products
            appearing first by default.
    """
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
    )

    sku = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    image = models.ImageField(
        upload_to="product_images/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name