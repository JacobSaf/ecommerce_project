from django.urls import path
from . import views


urlpatterns = [
    # -----------------------------------------
    # API ENDPOINTS (REST)
    # -----------------------------------------
    path(
        "api/products/<int:product_id>/reviews/",
        views.ProductReviewListView.as_view(),
        name="api_product_reviews"
    ),

    # -----------------------------------------
    # HTML VIEWS (WEB INTERFACE)
    # -----------------------------------------
    path("leave/<int:product_id>/", views.leave_review, name="leave_review"),
]