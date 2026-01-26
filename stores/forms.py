"""
Forms for creating and updating stores.

Provides a ModelForm used by sellers to manage their store information.
"""

from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    """
    Form used by sellers to create or update a store.

    This form exposes the editable fields of a Store:
        - name: The public-facing name of the store.
        - description: Optional text describing the store’s purpose,
          branding, or mission.

    The owner field is intentionally excluded because it is assigned
    automatically in the view logic based on the authenticated user.
    """
    class Meta:
        model = Store
        fields = ['name', 'description']