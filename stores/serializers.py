from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for converting Store model instances to and from JSON.

    This serializer exposes the key fields needed for API interactions:
        - id: Unique identifier for the store.
        - name: Public-facing store name.
        - description: Optional text describing the store.
        - owner: The user who created and manages the store (read‑only).

    The `owner` field is intentionally read‑only because it is assigned
    automatically in the API view logic based on the authenticated user.
    """
    class Meta:
        model = Store
        fields = ["id", "name", "description", "owner"]
        read_only_fields = ["owner"]