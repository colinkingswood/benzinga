from django import forms
from .models import Purchase

class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase
        exclude = ['price_paid']
        widgets = {'stock': forms.HiddenInput()}