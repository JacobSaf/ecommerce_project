from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .models import Cart, CartItem, Order, OrderItem
from .forms import GuestCheckoutForm
from products.models import Product


# -----------------------------
# Helper: Get or create DB cart (logged-in)
# -----------------------------
def get_user_cart(user):
    """
    Retrieve or create the authenticated user's cart.

    Ensures each logged-in user has exactly one persistent Cart object.
    """
    cart, created = Cart.objects.get_or_create(user=user)
    return cart


# ============================
# Helpers: Session cart (guest)
# ============================
def get_session_cart(request):
    """
    Retrieve the guest cart stored in the session.

    The session cart structure is:
        {
            "product_id_as_str": quantity_int,
            ...
        }
    """
    return request.session.get("cart", {})


def save_session_cart(request, cart):
    """
    Save the updated guest cart back into the session.
    """
    request.session["cart"] = cart
    request.session.modified = True


def add_to_session_cart(request, product_id, quantity=1):
    """
    Add a product to the guest session cart.

    If the product already exists, its quantity is incremented.
    """
    cart = get_session_cart(request)
    pid = str(product_id)
    cart[pid] = cart.get(pid, 0) + quantity
    save_session_cart(request, cart)


def update_session_cart_item(request, product_id, quantity):
    """
    Update the quantity of a product in the guest session cart.

    If quantity <= 0, the item is removed.
    """
    cart = get_session_cart(request)
    pid = str(product_id)

    if quantity <= 0:
        cart.pop(pid, None)
    else:
        cart[pid] = quantity

    save_session_cart(request, cart)


def remove_from_session_cart(request, product_id):
    """
    Remove a product entirely from the guest session cart.
    """
    cart = get_session_cart(request)
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    save_session_cart(request, cart)


def get_session_cart_items_with_totals(request):
    """
    Build a detailed list of guest cart items and compute the total.

    Returns:
        items (list of dict):
            {
                "product": Product instance,
                "quantity": int,
                "subtotal": Decimal
            }

        total (Decimal): Sum of all subtotals.
    """
    cart = get_session_cart(request)
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids)

    items = []
    total = 0
    product_map = {p.id: p for p in products}

    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = product_map.get(pid)
        if not product:
            continue

        subtotal = product.price * qty
        items.append({
            "product": product,
            "quantity": qty,
            "subtotal": subtotal,
        })
        total += subtotal

    return items, total


# -----------------------------
# ADD TO CART (shared)
# -----------------------------
def add_to_cart(request, product_id):
    """
    Add a product to the cart for both logged-in and guest users.

    - Logged-in users: stored in the database.
    - Guests: stored in the session.
    """
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart = get_user_cart(request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            item.quantity += 1
            item.save()
    else:
        add_to_session_cart(request, product_id, quantity=1)

    messages.success(request, f"{product.name} added to your cart.")
    return redirect("view_cart")


# ============================
# VIEW CART (handles both)
# ============================
def view_cart(request):
    """
    Display the cart for both logged-in and guest users.

    - Logged-in users: loads Cart and CartItems from the database.
    - Guests: loads items from the session cart.
    """
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)

        items = cart.items.select_related("product")
        return render(request, "orders/cart.html", {"cart": cart, "items": items})

    # Guest cart
    items, total = get_session_cart_items_with_totals(request)
    return render(request, "orders/guest_cart.html", {"items": items, "total": total})


# ============================
# UPDATE / REMOVE (logged-in)
# ============================
@login_required
def update_cart_item(request, item_id):
    """
    Update the quantity of a CartItem for a logged-in user.

    If quantity <= 0, the item is removed.
    """
    cart = get_user_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    try:
        new_qty = int(request.POST.get("quantity", 1))
    except ValueError:
        new_qty = 1

    if new_qty <= 0:
        item.delete()
        messages.info(request, "Item removed from cart.")
    else:
        item.quantity = new_qty
        item.save()
        messages.success(request, "Cart updated.")

    return redirect("view_cart")


@login_required
def remove_from_cart(request, item_id):
    """
    Remove a CartItem from the logged-in user's cart.
    """
    cart = get_user_cart(request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)

    item.delete()
    messages.info(request, "Item removed from cart.")
    return redirect("view_cart")


# ============================
# UPDATE / REMOVE (guest)
# ============================
def update_guest_cart_item(request, product_id):
    """
    Update the quantity of a product in the guest session cart.

    If quantity <= 0, the item is removed.
    """
    try:
        new_qty = int(request.POST.get("quantity", 1))
    except ValueError:
        new_qty = 1

    update_session_cart_item(request, product_id, new_qty)

    if new_qty <= 0:
        messages.info(request, "Item removed from cart.")
    else:
        messages.success(request, "Cart updated.")

    return redirect("view_cart")


