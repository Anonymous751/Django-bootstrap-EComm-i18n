from pyexpat import model
from django import forms
from .models import Product
from django.utils.translation import gettext_lazy as _

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'images', 'category', 'is_featured', 'is_trending']

        labels = {
            'name': _('Product Name'),
            'price': _('Price'),
            'images': _('Images'),
            'category': _('Category'),
            'is_featured': _('Featured Product'),
            'is_trending': _('Trending Product'),
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Product Name')}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': _('Price')}),
            'images': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_trending': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }