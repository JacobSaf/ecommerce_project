from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form used to submit a product review.

    This form exposes the user-editable fields of a Review:
        - rating: An integer score evaluating the product.
        - comment: The written text of the review.

    The user and product fields are intentionally excluded because they
    are assigned automatically in the view logic during review creation.
    """
    class Meta:
        model = Review
        fields = ["rating", "comment"]