import datetime
from datetime import time

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import ArticleForm
from .models import Article, Author


class ArticlesListView(ListView):
    template_name = 'BlogApp/articles-list.html'
    context_object_name = 'articles'
    queryset = (Article.objects.
                select_related('author').
                prefetch_related('tags'))

    
    def get_context_data(self, **kwargs):
        articles = [
            ('New year eve', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...', datetime.time(), 'Nick', 'Holidays', 'surprise'),
            ('Christmas eve', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...', datetime.time(), 'Alison', 'Holidays', 'surprise'),
            ('Birthday eve', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...', datetime.time(), 'Wishka', 'Holidays', 'surprise'),
        ]
        context = {
            "articles": articles,
        }
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    # Укажите имя для успешного URL-адреса, если у вас есть name в urls.py
    success_url = reverse_lazy("BlogApp:index")

    def form_valid(self, form):
        try:
            # Получаем профиль Author для текущего пользователя
            author = Author.objects.get(id=self.request.user.id)
        except Author.DoesNotExist:
            # Если у пользователя нет профиля Author, отобразите сообщение об ошибке и перенаправьте его
            messages.error(self.request, 'У вас нет профиля автора для публикации статей.')
            return redirect("BlogApp:index")
        else:
            # Если профиль Author найден, устанавливаем его как автора статьи
            form.instance.author = author
            # Вызываем метод базового класса
            return super().form_valid(form)

