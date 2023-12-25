from django import forms
from django.core import validators
from .models import Article, Author
from django.forms import ModelForm


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']