# -------------------------
# CLEAN IMPORTS AT THE TOP
# -------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from stores.models import Store
import uuid

# REST FRAMEWORK IMPORTS
from rest_framework import generics, permissions
from .serializers import ProductSerializer
from rest_framework.exceptions import PermissionDenied

# Twitter client import
from ecommerce.twitter_client import get_twitter_client


# -------------------------
# SECTION A: HTML VIEWS
# -------------------------

@login_required
def seller_dashboard(request):
    """
    Display the seller dashboard.

    Shows all products created by the currently authenticated seller.
    If the user is not a seller, an authorization page is displayed.
    """
    if not request.user.is_seller:
        return render(request, "not_authorized.html")

    products = Product.objects.filter(seller=request.user)

    return render(request, "products/seller_dashboard.html", {
        "products": products
    })


@login_required
def add_product(request):
    """
    Allow a seller to create a new product.

    Handles both GET and POST requests:
    - GET: Display an empty product form.
    - POST: Validate and save the product, assign seller and SKU,
      and optionally post a tweet announcing the new product.

    Only stores owned by the current seller are available in the form.
    """
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        form.fields["store"].queryset = Store.objects.filter(
            owner=request.user
        )

        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.sku = uuid.uuid4().hex[:10]
            product.save()

            # -----------------------------------------
            # SEND TWEET ABOUT NEW PRODUCT
            # -----------------------------------------
            try:
                client = get_twitter_client()

                tweet_text = (
                    f"New product added to {product.store.name}!\n"
                    f"{product.name} - {product.description}"
                )

                if product.image:
                    client.update_status_with_media(
                        status=tweet_text,
                        filename=product.image.path
                    )
                else:
                    client.update_status(status=tweet_text)

            except Exception as e:
                # Optional: log or print the error
                print("Twitter error:", e)

            return redirect("seller_dashboard")
    else:
        form = ProductForm()
        form.fields["store"].queryset = Store.objects.filter(
            owner=request.user
        )

    return render(request, "products/add_product.html", {"form": form})


@login_required
def edit_product(request, product_id):
    """
    Allow a seller to edit an existing product.

    Ensures the product belongs to the authenticated seller.
    Supports GET (load form) and POST (save changes).
    """
    if not request.user.is_seller:
        return render(request, "products/not_authorized.html")

    product = get_object_or_404(Product, id=product_id, seller=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect("seller_dashboard")
    else:
        form = ProductForm(instance=product)

    return render(request, "products/edit_product.html", {"form": form})


@login_required
def delete_product(request, product_id):
    """
    Delete a product owned by the authenticated seller.

    Ensures the product belongs to the seller before deleting it.
    Redirects back to the seller dashboard after deletion.
    """
    if not request.user.is_seller:
        return render(request, "products/not_authorized.html")

    product = get_object_or_404(Product, id=product_id, seller=request.user)
    product.delete()

    return redirect("seller_dashboard")


def product_list(request):
    """
    Display a public list of all products.

    Intended for buyers or general browsing.
    """
    products = Product.objects.all()
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, product_id):
    """
    Display detailed information for a single product.

    Accessible to all users, including non-authenticated visitors.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})


# -------------------------
# SECTION B: API VIEWS (REST)
# -------------------------

class StoreProductListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating products for a specific store.

    GET:
        Return all products belonging to the specified store.

    POST:
        Create a new product under the store, but only if the authenticated
        user is the owner of that store. Otherwise, a PermissionDenied
        exception is raised.
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return products filtered by the store ID provided in the URL.
        """
        store_id = self.kwargs["store_id"]
        return Product.objects.filter(store_id=store_id)

    def perform_create(self, serializer):
        """
        Validate store ownership before creating a product.

        Ensures that only the store owner can add products to their store.
        """
        store_id = self.kwargs["store_id"]
        store = get_object_or_404(Store, id=store_id)

        if store.owner != self.request.user:
            raise PermissionDenied("You do not own this store.")

        serializer.save(store=store, seller=self.request.user)