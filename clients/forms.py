from django import forms
from shop.models import Product


class AddProductForm(forms.ModelForm):
    class Meta:
        model   = Product 
        fields  = ['category', 'subcategory', 'variation', 'product_name',  'description', 'region', 'age', 'gender', 'color', 'price', 'stock', 'image1', 'image2', 'image3']
        #fields  = ['category', 'subcategorys']