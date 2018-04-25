from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'category', 'ue_version',
                  'main_image', 'product_file')


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('rating', 'review_text')
