from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.urls import reverse, reverse_lazy
from .models import News


class RSSListView(ListView):
    queryset = (
        News.objects
        .filter(published_at__isnull=False)
        .order_by('-published_at')
        )
    
class RSSDetailView(DetailView):
    model = News
    
class LatestNewsFeed(Feed):
    title = 'Latest News'
    description = 'Latest News updates from First Django Application'
    link = reverse_lazy("rss_news:news")
    
    def items(self):
        return (
            News.objects
            .filter(published_at__isnull=False)
            .order_by('-published_at')[:5] # При помощи среза закгрузим только последние 5 статей
        )
    
    def item_title(self, item: News):
        return item.title
    
    def item_description(self, item: News):
        return item.body[:200]
    
    def item_link(self, item: News):
        return reverse("rss_news:news", kwargs={"pk": item.pk})