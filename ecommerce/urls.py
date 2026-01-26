"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect


urlpatterns = [
    # Redirect root URL to login page
    path("", lambda request: redirect("login"), name="home"),

    # Accounts (login, register, logout, buyer dashboard)
    path("accounts/", include("accounts.urls")),

    # Seller dashboard + product management (HTML views)
    path("seller/", include("products.urls")),

    # Public product browsing (HTML views)
    path("products/", include("products.public_urls")),

    # Product API endpoints (REST)
    path("products/api/", include("products.api_urls")),

    # Stores app
    path("stores/", include("stores.urls")),

    # Orders app
    path("orders/", include("orders.urls")),

    # Reviews app
    path("reviews/", include("reviews.urls")),

    # Django admin
    path("admin/", admin.site.urls),

    # Password reset flow
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
