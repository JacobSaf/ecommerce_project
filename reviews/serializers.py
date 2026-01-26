from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for converting Review model instances to and from JSON.

    This serializer exposes all relevant review fields, including:
        - id: Unique identifier for the review.
        - product: The product being reviewed (read‑only).
        - user: The user who wrote the review, represented using the
          model's __str__ method via StringRelatedField.
        - rating: Numeric score evaluating the product.
        - comment: Written text of the review.
        - verified: Indicates whether the reviewer purchased the product.
        - created_at: Timestamp of when the review was submitted.

    The `product`, `user`, and `verified` fields are read‑only because
    they are assigned automatically during review creation and should not
    be modified through the API.
    """
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "rating",
            "comment",
            "verified",
            "created_at",
        ]
        read_only_fields = ["user", "verified", "product"]