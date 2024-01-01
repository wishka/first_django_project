from django.contrib.sitemaps import Sitemap
from .models import News

class NewsSitemap(Sitemap):
    # Указать, как часто меняется объект
    changefreq = "never"
    # priority - Говорит о том, какая страница самая главная от 0.1 до 1 в поисковой выдаче
    priority = 0.5
    def items(self):
        return News.objects.filter(published_at__isnull=False).order_by('-published_at')
        # Можно указать количество выдаваемой информации через срез, если ее очень много
    
    def lastmod(self, obj: News):
        return obj.published_at
    