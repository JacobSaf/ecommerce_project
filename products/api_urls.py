from django.urls import path
from . import views

urlpatterns = [
    path(
        "stores/<int:store_id>/products/",
        views.StoreProductListCreateView.as_view(),
        name="api_store_products"
    ),
]