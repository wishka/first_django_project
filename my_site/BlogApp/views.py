from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import AuthorForm
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


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'content', 'category', 'tags')
    template_name = 'BlogApp/article_form.html'
    success_url = reverse_lazy("BlogApp:index")

    def form_valid(self, form):
        author_article = Author.objects.get(name=self.request.user)
        #получаем объект модели Author по текущему залогиненому
        # пользователю, главное чтобы имена совпадали
        form.instance.author = author_article  #подставляем его по умолчанию в поле author модели Article

        return super(ArticleCreateView, self).form_valid(form)


class CreateAuthorView(CreateView):
    model = Author
    form_class = AuthorForm
    success_url = reverse_lazy('BlogApp:index')