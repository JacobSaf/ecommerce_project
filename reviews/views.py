from django.shortcuts import get_object_or_404, redirect, render
from .models import Review
from .forms import ReviewForm
from products.models import Product
from orders.models import OrderItem

# REST FRAMEWORK IMPORTS
from rest_framework import generics, permissions
from .serializers import ReviewSerializer


# -----------------------------------------
# SECTION A: REGULAR HTML VIEWS
# -----------------------------------------

def leave_review(request, product_id):
    """
    Allow a user to leave a review for a specific product.

    Handles both GET and POST:
    - GET: Display an empty review form.
    - POST: Validate and save the review, automatically attaching the
      authenticated user and the product being reviewed.

    Verification:
        A review is marked as "verified" if the user has previously
        purchased the product (checked via OrderItem records).

    After submission, the user is redirected back to the product detail page.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product

            # Determine if the user purchased the product
            purchased = OrderItem.objects.filter(
                order__user=request.user,
                product=product
            ).exists()

            review.verified = purchased
            review.save()

            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/leave_review.html",
        {"form": form, "product": product}
    )


# -----------------------------------------
# SECTION B: API VIEWS (REST FRAMEWORK)
# -----------------------------------------

class ProductReviewListView(generics.ListAPIView):
    """
    API endpoint for retrieving all reviews for a specific product.

    GET:
        Return a list of all Review objects associated with the product
        whose ID is provided in the URL path.
    """
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Filter reviews by the product ID provided in the URL.
        """
        product_id = self.kwargs["product_id"]
        return Review.objects.filter(product_id=product_id)