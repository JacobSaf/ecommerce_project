from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from orders.models import Cart
from .forms import CustomUserRegistrationForm


# -------------------------
# REGISTER VIEW
# -------------------------
def register(request):
    """
    Handle user registration.

    Displays the registration form on GET requests and processes the
    submitted form on POST. If the form is valid, a new user account
    is created and the user is redirected to the login page.
    """
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login")
    else:
        form = CustomUserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


# -------------------------
# LOGIN VIEW
# -------------------------
def login_view(request):
    """
    Authenticate and log in a user.

    On POST, attempts to authenticate the provided username and password.
    If successful, logs the user in and redirects them to the appropriate
    dashboard based on their role (seller or buyer). On failure, re-renders
    the login page with an error message.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on role
            if user.is_seller:
                return redirect("seller_dashboard")
            else:
                return redirect("buyer_dashboard")

        return render(request, "accounts/login.html", {
            "error": "Invalid username or password"
        })

    return render(request, "accounts/login.html")


# -------------------------
# LOGOUT VIEW
# -------------------------
def logout_view(request):
    """
    Log out the current user and redirect to the login page.
    """
    logout(request)
    return redirect("login")


@login_required
def buyer_dashboard(request):
    """
    Display the buyer dashboard.

    Ensures that only buyers can access this view. Loads or creates the
    user's shopping cart and displays the associated cart items.
    """
    # Prevent sellers from accessing buyer pages
    if request.user.is_seller:
        return redirect("seller_dashboard")

    # Load the actual cart for this user
    try:
        cart = request.user.cart
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    items = cart.items.select_related("product")

    return render(
        request,
        "accounts/buyer_dashboard.html",
        {"cart": cart, "items": items}
    )