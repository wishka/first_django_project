from django.contrib import admin
from .models import Author

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Поля, которые хотите отображать в админке
    search_fields = ('name',)  # Поля, по которым будет работать поиск