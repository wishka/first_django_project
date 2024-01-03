from django.contrib.sitemaps import Sitemap
from .models import Product, Order

class ProductsSitemap(Sitemap):
    # Указать, как часто меняется объект
    changefreq = "monthly"
    # priority - Говорит о том, какая страница самая главная от 0.1 до 1 в поисковой выдаче
    priority = 0.9
    
    def items(self):
        return Product.objects.filter(archived=False).order_by('-created_at')
        # Можно указать количество выдаваемой информации через срез, если ее очень много
    
    def lastmod(self, obj: Product):
        return obj.created_at


class OrdersSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8
    
    def items(self):
        return Order.objects.all()
    
    def lastmod(self, obj: Order):
        return obj.created_at
    