from django import forms
from django.core import validators
from .models import Article
from django.forms import ModelForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags']
