from django import forms
from .models import Product

class ProductImageForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_image', 'product_image2', 'product_image3']  