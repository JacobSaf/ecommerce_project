"""
HTML and API views for managing seller-owned stores.

Includes CRUD views for store management and REST API endpoints for
listing and creating stores within the marketplace.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Store
from .forms import StoreForm

# REST FRAMEWORK IMPORTS
from rest_framework import generics, permissions
from .serializers import StoreSerializer
from django.contrib.auth import get_user_model

# Twitter client import
from ecommerce.twitter_client import get_twitter_client

User = get_user_model()


# -----------------------------------------
# SECTION A: REGULAR HTML VIEWS
# -----------------------------------------

@login_required
def delete_store(request, store_id):
    """
    Delete a store owned by the authenticated user.

    Ensures the store belongs to the current user before deleting it.
    After deletion, the user is redirected back to their store list.
    """
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    store.delete()
    return redirect("store_list")


@login_required
def store_list(request):
    """
    Display a list of all stores owned by the authenticated user.

    Restricted to logged-in users and shows only stores where the
    current user is the owner.
    """
    stores = Store.objects.filter(owner=request.user)
    return render(request, "stores/store_list.html", {"stores": stores})


@login_required
def create_store(request):
    """
    Allow a user to create a new store.

    Handles GET and POST:
    - GET: Display an empty store creation form.
    - POST: Validate and save the store, assign the current user as
      owner, and optionally post a tweet announcing the new store.

    If a logo is uploaded, the tweet includes the image.
    """
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.owner = request.user
            store.save()

            # -----------------------------------------
            # SEND TWEET ABOUT NEW STORE
            # -----------------------------------------
            try:
                client = get_twitter_client()

                tweet_text = (
                    f"New store added: {store.name}\n"
                    f"{store.description}"
                )

                if store.logo:
                    client.update_status_with_media(
                        status=tweet_text,
                        filename=store.logo.path
                    )
                else:
                    client.update_status(status=tweet_text)

            except Exception as e:
                # Optional: print or log the error
                print("Twitter error:", e)

            return redirect("store_list")
    else:
        form = StoreForm()

    return render(request, "stores/create_store.html", {"form": form})


@login_required
def edit_store(request, store_id):
    """
    Allow a user to edit one of their stores.

    Ensures the store belongs to the authenticated user.
    Supports GET (load form) and POST (save changes).
    """
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            return redirect("store_list")
    else:
        form = StoreForm(instance=store)

    return render(
        request,
        "stores/edit_store.html",
        {
            "form": form,
            "store": store,
        }
    )


# -----------------------------------------
# SECTION B: API VIEWS (REST FRAMEWORK)
# -----------------------------------------

class StoreListCreateView(generics.ListCreateAPIView):
    """
    API endpoint for listing and creating stores.

    GET:
        Return a list of all stores in the system.

    POST:
        Create a new store owned by the authenticated user.
        Only logged-in users may create stores.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Assign the authenticated user as the store owner during creation.
        """
        serializer.save(owner=self.request.user)


class VendorStoreListView(generics.ListAPIView):
    """
    API endpoint for listing stores belonging to a specific vendor.

    GET:
        Return all stores owned by the vendor whose ID is provided
        in the URL path.
    """
    serializer_class = StoreSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """
        Filter stores by the vendor ID provided in the URL.
        """
        vendor_id = self.kwargs["vendor_id"]
        return Store.objects.filter(owner_id=vendor_id)