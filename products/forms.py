from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    Form used by sellers to create or update a product listing.

    This form exposes the core editable fields of a Product, including:
        - name: The product's display name.
        - description: Optional detailed text about the product.
        - price: The selling price.
        - stock: Available inventory count.
        - store: The store the product belongs to.

    The seller and SKU fields are intentionally excluded because they are
    assigned automatically in the view logic during product creation.
    """
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'store']