from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Author(models.Model):
    """Модель Author для создания авторов блогов."""
    
    class Meta:
        ordering = ["name"]
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")
    
    name = models.CharField(max_length=100)
    bio = models.TextField()


class Category(models.Model):
    """ Модель для создания категорий статей """
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    name = models.CharField(max_length=40, null=False, blank=False, db_index=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    """ Модель тегов для статей """
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
    
    name = models.CharField(max_length=20, blank=True)
    
    def __str__(self):
        return self.name

class Article(models.Model):
    """Модель для создания статей."""
    
    class Meta:
        ordering = ['pub_date']
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    
    