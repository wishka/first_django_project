import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import ArticleForm, AuthorForm
from .models import Article, Author


class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .defer("content")
        .select_related("author", "category")
        .prefetch_related("tags")
        .all()
    )
    template_name = 'BlogApp/articles-list.html'

    
    def get_context_data(self, **kwargs):
        articles = [
            ('New year eve', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...', datetime.time(), 'Nick', 'Holidays', 'surprise'),
            ('Christmas eve', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...', datetime.time(), 'Alison', 'Holidays', 'surprise'),
            ('Birthday eve', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...', datetime.time(), 'Wishka', 'Holidays', 'surprise'),
            ("Saint Valentine's day", 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...',
             datetime.time(), 'Wishka', 'Holidays', 'surprise'),
        ]
        context = {
            "articles": articles,
        }
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'category', 'tags')  # исправленное поле fields
    template_name = 'BlogApp/article_form.html'
    success_url = reverse_lazy("BlogApp:index")

    def form_valid(self, form):
        # Старайтесь использовать user, связанный с Author, а не предполагать, что их ID совпадают
        try:
            author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            messages.error(self.request, 'У вас нет профиля автора для публикации статей.')
            return HttpResponseRedirect(reverse_lazy("BlogApp:index"))  # возврат HttpResponse
        else:
            form.instance.author = author
            return super().form_valid(form)


# class ArticleCreateView(LoginRequiredMixin, CreateView):
#     # model = Article
#     queryset = Article.objects.defer('pub_date').select_related('author', 'category').prefetch_related('tags')
#     # form_class = ArticleForm
#     fields = 'title', 'content', 'category', 'tags'
#     template_name = 'BlogApp/article_form.html'
#     success_url = reverse_lazy("BlogApp:index")
#
#     def form_valid(self, form):
#         try:
#             # Получаем профиль Author для текущего пользователя
#             author = Author.objects.get(id=self.request.user.id)
#         except Author.DoesNotExist:
#             # Если у пользователя нет профиля Author, отобразите сообщение об ошибке и перенаправьте его
#             messages.error(self.request, 'У вас нет профиля автора для публикации статей.')
#             return redirect("BlogApp:index")
#         else:
#             # Если профиль Author найден, устанавливаем его как автора статьи
#             form.instance.author = author
#             # Вызываем метод базового класса
#             return super().form_valid(form)


class CreateAuthorView(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('BlogApp:index')