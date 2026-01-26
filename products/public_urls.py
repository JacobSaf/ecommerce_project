from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path(
        "api/stores/<int:store_id>/products/",
        views.StoreProductListCreateView.as_view(),
        name="api_store_products",
    )

]