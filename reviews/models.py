from django.conf import settings
from django.db import models
from products.models import Product


class Review(models.Model):
    """
    Represents a user-submitted review for a specific product.

    Reviews include a numeric rating, a written comment, and an optional
    "verified" flag indicating whether the reviewer actually purchased
    the product. Verified reviews are determined during submission by
    checking the user's order history.

    Fields:
        product:
            The product being reviewed. Deleting the product removes
            all associated reviews.

        user:
            The user who wrote the review. Deleting the user removes
            their reviews.

        rating:
            An integer score (typically 1–5) representing the user's
            evaluation of the product.

        comment:
            The written text of the review.

        verified:
            Boolean indicating whether the reviewer has purchased the
            product through the platform.

        created_at:
            Timestamp marking when the review was submitted.
    """
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} review by {self.user}"