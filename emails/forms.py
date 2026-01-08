from django import forms
from .models import Email


class EmailForm(forms.ModelForm):  # ModelForm - A ModelForm automatically creates a form from a Django model.
    class Meta:
        model = Email
        fields = ('__all__')
