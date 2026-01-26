from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer used to convert Product model instances to and from JSON.

    This serializer exposes the core fields needed for API responses:
        - id: Unique identifier for the product.
        - name: Display name of the product.
        - description: Optional detailed text about the product.
        - price: Current selling price.
        - stock: Available inventory count.
        - store: The store that owns the product (read‑only).

    The `store` field is marked read‑only because it is assigned
    automatically based on the authenticated seller in the API view logic.
    """
    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "store"]
        read_only_fields = ["store"]