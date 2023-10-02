from django import forms
from .models import Product, OrderItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'thumbnail']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['quantity']
# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['delivery_address']