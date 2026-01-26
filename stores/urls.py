from django.urls import path
from . import views


urlpatterns = [
    # -----------------------------------------
    # API ENDPOINTS (REST)
    # -----------------------------------------
    path("api/stores/", views.StoreListCreateView.as_view(), name="api_store_list_create"),
    path("api/vendors/<int:vendor_id>/stores/", views.VendorStoreListView.as_view(), name="api_vendor_stores"),

    # -----------------------------------------
    # HTML VIEWS (WEB INTERFACE)
    # -----------------------------------------
    path('', views.store_list, name='store_list'),
    path('create/', views.create_store, name='create_store'),
    path('edit/<int:store_id>/', views.edit_store, name='edit_store'),
    path('delete/<int:store_id>/', views.delete_store, name='delete_store'),
]
