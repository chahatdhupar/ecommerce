from django import forms
from .models import Product, Order


# Product form
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


# Checkout form
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone', 'address', 'city']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        # add placeholders
        self.fields['full_name'].widget.attrs.update({'placeholder': 'Enter full name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter email'})
        self.fields['phone'].widget.attrs.update({'placeholder': 'Enter phone number'})
        self.fields['address'].widget.attrs.update({'placeholder': 'Enter full address'})
        self.fields['city'].widget.attrs.update({'placeholder': 'Enter city'})