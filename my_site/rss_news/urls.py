from django.urls import path
from .views import RSSListView, RSSDetailView, LatestNewsFeed


app_name = "rss_news"

urlpatterns = [
    path("news/", RSSListView.as_view(), name="news"),
    path("news/<int:pk>/", RSSDetailView.as_view(), name="news_detail"),
    path("news/latest/feed/", LatestNewsFeed(), name="news-feed"),
]