from django import forms
from django.core import validators
from .models import Product, Order


# class ProductForm(forms.Form):
#     name = forms.CharField(max_length=100)
#     price = forms.DecimalField(min_value=1, max_value=9999999, decimal_places=2)
#     description = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 5,  'class': 'form-control', 'placeholder': 'Product description'}),
#         validators=[validators.RegexValidator(
#             regex=r"great", # Проверяем, что поле описание содержит слово "great"
#             message="Field must contains word 'great'"
#         )],
#     )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'name', 'price', 'description', 'discount' # Автоматическая генерация формы на основании данных в модели


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'products', 'user'