def remove_guest_cart_item(request, product_id):
    """
    Remove a product from the guest session cart.
    """
    remove_from_session_cart(request, product_id)
    messages.info(request, "Item removed from cart.")
    return redirect("view_cart")


# ============================
# CHECKOUT (logged-in)
# ============================
@login_required
@transaction.atomic
def checkout(request):
    """
    Process checkout for a logged-in user.

    Steps:
        1. Validate cart is not empty.
        2. Validate stock for each item.
        3. Create Order.
        4. Create OrderItems and deduct stock.
        5. Clear the cart.
        6. Send invoice email.

    Wrapped in a database transaction to ensure atomicity.
    """
    cart = get_user_cart(request.user)
    items = cart.items.select_related("product")

    if not items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    # Validate stock
    for item in items:
        if item.quantity > item.product.stock:
            messages.error(
                request,
                f"Not enough stock for {item.product.name}. Available: {item.product.stock}"
            )
            return redirect("view_cart")

    # Create order
    total = sum(item.total for item in items)
    order = Order.objects.create(
        user=request.user,
        billing_email=request.user.email,
        total_price=total,
        status="PAID",
    )

    # Create order items + deduct stock
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            quantity=item.quantity,
            price_at_purchase=item.product.price,
        )

        item.product.stock -= item.quantity
        item.product.save()

    # Clear cart
    items.delete()

    # Send invoice
    send_order_invoice_email(order)

    messages.success(request, "Checkout successful! Your order has been placed.")
    return redirect("order_detail", order_id=order.id)


# ============================
# CHECKOUT (guest)
# ============================
@transaction.atomic
def guest_checkout(request):
    """
    Process checkout for a guest user using the session cart.

    Steps:
        1. Validate cart is not empty.
        2. Validate stock.
        3. Collect guest billing/shipping info.
        4. Create Order with guest fields.
        5. Create OrderItems and deduct stock.
        6. Clear session cart.
        7. Send invoice email.
    """
    items, total = get_session_cart_items_with_totals(request)

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("view_cart")

    # Validate stock
    for item in items:
        product = item["product"]
        quantity = item["quantity"]
        if quantity > product.stock:
            messages.error(
                request,
                f"Not enough stock for {product.name}. Available: {product.stock}"
            )
            return redirect("view_cart")

    if request.method == "POST":
        form = GuestCheckoutForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            # Create guest order
            order = Order.objects.create(
                user=None,
                billing_email=cd["email"],
                total_price=total,
                status="PAID",
                guest_name=cd["full_name"],
                guest_email=cd["email"],
                guest_address=cd["address"],
                guest_city=cd["city"],
                guest_state=cd["state"],
                guest_zip=cd["zip_code"],
                guest_phone=cd.get("phone") or "",
            )

            # Create order items + deduct stock
            for item in items:
                product = item["product"]
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    quantity=quantity,
                    price_at_purchase=product.price,
                )

                product.stock -= quantity
                product.save()

            # Clear session cart
            save_session_cart(request, {})

            # Send invoice
            send_order_invoice_email(order)

            messages.success(request, "Checkout successful! Your order has been placed.")
            return redirect("order_detail", order_id=order.id)
    else:
        form = GuestCheckoutForm()

    return render(
        request,
        "orders/guest_checkout.html",
        {"form": form, "items": items, "total": total},
    )


# ============================
# ORDER DETAIL
# ============================
def order_detail(request, order_id):
    """
    Display the details of a specific order.

    If the order belongs to a logged-in user, ensure only that user
    can view it. Guest orders can be viewed by anyone with the link.
    """
    order = get_object_or_404(Order, id=order_id)

    if order.user and request.user.is_authenticated:
        if order.user != request.user:
            messages.error(request, "You do not have permission to view this order.")
            return redirect("product_list")

    return render(request, "orders/order_detail.html", {"order": order})


# ============================
# EMAIL INVOICE
# ============================
def send_order_invoice_email(order):
    """
    Send an invoice email for the given order.

    Uses both a plain-text and HTML template. Sends to:
        - order.billing_email (logged-in users)
        - order.guest_email (guest checkout)
    """
    subject = f"Your Order #{order.id} Invoice"
    context = {"order": order}

    message = render_to_string("orders/email_invoice.txt", context)
    html_message = render_to_string("orders/email_invoice.html", context)

    to_email = order.billing_email or order.guest_email
    if not to_email:
        return

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        html_message=html_message,
    )