from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ArticlesListView, ArticleCreateView, CreateAuthorView)


app_name = "BlogApp"

routers = DefaultRouter()
routers.register("articles", ArticlesListView)

# Обращение к ссылками на страницах всегда идет по имени - name
urlpatterns = [
    path("", ArticlesListView.as_view(), name="index"),
    path("new/", ArticleCreateView.as_view(), name="article-create"),
    path('create-author/', CreateAuthorView.as_view(), name='create_author'),
]