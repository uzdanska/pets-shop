from django import forms
from .models import Product
from bootstrap_datepicker_plus.widgets import DatePickerInput

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image', 'thumbnail']

class StatsForm(forms.Form):
    start_date = forms.DateField(
        widget=DatePickerInput(options={"format": "MM/DD/YYYY"}),
        label='Data początkowa'
    )
    end_date = forms.DateField(
        widget=DatePickerInput(options={"format": "MM/DD/YYYY"}),
        label='Data końcowa'
    )
    num_result_products = forms.IntegerField(
        label='Liczba produktów',
        min_value=3
    )