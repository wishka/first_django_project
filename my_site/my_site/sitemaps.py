from rss_news.sitemap import NewsSitemap
from shopapp.sitemap import ProductsSitemap, OrdersSitemap


sitemaps = {
    "RSS": NewsSitemap,
    "Products": ProductsSitemap,
    "Orders": OrdersSitemap,
}