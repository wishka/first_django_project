from django import forms
from django.core import validators
from .models import Product, Order
from django.forms import ModelForm
from django.contrib.auth.models import Group


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
        fields = 'name', 'price', 'description', 'discount', 'created_by', "preview" # Автоматическая генерация формы на основании данных в модели
    
    # Чтобы дать возможность загрузить сразу несколько изображений используем виджет
    # images = forms.FileField(
    #     widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #     required=False)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = 'delivery_address', 'promocode', 'products', 'user'
        
class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = 'name',
