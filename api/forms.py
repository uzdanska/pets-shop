from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'descrption', 'name', 'descrption', 'price', 'category', 'image', 'thumbnail']

    